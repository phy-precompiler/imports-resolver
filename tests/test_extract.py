# pylint: disable=missing-function-docstring
""" test extract import ast nodes """
# imports
import ast as builtin_ast
import pytest

# local imports
from phy_imports_resolver._extractor import extract_import_ast_nodes


# constants
from ._common import SRC_DIR


@pytest.mark.skip()
def test_extract_import_ast_nodes():
    test_py_file = SRC_DIR / 'phy_imports_resolver' / 'resolver.py'
    for import_ast in extract_import_ast_nodes(test_py_file):
        print(builtin_ast.dump(import_ast, indent=4))
