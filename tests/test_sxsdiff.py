import pytest
import six

from sxsdiff import DiffCalculator
from sxsdiff.calculator import DIFF_DELETE
from sxsdiff.calculator import DIFF_EQUAL
from sxsdiff.calculator import PlainElement
from sxsdiff.calculator import DeletionElement


@pytest.fixture
def diff_calc():
    return DiffCalculator()


same_codes_test_data = [
    "\n",
    "abc",
    "def\nghi",
    "a\nb\nc\n",
]


@pytest.mark.parametrize('code', same_codes_test_data,
                         ids=list(map(repr, same_codes_test_data)))
def test_same_code(code, diff_calc):
    result = diff_calc.run(code, code)
    result = list(result)
    assert len(result) == code.count('\n') + 1
    for change in result:
        assert not change.changed
        assert change.left == change.right
        assert change.left_no == change.right_no


first_line_changed_test_data = [
    ("This line is different from right.\n"
     "This is second line.\n"
     "This is third line.\n",
     "This line is different from left.\n"
     "This is second line.\n"
     "This is third line.\n"),
]


@pytest.mark.parametrize('left,right', first_line_changed_test_data)
def test_first_line_changed(left, right, diff_calc):
    result = diff_calc.run(left, right)
    result = list(result)
    assert result[0].changed
    assert result[0].left != result[0].right
    for change in result[1:]:
        assert not change.changed
        assert change.left == change.right


def test_simple_line_segment(diff_calc):
    left = 'abc'
    right = 'ac'
    result = diff_calc.run(left, right)
    result = list(result)
    assert len(result) == 1
    assert result[0].changed
    assert result[0].left._change_flag == DIFF_DELETE
    assert result[0].right._change_flag == DIFF_EQUAL
    # 'a' character, same
    assert result[0].left.elements[0].flag == DIFF_EQUAL
    assert isinstance(result[0].left.elements[0], PlainElement)
    # 'b' character, delete
    assert result[0].left.elements[1].flag == DIFF_DELETE
    assert isinstance(result[0].left.elements[1], DeletionElement)
    # 'c' character, same
    assert isinstance(result[0].left.elements[2], PlainElement)


test_data_lao = """\
The Way that can be told of is not the eternal Way;
The name that can be named is not the eternal name.
The Nameless is the origin of Heaven and Earth;
The Named is the mother of all things.
Therefore let there always be non-being,
  so we may see their subtlety,
And let there always be being,
  so we may see their outcome.
The two are the same,
But after they are produced,
  they have different names.
"""

test_data_tzu = """\
The Nameless is the origin of Heaven and Earth;
The named is the mother of all things.

Therefore let there always be non-being,
  so we may see their subtlety,
And let there always be being,
  so we may see their outcome.
The two are the same,
But after they are produced,
  they have different names.
They both may be called deep and profound.
Deeper and more profound,
The door of all subtleties!
"""


def test_diff_lao_tzu(diff_calc):
    result = diff_calc.run(test_data_lao, test_data_tzu)
    result = list(result)

    assert result[0].changed
    assert result[0].left_no == 1
    assert result[0].right_no is None
    assert str(result[0].left)
    assert not str(result[0].right)

    assert result[1].changed
    assert result[1].left_no == 2
    assert result[1].right_no is None
    assert str(result[1].left)
    assert not str(result[1].right)

    assert not result[2].changed
    assert result[2].left_no == 3
    assert result[2].right_no == 1

    assert result[3].changed
    assert result[3].left_no == 4
    assert result[3].right_no == 2

    assert result[4].changed
    assert result[4].left_no is None
    assert result[4].right_no == 3

    # Not changed
    for change in result[5:12]:
        assert not change.changed
