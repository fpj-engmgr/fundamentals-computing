"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # get the width and height
        puzzle_width = self.get_width()
        puzzle_height = self.get_height()
        # is tile zero located at target_row, target_col? if not return False
        if self.get_number(target_row, target_col) != 0:
            return False
        # are tiles to the right of tile zero in the correct position?
        for tile_col in range(target_col + 1, puzzle_width):
            expected_val = tile_col + target_row * puzzle_width
            if self.get_number(target_row, tile_col) != expected_val:
                return False
        # if there are more rows below our target_row, check them also
        for target_idx in range(target_row + 1, puzzle_height):
            for tile_col in range(puzzle_width):
                expected_val = tile_col + (target_idx) * puzzle_width
                if self.get_number(target_idx, tile_col) != expected_val:
                    return False
        # we passed all the tests, so the invariant is True
        return True

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        # verify that we're not trying to solve for column 0
        assert target_col != 0, "solve_interior_tile called for col 0; use solve_col0_tile instead!"
        # ensure that lower_row_invariant is True
        assert self.lower_row_invariant(target_row, target_col) == True, "solve_interior_tile: lower_row_invariant != True!"
        # initialize move string
        move_string = ""
        # find current position of target tile
        (target_cur_row, target_cur_col) = self.current_position(target_row, target_col)
        #
        # examine the options:
        # - same row:
        # - - move left for the number of steps
        if target_cur_row == target_row:
            # see how far away the target tile is
            move_steps = target_col - target_cur_col
            # cycle through the moves
            for move_idx in range(1, move_steps + 1):
                # if this is a repeated move, position the zero to the right of the target
                if move_idx == 1:
                    # move zero tile to left of target tile
                    move_string += ((move_steps + 1) - move_idx) * "l"
                elif move_idx > 1:
                    # we're let of the tile, so get to the right and move left
                    move_string += "urrdl"
            # update the puzzle and return the move string
            self.update_puzzle(move_string)
            # verify that lower_row_invariant holds for new position
            (tile_zero_row, tile_zero_col) = self.current_position(0, 0)
            assert self.lower_row_invariant(tile_zero_row, tile_zero_col) == True, "solve_interior_tile: lower_row_invariant != True"
            
            return move_string
        #
        # target tile is somewhere above us
        #
        elif target_cur_row < target_row:
            # first move up to the target_cur_row
            move_string = "u" * (target_row - target_cur_row)
            #
            # ensure target is in correct column
            #
            if target_cur_col < target_col:
                # target is to our left
                move_steps = target_col - target_cur_col
                # cycle through the moves
                for move_idx in range(1, move_steps + 1):
                    # if this is a repeated move, position the zero to the right of the target
                    if move_idx == 1:
                        # move zero tile to left of target tile
                        move_string += ((move_steps + 1) - move_idx) * "l"
                    elif move_idx > 1:
                        # we're let of the tile, so get to the right and move left
                        if target_cur_row == 0:
                            move_string += "drrul"
                        else:
                            move_string += "urrdl"
                # moves now have zero to the left of target, so...
                if target_cur_row == 0:
                    move_string += "dru"
                else:
                    move_string += "urd"
                # zero is now above the target
            elif target_cur_col > target_col:
                # target is to our right
                move_steps = target_cur_col - target_col
                # cycle through the moves
                for move_idx in range(1, move_steps + 1):
                    # if this is a repeated move, position the zero to the right of the target
                    if move_idx == 1:
                        # move zero tile to left of target tile
                        move_string += ((move_steps + 1) - move_idx) * "r"
                    elif move_idx > 1:
                        # we're let of the tile, so get to the right and move left
                        if target_cur_row == 0:
                            move_string += "dllur"
                        else:
                            move_string += "ulldr"
                # moves now have zero to the right of target, so...
                if target_cur_row == 0:
                    move_string += "dlu"
                else:
                    move_string += "uld"
            # zero is now above the target tile, which is down one row
            move_steps = target_row - target_cur_row
            for move_idx in range(1, move_steps):
                move_string += "lddru"
            # target should now be in place, so move zero to correct position
            move_string += "ld"
            # update the puzzle
            self.update_puzzle(move_string)
            # verify that lower_row_invariant holds for new position
            (tile_zero_row, tile_zero_col) = self.current_position(0, 0)
            #
            assert self.lower_row_invariant(tile_zero_row, tile_zero_col) == True, "solve_interior_tile: lower_row_invariant != True"
        
        return move_string

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        # replace with your code
        return ""

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        return False

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        return False

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        return ""

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        return ""

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        return ""

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        return ""

