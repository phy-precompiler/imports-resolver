""" extract import ast node """
# imports
from pathlib import Path
from typing import Iterator, List, Self

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
