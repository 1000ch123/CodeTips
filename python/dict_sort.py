# -*- coding: utf-8 -*-
from operator import attrgetter
from benchmarker import Benchmarker

loop = 1000 * 100


class Bid:
    def __init__(self, price, id):
        self._id = id
        self._price = price


with Benchmarker(loop, width=20, cycle=10, extra=3) as bench:
    b1 = Bid(200, 1)
    b2 = Bid(300, 2)
    b3 = Bid(150, 3)
    b4 = Bid(200, 1)
    b5 = Bid(200, 2)

    @bench("sorted")
    def _sorted(bm):
        for i in bm:
            bs = [b1, b3, b4, b5]
            bs = sorted(bs, key=attrgetter('_id'), reverse=True)
            bs = sorted(bs, key=attrgetter('_price'), reverse=True)

    @bench("sort")
    def _sort(bm):
        for i in bm:
            bs = [b1, b3, b4, b5]
            bs.sort(key=attrgetter('_id'), reverse=True)
            bs.sort(key=attrgetter('_price'), reverse=True)
