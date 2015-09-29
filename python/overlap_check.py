# -*- coding: utf-8 -*-


def overlap_check(ls):
    base = ls.copy()
    base.sort()
    fst = base[:-1]
    snd = base[1:]

    for i, j in zip(fst, snd):
        if i == j:
            return True
    return False

if __name__ == '__main__':
    print(overlap_check([1, 2, 4, 3, 5, 6]))
    print(overlap_check([1, 2, 4, 3, 5, 6, 3]))
