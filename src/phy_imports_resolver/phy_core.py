# TODO: move to standalone package `phy-core`
""" core members of `phy` """
# imports
from pathlib import Path
from abc import abstractmethod
from typing import Iterator, List, Self, Tuple, Optional, Any

# always use `builtin` prefix for ambiguous token-related names
import token as builtin_token
import tokenize as builtin_tokenize
from tokenize import TokenInfo as BuiltinTokenInfo



class Tokenizer:
    """ simple tokenzier for internal usage """

    # instance attributes
    _tok_list: List[BuiltinTokenInfo]

    # internal typings
    Mark = int

    def __init__(self, tok_gen: Iterator[BuiltinTokenInfo]):
        """ constructor; always use shorthand `tok` to avoid ambiguity """
        # filter meaningful tokens
        self._tok_list: List[BuiltinTokenInfo] = []
        for tok in tok_gen:
            # skip token.ENCODING
            if tok.type == builtin_token.ENCODING:
                continue

            # token.NL and token.NEWLINE are subtly different, and the distinction matters 
            # when you're tokenizing Python source code.
            # + token.NL:	A non-significant newline (e.g. inside multi-line blocks)
            # + token.NEWLINE:	A logical line break (end of a full Python statement)
            if tok.type in (builtin_token.NL, builtin_token.COMMENT):
                continue
            
            # `token.ERRORTOKEN` is a special token type in Python's tokenize module used to 
            # represent unexpected or invalid characters in the input stream.
            if tok.type == builtin_token.ERRORTOKEN and tok.string.isspace():
                continue
            
            # encounter newline
            if (
                tok.type == builtin_token.NEWLINE
                and (
                    self._tok_list  # ensure self._tok_list can be subscripted
                    and self._tok_list[-1].type == builtin_token.NEWLINE
                )
            ):
                continue

            self._tok_list.append(tok)

        # current index
        self._index = 0  

    def peek(self) -> BuiltinTokenInfo:
        """ return the next token *WITHOUT* updating the index """
        return self._tok_list[self._index]


    def get_next(self) -> BuiltinTokenInfo:
        """ return the next token and *DOES* update the index """
        tok = self.peek()
        self._index += 1

        return tok
    
    @property
    def mark(self) -> Mark:
        """ getter for index """
        return self._index
    
    def reset(self, to_index: Mark) -> None:
        """ reset index """
        if to_index == self._index:
            return
        
        assert 0 <= to_index <= len(self._tok_list), (to_index, len(self._tok_list))

        # restore previous index for later use
        prev_index = self._index
        _ = prev_index

        self._index = to_index

    @classmethod
    def tokenize(cls, file: Path) -> Self:
        """ tokenize a given file path """
        with builtin_tokenize.open(file) as _f:
            tok_gen = builtin_tokenize.generate_tokens(_f.readline)
            return cls(tok_gen)



class BaseParser:
    """ simple parser for internal usage """

    # instance attributes
    _toknzer: Tokenizer

    # class attributes
    KEYWORDS: Tuple[str] = ()

    def __init__(self, toknzer: Tokenizer):
        """ constructor; alway use shorthand `toknzer` to distingush from builtin `tokenize` module """
        self._toknzer = toknzer

    @abstractmethod
    def start(self) -> Any:
        """ expected grammar entry point """
        pass

    def expect(self, tok_type: str) -> Optional[BuiltinTokenInfo]:
        """ `expect()` checks that a specific token or symbol is present next.

        It is typically used inside grammar rules to ensure the next token matches a 
        required type (like a keyword, punctuation, etc).
        """
        tok = self._toknzer.peek()
        
        # The `.string` attribute of a TokenInfo object is the actual string from the source code 
        # that the token represents.
        if tok.string == tok_type:
            return self._toknzer.get_next()
        
        # `builtin_token.EXACT_TOKEN_TYPES` a dictionary that maps operator strings (like '+', '==', '(', etc.) 
        # to their exact token types (integer constants).
        if tok_type in builtin_token.EXACT_TOKEN_TYPES:
            if tok.type == builtin_token.EXACT_TOKEN_TYPES[tok_type]:
                return self._toknzer.get_next()
        
        # other token types defined in builtin `token` module; pylint: disable=invalid-name
        TOKEN_TYPES = builtin_token.__dict__
        if tok_type in TOKEN_TYPES:
            if tok.type == TOKEN_TYPES[tok_type]:
                return self._toknzer.get_next()

        # operator   
        if tok.type == builtin_token.OP and tok.string == tok_type:
            return self._toknzer.get_next()
        
        return None

    # some common parsers
    def name(self) -> Optional[BuiltinTokenInfo]:
        """ parse name (identifier) """
        tok = self._toknzer.peek()

        # the identifier should not be keyword
        if tok.type == builtin_token.NAME and tok.string not in self.KEYWORDS:
            return self._toknzer.get_next()
        return None

    def number(self) -> Optional[BuiltinTokenInfo]:
        """ parse number """
        tok = self._toknzer.peek()
        if tok.type == builtin_token.NUMBER:
            return self._toknzer.get_next()
        return None
    
    def string(self) -> Optional[BuiltinTokenInfo]:
        """ parse string """
        tok = self._toknzer.peek()
        if tok.type == builtin_token.STRING:
            return self._toknzer.get_next()
        return None
    
    def op(self) -> Optional[BuiltinTokenInfo]:
        """ parse operator """
        tok = self._toknzer.peek()
        if tok.type == builtin_token.OP:
            return self._toknzer.get_next()
        return None
