# -*- coding: utf-8 -*-
import random
from itertools import combinations, chain
from collections import Counter


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


def score(score_map, pattern):
    result = 0
    for ix, students in enumerate(pattern):
        for student in students:
            result += score_map[ix][student]
    return result


def is_vaild_patterns(num_students, min_count, max_count, patterns):
    """
    与えられたpatternsが実用に耐えうるか
    patternsをflattenしてcounterにぶち込む
    各countがmin~maxの間にあればok
    """
    def valid(count):
        return min_count <= count and count <= max_count

    counter = Counter()
    for i in range(num_students):
        counter[i] = 0

    print(patterns)
    flatten = chain.from_iterable
    for i in flatten(flatten(patterns)):
        counter[i] += 1

    print(counter)
    return all(valid(x) for x in counter.values())

if __name__ == '__main__':
    campanies = 3
    students = 8
    students_per_campany = 2
    score_map = gen_scores()
    candidates = gen_candidates(campanies, students, students_per_campany)

    calc = lambda x: score(score_map, x)
    result = [(i, calc(i)) for i in candidates]

    sorted_result = sorted(result, key=lambda x: x[1], reverse=True)

    result = is_vaild_patterns(students, 1, campanies,
                               [x[0] for x in sorted_result[:3]])
    print(result)
