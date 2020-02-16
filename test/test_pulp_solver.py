from killer_sudoku import pulp_solver
import numpy as np

CAGE_CONSTRAINTS = [
    (8, [[0, 0], [0, 1]]),
    (9, [[0, 6], [0, 7]]),
    (8, [[0, 2], [1, 2]]),
    (12, [[0, 3], [0, 4], [1, 3]]),
    (15, [[0, 5], [1, 5], [2, 5]]),
    (19, [[1, 6], [1, 7], [2, 7]]),
    (16, [[0, 8], [1, 8], [2, 8]]),
    (14, [[1, 0], [1, 1], [2, 0]]),
    (15, [[2, 1], [2, 2]]),
    (10, [[2, 3], [3, 3]]),
    (12, [[1, 4], [2, 4]]),
    (7, [[2, 6], [3, 6]]),
    (24, [[3, 0], [3, 1], [4, 1]]),
    (17, [[3, 7], [3, 8], [4, 8]]),
    (8, [[3, 2], [4, 2]]),
    (12, [[4, 3], [5, 3]]),
    (19, [[3, 4], [4, 4], [5, 4]]),
    (4, [[3, 5], [4, 5]]),
    (15, [[4, 6], [5, 6]]),
    (12, [[4, 0], [5, 0], [5, 1]]),
    (7, [[4, 7], [5, 7], [5, 8]]),
    (8, [[5, 2], [6, 2]]),
    (10, [[6, 4], [7, 4]]),
    (14, [[5, 5], [6, 5]]),
    (12, [[6, 6], [6, 7]]),
    (18, [[6, 8], [7, 7], [7, 8]]),
    (15, [[6, 0], [7, 0], [8, 0]]),
    (13, [[6, 1], [7, 1], [7, 2]]),
    (12, [[6, 3], [7, 3], [8, 3]]),
    (15, [[7, 5], [8, 4], [8, 5]]),
    (7, [[7, 6], [8, 6]]),
    (10, [[8, 1], [8, 2]]),
    (8, [[8, 7], [8, 8]]),
]


def test_solve():
    killer_solver = pulp_solver.KillerSudokuSolver(cage_constraints=CAGE_CONSTRAINTS)

    solution = killer_solver.solve()

    # checking some constraints
    assert solution[8][7] + solution[8][8] == 8
    assert solution[0][0] + solution[0][1] == 8
    assert solution[6][8] + solution[7][7] + solution[7][8] == 18
    assert solution[3][2] + solution[4][2] == 8

    # checking rows and columns sum to 45
    solution_array = np.array(solution)
    assert (solution_array.sum(axis=1) == 45).all()
    assert (solution_array.sum(axis=0) == 45).all()
