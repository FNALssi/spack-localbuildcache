import sys
import spack.config
from spack.extensions import localbuildcache as lext


def setup_parser(subparser):
    subparser.add_argument(
        "--key",
        default=None,
        help="signing key for packges"
    )

    
def installdir(parser, args):
    lext.local_buildcache(args)
