""" extract import ast node from code. """
# imports
import ast as builtin_ast
from enum import Enum
from pathlib import Path
import token as builtin_token
import tokenize as builtin_tokenize


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
            for _token in builtin_tokenize.generate_tokens(_f.readline):
                if _token.type != builtin_token.ENCODING:
                    raise builtin_tokenize.TokenError(f'Cannot recognize the encoding of {file}.')
                
                _encoding = _token.string
                break  # first token is encoding
        
        # parse code file
        with file.open('r', encoding=_encoding) as _f:
            return builtin_ast.parse(_f.read(), filename=str(file))
        