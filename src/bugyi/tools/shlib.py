"""Used to dynamically source bash libraries.

Examples:
    # Source default bash library...
    source $(shlib)

    # Source "foo.sh" bash library...
    source $(shlib foo.sh)

    # Source "foo.sh" bash library (the .sh extension is not necessary)...
    source $(shlib foo)
"""

from importlib.resources import read_text
from typing import Sequence

import clap
from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class Arguments(clap.Arguments):
    """Command-line arguments."""

    library_name: str


def parse_cli_args(argv: Sequence[str]) -> Arguments:
    """Parses command-line arguments."""
    parser = clap.Parser()
    parser.add_argument(
        "library_name",
        default="bugyi",
        nargs="?",
        help="The basename of the bash library you want to use.",
    )

    args = parser.parse_args(argv[1:])
    kwargs = vars(args)

    return Arguments(**kwargs)


def run(args: Arguments) -> int:
    """This function acts as this tool's main entry point."""
    if "." not in args.library_name:
        libname = args.library_name + ".sh"
    else:
        libname = args.library_name

    print(read_text("bugyi.tools.data.shlib", libname))
    return 0


main = clap.main_factory(parse_cli_args, run)
