import numpy as np
import argparse
import re


def test_ingr():
    assert (intersect((1, 10), (2, 5)) == True)
    assert (merge((1, 10), (2, 5)) == (1, 10))

    assert (intersect((1, 10), (1, 10)) == True)
    assert (merge((1, 10), (1, 10)) == (1, 10))

    assert (intersect((1, 10), (9, 15)) == True)
    assert (merge((1, 10), (9, 15)) == (1, 15))

    assert (intersect((1, 10), (10, 15)) == True)
    assert (merge((1, 10), (10, 15)) == (1, 15))

    assert (intersect((8, 12), (10, 15)) == True)
    assert (merge((8, 12), (10, 15)) == (8, 15))


def is_valid(ingre, rules):
    for s1, s2 in rules:
        if s1 <= ingre and s2 >= ingre:
            return True
    return False


def merge(a, b):
    return (min(a[0], b[0]), max(a[1], b[1]))


def intersect(a, b):
    if b[1] < a[0] or b[0] > a[1]:
        return False
    return True

    # if a[0] <= b[1] and a[0] >= b[0]:
    #     return True
    # if b[0] >= a[0] and b[0] <= a[1]:
    #     return True
    # if b[1] >= a[0] and b[1] <= a[1]:
    #     return True
    # if a[1] <= b[1] and a[1] >= b[0]:
    #     return True
    # return False


def count_valid(rules):
    merged_intervals = []
    rules = set(rules)
    while (rules):
        # print(f"Starting loop with rules {rules}")
        b = rules.pop()
        to_delete = []
        things_to_merge = True
        while things_to_merge:
            things_to_merge = False
            for r in rules:
                if intersect(b, r):
                    things_to_merge = True
                    b = merge(b, r)
                    rules.remove(r)
                    break
        merged_intervals.append(b)

    # Now count
    valid = 0
    for s1, s2 in merged_intervals:
        valid += s2-s1+1
    return valid


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--test", action="store_true")  # on/off flag
    args = parser.parse_args()

    filename = __file__.split("/")[-1]
    day = int(re.findall(r"\d+", filename)[0])

    if args.test:
        filename = f"./data/test{day}.txt"
    else:
        filename = f"./data/input{day}.txt"

    with open(filename, "r") as f:
        d = f.read().split('\n\n')
        validities = [tuple(map(int, x.split('-'))) for x in d[0].split('\n')]
        ingredients = list(map(int, d[1].split('\n')))

    sum_p1 = 0
    for ingr in ingredients:
        if is_valid(ingr, validities):
            sum_p1 += 1

    print(f"Part 1: {sum_p1} ingredients ID are fresh")

    valid = count_valid(validities)
    print(f"Part 2: {valid} fresh ingredients")
