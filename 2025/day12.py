import numpy as np
import argparse
import re
from collections import defaultdict
import time


def rotateTile(tile, count):
    rotTile = np.rot90(np.array(tile))
    if count == 4:
        rotTile = np.flip(np.array(rotTile), axis=0)
    return rotTile


tiles = []


def get_all_rotations(tile):
    variations = [np.copy(tile)]
    for i in range(8):
        tile = rotateTile(tile, i)
        if np.all([np.any(x != tile) for x in variations]):
            variations.append(np.copy(tile))
    return variations


def get_tiles(data):
    tile = (np.array([list(x.strip()) for x in data]) == '#').astype(int)  # .astype(char)
    return tile


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
        d = f.readlines()

    tiles = [get_tiles(d[i*5+1:i*5+4]) for i in range(6)]
    print(f"Parsed {len(tiles)} tiles")
    tiles_size = [int(np.sum(np.sum(t))) for t in tiles]

    for t in tiles:
        _ = get_all_rotations(t)

    d.reverse()
    mat = d[:d.index('\n')]

    sum_p1 = 0
    for x in mat:
        grid = list(map(int, x.strip().split(":")[0].split("x")))
        nums = list(map(int, x.strip().split(":")[1].split()))
        print(grid, f"({grid[0]*grid[1]})", nums, tiles_size)
        occupancy = np.dot(np.array(nums), np.array(tiles_size))
        print(f"Occupancy = {occupancy}")
        if grid[0]*grid[1] >= occupancy:
            sum_p1 += 1
    print(f"Part 1 = {sum_p1}")
