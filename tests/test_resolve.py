# pylint: disable=missing-function-docstring
""" test `phy_imports_resolver/_resolve_import.py` """
# imports
import pytest

# local imports
from phy_imports_resolver.resolver import ImportResolver

from ._common import SRC_DIR, TEST_OUTPUT_DIR, TMP_DIR


# @pytest.mark.skip()
def test_resolve_file():
    entry_file = SRC_DIR / 'phy_imports_resolver' / 'resolver.py'
    resolver = ImportResolver(project_dir=SRC_DIR)
    result = resolver.start(entry_file)
    
    with open(TEST_OUTPUT_DIR / f'{entry_file.stem}.xml', 'w+', encoding='utf8') as _f:
        _f.write(result.repr_xml())


@pytest.mark.skip()
def test_resolve_pypi_package_module():
    project_dir = TMP_DIR / 'django'
    entire_file = project_dir / 'django' / '__init__.py'
    resolver = ImportResolver(project_dir=project_dir)
    result = resolver.start(entire_file)
    
    with open(TEST_OUTPUT_DIR / 'django.xml', 'w+', encoding='utf8') as _f:
        _f.write(result.repr_xml())
