# pylint: disable=missing-function-docstring
""" test internal tokenizer """
# imports
from pathlib import Path
from pprint import pprint

from phy_imports_resolver.phy_core import Tokenizer


# constants
TEST_DIR = Path(__file__).parent.resolve()


def test_tokenize():
    target_file = TEST_DIR / 'imports_parser.py'
    toknzer = Tokenizer.tokenize(target_file)

    pprint(toknzer._tok_list)
