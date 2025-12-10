import numpy as np
import argparse
import re


def get_joltage_p1(data):
    c1 = max(data[:-1])
    N = data.index(c1)
    c2 = max(data[N + 1 :])
    return c1 * 10 + c2


def get_joltage_N(data, N):
    size = len(data)
    istart = 0
    n_to_find = N
    iend = size - n_to_find + 1
    num = 0
    for ix in range(N):
        c = max(data[istart:iend])
        n_to_find -= 1
        istart += data[istart:iend].index(c) + 1
        # iend = size - N + ix + 2
        iend = size - n_to_find + 1
        num += c * 10 ** (N - ix - 1)
    return num


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
        d = [list(map(int, x.strip())) for x in f.readlines()]
    sum_p1 = 0
    sum_p2 = 0
    for item in d:
        # sum_p1 += get_joltage_p1(item)
        sum_p1 += get_joltage_N(item, 2)
        ans = get_joltage_N(item, 12)
        sum_p2 += ans
    print(f"Part 1 joltage = {sum_p1}")
    print(f"Part 2 joltage = {sum_p2}")
