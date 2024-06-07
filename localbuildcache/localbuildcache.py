import llnl.util.lang as lang
import llnl.util.tty as tty

import os
import spack
import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.environment as ev
import spack.spec


def get_local_hashes():
    res = set()
    with os.popen("spack spec --install-status --long") as ssis:
        for line in ssis:
            if line.startswith('[+]'):
                hval = line[5:13].strip()
                res.add(hval)
    return res

def make_reconstitute_script(path, active, upstream_setup):
    with os.open(f"{path}/bc/reconstitute.bash", "w") as fout:
        fout.write(

f"""#!/bin/bash

. {upstream_setup}

spack subspack $PWD/packages
. $PWD/packages/setup-env.sh
spack mirror add job_local file://$INPUT_TAR_DIR_LOCAL
spack env create {active} $INPUT_TAR_DIR_LOCAL/spack.lock
spack --env {active} install
""" )


def find_upstream_setup():
    upstreams = spack.config.get('upstreams')
    for uname, val in upstreams:
        if 'install_tree' in val:
            res = val['install_tree']
            if res.endswith("/opt/spack"):
                res = res[:-10]
            if os.path.exists(res + "/setup-env.sh"):
                return res + "/setup-env.sh"
            if os.path.exists(res + "/share/spack/setup-env.sh"):
                return res +  "/share/spack/setup-env.sh"

def local_buildcache(args):
    if args.key:
        ka = f"--key {args.key}"
    else:
        ka = "--unsigned"

    spack.cmd.require_active_env("location -e")
    path = ev.active_environment().path
    active = ev.active_environment().name
    upstream_setup = find_upstream_setup()
 
    for hs in get_local_hashes():
        os.system(f"spack buildcache creaete {ka} --only packages {path}/bc {hs}")
    os.system(f"spack buildcache update-index {path}/bc")
    make_reconstitute_script(path, active, upstream_setup)
