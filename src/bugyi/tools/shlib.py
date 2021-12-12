"""Contains the bugyi.tools package's main entry point."""

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
        help=(
            "The basename (i.e. no extension) of the bash library you want to"
            " use."
        ),
    )

    args = parser.parse_args(argv[1:])
    kwargs = vars(args)

    return Arguments(**kwargs)


def run(args: Arguments) -> int:
    """This function acts as this tool's main entry point."""
    print(read_text("bugyi.tools.data.shlib", args.library_name + ".sh"))
    return 0


main = clap.main_factory(parse_cli_args, run)
