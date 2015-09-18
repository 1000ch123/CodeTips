# -*- coding: utf-8 -*-

from benchmarker import Benchmarker

loop = 1000 * 100

with Benchmarker(loop, width=20, cycle=10, extra=3) as bench:
    ls = "Haruhi", "Mikuru", "Yuki", "Itsuki", "Kyon"

    @bench("set comprehension")
    def _set(bm):
        for i in bm:
            s = {n for n in ls}

    @bench("list comprehenion")
    def _ls(bm):
        for _ in bm:
            s = [n for n in ls]

    @bench("list for")
    def _ls_for(bm):
        for _ in bm:
            s = []
            for i in ls:
                s.append(i)

    @bench("ls -> set")
    def _ls_set(bm):
        for _ in bm:
            s = set([n for n in ls])

    @bench("dict comprehenion")
    def _dict(bm):
        for _ in bm:
            s = {n: n for n in ls}

# 圧倒的にset complehentionが早い
