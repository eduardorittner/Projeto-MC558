from pulp import *
from reduce import read_input, reduce
import sys


def solve_binpack(items, num_bins, cap) -> None | Dict[int, int]:
    num_items = len(items)

    # Create the model
    model = LpProblem("Bin-packing", LpMinimize)

    # Create decision variables
    x = LpVariable.dicts(
        "x", [(i, j) for i in range(num_items) for j in range(num_bins)], cat="Binary"
    )

    # Objective function (dummy, as we're checking feasibility)
    model += 0

    # Constraints
    # Each item must be assigned to exactly one bin
    for i in range(num_items):
        model += lpSum([x[i, j] for j in range(num_bins)]) == 1

    # Total weight of items in each bin must equal its capacity
    for j in range(num_bins):
        model += lpSum([items[i] * x[i, j] for i in range(num_items)]) == cap

    # Solve the model (without logging)
    model.solve(PULP_CBC_CMD(msg=False))

    if LpStatus[model.status] == "Optimal":
        # Extract the solution
        solution = {}
        for i in range(num_items):
            for j in range(num_bins):
                if x[i, j].varValue == 1:
                    solution[i] = j
        return solution
    else:
        return None


def pretty(items: list[int], bins: int, solution: Dict[int, int]) -> str:
    string = ""

    bin_items = [[] for _ in range(bins)]

    for item, bin in solution.items():
        bin_items[bin].append(item)

    for bin in bin_items:
        string += "["
        for item in bin:
            string += f" {items[item]} "
        string += "]\n"

    return string


if __name__ == "__main__":
    save = True if len(sys.argv) > 1 and sys.argv[1] == "--save" else False
    show = True if len(sys.argv) > 1 and sys.argv[1] == "--show" else False

    items, bins, cap = read_input()
    solution = solve_binpack(items, bins, cap)

    if solution:
        print("Solution:")
        print(pretty(items, bins, solution))
        if save:
            reduce(items, bins, cap).solve(solution).save()
        elif show:
            reduce(items, bins, cap).solve(solution).show()
    else:
        print("No feasible solution exists.")
