import llnl.util.lang as lang
import llnl.util.tty as tty

import os
import re
import spack
import spack.cmd
import spack.mirror
import spack.cmd.common.arguments as arguments
import spack.environment as ev
import spack.spec
import spack.binary_distribution as bindist
import spack.main

# not all versions of spack have _format_spec, , etc. 
try:
    import spack.cmd.buildcache.update_index as update_index
    from spack.cmd.buildcache import _format_spec
except:
    def _format_spec(spec):
        return repr(spec)       

    def update_index(url, update_keys=False):
        os.system(f"spack buildcache update-index {url} {'--keys' if update_keys else ''} ")


def get_env_hashes(env, local=True):
    res = set()

    # with os.popen("spack spec --install-status --long") as ssis:
    #    for line in ssis:

    tree_context = spack.store.STORE.db.read_transaction
    tree_kwargs = {
        "format": spack.spec.DISPLAY_FORMAT,
        "hashlen": 7,
        "status_fn": spack.spec.Spec.install_status,
        "hashes": True,
        "color": False,
    }
    if env:
        env.concretize()
        specs = env.concretized_specs()

    for input, output in specs:
        with tree_context():
            spec_out = output.tree(**tree_kwargs)

        for line in spec_out.split("\n"):
            if line.startswith("[+]") or not local and line.startswith("[^]"):
                hval = line[5:13].strip()
                res.add(hval)

    return res


def make_reconstitute_script(path, active, upstream_setup):
    with open(f"{path}/reconstitute.bash", "w") as fout:
        fout.write(
            f"""#!/bin/bash

. {upstream_setup}

spack subspack $PWD/packages
. $PWD/packages/setup-env.sh
spack mirror add job_local file://$INPUT_TAR_DIR_LOCAL
spack env create {active} $INPUT_TAR_DIR_LOCAL/spack.lock
spack --env {active} install
"""
        )


def find_upstream_setup():
    upstreams = spack.config.get("upstreams")
    for uname in upstreams:
        val = upstreams[uname]
        if "install_tree" in val:
            res = val["install_tree"]
            if res.endswith("/opt/spack"):
                res = res[:-10]
            if os.path.exists(res + "/setup-env.sh"):
                return res + "/setup-env.sh"
            if os.path.exists(res + "/share/spack/setup-env.sh"):
                return res + "/share/spack/setup-env.sh"


def local_buildcache(args):

    spack.cmd.require_active_env("location -e")
    env = ev.active_environment()
    path = env.path
    active = env.name
    upstream_setup = find_upstream_setup()

    if not args.mirror:
        args.mirror = spack.mirror.Mirror.from_local_path(f"{path}/bc")

    skipped = []
    failed = []

    dest = args.mirror.fetch_url.replace("file://","") + "/.."
    os.makedirs(os.path.dirname(dest), exist_ok=True)

    # pick specs to upload from environment

    for hs in get_env_hashes(env, args.local):
        if not hs:
            continue
        print(f"hash: {hs}")

        specs = spack.cmd.parse_specs([f"/{hs}"], concretize=True)

        if not specs:
            print(f"no specs for hash: {hs}")
            skipped.append(f"/{hs}")
            continue

        spec = specs[0]

        bdf = f"{str(spec.prefix)}/.spack/binary_distribution"
        if args.not_bc and os.path.exists(bdf):
            print("...was from buildcache, skipping")
            # was installed from a buildcache, skip it
            continue

        # build spack buildcache command and call main, since
        # the underlying interface keeps shifting around..
        argv = [ "buildcache", "push" ]
        if args.force:
            argv.append("--force")
        if args.update_index:
            argv.append("--update_index")
        if args.key:
            argv.append("--key")
            argv.append(args.key)
        if args.signed == False and not args.key:
            argv.append("-u")
        argv.append("--only")
        argv.append("package")
        argv.append(str(args.mirror.get_url("push")))
        argv.append("/" + hs)
        print("Running: ", " ".join(argv))
        spack.main.main(argv)

    make_reconstitute_script(dest, active, upstream_setup)
