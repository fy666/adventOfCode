import numpy as np
import argparse
import re
from collections import defaultdict


def push_buttons(buttons, state):
    new_state = list(state)
    for b in buttons:
        new_state[b] = not new_state[b]
    return new_state


def get_min_pushes(buttons, wanted_state):
    original_state = [False for _ in range(len(wanted_state))]
    queue = [(0, original_state)]
    history = defaultdict(int)
    while queue:
        pushes, state = queue.pop(0)
        # print(
        #     f"Current state {(pushes, state)}: {np.all(np.array(state) == np.array(wanted_state))}"
        # )
        if np.all(np.array(state) == np.array(wanted_state)):
            return pushes
        else:
            for b in buttons:
                new_state = push_buttons(b, state)
                new_pushes = pushes + 1
                if (
                    tuple(new_state) in history
                    and history[tuple(new_state)] <= new_pushes
                ):
                    continue
                # print(f"Adding {(pushes + 1, new_state)}")
                history[tuple(new_state)] = new_pushes
                queue.append((pushes + 1, new_state))


def push_buttons_p2(buttons, state):
    new_state = list(state)
    for b in buttons:
        new_state[b] += 1
    return new_state


def get_min_pushes_p2(buttons, wanted_state):
    original_state = [0 for _ in range(len(wanted_state))]
    queue = [(0, original_state)]
    history = defaultdict(int)
    print("--------------------------------")
    while queue:
        pushes, state = queue.pop(0)
        # print(f"Current state {(pushes, state)}: wanted state: {wanted_state}")
        if np.all(np.array(state) == np.array(wanted_state)):
            return pushes
        else:
            for b in buttons:
                new_state = push_buttons_p2(b, state)
                # No need to continue if overflow
                if np.any(np.array(new_state) > np.array(wanted_state)):
                    continue
                new_pushes = pushes + 1
                if (
                    tuple(new_state) in history
                    and history[tuple(new_state)] <= new_pushes
                ):
                    continue
                # print(f"Adding {(pushes + 1, new_state)}")
                history[tuple(new_state)] = new_pushes
                queue.append((pushes + 1, new_state))


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

    # # means on, . mean off
    # all lights starts off
    sum_p1 = 0
    sum_p2 = 0
    for x in d:
        match = re.search(r"\[(.*)\] (.*) {(.*)}", x.strip())
        code = [m == "#" for m in match.group(1)]
        buttons = [
            list(eval(m)) if isinstance(eval(m), tuple) else [eval(m)]
            for m in match.group(2).split(" ")
        ]
        seq = [int(m) for m in match.group(3).split(",")]
        sum_p1 += get_min_pushes(buttons, code)
        # sum_p2 += get_min_pushes_p2(buttons, seq)
        if len(buttons) == len(seq):
            # Solve using linalg ?
            pass
            # print(x.strip())
        else:
            sum_p2 += get_min_pushes_p2(buttons, seq)

    print(f"Part 1 = {sum_p1}")
    print(f"Part 2 = {sum_p2}")
