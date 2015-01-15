# -*- coding: utf-8 -*-
import contextlib


class BaseGenerator(object):
    def run(self, sxs_result):
        with self.wrap_result(sxs_result):
            left_no = 1
            right_no = 1
            for changed, left, right in sxs_result:
                with self.wrap_row(changed, left, left_no, right, right_no):
                    self.visit_row(changed, left, left_no, right, right_no)
                if left:
                    left_no += 1
                if right:
                    right_no += 1

    @contextlib.contextmanager
    def wrap_result(self, sxs_result):
        yield

    @contextlib.contextmanager
    def wrap_row(self, changed, left, left_no, right, right_no):
        yield

    def visit_row(self, changed, left, left_no, right, right_no):
        pass
