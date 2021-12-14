"""Used to generate anagrams of a given word.

What is an anagram?
-------------------
An anagram is formed when letters in a name, word or phrase are rearranged into
another name, word or phrase.
"""

from __future__ import annotations

from functools import lru_cache as cache
import itertools as it
import json
from pathlib import Path
from typing import Callable, Sequence

from bugyi.lib.types import Final, Literal
import clap
from pydantic.dataclasses import dataclass
from rich.console import Console


console = Console()

ENGLISH_JSON: Final = str(Path().home() / ".config/words/english.json")
ONE = Literal[1]


@dataclass(frozen=True)
class Arguments(clap.Arguments):
    """Command-line arguments."""

    phrase: str
    minimum_word_size: int


def parse_cli_args(argv: Sequence[str]) -> Arguments:
    """Parses command-line arguments."""
    parser = clap.Parser()
    parser.add_argument("phrase", help="The phrase to create anagrams from.")
    parser.add_argument(
        "-m",
        "--minimum-word-size",
        type=int,
        default=4,
        help=(
            "The minimum size of the anagrams we will output. Defaults to"
            " %(default)s."
        ),
    )

    args = parser.parse_args(argv[1:])
    kwargs = vars(args)

    return Arguments(**kwargs)


def run(args: Arguments) -> int:
    """This function acts as this tool's main entry point."""
    is_english_word = is_word_factory(english_words)

    found_any_matches = False
    for i in range(args.minimum_word_size - 1, len(args.phrase)):
        valid_words = set()
        for combo in it.combinations(args.phrase, i + 1):
            new_word = "".join(combo)
            if is_english_word(new_word):
                valid_words.add(new_word)

        if valid_words:
            if found_any_matches:
                console.print()
            else:
                found_any_matches = True

            console.rule(f"{i + 1}-letter words", style="bold black")
            console.print(
                sorted(
                    list(valid_words), key=lambda word: (len(word), word)
                )
            )
    return 0


@cache()
def english_words() -> dict[str, ONE]:
    """Returns a dictionary of english words to the integer 1.

    Used for fast boolean check.
    """
    with Path(ENGLISH_JSON).open("r") as fp:
        result: dict[str, ONE] = json.load(fp)
        return result


def is_word_factory(
    lang_words: Callable[[], dict[str, ONE]]
) -> Callable[[str], bool]:
    """Returns an 'is_word(word: str) -> bool' function."""

    def is_word(word: str) -> bool:
        """Is ``word`` a valid word?."""
        return word in lang_words()

    return is_word


main = clap.main_factory(parse_cli_args, run)
