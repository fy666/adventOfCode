import numpy as np
import argparse
import re
from collections import defaultdict
import time
from functools import lru_cache


@lru_cache
def rec_way(pos, stop, network):
    n = 0
    if pos == stop:
        return 1
    for b in network.dict[pos]:
        n += rec_way(b, stop, network)
    return n


class HashableDict:
    def __init__(self, dict_obj):
        self.dict = dict_obj

    def __hash__(self):
        return hash(tuple(sorted(self.dict.items())))


def get_network(filename):
    network = {}
    with open(filename, "r") as f:
        for x in f.readlines():
            key = x.split(":")[0]
            cons = x.split(":")[1].split()
            network[key] = tuple(cons)
    network["out"] = tuple()
    return HashableDict(network)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--test", action="store_true")  # on/off flag
    args = parser.parse_args()

    filename = __file__.split("/")[-1]
    day = int(re.findall(r"\d+", filename)[0])

    if args.test:
        filename_p1 = f"./data/test{day}.txt"
        filename = f"./data/test{day}_p2.txt"
    else:
        filename = f"./data/input{day}.txt"

    if args.test:
        network = get_network(filename_p1)
    else:
        network = get_network(filename)

    # Part 1
    n = rec_way("you", "out", network)
    print(f"Part 1 = {n}")

    if args.test:
        network = get_network(filename)

    p2 = 0

    n1 = rec_way("svr", "fft", network)
    print(f"\tFrom svr to fft: {n1}")

    n2 = rec_way("fft", "dac", network)
    print(f"\tFrom fft to dac: {n2}")

    n3 = rec_way("dac", "out", network)
    print(f"\tFrom dac to out: {n3}")

    p2 += n1*n2*n3

    print(f"Part 2 = {p2}")
