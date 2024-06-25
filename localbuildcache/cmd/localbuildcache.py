import sys
import spack.config
from spack.extensions import localbuildcache as lext

description = "create buildcache of local packages in environment"
section = "basic"
level = "short"

def setup_parser(subparser):
    subparser.add_argument(
        "--key",
        default=None,
        help="signing key for packges"
    )

    
def localbuildcache(parser, args):
    lext.local_buildcache(args)
