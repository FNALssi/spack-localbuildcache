import llnl.util.lang as lang
import llnl.util.tty as tty

import os
import spack
import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.environment as ev
import spack.spec
import spack.binary_distribution as bindist


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
 
    url = "{path}/bc"

    for hs in get_local_hashes():
        spec = spack.cmd.disambiguate_spec_from_hashes(f"/{hs}", spec, local=True, installed=True, first=True)

        try:
            bindist.push_or_raise(
                spec,
                url,
                bindist.PushOptions(
                    force=args.force,
                    unsigned=args.unsigned,
                    key=args.key,
                    regenerate_index=None,
                ),
            )

            msg = f"{_progress(i, len(specs))}Pushed {_format_spec(spec)}"
            if len(specs) == 1:
                msg += f" to {url}"
            tty.info(msg)

        except bindist.NoOverwriteException:
            skipped.append(_format_spec(spec))

        # Catch any other exception unless the fail fast option is set
        except Exception as e:
            if args.fail_fast or isinstance(
                e, (bindist.PickKeyException, bindist.NoKeyException)
            ):
                raise
            failed.append((_format_spec(spec), e))

>>>>>>> Stashed changes
    os.system(f"spack buildcache update-index {path}/bc")
    make_reconstitute_script(path, active, upstream_setup)
