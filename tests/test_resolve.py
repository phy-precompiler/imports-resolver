# pylint: disable=missing-function-docstring

""" test `phy_imports_resolver/_resolve_import.py` """
# imports
from typing import List, Tuple
from pprint import pprint

import pytest

# local imports
from phy_imports_resolver._resolver import _resolve_import_name
from phy_imports_resolver import resolve_entry_file, print_xml_formatted_import_tree
from phy_imports_resolver.resolver import ImportResolver

from ._common import BASE_DIR, SRC_DIR, TEST_OUTPUT_DIR


@pytest.mark.skip()
def test_resolve_import_name():
    pprint(_resolve_import_name('phy_imports_resolver', SRC_DIR))
    pprint(_resolve_import_name('phy_imports_resolver.core', SRC_DIR))
    pprint(_resolve_import_name('phy_imports_resolver.submodule', SRC_DIR))


# @pytest.mark.skip()
def test_resolve_file():
    entry_file = SRC_DIR / 'phy_imports_resolver' / '_resolver.py'
    resolver = ImportResolver(project_dir=SRC_DIR)
    result = resolver.start(entry_file)
    
    with open(TEST_OUTPUT_DIR / '_resolver.xml', 'w+', encoding='utf8') as _f:
        _f.write(str(result))


@pytest.mark.skip()
def test_resolve_pypi_package_module():

    files_to_parse: List[Tuple[str, str]] = [
        # ('tmp/pandas/pandas/__init__.py', 'tmp/pandas'),
        # ('tmp/django/django/__init__.py', 'tmp/django'),
        ('tmp/numpy/numpy/__init__.py', 'tmp/numpy/numpy'),
    ]

    for _file_name, _find_dir_name in files_to_parse:
        file_to_parse = BASE_DIR / _file_name
        parsed_result = resolve_entry_file(
            file_to_parse,
            find_path= BASE_DIR / _find_dir_name
        )
        
        xml_format_result = print_xml_formatted_import_tree(parsed_result)
        with open(TEST_OUTPUT_DIR / 'imports_path.xml', 'w+', encoding='utf8') as _f:
            _f.write(xml_format_result)
