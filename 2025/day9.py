import numpy as np
import argparse
import re
from collections import defaultdict
import shapely.plotting
from shapely.geometry import Polygon
import matplotlib.pyplot as plt


def get_area(a, b):
    dx = abs(a[0] - b[0]) + 1
    dy = abs(a[1] - b[1]) + 1
    return dx * dy


def get_poly(a, b):
    return Polygon.from_bounds(min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1]))


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
        d = [tuple(map(int, x.split(","))) for x in f.readlines()]

    polygon1 = Polygon(d)

    # shapely.plotting.plot_polygon(polygon1)
    # plt.draw()
    # plt.show()

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
            if area == 0:
                continue
            areas.append(area)
            p = get_poly(d[ix], d[iy])
            if polygon1.contains(p):
                continuous_areas.append(area)

    print(f"Part 1 max area is {max(areas)}")
    print(f"Part 2 max area is {max(continuous_areas)}")