# Start interactive simulation
# poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))

"""
Test section 
- do some basic tests first
- lower_row_invariant
"""

def test_puzzle():
    # set up a defined puzzle
    grid_0 = [[4, 2, 3, 7],
              [8, 5, 6, 10],
              [9, 1, 13, 11],
              [12, 0, 14, 15]]
    height_0 = 4
    width_0 = 4
    puzzle_0 = Puzzle(height_0, width_0, grid_0)
    # check a couple of basic items
    print "Basics testing"
    print puzzle_0
#    print puzzle_0.get_number(3, 1)
#    print puzzle_0.lower_row_invariant(3, 1)
    assert puzzle_0.get_height() == height_0, "get_height: Height assertion failure!"
    assert puzzle_0.get_width() == width_0, "get_width: Width assertion failure!"
    assert puzzle_0.get_number(3, 1) == 0, "get_number: Tile zero not at (3, 1)"
    assert puzzle_0.current_position(0, 0) == (3, 1), "current_position: Tile zero not at (3, 1)"
    #
    assert puzzle_0.lower_row_invariant(3, 1), "lower_row_invariant failure of (3, 1)"
    assert not puzzle_0.lower_row_invariant(1, 2), "lower_row_invariant failure of (1, 2)"
    grid_0 = [[4, 2, 3, 5],
              [1, 0, 6, 7],
              [8, 9, 10, 11],
              [12, 13, 14, 15]]
    height_0 = 4
    width_0 = 4
    puzzle_0 = Puzzle(height_0, width_0, grid_0)
    # check a couple of basic items
    print "Basics testing"
    print puzzle_0
#    print puzzle_0.get_number(3, 1)
#    print puzzle_0.lower_row_invariant(3, 1)
    assert puzzle_0.get_height() == height_0, "get_height: Height assertion failure!"
    assert puzzle_0.get_width() == width_0, "get_width: Width assertion failure!"
    assert puzzle_0.get_number(1, 1) == 0, "get_number: Tile zero not at (1, 1)"
    assert puzzle_0.current_position(0, 0) == (1, 1), "current_position: Tile zero not at (1, 1)"
    #
    assert puzzle_0.lower_row_invariant(1, 1), "lower_row_invariant failure of (1, 1)"
    assert not puzzle_0.lower_row_invariant(1, 2), "lower_row_invariant failure of (1, 2)"
    #
    # test solve_interior_tile - same row
    grid_1 = [[4, 2, 3, 7],
              [8, 5, 6, 9],
              [10, 1, 0, 11],
              [12, 13, 14, 15]]
    height_1 = 4
    width_1 = 4
    puzzle_1 = Puzzle(height_1, width_1, grid_1)
    #
    print "solve_interior_tile - same row test"
    print puzzle_1
    print "Tile zero at ", puzzle_1.current_position(0, 0)
    move_string_1 = puzzle_1.solve_interior_tile(2, 2)
    print "move_string_1 : ", move_string_1
    print puzzle_1
    # 2nd same row test...simple case
    grid_2 = [[4, 2, 3, 7],
              [8, 5, 6, 9],
              [1, 10, 0, 11],
              [12, 13, 14, 15]]
    height_2 = 4
    width_2 = 4
    puzzle_2 = Puzzle(height_2, width_2, grid_2)
    #
    print "solve_interior_tile - same row test - simple case"
    print puzzle_2
    move_string_2 = puzzle_2.solve_interior_tile(2, 2)
    print "move_string_2 : ", move_string_2
    print puzzle_2
    # solve_interior_tile - not same row tests
    # 1st not ...simple case (same column)
    grid_3 = [[4, 13, 1, 3],
              [5, 10, 2, 7],
              [8, 12, 6, 11],
              [9, 0, 14, 15]]
    height_3 = 4
    width_3 = 4
    puzzle_3 = Puzzle(height_3, width_3, grid_3)
    #
    print "solve_interior_tile - different row test - simple case"
    print puzzle_3
    move_string_3 = puzzle_3.solve_interior_tile(3, 1)
    print "move_string_3 : ", move_string_3
    print puzzle_3
#
test_puzzle()
