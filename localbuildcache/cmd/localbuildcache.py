import sys
import spack.config
import argparse
from spack.extensions import localbuildcache as locext
from spack.cmd.buildcache import setup_parser as orig_buildcache_setup_parser

description = "create buildcache of local packages in environment"
section = "environments"
level = "short"


def setup_parser(subparser):
    origp = argparse.ArgumentParser()
    orig_buildcache_setup_parser(orig_p)
    subparser.__init__(prog="localbuildcache", parents=[origp.choices["create"]])
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


def localbuildcache(parser, args):
    locext.local_buildcache(args)
