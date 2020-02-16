import base64

boardTypes = {0: "SUDOKU", 1: "KILLER_SUDOKU", 2: "GREATER_THAN_KILLER_SUDOKU"}


class KillerSudoku:
    def __init__(
        self, boardEncoding
    ):  # Extend this later to also input and use the solution encoding
        boardDecoded = self.decode_base64_input(boardEncoding)

        boardType = self.get_board_type(boardDecoded)
        if boardType != "KILLER_SUDOKU":
            raise Exception(
                "Wrong board type of {} was inputted. Only KILLER_SUDOKU is supported here."
            )

        self.parse_initial_board_state(boardDecoded)

    def decode_base64_input(self, base64Input):
        base64_bytes = base64Input.encode("ascii")
        message_bytes = base64.b64decode(base64_bytes)
        # Unpack byte code to integer values
        t = []
        for messageByte in message_bytes:
            t.append(messageByte)
        return t

    def get_board_type(self, boardDecoded):
        typeCode = boardDecoded[0]
        if typeCode > 2 or typeCode < 0:
            raise ValueError(
                "\n\nBoard type is not in the range 0-2 of recognised types. Input typeCode = {}.\n".format(
                    typeCode
                )
            )
        return boardTypes[typeCode]

    def parse_initial_board_state(self, boardDecoded):
        # First two value of boardDecoded are the typeCode and I think some sort
        # of error checking number, therefore information is everything after this.
        sudokuInformation = boardDecoded[2:164]
        initialValues = sudokuInformation[0::2]
        cageAssignments = sudokuInformation[1::2]
        cageValues = boardDecoded[164:]

        # Now to initial the list of cages
        self.startingGrid = [[0] * 9] * 9
        self.cages = [(k, []) for k in cageValues]
        for row in range(9):
            for column in range(9):
                index = 9 * row + column

                cageAssignment = cageAssignments[index]
                initialValue = initialValues[index]

                self.cages[cageAssignment][1].append([row, column])
                self.startingGrid[row][column] = initialValue


if __name__ == "__main__":
    boardEncoding = "AZoAAAAAAAIAAwADAAQAAQABAAYABwAHAAIAAwAKAAQABQAFAAYABwAIAAgACQAKAAQACwAFAAYADAAMAA4ACQAQABEACwANAA0AEwAMAA4ADwAQABEAEgAUAA0AEwATABUADwAQABcAEgAUABQAGgAbABUAHAAWABcAGAAYABkAGgAbABsAHAAWAB0AHgAZABkAGgAfAB8AHAAdAB0AHgAgACAICQgMDxMQDg8KDAcYEQgMEwQPDAcICg4MEg8NDA8HCgg="
    killerSudoku = KillerSudoku(boardEncoding)

    print(killerSudoku.startingGrid)
    print(killerSudoku.cages)
