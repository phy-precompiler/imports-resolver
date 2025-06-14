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

from ._common import BASE_DIR, SRC_DIR, TEST_OUTPUT_DIR, TMP_DIR


@pytest.mark.skip()
def test_resolve_import_name():
    pprint(_resolve_import_name('phy_imports_resolver', SRC_DIR))
    pprint(_resolve_import_name('phy_imports_resolver.core', SRC_DIR))
    pprint(_resolve_import_name('phy_imports_resolver.submodule', SRC_DIR))


@pytest.mark.skip()
def test_resolve_file():
    entry_file = SRC_DIR / 'phy_imports_resolver' / 'resolver.py'
    resolver = ImportResolver(project_dir=SRC_DIR)
    result = resolver.start(entry_file)
    
    with open(TEST_OUTPUT_DIR / '_resolver.xml', 'w+', encoding='utf8') as _f:
        _f.write(str(result))


# @pytest.mark.skip()
def test_resolve_pypi_package_module():
    project_dir = TMP_DIR / 'django'
    entire_file = project_dir / 'django' / '__init__.py'
    resolver = ImportResolver(project_dir=project_dir)
    result = resolver.start(entire_file)
    
    with open(TEST_OUTPUT_DIR / 'django.xml', 'w+', encoding='utf8') as _f:
        _f.write(str(result))
