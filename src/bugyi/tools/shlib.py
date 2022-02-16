"""Used to dynamically source bash libraries.

Examples:
    # Source default bash library...
    source $(shlib)

    # Source "foo.sh" bash library...
    source $(shlib foo.sh)

    # Source "foo.sh" bash library (the .sh extension is not necessary)...
    source $(shlib foo)
"""

from __future__ import annotations

from importlib.resources import read_text
from typing import Sequence

import clack


class Config(clack.Config):
    """Command-line arguments."""

    library_name: str

    @classmethod
    def from_cli_args(cls, argv: Sequence[str]) -> Config:
        """Parses command-line arguments."""
        parser = clack.Parser()
        parser.add_argument(
            "library_name",
            default="bugyi",
            nargs="?",
            help="The basename of the bash library you want to use.",
        )

        args = parser.parse_args(argv[1:])
        kwargs = vars(args)

        return Config(**kwargs)


def run(cfg: Config) -> int:
    """This function acts as this tool's main entry point."""
    if "." not in cfg.library_name:
        libname = cfg.library_name + ".sh"
    else:
        libname = cfg.library_name

    print(read_text("bugyi.tools.data.shlib", libname))
    return 0


main = clack.main_factory("shlib", run)
