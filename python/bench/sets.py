# -*- coding: utf-8 -*-

from benchmarker import Benchmarker

loop = 1000 * 100

with Benchmarker(loop, width=20, cycle=10, extra=3) as bench:
    s1, s2, s3, s4, s5 = "Haruhi", "Mikuru", "Yuki", "Itsuki", "Kyon"

    @bench("join")
    def _join(bm):
        for i in bm:
            sos = ''.join((s1, s2, s3, s4, s5))

    @bench("concat")
    def _concat(bm):
        for _ in bm:
            sos = s1 + s2 + s3 + s4 + s5

    @bench("format")
    def _format(bm):
        for _ in bm:
            sos = '%s%s%s%s%s' % (s1, s2, s3, s4, s5)
