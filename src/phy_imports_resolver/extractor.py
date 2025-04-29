# pylint: disable=missing-function-docstring
""" extract import statements """
# imports
from typing import Any, Optional, Callable

from .phy_core import BaseParser


class ImportsParser(BaseParser):
    """ parser for import statement; this class is mainly generate by `pegen` """

    def negative_lookahead(self, func: Callable[..., object], *args: object) -> bool:
        mark = self.mark
        ok = func(*args)
        self.reset(mark)
        return not ok
    
    def start(self) -> Optional[Any]:
        # start: import_name | import_from
        mark = self.mark
        if (
            (import_name := self.import_name())
        ):
            return import_name
        self.reset(mark)
        if (
            (import_from := self.import_from())
        ):
            return import_from
        self.reset(mark)
        return None

    
    def import_name(self) -> Optional[Any]:
        # import_name: 'import' dotted_as_names
        mark = self.mark
        if (
            (literal := self.expect('import'))
            and
            (dotted_as_names := self.dotted_as_names())
        ):
            return [literal, dotted_as_names]
        self.reset(mark)
        return None

    
    def import_from(self) -> Optional[Any]:
        # import_from: 'from' (('.' | '...'))* dotted_name 'import' import_from_targets | 'from' (('.' | '...'))+ 'import' import_from_targets
        mark = self.mark
        if (
            (literal := self.expect('from'))
            and
            (_loop0_1 := self._loop0_1(),)
            and
            (dotted_name := self.dotted_name())
            and
            (literal_1 := self.expect('import'))
            and
            (import_from_targets := self.import_from_targets())
        ):
            return [literal, _loop0_1, dotted_name, literal_1, import_from_targets]
        self.reset(mark)
        if (
            (literal := self.expect('from'))
            and
            (_loop1_2 := self._loop1_2())
            and
            (literal_1 := self.expect('import'))
            and
            (import_from_targets := self.import_from_targets())
        ):
            return [literal, _loop1_2, literal_1, import_from_targets]
        self.reset(mark)
        return None

    
    def import_from_targets(self) -> Optional[Any]:
        # import_from_targets: '(' import_from_as_names ','? ')' | import_from_as_names !',' | '*'
        mark = self.mark
        if (
            (literal := self.expect('('))
            and
            (import_from_as_names := self.import_from_as_names())
            and
            (opt := self.expect(','),)
            and
            (literal_1 := self.expect(')'))
        ):
            return [literal, import_from_as_names, opt, literal_1]
        self.reset(mark)
        if (
            (import_from_as_names := self.import_from_as_names())
            and
            (self.negative_lookahead(self.expect, ','))
        ):
            return import_from_as_names
        self.reset(mark)
        if (
            (literal := self.expect('*'))
        ):
            return literal
        self.reset(mark)
        return None

    
    def import_from_as_names(self) -> Optional[Any]:
        # import_from_as_names: ','.import_from_as_name+
        mark = self.mark
        if (
            (_gather_3 := self._gather_3())
        ):
            return _gather_3
        self.reset(mark)
        return None

    
    def import_from_as_name(self) -> Optional[Any]:
        # import_from_as_name: NAME ['as' NAME]
        mark = self.mark
        if (
            (name := self.name())
            and
            (opt := self._tmp_5(),)
        ):
            return [name, opt]
        self.reset(mark)
        return None

    
    def dotted_as_names(self) -> Optional[Any]:
        # dotted_as_names: ','.dotted_as_name+
        mark = self.mark
        if (
            (_gather_6 := self._gather_6())
        ):
            return _gather_6
        self.reset(mark)
        return None

    
    def dotted_as_name(self) -> Optional[Any]:
        # dotted_as_name: dotted_name ['as' NAME]
        mark = self.mark
        if (
            (dotted_name := self.dotted_name())
            and
            (opt := self._tmp_8(),)
        ):
            return [dotted_name, opt]
        self.reset(mark)
        return None

    def dotted_name(self) -> Optional[Any]:
        # dotted_name: dotted_name '.' NAME | NAME
        mark = self.mark
        if (
            (dotted_name := self.dotted_name())
            and
            (literal := self.expect('.'))
            and
            (name := self.name())
        ):
            return [dotted_name, literal, name]
        self.reset(mark)
        if (
            (name := self.name())
        ):
            return name
        self.reset(mark)
        return None

    
    def _loop0_1(self) -> Optional[Any]:
        # _loop0_1: ('.' | '...')
        mark = self.mark
        children = []
        while (
            (_tmp_9 := self._tmp_9())
        ):
            children.append(_tmp_9)
            mark = self.mark
        self.reset(mark)
        return children

    
    def _loop1_2(self) -> Optional[Any]:
        # _loop1_2: ('.' | '...')
        mark = self.mark
        children = []
        while (
            (_tmp_10 := self._tmp_10())
        ):
            children.append(_tmp_10)
            mark = self.mark
        self.reset(mark)
        return children

    
    def _loop0_4(self) -> Optional[Any]:
        # _loop0_4: ',' import_from_as_name
        mark = self.mark
        children = []
        while (
            (self.expect(','))
            and
            (elem := self.import_from_as_name())
        ):
            children.append(elem)
            mark = self.mark
        self.reset(mark)
        return children

    
    def _gather_3(self) -> Optional[Any]:
        # _gather_3: import_from_as_name _loop0_4
        mark = self.mark
        if (
            (elem := self.import_from_as_name())
            is not None
            and
            (seq := self._loop0_4())
            is not None
        ):
            return [elem] + seq
        self.reset(mark)
        return None

    
    def _tmp_5(self) -> Optional[Any]:
        # _tmp_5: 'as' NAME
        mark = self.mark
        if (
            (literal := self.expect('as'))
            and
            (name := self.name())
        ):
            return [literal, name]
        self.reset(mark)
        return None

    
    def _loop0_7(self) -> Optional[Any]:
        # _loop0_7: ',' dotted_as_name
        mark = self.mark
        children = []
        while (
            (self.expect(','))
            and
            (elem := self.dotted_as_name())
        ):
            children.append(elem)
            mark = self.mark
        self.reset(mark)
        return children

    
    def _gather_6(self) -> Optional[Any]:
        # _gather_6: dotted_as_name _loop0_7
        mark = self.mark
        if (
            (elem := self.dotted_as_name())
            is not None
            and
            (seq := self._loop0_7())
            is not None
        ):
            return [elem] + seq
        self.reset(mark)
        return None

    
    def _tmp_8(self) -> Optional[Any]:
        # _tmp_8: 'as' NAME
        mark = self.mark
        if (
            (literal := self.expect('as'))
            and
            (name := self.name())
        ):
            return [literal, name]
        self.reset(mark)
        return None

    
    def _tmp_9(self) -> Optional[Any]:
        # _tmp_9: '.' | '...'
        mark = self.mark
        if (
            (literal := self.expect('.'))
        ):
            return literal
        self.reset(mark)
        if (
            (literal := self.expect('...'))
        ):
            return literal
        self.reset(mark)
        return None

    
    def _tmp_10(self) -> Optional[Any]:
        # _tmp_10: '.' | '...'
        mark = self.mark
        if (
            (literal := self.expect('.'))
        ):
            return literal
        self.reset(mark)
        if (
            (literal := self.expect('...'))
        ):
            return literal
        self.reset(mark)
        return None

    KEYWORDS = ('as', 'from', 'import')
    SOFT_KEYWORDS = ()
