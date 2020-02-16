import numpy as np
from copy import deepcopy


class Sukoku:
    """
    Sudoku solver - uses DFS + rules

    Attributes:
        solve (method): solves sudoku
    """

    def __init__(self, input_board):
        """
        Args:
            board (list): list of starting board
                Each row is list, each value is cell value. 
                Zeros represent missing.
        """
        self.board = input_board
        self.prev_board = np.zeros((9, 9))
        self._find_possibilities()

    def _find_possibilities(self):
        """
        Finds possible moves according to 'filter_logic' that 
        rows/columns/boxes must have unique values

        cell candidates stored in self.cands

        Returns:
            contradiction_flag (bool): flag is board state already impossible
        """
        # What moves are valid? - start with all, except cells already filled in
        self.cands = [
            [[cell] if cell != 0 else [1, 2, 3, 4, 5, 6, 7, 8, 9] for cell in row]
            for row in self.board
        ]

        # Is there a contradiction in the board?
        contradiction_flag = False
        # Update each cell's 'cands' using the 3 rules
        for i in range(9):
            for j in range(9):
                # Filter out numbers sharing row, column and box
                self._row_filter(i, j)
                self._col_filter(i, j)
                self._box_filter(i, j)
                # If only single entry remains, add to board
                cell_cands = self.cands[i][j]
                if len(cell_cands) == 1:
                    self.board[i][j] = cell_cands[0]

                # If solution is impossible, return contradiction flag
                if len(cell_cands) == 0:
                    contradiction_flag = True
        return contradiction_flag

    def _row_filter(self, i, j):
        """
        Filter out numbers in same row as cell i,j
        
        Updates self.cands
        """
        for row_val in range(9):
            remove_val = self.board[i][row_val]
            if row_val != j and remove_val in self.cands[i][j]:
                self.cands[i][j].remove(remove_val)

    def _col_filter(self, i, j):
        """
        Filter out numbers in same column as cell i,j
        
        Updates self.cands
        """
        for col_val in range(9):
            remove_val = self.board[col_val][j]
            if col_val != i and remove_val in self.cands[i][j]:
                self.cands[i][j].remove(remove_val)

    def _box_filter(self, i, j):
        """
        Filter out numbers in same 3x3 box as cell i,j

        Updates self.cands
        """
        # Find upper left corner of box
        box_i_start = (i // 3) * 3
        box_j_start = (j // 3) * 3

        # Loop through all 9 cells in box
        for i_add in range(0, 3):
            for j_add in range(0, 3):
                compare_i = box_i_start + i_add
                compare_j = box_j_start + j_add
                remove_val = self.board[compare_i][compare_j]
                if remove_val in self.cands[i][j]:
                    if not (compare_i == i and compare_j == j):
                        self.cands[i][j].remove(remove_val)

    def _check_finished(self):
        """
        Check if the board is already 'finished'
        Are there are any zeros left in board?
        
        Returns:
            completion_flag (bool): flag is board is completed
        """
        return min([val for sublist in self.board for val in sublist]) > 0

    def _find_guess(self):
        """
        Of the remaining cells, guess the one with the fewest candidates - speeds up search
        
        Returns:
            (shortest_i (int): i coordinate of shortest guess,
            shortest_j (int): j coordinate of shortest guess,
            shortest_cands (list): valid candidates for shortest guess
            )
        """

        shortest_i, shortest_j, shortest_val = "placeholder", "placeholder", 100
        for i in range(9):
            for j in range(9):
                #  If value not already determinied
                if self.board[i][j] == 0:
                    # If shortest number of candiates so far
                    if len(self.cands[i][j]) < shortest_val:
                        # update shortest guess candiate
                        shortest_i = i
                        shortest_j = j
        return shortest_i, shortest_j, self.cands[shortest_i][shortest_j]

    def solve(self):
        """
        Solves sudoku by recursively calling this

        Returns:
            ans (list):
                list of answers to Sudoku
        """
        # Update candidate cells, contradiction_flag and board
        contradiction_flag = self._find_possibilities()
        # Check if finished
        completion_flag = self._check_finished()

        # Stop search if contradiction (will result in backtrack)
        if contradiction_flag:
            return None

        # If completed, return solution
        if completion_flag and not contradiction_flag:
            print("Solution")
            print("---")
            for r in self.board:
                print(r)
            print("---")
            return self.board

        # Guess one of the uncompleted cells
        if not contradiction_flag:
            guess_i, guess_j, guess_vals = self._find_guess()
            prev_board = deepcopy(self.board)
            for val in guess_vals:
                self.board = deepcopy(prev_board)
                self.board[guess_i][guess_j] = val
                ans = self.solve()
                # Return if you find a solution (i.e. doesn't return None)
                # This effectively causes backtracking - higher for-loops continue if no solution found
                if ans is not None:
                    return ans


test = [
    [0, 0, 2, 0, 6, 0, 3, 0, 0],
    [0, 6, 0, 9, 0, 0, 0, 7, 0],
    [9, 0, 0, 0, 0, 2, 0, 0, 6],
    [0, 0, 1, 0, 0, 0, 0, 5, 0],
    [5, 0, 0, 0, 2, 0, 0, 0, 3],
    [0, 4, 0, 0, 0, 0, 8, 0, 0],
    [1, 0, 0, 7, 0, 0, 0, 0, 9],
    [0, 5, 0, 0, 0, 4, 0, 8, 0],
    [0, 0, 8, 0, 9, 0, 2, 0, 0],
]


test = [
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

puz = Sukoku(test)
puz.solve()
