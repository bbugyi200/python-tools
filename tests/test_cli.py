"""Tests the bugyi.tools project's CLI."""

from bugyi.tools import main


def test_main() -> None:
    """Tests main() function."""
    assert main([""]) == 0
