# pylint: disable=missing-function-docstring
""" test `phy_imports_resolver/_resolve_import.py` """
# imports
import os
import shutil
import pytest

# local imports
from phy_imports_resolver.resolver import ImportResolver

from ._common import SRC_DIR, TEST_OUTPUT_DIR, TMP_DIR


@pytest.mark.skip()
def test_resolve_file():
    entry_file = SRC_DIR / 'phy_imports_resolver' / 'resolver.py'
    resolver = ImportResolver(project_dir=SRC_DIR)
    result = resolver.start(entry_file)
    
    with open(TEST_OUTPUT_DIR / f'{entry_file.stem}.xml', 'w+', encoding='utf8') as _f:
        _f.write(str(result))


# Make file & package to be resolved, mainly partially copy from popular pypi repo
@pytest.mark.skip()
def test_make_resolve_target():
    from_dir = TMP_DIR / 'django'
    target_dir = TMP_DIR / 'test_target'

    # clean target dir
    shutil.rmtree(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    copy_items = [
        'django/*.py',
        'django/apps/*.py',
        'django/urls/*.py',
    ]

    for _item in copy_items:
        for src_path in from_dir.glob(_item):  # use `glob` to match wildcard
            dst_path = (target_dir / _item).parent / src_path.name

            dst_dir = dst_path.parent
            dst_dir.mkdir(parents=True, exist_ok=True)

            shutil.copy(src_path, dst_path)


@pytest.mark.skip()
@pytest.mark.dependency(name="test_make_resolve_target")
def test_resolve_target():
    project_dir = TMP_DIR / 'test_target'
    entire_file = project_dir / 'django' / '__init__.py'
    resolver = ImportResolver(project_dir=project_dir)

    try:
        result = resolver.start(entire_file)

    except RecursionError:
        print('Resolved mod: ', resolver.resolved_mod)
    
    with open(TEST_OUTPUT_DIR / 'test_target.xml', 'w+', encoding='utf8') as _f:
        _f.write(str(result))


@pytest.mark.skip()
def test_resolve_pypi_package_module():
    lib_name = 'numpy'
    project_dir = TMP_DIR / lib_name
    entire_file = project_dir / lib_name / '__init__.py'
    resolver = ImportResolver(project_dir=project_dir)

    try:
        result = resolver.start(entire_file)

    except RecursionError:
        print('Resolved mod: ', resolver.resolved_mod)
    
    with open(TEST_OUTPUT_DIR / f'{lib_name}.xml', 'w+', encoding='utf8') as _f:
        _f.write(str(result))


@pytest.mark.skip()
def test_resolve_result_coverage():
    lib_name = 'django'
    project_dir = TMP_DIR / lib_name
    project_src_dir = project_dir / lib_name

    # walk project directory
    py_file_names = []
    for _, _, _files in os.walk(str(project_src_dir.resolve())):
        for _file_name in _files:
            if _file_name.endswith('.py'):
                if _file_name != '__init__.py':
                    py_file_names.append(_file_name)
    
    print(len(py_file_names))

    # test coverage
    with open(TEST_OUTPUT_DIR / f'{lib_name}.xml', encoding='utf8') as _f:
        xml_str = _f.read()

    for _py_file_name in py_file_names:
        if _py_file_name not in xml_str:
            print(f'Not included in resolved tree: {_py_file_name}')
