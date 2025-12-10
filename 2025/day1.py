import numpy as np
import argparse
import re


def numpy_count(start, stop, max_val=99):
    step = 1 if start < stop else -1
    b = np.arange(start, stop+step, step) % (max_val+1)
    try:
        b[0] = 10  # dont cont first zero
    except Exception as e:
        print(f"{start} to {stop} (step {step})")
        raise (e)
    return int(np.sum(b == 0))


def test_count_zero():

    args = [(0, 50, 99), (93, 0, 100), (1, 50, 99), (1, 100, 99), (0, 100, 99), (0, 200, 99),
            (10, -10, 99), (0, -10, 99), (50, 1050), (1, -100), (1, -1000)]

    for arg in args:
        assert (count_zero_passages(*arg) == numpy_count(*arg))
        print("-----------------")


def count_zero_passages(start, stop, max_val=99):
    rounded_stop = stop % (max_val+1)
    pass_by_0 = 0
    # print(f"{start} to {stop} ({rounded_stop})")

    if stop < 0 or stop > max_val:
        if start < stop:
            pass_by_0 = abs(stop//(max_val+1))
        else:
            pass_by_0 = abs(stop//(max_val+1))
            if start == 0:
                pass_by_0 -= 1

    if start > stop and rounded_stop == 0:
        pass_by_0 += 1
    return pass_by_0


def run(data, start=50, debug_np=False):
    count = start
    before_count = 0
    part1_res = 0
    part2_count = 0
    for move, tics in data:
        pass_by_0 = 0
        before_count = count
        # Turn
        if move == 'R':
            count += tics
        elif move == 'L':
            count -= tics
        p2, p1 = divmod(count, 100)
        pass_by_0 = count_zero_passages(before_count, count, 99)
        if debug_np:
            pass_by_0_np = numpy_count(before_count, count, 99)
            if pass_by_0_np != pass_by_0:
                print(f"DIFF {before_count} to {count}: {pass_by_0_np} (np) != {pass_by_0} (computed)")

        count = p1

        part2_count += pass_by_0

        if p1 == 0:
            part1_res += 1

    print(f"Part 1 password is {part1_res}")
    print(f"Part 2 password is {part2_count}")
    print("------------------")


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
        d = [(x[0], int(x[1:])) for x in f.readlines()]

    if args.test:
        run([("L", 50), ("R", 200)])
    run(d)
