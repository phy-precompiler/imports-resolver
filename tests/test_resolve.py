""" test `phy_imports_resolver/_resolve_import.py` """
# imports
from pathlib import Path
from pprint import pprint

# local imports
from phy_imports_resolver._resolve_import import resolve_import_name


# constants
TEST_DIR = Path(__file__).resolve().parent
BASE_DIR = TEST_DIR.parent
SRC_DIR = BASE_DIR / 'src'


# pylint: disable=missing-function-docstring
def test_resolve_import_name():
    pprint(resolve_import_name('phy_imports_resolver', SRC_DIR))
    pprint(resolve_import_name('phy_imports_resolver.core', SRC_DIR))
    pprint(resolve_import_name('phy_imports_resolver.submodule', SRC_DIR))
