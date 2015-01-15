# -*- coding: utf-8 -*-
import itertools
import re

import diff_match_patch


DIFF_DELETE = diff_match_patch.diff_match_patch.DIFF_DELETE
DIFF_EQUAL = diff_match_patch.diff_match_patch.DIFF_EQUAL
DIFF_INSERT = diff_match_patch.diff_match_patch.DIFF_INSERT


class Element(object):
    __slots__ = ['text', 'flag']

    def __init__(self, text, flag):
        self.text = text
        self.flag = flag

    def __eq__(self, other):
        return self.text == other.text and self.flag == other.flag

    def __ne__(self, other):
        return self.text != other.text or self.flag != other.flag

    def __str__(self):
        return self.text

    def __repr__(self):
        return '<%s at %X: %s>' % (
            self.__class__.__name__, id(self), repr(self.text))

    @property
    def is_changed(self):
        return self.flag != DIFF_EQUAL


class PlainElement(Element):
    def __init__(self, text):
        super(PlainElement, self).__init__(text, DIFF_EQUAL)


class AdditionElement(Element):
    def __init__(self, text):
        super(AdditionElement, self).__init__(text, DIFF_INSERT)


class DeletionElement(Element):
    def __init__(self, text):
        super(DeletionElement, self).__init__(text, DIFF_DELETE)


class ElementsHolder(object):
    __slots__ = ['elements', '_change_flag']

    def __init__(self, *items):
        self._change_flag = DIFF_EQUAL
        if not items:
            self.elements = []
        else:
            self.elements = list(items)

    def append(self, elem):
        # Update holder flag
        if self._change_flag == DIFF_EQUAL:
            self._change_flag = elem.flag
        # Meld into previos one if element flag is same
        if len(self.elements):
            prev_elem = self.elements[-1]
            if not prev_elem.text or prev_elem.flag == elem.flag:
                self.elements[-1] = Element(
                    prev_elem.text + elem.text, elem.flag)
                return
        self.elements.append(elem)

    def __str__(self):
        return ''.join((elem.text for elem in self.elements if elem.text))

    def __eq__(self, other):
        return self.elements == other.elements

    def __ne__(self, other):
        return self.elements != other.elements

    def __len__(self):
        return len(self.elements)

    def __repr__(self):
        if self._change_flag == DIFF_EQUAL:
            type_text = 'EQUAL'
        elif self._change_flag == DIFF_INSERT:
            type_text = 'INSERT'
        else:
            type_text = 'DELETE'
        return '<%s> ' % type_text + repr(self.elements)


class DiffCalculator(object):
    """Calculate a side-by-side line based diff."""

    def __init__(self):
        self.dmp = diff_match_patch.diff_match_patch()

    def calc_diff_result(self, old, new):
        diffs = self.dmp.diff_main(old, new, checklines=False)
        self.dmp.diff_cleanupSemantic(diffs)
        return diffs

    @classmethod
    def _coerce_holder(cls, holder):
        if holder:
            return holder
        return ElementsHolder()

    @classmethod
    def _coerce_holders(cls, l, r):
        return cls._coerce_holder(l), cls._coerce_holder(r)

    @classmethod
    def _yield_open_entry(cls, open_entry):
        """Yields all open entries."""
        ls, rs = open_entry
        # Get unchanged parts onto the right line
        if ls[0] == rs[0]:
            yield False, str(ls[0]), str(rs[0])
            for l, r in itertools.izip_longest(ls[1:], rs[1:]):
                l, r = cls._coerce_holders(l, r)
                yield True, l, r
        elif ls[-1] == rs[-1]:
            for l, r in itertools.izip_longest(ls[:-1], rs[:-1]):
                l, r = cls._coerce_holders(l, r)
                yield l != r, l, r
            yield False, str(ls[-1]), str(rs[-1])
        else:
            for l, r in itertools.izip_longest(ls, rs):
                l, r = cls._coerce_holders(l, r)
                yield True, l, r

    def run(self, old, new):
        diffs = self.calc_diff_result(old, new)
        re_linesplit = re.compile(r'(?:\r?\n)')
        open_entry = ([ElementsHolder()], [ElementsHolder()])
        for flag, data in diffs:
            lines = re_linesplit.split(data)
            # Merge with previous entry if still open
            ls, rs = open_entry
            line = lines[0]
            if flag == DIFF_EQUAL:
                ls[-1].append(PlainElement(line))
                rs[-1].append(PlainElement(line))
            elif flag == DIFF_INSERT:
                rs[-1].append(AdditionElement(line))
            elif flag == DIFF_DELETE:
                ls[-1].append(DeletionElement(line))
            lines = lines[1:]
            if lines:
                if flag == DIFF_EQUAL:
                    # Push out open entry
                    for entry in self._yield_open_entry(open_entry):
                        yield entry
                    # Directly push out lines until last
                    for line in lines[:-1]:
                        yield False, line, line
                    # Keep last line open
                    open_entry = (
                        [ElementsHolder(PlainElement(lines[-1]))],
                        [ElementsHolder(PlainElement(lines[-1]))],
                    )
                elif flag == DIFF_INSERT:
                    ls, rs = open_entry
                    for line in lines:
                        rs.append(ElementsHolder(AdditionElement(line)))
                elif flag == DIFF_DELETE:
                    ls, rs = open_entry
                    for line in lines:
                        ls.append(ElementsHolder(DeletionElement(line)))
        # Push out open entry
        for entry in self._yield_open_entry(open_entry):
            yield entry
