import numpy as np
import argparse
import re


def is_invalid_p2(tmp):
    for N in range(2, len(tmp) + 1):
        if len(tmp) % N == 0:
            a = np.split(np.array(tmp), N)
            if np.all([x == a[0] for x in a]):
                return True
    return False


def is_invalid_p1(tmp):
    if len(tmp) % 2 == 0:
        N = int(len(tmp) / 2)
        return tmp[:N] == tmp[N:]
    return False


def get_invalid_ids_sum(input, part1=True):
    [start, stop] = input
    sum = 0
    for d in np.arange(int(start), int(stop) + 1):
        tmp = list(str(d))
        if part1 and is_invalid_p1(tmp):
            sum += d
        if not part1 and is_invalid_p2(tmp):
            sum += d
    return sum


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
        d = [x.split("-") for x in f.readlines()[0].strip().split(",")]
    sum_p1 = 0
    sum_p2 = 0
    for dd in d:
        sum_p1 += get_invalid_ids_sum(dd, part1=True)
        sum_p2 += get_invalid_ids_sum(dd, part1=False)
    print(f"Part 1 sum = {sum_p1}")
    print(f"Part 2 sum = {sum_p2}")
    if args.test:
        gt_p2 = 4174379265
        print(f"sum_p2 == gt_p2 ? {sum_p2 == gt_p2}")
