# -*- coding: utf-8 -*-

from benchmarker import Benchmarker

loop = 1000 * 100
large_int = 2 ** 48
large_long = 2 ** 70

with Benchmarker(loop, width=20, cycle=10, extra=3) as bench:

    @bench("int eq")
    def _int(bm):
        for i in bm:
            1 == 1

    @bench("int is")
    def _is(bm):
        for i in bm:
            1 is 1

    @bench("long eq")
    def _long_eq(bm):
        for _ in bm:
            1L == 1L

    @bench("large int eq")
    def _large_int(bm):
        for _ in bm:
            large_int == large_int

    @bench("large long eq")
    def _large_long(bm):
        for _ in bm:
            large_long == large_long
