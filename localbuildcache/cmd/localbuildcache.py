import sys
import spack.config
import argparse
#from spack.cmd.common import arguments
from spack.extensions import localbuildcache as locext
from spack.cmd.buildcache import setup_parser as orig_buildcache_setup_parser

description = "create buildcache of packages in environment"
section = "environments"
level = "short"

def setup_parser(subparser):
    subparser.add_argument(
        "--local",
        default=False,
        action="store_true",
        help="Restrict to packages local to this instance (not upstream)",
    )
    subparser.add_argument(
        "--not-bc",
        default=False,
        action="store_true",
        help="Restrict to packages not installed from a buildcache",
    )
    subparser.add_argument(
        "--dest",
        default="",
        help="destination url -- default is file:///environment_dir/bc",
    )
    #arguments.add_common_arguments(subparser, ["specs", "deptype_default_default_deptype", "jobs"])


def localbuildcache(parser, args):
    locext.local_buildcache(args)
