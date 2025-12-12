import numpy as np
import argparse
import re
from collections import defaultdict
import time
import cvxpy as cp
from numpy.linalg import svd, lstsq


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

# Too slow


def push_buttons_p2(buttons, state):
    new_state = list(state)
    for b in buttons:
        new_state[b] += 1
    return new_state


def get_min_pushes_p2(buttons, wanted_state):
    original_state = [0 for _ in range(len(wanted_state))]
    queue = [([0 for _ in range(len(buttons))], original_state)]
    history = defaultdict(int)
    while queue:
        pushes, state = queue.pop(0)
        # print(f"Current state {(pushes, state)}: wanted state: {wanted_state}")
        if np.all(np.array(state) == np.array(wanted_state)):
            return pushes, np.sum(pushes)
        else:
            for ib, b in enumerate(buttons):
                new_state = push_buttons_p2(b, state)
                new_pushes = list(pushes)
                new_pushes[ib] += 1
                # No need to continue if overflow
                if np.any(np.array(new_state) > np.array(wanted_state)):
                    continue
                if (
                    tuple(new_state) in history
                    and np.sum(history[tuple(new_state)]) <= np.sum(new_pushes)
                ):
                    continue
                # print(f"Adding {(pushes + 1, new_state)}")
                history[tuple(new_state)] = new_pushes
                queue.append((new_pushes, new_state))


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

        # too slow
        # p, p2 = get_min_pushes_p2(buttons, seq)

        a = np.zeros((len(seq), len(buttons)))
        for ix, button in enumerate(buttons):
            for b in button:
                a[b][ix] = 1
        b = np.array(seq).T

        # PFFF
        x = cp.Variable(len(buttons), integer=True,  nonneg=True)  # 2 variables: x and y

        # Define the objective to minimize the L2 norm (sum of squares)
        # Note: for L1 norm, you would use cp.norm1(x)
        objective = cp.Minimize(cp.norm1(x))

        # Define the constraints
        constraints = [a @ x == b]

        # Form and solve the problem
        problem = cp.Problem(objective, constraints)
        # ECOS_BB is an appropriate solver for mixed-integer problems
        problem.solve(solver=cp.ECOS_BB)
        int_sol = np.array([int(round(xx)) for xx in x.value])
        if np.all(np.dot(a, int_sol) != b):
            print(np.dot(a, int_sol), " = ? ", b)

            print(np.all(np.dot(a, int_sol) == b))
            print("Solution (integers):", x.value)
            print("Minimum L2 Norm value:", problem.value,
                  f" adding {int(round(problem.value))}, sum = {np.sum([round(xx) for xx in x.value])}")
        sum_p2 += int(round(problem.value))

    print(f"Part 1 = {sum_p1}")
    print(f"Part 2 = {sum_p2}")
