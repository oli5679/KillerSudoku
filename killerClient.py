from killerSudoku import KillerSudoku
from killerSolver import KillerSudokuSolver
import requests
import re


class KillerCient:
    def __init__(self):
        self.baseAddress = "https://www.dailykillersudoku.com"

    def get_killer_sudoku(self, puzzleId):
        response = requests.get("{}/puzzle/{}".format(self.baseAddress, puzzleId))

        content = str(response.content)

        matches = re.findall(
            r'board_base64":"([a-zA-Z\d=]*)","solution_base64":"([a-zA-Z\d=]*)"',
            content,
        )

        boardBase64, solutionBase64 = matches[0]

        killer = KillerSudoku(boardBase64)

        return killer


if __name__ == "__main__":
    client = KillerCient()

    killer = client.get_killer_sudoku(19664)

    print('Pulling Sudoku')

    killer_solver = KillerSudokuSolver(cage_constraints=killer.cages)
    
    print('Solving Sudoku')
    solution = killer_solver.solve()

    print('Solution found')
    for row in solution:
        print(row)


