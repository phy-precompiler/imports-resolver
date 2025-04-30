# pylint: disable=missing-function-docstring

""" test `phy_imports_resolver/_resolve_import.py` """
# imports
from pathlib import Path
from typing import List, Tuple
from pprint import pprint

import pytest

# local imports
from phy_imports_resolver._resolve_import import _resolve_import_name
from phy_imports_resolver import resolve_entry_file, print_xml_formatted_import_tree


# constants
TEST_DIR = Path(__file__).resolve().parent
BASE_DIR = TEST_DIR.parent
SRC_DIR = BASE_DIR / 'src'
TMP_DIR = BASE_DIR / 'tmp'


@pytest.mark.skip()
def test_resolve_import_name():
    pprint(_resolve_import_name('phy_imports_resolver', SRC_DIR))
    pprint(_resolve_import_name('phy_imports_resolver.core', SRC_DIR))
    pprint(_resolve_import_name('phy_imports_resolver.submodule', SRC_DIR))


@pytest.mark.skip()
def test_resolve_file():
    pprint(resolve_entry_file(SRC_DIR / 'phy_imports_resolver' / '_resolve_import.py'))


def test_resolve_pypi_package_module():

    files_to_parse: List[Tuple[str, str]] = [
        (r'tmp\tomlkit\tomlkit\__init__.py', r'tmp\tomlkit'),
    ]

    for _file_name, _find_dir_name in files_to_parse:
        file_to_parse = BASE_DIR / _file_name
        parsed_result = resolve_entry_file(
            file_to_parse,
            find_path= BASE_DIR / _find_dir_name
        )
        
        xml_format_result = print_xml_formatted_import_tree(parsed_result)
        with open(BASE_DIR / _find_dir_name / 'imports_path.xml', 'w+', encoding='utf8') as _f:
            _f.write(xml_format_result)
