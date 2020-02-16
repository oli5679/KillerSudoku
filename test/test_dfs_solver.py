import pytest
from killer_sudoku import dfs_solver

TEST_INPUT = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 4, 0, 0, 6, 0, 0, 0],
    [0, 0, 3, 1, 4, 9, 7, 0, 0],
    [0, 0, 7, 8, 0, 0, 1, 0, 2],
    [2, 0, 0, 0, 0, 1, 0, 9, 0],
    [0, 0, 1, 5, 0, 0, 4, 0, 6],
    [0, 0, 2, 4, 1, 8, 9, 0, 0],
    [8, 0, 5, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]

EXPECTED_OUTPUT = [
    [7, 9, 6, 2, 8, 5, 3, 1, 4],
    [1, 8, 4, 7, 3, 6, 2, 5, 9],
    [5, 2, 3, 1, 4, 9, 7, 6, 8],
    [6, 5, 7, 8, 9, 4, 1, 3, 2],
    [2, 4, 8, 3, 6, 1, 5, 9, 7],
    [9, 3, 1, 5, 2, 7, 4, 8, 6],
    [3, 6, 2, 4, 1, 8, 9, 7, 5],
    [8, 1, 5, 9, 7, 2, 6, 4, 3],
    [4, 7, 9, 6, 5, 3, 8, 2, 1],
]


def test_solve():
    puz = dfs_solver.Sukoku(TEST_INPUT)
    solution = puz.solve()
    print(solution)
    flat_solution = [item for sublist in solution for item in sublist]
    flat_expected = [item for sublist in EXPECTED_OUTPUT for item in sublist]
    assert all([a == b for a, b in zip(flat_expected, flat_solution)])
