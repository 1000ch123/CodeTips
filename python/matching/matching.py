# -*- coding: utf-8 -*-
import random
from itertools import combinations


def gen_scores(num_campany=4, num_students=10):
    """
    企業ごとの学生に対するscoreマップを生成
    TODO:外部ファイル読み込みにしたほうがよさ気
    """
    scores = []
    for i in range(num_campany):
        score = list(range(num_students))
        random.shuffle(score)
        scores.append(score)
    return scores


def gen_candidates(num_campany=4, num_students=10, students_per_campany=2):
    """
    1term分の組み合わせを返すgenerator
    """
    def step(people, depth):
        if depth == 0:
            yield []

        for sel, rest in canididates(people, students_per_campany):
            yield from (n + [sel] for n in step(rest, depth-1))

    yield from step(set(range(num_students)), num_campany)


def canididates(people, sel):
    """
    people(iterable)を sel人とn-sel人に分割して返すgenerator
    """
    all = set(people)
    selected = combinations(all, sel)

    for i in selected:
        sel = set(i)
        yield sel, all.difference(sel)


if __name__ == '__main__':
    for i in gen_candidates(3, 7, 1):
        print(i)
