# -*- coding: utf-8 -*-
from __future__ import print_function

import contextlib
import textwrap
from xml.sax.saxutils import escape

from sxsdiff.generators import BaseGenerator


_html_escape_table = {
    ' ': "&nbsp;",
    '"': "&quot;",
    "'": "&apos;",
}


def html_escape(text):
    return escape(text, _html_escape_table)


INLINE_CSS = """
    table {
    border-spacing:0;
    }

    * {
    box-sizing:border-box;
    }

    .container {
    width:100%;
    padding-left:30px;
    padding-right:30px;
    }

    .blob-wrapper {
    overflow-x:auto;
    overflow-y:hidden;
    border-bottom-left-radius:3px;
    border-bottom-right-radius:3px;
    }

    .diff-table {
    width:100%;
    border-collapse:separate;
    }

    .diff-table tr:not(:last-child) .line-comments {
    border-top:1px solid #eee;
    border-bottom:1px solid #eee;
    }

    .blob-num {
    width:1%;
    min-width:50px;
    padding-left:10px;
    padding-right:10px;
    font-family:Consolas,"Liberation Mono",Menlo,Courier,monospace;
    font-size:12px;
    line-height:18px;
    color:rgba(0,0,0,0.3);
    vertical-align:top;
    text-align:right;
    border:solid #eee;
    cursor:pointer;
    -webkit-user-select:none;
    -moz-user-select:none;
    -ms-user-select:none;
    user-select:none;
    border-width:0 1px 0 0;
    }

    .blob-num:hover {
    color:rgba(0,0,0,0.6);
    }

    .blob-num:before {
    content:attr(data-line-number);
    }

    .blob-num.non-expandable:hover {
    color:rgba(0,0,0,0.3);
    }

    .blob-code {
    position:relative;
    padding-left:10px;
    padding-right:10px;
    font-family:Consolas,"Liberation Mono",Menlo,Courier,monospace;
    font-size:12px;
    color:#333;
    vertical-align:top;
    white-space:pre;
    overflow:visible;
    }

    .blob-code .x-first {
    border-top-left-radius:.2em;
    border-bottom-left-radius:.2em;
    }

    .blob-code .x-last {
    border-top-right-radius:.2em;
    border-bottom-right-radius:.2em;
    }

    .blob-code-addition {
    background-color:#eaffea;
    }

    .blob-code-addition .x {
    background-color:#a6f3a6;
    }

    .blob-num-addition {
    background-color:#dbffdb;
    border-color:#c1e9c1;
    }

    .blob-code-deletion {
    background-color:#ffecec;
    }

    .blob-code-deletion .x {
    background-color:#f8cbcb;
    }

    .blob-num-deletion {
    background-color:#fdd;
    border-color:#f1c0c0;
    }

    .selected-line.blob-code {
    background-color:#f8eec7;
    }

    .selected-line.blob-num {
    background-color:#f6e8b5;
    border-color:#f0db88;
    }

    .file-diff-split .blob-code {
    width:49%;
    white-space:pre-wrap;
    word-break:break-word;
    }

    .file-diff-split .empty-cell {
    cursor:default;
    background-color:#fafafa;
    border-right-color:#eee;
    }

    .file {
    position:relative;
    margin-top:20px;
    margin-bottom:15px;
    border:1px solid #ddd;
    border-radius:3px;
    }

    .file .meta {
    text-shadow:0 1px 0 #fff;
    border-bottom:1px solid #d8d8d8;
    background-color:#f7f7f7;
    border-top-left-radius:4px;
    border-top-right-radius:4px;
    padding:5px 10px;
    }"""


class GitHubGenerator(BaseGenerator):
    def __init__(self, file=None):
        self._file = file

    def _spit(self, content):
        print(content, file=self._file)

    def visit_row(self, changed, left, left_no, right, right_no):
        if not changed:
            self._spit_unchanged_side(left, left_no)
            self._spit_unchanged_side(right, right_no)
        else:
            self._spit_changed_side(left, left_no, 'deletion')
            self._spit_changed_side(right, right_no, 'addition')

    @contextlib.contextmanager
    def wrap_row(self, changed, left, left_no, right, right_no):
        self._spit('      <tr>')
        yield
        self._spit('      </tr>')

    @contextlib.contextmanager
    def wrap_result(self, sxs_result):
        self._spit(textwrap.dedent("""\
        <head>
          <style>
          %s
          </style>
        </head>
        <body>
          <div class="container">
          <div class="file">
          <div class="data highlight blob-wrapper">
            <table class="diff-table file-diff-split">
            <tbody>""" % INLINE_CSS))

        yield

        self._spit(textwrap.dedent("""\
            </tbody>
            </table>
          </div>
          </div>
          </div>
        </body>"""))

    def _spit_side_from_context(self, context):
        self._spit('      <td class="blob-num blob-num-%(mode)s base js-linkable-line-number" '
                   'data-line-number="%(lineno)d"></td>' % context)
        self._spit('      <td class="blob-code blob-code-%(mode)s base">%(code)s</td>' % context)

    def _spit_empty_side(self):
        self._spit('      <td class="blob-num blob-num-empty head empty-cell"></td>')
        self._spit('      <td class="blob-code blob-code-empty head empty-cell"></td>')

    def _spit_changed_side(self, holder, lineno, mode):
        if not holder:
            self._spit_empty_side()
            return

        bits = []
        for elem in holder.elements:
            piece = html_escape(str(elem))
            if elem.is_changed:
                bits.append('<span class="x x-first x-last">%s</span>' % piece)
            else:
                bits.append(piece)
        code = ''.join(bits)
        context = {
            'mode': mode,
            'lineno': lineno,
            'code': code,
        }
        self._spit_side_from_context(context)

    def _spit_unchanged_side(self, holder, lineno):
        context = {
            'mode': 'context',
            'lineno': lineno,
            'code': html_escape(holder),
        }
        self._spit_side_from_context(context)
