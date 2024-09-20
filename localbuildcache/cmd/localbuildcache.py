import sys
import spack.config
import argparse
from spack.cmd.common import arguments
from spack.extensions import localbuildcache as locext
import spack.cmd.buildcache

description = "create buildcache of local packages in environment"
section = "environments"
level = "short"


def setup_parser(subparser):

    subparser.add_argument("-f", "--force", action="store_true", help="overwrite tarball if it exists")
    subparser.add_argument(
        "--unsigned",
        "-u",
        action="store_false",
        dest="signed",
        default=False,
        help="push unsigned buildcache tarballs",
    )
    subparser.add_argument(
        "--signed",
        action="store_true",
        dest="signed",
        default=None,
        help="push signed buildcache tarballs",
    )
    subparser.add_argument(
        "--key", "-k", metavar="key", type=str, default=None, help="key for signing"
    )
    subparser.add_argument(
        "--mirror", type=arguments.mirror_name_or_url, help="mirror name, path, or URL", 
        required=False, default=None,
    )
    subparser.add_argument(
        "--update-index",
        "--rebuild-index",
        action="store_true",
        default=False,
        help="regenerate buildcache index after building package(s)",
    )
    subparser.add_argument(
        "--with-build-dependencies",
        action="store_true",
        help="include build dependencies in the buildcache",
    )
    subparser.add_argument(
        "--without-build-dependencies",
        action="store_true",
        help="exclude build dependencies from the buildcache",
    )
    subparser.add_argument(
        "--fail-fast",
        action="store_true",
        help="stop pushing on first failure (default is best effort)",
    )
    subparser.add_argument(
        "--base-image", default=None, help="specify the base image for the buildcache"
    )
    subparser.add_argument(
        "--tag",
        "-t",
        default=None,
        help="when pushing to an OCI registry, tag an image containing all root specs and their "
        "runtime dependencies",
    )
    subparser.add_argument(
        "--private",
        action="store_true",
        help="for a private mirror, include non-redistributable packages",
    )
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


def localbuildcache(parser, args):
    locext.local_buildcache(args)
