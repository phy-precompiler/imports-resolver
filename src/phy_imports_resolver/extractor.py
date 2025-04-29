""" extract import ast node from code. """
# imports
import ast as builtin_ast
from enum import Enum
from pathlib import Path
import token as builtin_token
import tokenize as builtin_tokenize
from typing import List, Union
from pprint import pprint


class ImportGrammer(Enum):
    """ enum for import statement grammer rule """
    IMPORT_NAME = 0
    IMPORT_FROM = 1


# TODO: use `phy-core` ast node
_AstNode = builtin_ast.AST


# TODO: use `phy-core` parser
class _Parser:
    
    def parse(self, file: Path) -> _AstNode:
        """ parse code file as ast root node """
        # get file encoding by builtin tokenizer
        _encoding = 'utf-8'  # default encoding
        with builtin_tokenize.open(file) as _f:
            for _tok in builtin_tokenize.generate_tokens(_f.readline):
                if _tok.type == builtin_token.ENCODING:
                    _encoding = _tok.string
                break  # encoding token is placed first or omitted
        
        # parse code file
        with file.open('r', encoding=_encoding) as _f:
            return builtin_ast.parse(_f.read(), filename=str(file))


# TODO: use `phy-core` visitor
class _Visitor(builtin_ast.NodeVisitor):

    # instance attributes
    import_ast_nodes: List[Union[builtin_ast.Import, builtin_ast.ImportFrom]]

    def __init__(self):
        """ constructor """
        super().__init__()
        self.import_ast_nodes = []

    def visit_Import(self, node):
        """ override `visit_Import` method """
        self.import_ast_nodes.append(node)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """ override `visit_ImportFrom` method """
        self.import_ast_nodes.append(node)
        self.generic_visit(node)


if __name__ == '__main__':
    _file = Path(__file__).parent.resolve() / 'extractor.py'
    _parser = _Parser()

    _ast_root = _parser.parse(_file)
    _visitor = _Visitor()
    _visitor.visit(_ast_root)

    pprint(_visitor.import_ast_nodes)
