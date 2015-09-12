# -*- coding: utf-8 -*-

import json
import csv


def write_as_csv(data):
    with open('data.csv', 'w') as f:
        csv_writer = csv.writer(f)
        for d in data:
            csv_writer.writerow(d)


def write_as_json(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, sort_keys=True, indent=4)


if __name__ == '__main__':
    data = [
        [1, 2, 3],
        [4, 2, 3],
        [4, 7, 8],
        [9, 23, 13]
        ]
    s = set()
    s.add((1, 2))
    s.add((3, 5))
    s.add((6, 7))
    write_as_csv(s)

    dic = {"Hello": "World", "No": "Thank you", "Perfect": "Python"}
    write_as_json(dic)
