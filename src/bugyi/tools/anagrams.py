"""Used to generate anagrams of a given word.

What is an anagram?
-------------------
An anagram is formed when letters in a name, word or phrase are rearranged into
another name, word or phrase.
"""

from __future__ import annotations

from collections import defaultdict
from functools import lru_cache as cache
import itertools as it
import json
from pathlib import Path
from typing import Callable, Dict, Optional, Sequence

from bugyi.lib.types import Final
import clap
from pydantic.dataclasses import dataclass
from rich.console import Console


# dynamic globals
console = Console()

# custom types
WordContainer = Dict[str, bool]

# constants
BIG_WORD_MINIMUM: Final = 4
ENGLISH_JSON: Final = str(Path().home() / ".config/words/english.json")
SMALL_WORD_MINIMUM: Final = 3


@dataclass(frozen=True)
class Arguments(clap.Arguments):
    """Command-line arguments."""

    phrase: str
    minimum_word_size: Optional[int]


def parse_cli_args(argv: Sequence[str]) -> Arguments:
    """Parses command-line arguments."""
    parser = clap.Parser()
    parser.add_argument("phrase", help="The phrase to create anagrams from.")
    parser.add_argument(
        "-m",
        "--minimum-word-size",
        type=int,
        default=None,
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

    minimum_word_size = args.minimum_word_size or default_minimum_word_size(
        args.phrase
    )

    found_any_matches = False
    for i in range(minimum_word_size - 1, len(args.phrase)):
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
                sorted(list(valid_words), key=lambda word: (len(word), word))
            )
    return 0


@cache()
def english_words() -> WordContainer:
    """Returns a dictionary of english words to the integer 1.

    Used for fast boolean check.
    """
    result: WordContainer = defaultdict(bool)
    with Path(ENGLISH_JSON).open("r") as fp:
        result.update(json.load(fp))
        return result


def is_word_factory(
    make_word_container: Callable[[], WordContainer]
) -> Callable[[str], bool]:
    """Returns an 'is_word(word: str) -> bool' function."""

    def is_word(word: str) -> bool:
        """Is ``word`` a valid word?."""
        return make_word_container()[word]

    return is_word


def default_minimum_word_size(phrase: str) -> int:
    """Returns the default minimum anagram size."""
    if len(phrase) < 10:
        return SMALL_WORD_MINIMUM
    else:
        return BIG_WORD_MINIMUM


main = clap.main_factory(parse_cli_args, run)
