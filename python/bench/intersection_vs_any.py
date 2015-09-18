# -*- coding: utf-8 -*-

from benchmarker import Benchmarker

loop = 1000 * 100

with Benchmarker(loop, width=20, cycle=10, extra=3) as bench:
    a = [1, 2, 3, 4, 5, 6]
    b = [1, 2, 3, 6, 7, 8, 9, 10]

    @bench("any")
    def _join(bm):
        for i in bm:
            any([category in b for category in a])

    @bench("any_gen")
    def _join(bm):
        for i in bm:
            any(category in b for category in a)

    @bench("set")
    def _concat(bm):
        for _ in bm:
            set(a).intersection(b)
