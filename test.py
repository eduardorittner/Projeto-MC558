from linear import solve_binpack, pretty
from typing import List


def test(items: List[int], bins: int, cap: int):
    print("-------------------------")
    print(f"Items: {items}, Bins: {bins}, Capacity: {cap}")
    solution = solve_binpack(items, bins, cap)
    if solution:
        print("Solution:")
        print(pretty(items, bins, solution))
    else:
        print("No solution\n")


if __name__ == "__main__":
    test([3], 1, 3)
    test([3], 1, 2)
    test([3, 3, 3, 3, 3], 5, 3)
    test([5, 5, 3, 7], 2, 10)
    test([10, 11, 1, 20, 21], 3, 21)
