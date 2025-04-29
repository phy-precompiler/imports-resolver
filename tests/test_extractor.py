""" test `phy_imports_resolver/_extractor.py` """
# imports
from pathlib import Path
from pprint import pprint

# local imports
from phy_imports_resolver._extractor import extract_import_ast_nodes


# constants
TEST_DIR = Path(__file__).resolve().parent
BASE_DIR = TEST_DIR.parent
SRC_DIR = BASE_DIR / 'src'


# pylint: disable=missing-function-docstring
def test_extract_import_ast_nodes():
    test_py_file = SRC_DIR / 'phy_imports_resolver' / '_extractor.py'
    pprint(extract_import_ast_nodes(test_py_file))
