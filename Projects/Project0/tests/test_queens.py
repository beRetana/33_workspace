# test_queens.py
#
# ICS 33 Winter 2025
# Project 0: History of Modern
#
# Unit tests for the QueensState class in "queens.py".
#
# Docstrings are not required in your unit tests, though each test does need to have
# a name that clearly indicates its purpose.  Notice, for example, that the provided
# test method is named "test_queen_count_is_zero_initially" instead of something generic
# like "test_queen_count", since it doesn't entirely test the "queen_count" method,
# but instead focuses on just one aspect of how it behaves.  You'll want to do likewise.

from queens import QueensState, Position
import unittest



class TestQueensState(unittest.TestCase):
    def test_queen_count_is_zero_initially(self):
        state = QueensState(8, 8)
        self.assertEqual(state.queen_count(), 0)

    def test__init__creation_of_board_with_correct_size_and_empty_spaces(self):

        def test_with_different_size(row_size, column_size):
            state = QueensState(row_size, column_size)
            self.assertEqual(len(state._board), row_size)

            for row in state.get_queen_state_board():
                self.assertEqual(len(row), column_size)
                for column in row:
                    self.assertEqual(column, 0)
                    
        test_with_different_size(8, 8)
        test_with_different_size(1, 1)
        test_with_different_size(20, 5)

    def test_get_queen_state_board_to_return_copies(self):
        state = QueensState(3, 3)
        self.assertNotEqual(id(state.get_queen_state_board()), id(state.get_queen_board_reference()))

    def test_with_queens_added_returns_expected_three_by_three(self):

        expected_new_board = [[0,0,0],
                              [1,0,0],
                              [0,0,1]]

        expected_old_board = [[0, 0, 0],
                              [0, 0, 0],
                              [0, 0, 0]]

        state = QueensState(3, 3)
        positions = [Position(2,2), Position(2,2), Position(1,0)]
        new_state = state.with_queens_added(positions)

        self.assertEqual(expected_new_board, new_state.get_queen_state_board())
        self.assertEqual(expected_old_board, state.get_queen_state_board())

    def test_with_queens_added_raises_an_exception(self):
        state = QueensState(3, 3)
        positions = [Position(2, 2), Position(1, 0)]
        state = state.with_queens_added(positions)

        from queens import DuplicateQueenError
        positions = [Position(1, 2), Position(1, 0)]

        with self.assertRaises(DuplicateQueenError):
            state.with_queens_added(positions)

    def test_with_queens_added_out_of_bounds_positions(self):
        state = QueensState(3, 3)
        positions = [Position(0, 0), Position(-1, 1), Position(2, 4), Position(1, 1), Position(2, 2)]
        expected_new_board = [[1, 0, 0],
                              [0, 1, 0],
                              [0, 0, 1]]
        state = state.with_queens_added(positions)

        self.assertEqual(expected_new_board, state.get_queen_state_board())

    def test_with_queens_removed_returns_expected_three_by_three(self):

        expected_new_board = [[0,0,0],
                              [0,1,0],
                              [0,0,0]]

        expected_old_board = [[1, 1, 1],
                              [0, 1, 1],
                              [0, 0, 1]]

        state = QueensState(3, 3)
        positions = [Position(0,0), Position(0,1), Position(0,2),
                     Position(1,1), Position(1,2),
                     Position(2,2)]

        state = state.with_queens_added(positions)

        positions = [Position(0, 0), Position(0, 1), Position(0, 2),
                     Position(1, 2), Position(1, 2),
                     Position(2, 2), Position(2, 2)]

        new_state = state.with_queens_removed(positions)

        self.assertEqual(expected_new_board, new_state.get_queen_state_board())
        self.assertEqual(expected_old_board, state.get_queen_state_board())

    def test_with_queens_removed_raises_an_exception(self):
        state = QueensState(3, 3)
        positions = [Position(2, 2), Position(1, 0)]
        state = state.with_queens_added(positions)

        from queens import MissingQueenError
        positions = [Position(1, 2), Position(1, 0)]

        with self.assertRaises(MissingQueenError):
            state.with_queens_removed(positions)

        try:
            state.with_queens_removed(positions)
        except MissingQueenError as error:
            self.assertEqual(error.__str__(), 'missing queen in row 1 column 2')


    def test_with_queens_removed_out_of_bounds_positions(self):
        state = QueensState(3, 3)
        positions = [Position(0, 0), Position(-1, 1), Position(2, 4), Position(1, 1), Position(2, 2)]
        expected_new_board = [[0, 0, 0],
                              [0, 0, 0],
                              [0, 0, 1]]
        state = state.with_queens_added(positions)
        positions = positions[:-1]
        state = state.with_queens_removed(positions)

        self.assertEqual(expected_new_board, state.get_queen_state_board())

    def test_queen_searcher_added(self):
        from queens import DuplicateQueenError
        expected_new_board = [[1, 0, 0],
                              [0, 0, 0],
                              [0, 1, 0]]

        expected_old_board = [[0, 0, 0],
                              [0, 0, 0],
                              [0, 0, 0]]

        def tester(value_in_space, position):
            if value_in_space:
                raise DuplicateQueenError(position)
            else:
                return QueensState._QUEEN

        state = QueensState(3, 3)
        positions = [Position(0, 0), Position(2, 1)]
        new_state = state.with_queens_searcher(positions, tester)

        self.assertEqual(expected_new_board, new_state.get_queen_state_board())
        self.assertEqual(expected_old_board, state.get_queen_state_board())

    def test_queen_searcher_added_raise_exception(self):
        from queens import DuplicateQueenError

        def tester(value_in_space: int, position: Position):
            if value_in_space:
                raise DuplicateQueenError(position)
            else:
                return QueensState._QUEEN

        state = QueensState(3, 3)
        positions = [Position(0, 0), Position(2, 1)]
        state = state.with_queens_searcher(positions, tester)

        with self.assertRaises(DuplicateQueenError):
            state.with_queens_searcher(positions, tester)
        try:
            state.with_queens_searcher(positions, tester)
        except DuplicateQueenError as error:
            self.assertEqual(error.__str__(), 'duplicate queen in row 0 column 0')

    def test_queen_count_with_more_than_one_queen(self):
        state = QueensState(3, 3)
        positions = [Position(2, 2), Position(1, 0)]
        state = state.with_queens_added(positions)

        self.assertEqual(2, state.queen_count())

        positions = [Position(0, 0), Position(0, 1), Position(0, 2)]
        state = state.with_queens_added(positions)

        self.assertEqual(5, state.queen_count())

    def test_queens_return_an_empty_list(self):
        state = QueensState(3, 3)
        self.assertEqual([], state.queens())

    def test_queens_return_positions(self):
        state = QueensState(3, 3)

        positions = [Position(0, 0), Position(0, 1), Position(0, 2)]
        state = state.with_queens_added(positions)

        self.assertEqual(positions, state.queens())

    def test_queens_returns_false(self):
        state = QueensState(3, 3)
        self.assertEqual(False, state.has_queen(Position(0, 0)))
        self.assertEqual(False, state.has_queen(Position(2, 0)))
        self.assertEqual(False, state.has_queen(Position(2, 2)))

    def test_queens_returns_true(self):
        state = QueensState(3, 3)

        positions = [Position(0, 0), Position(2, 0), Position(2, 2)]

        state = state.with_queens_added(positions)

        self.assertEqual(True, state.has_queen(Position(0, 0)))
        self.assertEqual(True, state.has_queen(Position(2, 0)))
        self.assertEqual(True, state.has_queen(Position(2, 2)))

    def test_any_queens_unsafe(self):
        state = QueensState(4, 4)
        self.assertEqual(False, state.any_queens_unsafe())
        state = state.with_queens_added([Position(0, 1)])
        self.assertEqual(False, state.any_queens_unsafe())
        state = state.with_queens_added([Position(1, 3)])
        self.assertEqual(False, state.any_queens_unsafe())
        state = state.with_queens_added([Position(2, 0)])
        self.assertEqual(False, state.any_queens_unsafe())
        state = state.with_queens_added([Position(3, 2)])
        self.assertEqual(False, state.any_queens_unsafe())
        state = state.with_queens_added([Position(2, 2)])
        self.assertEqual(True, state.any_queens_unsafe())

if __name__ == '__main__':
    unittest.main()
