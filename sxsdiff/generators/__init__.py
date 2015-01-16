# -*- coding: utf-8 -*-
import contextlib


class BaseGenerator(object):
    def run(self, diff_result):
        with self.wrap_result(diff_result):
            for line_change in diff_result:
                with self.wrap_row(line_change):
                    self.visit_row(line_change)

    @contextlib.contextmanager
    def wrap_result(self, sxs_result):
        yield

    @contextlib.contextmanager
    def wrap_row(self, line_change):
        yield

    def visit_row(self, line_change):
        pass
