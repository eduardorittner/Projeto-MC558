from enum import Enum
from PIL import Image, ImageDraw
import copy


class Square(Enum):
    UNKNOWN = 0
    WATER = 1
    SHIP = 2


class Battleship:
    def __init__(
        self,
        nrows: int,
        ncols: int,
        initial: list[list[Square]],
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

    def generate_img(self, square_size=20):
        # Calculate image height and width. 1 extra tile for text
        width = (self.ncols + 1) * square_size
        height = (self.nrows + 1) * square_size

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
                if self.grid[row][col] == Square.UNKNOWN:
                    color = unknown_color
                elif self.grid[row][col] == Square.WATER:
                    color = water_color
                elif self.grid[row][col] == Square.SHIP:
                    color = ship_color
                else:
                    raise Exception("Invalid Square enum value")
                draw.rectangle(
                    [
                        (col * square_size + 1, row * square_size + 1),
                        (col * square_size + 19, row * square_size + 19),
                    ],
                    fill=color,
                )

        # Write row tally numbers
        for i in range(self.nrows):
            draw.text(
                (width - 3 * square_size / 4, i * 20 + 5),
                str(self.row_tallies[i]),
                fill=(0, 0, 0),
            )

        # Write col tally numbers
        for i in range(self.ncols):
            draw.text(
                (i * 20 + 5, height - 3 * square_size / 4),
                str(self.col_tallies[i]),
                fill=(0, 0, 0),
            )

        return img

    def show(self):
        """Show visual instance of puzzle"""
        self.generate_img().show()


def reduce(items: list[int], bins: int, cap: int) -> Battleship:
    # Calculate grid size
    nrows = len(items) + sum(items)
    ncols = bins * 2

    # Initialize all tiles to WATER
    initial = [[Square.WATER for _ in range(ncols)] for _ in range(nrows)]

    # Set the corresponding tiles to UNKNOWN
    height = 1
    for i in range(len(items)):
        for j in range(bins):
            for k in range(items[i]):
                initial[height + k][1 + 2 * j] = Square.UNKNOWN
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


def bin_packing_input() -> tuple[list[int], int, int]:
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


if __name__ == "__main__":
    items, bins, cap = bin_packing_input()
    puzzle = reduce(items, bins, cap)
    puzzle.show()