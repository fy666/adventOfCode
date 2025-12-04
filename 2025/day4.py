import numpy as np
import argparse
import re


DIRS = [(-1, 0), (-1, 1), (-1, -1), (1, 0), (1, 1), (1, -1), (0, 1), (0, -1)]


def get_accessible_rolls(pos):
    res = 0
    remaining = []
    for px, py in pos:
        forklift_access = 0
        for nx, ny in DIRS:
            c = (px+nx, py+ny)
            if c in pos:
                forklift_access += 1
        if forklift_access < 4:
            res += 1
        else:
            remaining.append((px, py))
    return res, set(remaining)


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
        d = np.array([np.array([y for y in x.strip()]) for x in f.readlines()])

    pos = set([(x, y) for (x, y) in zip(*np.where(d == '@'))])
    print(f"Found {len(pos)} rolls")

    res, remaining = get_accessible_rolls(pos)
    print(f"Part 1 accessible rolls = {res}")

    prev_len = len(pos)
    while len(remaining) != prev_len:
        prev_len = len(remaining)
        _, remaining = get_accessible_rolls(remaining)
        # print(f"Removing {n} rolls")
    print(f"Part 2 removed rolls = {len(pos)-len(remaining)}")
