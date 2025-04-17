""" core variables, methods & classes """
# imports
import os
import ast
from pathlib import Path
from typing import Tuple, Optional, Set, TypedDict, List


def _assert_utf8_encoded(file_path: Path, check_bytes: int = 8192):
    """ Assert whether a file is text & encoded with utf-8; or error raised. """
    try:
        with file_path.open('rb') as _file_io:
            chunk = _file_io.read(check_bytes)
            if b'\x00' in chunk:
                # Likely to be binary file
                raise UnicodeDecodeError
            
            chunk.decode('utf-8')
    except (UnicodeDecodeError, OSError):
        # pylint: disable=raise-missing-from
        raise UnicodeDecodeError


def resolve_import_name(
        name: str, 
        base_path: Path, 
        include_suffixes: Tuple[str, ...] = ('.py', '.pyi')
    ) -> Optional[Path]:
    """ resolve module name into path (e.g., foo.bar → foo/bar.py) """
    for _suffix in include_suffixes:
        mod_path = name.replace('.', os.sep) + _suffix
        abs_path = (base_path / mod_path).resolve()

        if abs_path.exists():
            return abs_path

    return None


def extract_import_names(
        code_path: Path, 
        include_suffixes: Tuple[str, ...] = ('.py', )
    ) -> Set[str]:
    """ extract import info by `ast` parsing """
    # only parse utf8 encoded python code file
    if code_path.suffix not in include_suffixes:
        _err_msg = '|'.join(['*' + _sfx for _sfx in include_suffixes])
        raise AssertionError(f'{code_path} is not a python code file ({_err_msg}).')
    
    _assert_utf8_encoded(code_path)

    # parsing code to ast tree    
    import_names: Set[str] = set()

    with code_path.open('r', encoding='utf8') as _file_io:
        ast_tree = ast.parse(_file_io.read(), filename=str(code_path))

    # filter import node
    for ast_node in ast.walk(ast_tree):
        if isinstance(ast_node, ast.Import):
            for alias in ast_node.names:
                import_names.add(alias.name)

        elif isinstance(ast_node, ast.ImportFrom):
            if ast_node.module:
                import_names.add(ast_node.module)
    return import_names


class ImportTree(TypedDict):
    """ json schema for import tree data """
    path: str
    imports: List['ImportTree']


def resolve_entry_file(entry_file_path: Path):
    """ resolve dependent code files starting from given entry code file. """
    entry_file_path = entry_file_path.resolve()
    visited_files: Set[Path] = set()

    def _resolve_file(_file_path: Path) -> ImportTree:
        _file_path = _file_path.resolve()
        if not _file_path.exists():
            # TODO: or raise error ?
            return
        
        if _file_path in visited_files:
            return
        
        visited_files.add(_file_path)

        # extract import names, recursively
        _import_tree: ImportTree = {
            'path': str(_file_path),
            'imports': []
        }

        import_names = extract_import_names(_file_path)
        base_path = _file_path.parent.resolve()

        for _name in import_names:
            # TODO: consider using PYTHONPATH
            resolved_path = resolve_import_name(_name, base_path)
            if resolved_path and str(resolved_path).startswith(str(base_path)):
                _import_tree['imports'].append(
                    _resolve_file(resolved_path)
                )  # recursively

        return _import_tree

    # start recurse
    return _resolve_file(entry_file_path)


if __name__ == '__main__':
    _code = Path(__file__).resolve().parent / '__init__.py'
    from pprint import pprint
    pprint(resolve_entry_file(_code))
