import numpy as np
import argparse
import re
import itertools


def apply_op(operand, data):
    # print(f"Applying operation {operand} on {data}")
    if operand == '+':
        return (np.sum(data))
    elif operand == '*':
        return (np.prod(data))
    else:
        raise Exception


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
    numbers = np.array([np.array(list(map(int, x.strip().split()))) for x in d[:-1]])
    operands = d[-1].strip().split()

    sum_p1 = 0
    for op, data in zip(operands, numbers.T):
        sum_p1 += apply_op(op, data)
    print(f"Part 1 cephalopod math = {sum_p1}")

    numbers = np.array([list(x) for x in d[:-1]]).T

    wip_num = []
    sum_p2 = 0
    it = itertools.count(0)
    for line in numbers:
        txt = "".join(line)
        if not txt.strip():
            sum_p2 += apply_op(operands[next(it)], np.array(wip_num))
            wip_num = []
        else:
            wip_num.append(int(txt))

    print(f"Part 2 cephalopod math = {sum_p2}")
