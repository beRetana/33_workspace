# queens.py
#
# ICS 33 Winter 2025
# Project 0: History of Modern
#
# A module containing tools that could assist in solving variants of the
# well-known "n-queens" problem.  Note that we're only implementing one part
# of the problem: immutably managing the "state" of the board (i.e., which
# queens are arranged in which cells).  The rest of the problem -- determining
# a valid solution for it -- is not our focus here.
#
# Your goal is to complete the QueensState class described below, though
# you'll need to build it incrementally, as well as test it incrementally by
# writing unit tests in test_queens.py.  Make sure you've read the project
# write-up before you proceed, as it will explain the requirements around
# following (and documenting) an incremental process of solving this problem.
#
# DO NOT MODIFY THE Position NAMEDTUPLE OR THE PROVIDED EXCEPTION CLASSES.

from collections import namedtuple
from typing import Self



Position = namedtuple('Position', ['row', 'column'])

# Ordinarily, we would write docstrings within classes or their methods.
# Since a namedtuple builds those classes and methods for us, we instead
# add the documentation by hand afterward.
Position.__doc__ = 'A position on a chessboard, specified by zero-based row and column numbers.'
Position.row.__doc__ = 'A zero-based row number'
Position.column.__doc__ = 'A zero-based column number'



class DuplicateQueenError(Exception):
    """An exception indicating an attempt to add a queen where one is already present."""

    def __init__(self, position: Position):
        """Initializes the exception, given a position where the duplicate queen exists."""
        self._position = position


    def __str__(self) -> str:
        return f'duplicate queen in row {self._position.row} column {self._position.column}'



class MissingQueenError(Exception):
    """An exception indicating an attempt to remove a queen where one is not present."""

    def __init__(self, position: Position):
        """Initializes the exception, given a position where a queen is missing."""
        self._position = position


    def __str__(self) -> str:
        return f'missing queen in row {self._position.row} column {self._position.column}'



class QueensState:
    """Immutably represents the state of a chessboard being used to assist in
    solving the n-queens problem."""

    _EMPTY = 0
    _QUEEN = 1

    def __init__(self, rows: int, columns: int):
        """Initializes the chessboard to have the given numbers of rows and columns,
        with no queens occupying any of its cells."""

        board = []

        for row in range(rows):
            new_row = []
            for column in range(columns):
                new_row.append(QueensState._EMPTY)
            board.append(new_row)

        self._board = board

    def get_queen_board_reference(self)-> list[list[int]]:
        """Returns the state of the chessboard as a list (reference)."""
        return self._board

    def get_queen_state_board(self) -> list[list[int]]:
        """Returns the state of the chessboard as a copy of the list."""
        import copy
        return copy.deepcopy(self._board)

    def set_queen_state_board(self, new_state: list[list[int]]) -> None:
        """Gets the state of the chessboard as a list and sets it"""
        import copy
        self._board = copy.deepcopy(new_state)

    def queen_count(self) -> int:
        """Returns the number of queens on the chessboard."""
        count = 0

        for row in self.get_queen_board_reference():
            for column in row:
                count += column

        return count

    def queens(self) -> list[Position]:
        """Returns a list of the positions in which queens appear on the chessboard,
        arranged in no particular order."""

        queen_positions = []
        queen_board = self.get_queen_board_reference()

        for row in range(len(queen_board)):
            for column in range(len(queen_board[row])):
                if queen_board[row][column]:
                    queen_positions.append(Position(row, column))

        return queen_positions

    def has_queen(self, position: Position) -> bool:
        """Returns True if a queen occupies the given position on the chessboard, or
        False otherwise."""

        if self.get_queen_board_reference()[position.row][position.column]:
            return True
        else:
            return False

    def any_queens_unsafe(self) -> bool:
        """Returns True if any queens on the chessboard are unsafe (i.e., they can
        be captured by at least one other queen on the chessboard), or False otherwise."""

        queen_positions = self.queens()

        for queen_position in queen_positions:
            if self._unsafe(queen_position):
                return True

        return False

    def _unsafe(self, position) -> bool:
        """Returns True if there is a queen in the attack zone of the
        queen in the location given,False otherwise."""

        queen_board = self.get_queen_board_reference()

        def search_queen(row_direction, column_direction) -> bool:

            row_position = position.row
            column_position = position.column
            while True:
                row_position += row_direction
                column_position += column_direction
                if -1 < column_position < len(queen_board[position.row]):
                    if -1 < row_position < len(queen_board):
                        if queen_board[row_position][column_position]:
                            return True
                    else:
                        break
                else:
                    break

        for row_change in range(-1,2,1):
            for column_change in range(-1, 2, 1):
                if row_change == 0 and column_change == 0:
                    continue
                if search_queen(row_change, column_change):
                    return True

        return False


    def with_queens_added(self, positions: list[Position]) -> Self:
        """Builds a new QueensState with queens added in the given positions,
        without modifying 'self' in any way.  Raises a DuplicateQueenError when
        there is already a queen in at least one of the given positions."""

        def condition_checker(value_in_space: int, position_param: Position) -> int:
            """Returns a queen (1) when the space is empty and returns an error if it
            already has a queen in the given position."""

            if value_in_space:
                raise DuplicateQueenError(position_param)
            else:
                return QueensState._QUEEN

        new_queen_state = self.with_queens_searcher(positions, condition_checker)
        return new_queen_state


    def with_queens_removed(self, positions: list[Position]) -> Self:
        """Builds a new QueensState with queens removed from the given positions,
        without modifying 'self' in any way.  Raises a MissingQueenError when there
        is no queen in at least one of the given positions."""

        def condition_checker(value_in_space: int, position_param: Position) -> int:
            if value_in_space:
                return QueensState._EMPTY
            else:
                raise MissingQueenError(position_param)

        new_queen_state = self.with_queens_searcher(positions, condition_checker)
        return new_queen_state

    def with_queens_searcher(self, positions: list[Position], funct: "function") -> Self:
        """Searches through the board in look out for the positions that are sent down to
        then call the function passed as a parameter that determines what change happens to
        the board, then the board in the new instance gets updated."""

        initial_row = 0
        old_queen_board = self.get_queen_state_board()
        temp_old_queen_board = self.get_queen_state_board()
        new_queen_state = QueensState(len(old_queen_board), len(old_queen_board[initial_row]))

        for position in positions:
            if not (-1 < position.row < len(old_queen_board)):
                continue

            if not (-1 < position.column < len(old_queen_board[initial_row])):
                continue

            value_in_space = old_queen_board[position.row][position.column]
            temp_old_queen_board[position.row][position.column] = funct(value_in_space, position)

        new_queen_state.set_queen_state_board(temp_old_queen_board)

        return new_queen_state
