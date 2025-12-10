import numpy as np
import argparse
import re
from collections import defaultdict

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

    start_node = (0, d[0].index('S'))
    laser_pos = [[start_node]]
    visited_nodes = defaultdict(int)
    visited_splits = set()
    while (laser_pos):
        pos_list = laser_pos.pop()
        pos = pos_list[-1]
        pos_l, pos_c = pos
        pos_l += 1

        if pos_l >= len(d):
            for p in pos_list:
                visited_nodes[p] += 1
            continue

        nodes_to_add = []
        if d[pos_l][pos_c] == '^':
            visited_splits.add(pos)
            nodes_to_add.append((pos_l, pos_c+1))
            nodes_to_add.append((pos_l, pos_c-1))
        else:
            nodes_to_add.append((pos_l, pos_c))

        for n in nodes_to_add:
            if n in visited_nodes:
                for p in pos_list:
                    visited_nodes[p] += visited_nodes[n]
            else:
                new_pos_list = list(pos_list)
                new_pos_list.append(n)
                laser_pos.append(new_pos_list)

    print(f"Part 1: {len(visited_splits)} number of splits")
    print(f"Part 2: {visited_nodes[start_node]} number of timelines")
