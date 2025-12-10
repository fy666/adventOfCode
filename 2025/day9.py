import numpy as np
import argparse
import re
from collections import defaultdict


def is_included(a, b, x_vals, y_vals):
    if a[0] < b[0]:
        x1, y1 = a
        x2, y2 = b
    else:
        x1, y1 = b
        x2, y2 = a

    # case 1
    if y2 > y1:
        if not (np.any(np.array(y_vals[y1]) >= x2)):
            return False
        if not (np.any(np.array(y_vals[y2]) <= x1)):
            return False
        if not (np.any(np.array(x_vals[x1]) >= y2)):
            return False
        if not (np.any(np.array(x_vals[x2]) <= y1)):
            return False
        return True
    else:
        if not (np.any(np.array(y_vals[y1]) >= x2)):
            return False
        if not (np.any(np.array(y_vals[y2]) <= x1)):
            return False
        if not (np.any(np.array(x_vals[x1]) <= y2)):
            return False
        if not (np.any(np.array(x_vals[x2]) >= y1)):
            return False
        return True


def get_area(a, b):
    dx = abs(a[0] - b[0] + 1)
    dy = abs(a[1] - b[1] + 1)
    return dx * dy


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
        d = [list(map(int, x.split(","))) for x in f.readlines()]
    print(d)

    x_vals = defaultdict(list)
    y_vals = defaultdict(list)
    for dx, dy in d:
        x_vals[dx].append(dy)
        y_vals[dy].append(dx)

    areas = []
    continuous_areas = []
    for ix in range(len(d)):
        for iy in range(ix + 1, len(d)):
            area = get_area(d[ix], d[iy])
            areas.append(area)
            if is_included(d[ix], d[iy], x_vals, y_vals):
                continuous_areas.append(area)

    print(f"Part 1 max area is {max(areas)}")
    print(f"Part 2 max area is {max(continuous_areas)}")
