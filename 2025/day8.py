import numpy as np
import argparse
import re
import itertools
from scipy.spatial.distance import pdist, squareform
from matplotlib import pyplot as plt


def merge(clusters):
    something_to_merge = True
    while something_to_merge:
        something_to_merge = False
        for ic, c1 in enumerate(clusters):
            if something_to_merge:
                break
            for c2 in clusters[ic+1:]:
                if c1.intersection(c2):
                    something_to_merge = True
                    clusters[ic] = c1.union(c2)
                    clusters.remove(c2)
    return clusters


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--test", action="store_true")  # on/off flag
    args = parser.parse_args()

    filename = __file__.split("/")[-1]
    day = int(re.findall(r"\d+", filename)[0])

    if args.test:
        filename = f"./data/test{day}.txt"
        N = 10
    else:
        filename = f"./data/input{day}.txt"
        N = 1000

    with open(filename, "r") as f:
        data = [tuple(map(int, x.split(","))) for x in f.readlines()]

    print(f"{len(data)} pairs")

    distance_matrix = squareform(pdist(data))  # could have directly used pdist...

    np.fill_diagonal(distance_matrix, np.nan)
    closest_nodes = []

    for ix, l in enumerate(distance_matrix):
        for iy, dist in enumerate(l[ix+1:]):
            closest_nodes.append([float(dist), ix, ix+1+iy])

    closest_nodes.sort(key=lambda x: x[0])
    clusters = []

    for ix, node in enumerate([set([a, b]) for _, a, b in closest_nodes]):
        clusters.append(set(node))
        clusters = merge(clusters)
        if ix == N-1:
            lengths = list(set([len(x) for x in clusters]))
            lengths.sort(reverse=True)
            print(f"Part 1 = {np.prod(list(lengths[:3]))}")
        if len(clusters[0]) == len(data):
            coords = list(node)
            p2 = data[coords[0]][0] * data[coords[1]][0]
            print(f"Part 2 = {p2}")
            break
