from pulp import *
import sys
from enum import Enum
from PIL import Image, ImageDraw
import copy
from typing import Dict, Self


class Tile(Enum):
    UNKNOWN = 0
    WATER = 1
    SHIP = 2


class Battleship:
    def __init__(
        self,
        nrows: int,
        ncols: int,
        initial: list[list[Tile]],
        row_tallies: list[int],
        col_tallies: list[int],
        fleet: list[int],
    ):
        if nrows != len(row_tallies):
            raise Exception(
                f"Expected rows to have length {nrows}, has {len(row_tallies)}"
            )
        if ncols != len(col_tallies):
            raise Exception(
                f"Expected cols to have length {ncols}, has {len(col_tallies)}"
            )
        if nrows != len(initial):
            raise Exception(
                f"Expected initial to have {nrows} rows, has {len(initial)}"
            )
        if ncols != len(initial[0]):
            raise Exception(
                f"Expected initial to have {ncols} cols, has {len(initial[0])}"
            )

        self.nrows = nrows
        self.ncols = ncols
        self.initial = initial
        self.row_tallies = row_tallies
        self.col_tallies = col_tallies
        self.fleet = fleet
        self.grid = copy.deepcopy(self.initial)

    def generate_img(self, tile_size=20):
        # Calculate image height and width. 1 extra tile for text
        width = (self.ncols + 1) * tile_size
        height = (self.nrows + 1) * tile_size

        # Create image
        img = Image.new("RGB", (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        # Define colors
        water_color = (0, 0, 255)
        ship_color = (0, 0, 0)
        unknown_color = (155, 155, 155)

        # Choose color based on enum and fill it
        for row in range(self.nrows):
            for col in range(self.ncols):
                if self.grid[row][col] == Tile.UNKNOWN:
                    color = unknown_color
                elif self.grid[row][col] == Tile.WATER:
                    color = water_color
                elif self.grid[row][col] == Tile.SHIP:
                    color = ship_color
                else:
                    raise Exception("Invalid Tile enum value")
                draw.rectangle(
                    [
                        (col * tile_size + 1, row * tile_size + 1),
                        (col * tile_size + 19, row * tile_size + 19),
                    ],
                    fill=color,
                )

        # Write row tally numbers
        for i in range(self.nrows):
            draw.text(
                (width - 3 * tile_size / 4, i * 20 + 5),
                str(self.row_tallies[i]),
                fill=(0, 0, 0),
            )

        # Write col tally numbers
        for i in range(self.ncols):
            draw.text(
                (i * 20 + 5, height - 3 * tile_size / 4),
                str(self.col_tallies[i]),
                fill=(0, 0, 0),
            )

        return img

    def show(self):
        self.generate_img().show()

    def save(self):
        self.generate_img().save("battleship.png")

    # Returns a new problem instance with the solution
    def solve(self, solution: Dict[int, int]) -> Self:
        def get_ship_index(item: int, bin: int) -> tuple[int, int]:
            col = (bin * 2) + 1
            row = sum(self.fleet[:item]) + item + 1
            return (row, col)

        def set_ship(puzzle: Battleship, row: int, col: int, length: int):
            for i in range(length):
                puzzle.grid[row + i][col] = Tile.SHIP

        solved = copy.deepcopy(self)
        for item, bin in solution.items():
            set_ship(solved, *get_ship_index(item, bin), self.fleet[item])

        return solved


def reduce(items: list[int], bins: int, cap: int) -> Battleship:
    # Calculate grid size
    nrows = len(items) + sum(items)
    ncols = bins * 2

    # Initialize all tiles to WATER
    initial = [[Tile.WATER for _ in range(ncols)] for _ in range(nrows)]

    # Set the corresponding tiles to UNKNOWN
    height = 1
    for i in range(len(items)):
        for j in range(bins):
            for k in range(items[i]):
                initial[height + k][1 + 2 * j] = Tile.UNKNOWN
        height += items[i] + 1

    # Initialize col and row tallies
    col_tallies = [0 if i % 2 == 0 else cap for i in range(ncols)]
    row_tallies = [0 for _ in range(nrows)]

    height = 1
    for i in range(len(items)):
        for j in range(items[i]):
            row_tallies[height + j] = 1
        height += items[i] + 1

    # Initialize fleet
    fleet = items.copy()

    return Battleship(nrows, ncols, initial, row_tallies, col_tallies, fleet)


def read_input() -> tuple[list[int], int, int]:
    first_line = input().split(" ")
    if len(first_line) != 3:
        raise Exception(f"Expected 3 numbers in input, got {len(first_line)}")

    first_line = [int(num) for num in first_line]
    n_items, bins, cap = first_line

    second_line = input().split(" ")
    if len(second_line) != n_items:
        raise Exception(f"Expected {n_items} numbers in input, got {len(second_line)}")

    items = [int(num) for num in second_line]

    return (items, bins, cap)


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
    pli_show = True if len(sys.argv) > 1 and sys.argv[1] == "--pli-show" else False
    pli = True if len(sys.argv) > 1 and sys.argv[1] == "--pli" else False

    items, bins, cap = read_input()
    solution = solve_binpack(items, bins, cap)

    if pli or pli_show:
        if solution:
            if pli:
                print("Solution:")
                print(pretty(items, bins, solution))
            else:
                reduce(items, bins, cap).solve(solution).show()
        else:
            print("No feasible solution exists.")
    else:
        reduce(items, bins, cap).show()
