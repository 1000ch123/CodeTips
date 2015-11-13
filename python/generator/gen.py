# -*- coding: utf-8 -*-


def g1():
    yield 1
    yield 2
    yield 3


def g2():
    yield 4
    yield 5
    yield 6


def g3():
    yield 7
    yield 8
    yield 9


if __name__ == '__main__':
    generator = g1
    for i in generator():
        print(i)
