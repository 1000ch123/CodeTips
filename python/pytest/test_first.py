# -*- coding: utf-8 -*-
# how to test
#
# py.test
# py.test test_first.py
# py.test -k <exp> [filename]  ignorecaseできないかなー


def func(x):
    return x + 1


def test_answer():
    assert func(3) == 5


def test_fail():
    assert False


class TestClass:
    def test_one(self):
        assert 1 == 1

    def test_two(self):
        assert 1 == 2
