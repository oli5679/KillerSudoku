import pulp

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


class KillerSudokuSolver:
    """
    Solve Killer Sudokus 

    https://en.wikipedia.org/wiki/Killer_sudoku

    Attributes:
        solve (method): solves sudoku
    """

    def __init__(self, cage_constraints):
        """
        Args:
            cage_constraints (list): Lists of tuples 'cage constraints'
                e.g. if cells [0,0], [0,1], and [0,2] sum to 12 would be
                (12, [[0,0],[0,1],[0,2]])
        """
        self.cage_constraints = cage_constraints
        self.problem = pulp.LpProblem("Killer Sudoku Problem")
        self.choices = pulp.LpVariable.dicts(
            "Choice", (range(9), range(9), range(1, 10),), cat="Binary"
        )
        self.distinct_groups = self._generate_distinct_groups()
        self._add_constraints()

    def _generate_distinct_groups(self):
        """
        Creates groups where each value 1-9 should be unique:
            puzzle rows, columns and boxes

        Returns:
            distinct_groups (list): list of lists, each list contains coordinates of a different 'distinct_group'
        """
        row_groups = [[(i, j) for i in range(9)] for j in range(9)]
        col_groups = [[(j, i) for i in range(9)] for j in range(9)]

        box_groups = [
            [((3 * i) + k, (3 * j) + l) for k in range(3) for l in range(3)]
            for i in range(3)
            for j in range(3)
        ]
        return row_groups + col_groups + box_groups

    def _add_constraints(self):
        """
        Adds constraints to problem

        NOTE - not sure why equality constraints don't work, wierd!

        a) arbitrary objective

        b) Each cell can have at most 1 value

        c) each 'distinct_group' must have at most 1 of each number

        d) each cage must sum to at least target
        """
        # Arbitrary objective. Only aim is to satisfy constraints
        self.problem += (0, "Arbitrary Objective Function")

        # One value per cell.
        for i in range(9):
            for j in range(9):
                one_val_per_cell = (
                    pulp.lpSum([self.choices[i][j][n] for n in range(1, 10)]) <= 1
                )
                self.problem += one_val_per_cell

        # No repeates in 'distinct_groups' row, col & box
        for n in range(1, 10):
            for distinct_group in self.distinct_groups:
                for i, j in distinct_group:
                    group_count_number = [
                        self.choices[i][j][n] for i, j in distinct_group
                    ]
                self.problem += pulp.lpSum(group_count_number) <= 1

        # Cages add up to cage totals
        for target, cells in self.cage_constraints:
            cage_cells_constraint = [
                self.choices[i][j][n] * n for i, j in cells for n in range(1, 10)
            ]
            self.problem += pulp.lpSum(cage_cells_constraint) >= target

    def solve(self):
        """
        Solves the problem

        Returns:
            parsed_result (list): list of row values for parsed solution
        """
        self.problem.solve()
        if self.problem.status != 1:
            raise AssertionError("Problem not sucessfully solved")
        self.parsed_result = [
            [
                int(sum([self.choices[i][j][n].varValue * n for n in range(1, 10)]))
                for j in range(9)
            ]
            for i in range(9)
        ]

        return self.parsed_result


if __name__ == "__main__":
    killer_solver = KillerSudokuSolver(cage_constraints=CAGE_CONSTRAINTS)

    solution = killer_solver.solve()

    assert solution[8][7] + solution[8][8] == 8
    assert solution[0][0] + solution[0][1] == 8

    for row in solution:
        print(row)
