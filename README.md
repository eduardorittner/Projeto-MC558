# Project

This code is part of a project from MC558, the second course on algorithm design and analysis at UNICAMP. The goal of the project was to prove that the [Battleship](https://en.wikipedia.org/wiki/Battleship_(puzzle)) game is NP-hard by applying a reduction to a problem which is known to be NP-hard. We were supplied this [paper](./paper.pdf) as inspiration, which applies a reduction to the [bin-packing](https://en.wikipedia.org/wiki/Bin_packing_problem) algorithm. This code is an implementation of the reduction algorithm that takes a bin-packing problem instance as input and outputs a visual representation of the equivalent Battleship puzzle.

## Input

The first input line contains 3 numbers N, B, C, separated by spaces, representing the number of items, number of bins and capacity of each bin, respectively.
The second line contains N numbers, separated by spaces, representing the size of each item

## Output

The output is an image in .png format, which by default is shown using Pillow's default image renderer, but can also be saved locally by passing the `--save` parameter

## Bin packing

We use a specific variant of the bin-packing problem which is 1D (each item has width = 1 and variable length) and where instead of trying to find a configuration where all items are distributed among the bins such that no bin exceeds the capacity, we look for a configuration where all bins are completely full, that is, there is no capacity remaining. This problem is still NP-hard and makes the reduction to a batlleship puzzle instance substantially easier.
