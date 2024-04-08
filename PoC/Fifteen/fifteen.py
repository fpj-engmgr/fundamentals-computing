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
        #
        assert target_row > 1, "lower_row_invariant: target_row too low!"
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
        assert target_col != 0, "use solve_col0_tile for column 0!"
        # ensure that lower_row_invariant is True
        assert self.lower_row_invariant(target_row, target_col) == True, "solve_interior_tile: lower_row_invariant != True!"
        # initialize move string
        move_string = ""
        # find current position of target tile
        (target_cur_row, target_cur_col) = self.current_position(target_row, target_col)
        #
        # same row - move left for the number of steps
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
                        # we're left of the tile, so get to the right and move left
                        if target_cur_row == 0:
                            move_string += "drrul"
                        else:
                            move_string += "urrdl"
                # moves now have zero to the left of target, so...
                if target_cur_row == 0:
                    move_string += "dru"
                    # note that we moved the target down a row
                    target_cur_row += 1
                else:
                    move_string += "ur"
                # zero is now above the target
            elif target_cur_col > target_col:
                # target is to our right
                move_steps = target_cur_col - target_col
                # cycle through the moves
#                print "move_steps : ", move_steps, " move_string : ", move_string
                for move_idx in range(1, move_steps + 1):
                    # if this is a repeated move, position the zero to the right of the target
                    if move_idx == 1:
                        # move zero tile to left of target tile
                        move_string += ((move_steps + 1) - move_idx) * "r"
                    elif move_idx > 1:
                        # we're right of the tile, so get to the left and move right
                        if target_cur_row == 0:
                            move_string += "dllur"
                        else:
                            move_string += "ulldr"
#                    print move_idx, " : ", move_string
                # moves now have zero to the right of target, so...
                if target_cur_row == 0:
                    move_string += "dlu"
                    # note that we moved the target down a row
                    target_cur_row += 1
                else:
                    move_string += "ul"
            elif target_cur_col == target_col:
                # we have moved the target down a row with the u's
                target_cur_row += 1
            # zero is now above the target tile, which is down one row
#            print "we should be above the target tile"
            move_steps = 1 + (target_row - target_cur_row)
#            print self, move_string, move_steps
            for move_idx in range(1, move_steps):
                move_string += "lddru"
            # target should now be in place, so move zero to correct position
            move_string += "ld"
#            print "solve_interior_tile : move_string : ", move_string
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

        # ensure that lower_row_invariant is True
        assert self.lower_row_invariant(target_row, 0) == True, "solve_col0_tile: lower_row_invariant != True!"
        # initialize move string and save the width
        move_string = ""
        puzzle_width = self.get_width()
        # find current position of target tile
        (target_cur_row, target_cur_col) = self.current_position(target_row, 0)
#       #
#        print "solve_col0_tile - target is at (", target_cur_row, ", ", target_cur_col, ")" 
        # if target is in column 0, right above us life's nice!
        if (target_cur_col == 0) and (target_cur_row == (target_row - 1)):
            # move tile zero up and to the end of the row
            move_string = "u" + (puzzle_width - 1) * "r"
        else:
            # move tile zero up
            move_string = "u"
            # get the target into column 1 - first check the rows we need to move
            num_row_moves = (target_row - (target_cur_row + 1))
            #
            if target_cur_col == 1:
                # we want to get target to (target_row - 1, 1)
                # if we're one the same row already...don't do a thing
                if num_row_moves > 0:
                    move_string += "r" + num_row_moves * "u"
                    target_cur_row += 1
#                print "solve_col0_tile - target in col 1 : ", move_string
                # tile zero is now above the target, which is one step closer
            elif target_cur_col == 0:
                # move tile zero to right and go up to target_cur_row
                move_string += "r" + num_row_moves * "u"
                # we're to the right of the target, so go left and around
                move_string += "ldru"
                target_cur_row += 1
                # tile zero is now above the target, which is one step closer
            else:
                # move tile zero to col 1 and to the target_cur_row and target_cur_col
                move_string += "r" + num_row_moves * "u"
                num_col_moves = target_cur_col - 1
                move_string += num_col_moves * "r"
                # loop through additional moves to get target to col 1, if needed
                for move_idx in range(1, num_col_moves):
                    if target_cur_row == 0:
                        move_string += "dllur"
                    else:
                        move_string += "ulldr"
                # we're to the right of the target, which is in col 1
                if target_cur_row == 0:
                    move_string += "dlu"
                    target_cur_row += 1
                else:
                    move_string += "ul"
                # tile zero is now above the target, which is one step closer
                
            # common moves start here
            # move target down toward (target_row - 1, 1)
            num_row_moves = (target_row - 1) - target_cur_row
            # iterate the number of rows to come down
            if num_row_moves > 0:
                move_string += "lddru" * num_row_moves
                # move zero from above target to left of target
                move_string += "ld"
            
            # and now target is above target's neighbor, so...
            move_string += "ruldrdlurdluurddlur"
            # tile zero is now at (target_row - 1, 1), so go to end of row
            move_string += (puzzle_width - 2) * "r"
            
        # make it so
#        print "solve_col0_tile - move_string at end : ", move_string
        # update the puzzle
        self.update_puzzle(move_string)
        # verify that lower_row_invariant holds for new position
        (tile_zero_row, tile_zero_col) = self.current_position(0, 0)
        assert self.lower_row_invariant(tile_zero_row, tile_zero_col) == True, "solve_col0_tile: lower_row_invariant != True"
        
        return move_string


    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        assert target_col > 1, "row0_invariant: target column not > 1"
        # get the width and height
        puzzle_width = self.get_width()
        puzzle_height = self.get_height()
        # set the row we're starting with
        target_row = 0
        # is tile zero located at (0, target_col)? if not return False
        if self.get_number(0, target_col) != 0:
            return False
        # are tiles to the right of tile zero in the correct position?
        for tile_col in range(target_col + 1, puzzle_width):
            expected_val = tile_col + target_row * puzzle_width
            if self.get_number(target_row, tile_col) != expected_val:
                return False
        # are tiles at (1, target_col) and to its right correct?
        for tile_col in range(target_col, puzzle_width):
            expected_val = tile_col + (target_row + 1) * puzzle_width
            if self.get_number(target_row + 1, tile_col) != expected_val:
                return False
        # if there are more rows below our target_row, check them also
        for target_idx in range(target_row + 1, puzzle_height):
            for tile_col in range(target_col, puzzle_width):
                expected_val = tile_col + (target_idx) * puzzle_width
                if self.get_number(target_idx, tile_col) != expected_val:
                    return False
        # we passed all the tests, so the invariant is True
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        assert target_col > 1, "row1_invariant: target column not > 1"
        # get the width and height
        puzzle_width = self.get_width()
        puzzle_height = self.get_height()
        # set the row we're starting with
        target_row = 1
        # is tile zero located at (1, target_col)? if not return False
        if self.get_number(1, target_col) != 0:
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

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        # 
        move_string = ""
        # where is the target?
        (target_cur_row, target_cur_col) = self.current_position(0, target_col)
        # if the target is to the left of zero...we're home free!
        if (target_cur_row == 0) and (target_cur_col == (target_col - 1)):
            move_string = "l"
        else:
            # solve for a 2x3 puzzle
            my_clone = self.clone()
            # we have to move the zero tile first left and down
            move_string = "ldl"
            # update the clone
            my_clone.update_puzzle("ldl")
            # check where the target is
            (clone_cur_row, clone_cur_col) = my_clone.current_position(1, target_col)
            # is it in the right spot? (2, target_col - 1)
            if (clone_cur_row == 2) and (clone_cur_col == (target_col - 1)):
                # once we have the target and zero in the right place, we do...
                move_string += "urdlurrdluldrruld"
            else:
                for move_count in range(2):
                    move_string += "urdl"
                    # update the clone
                    my_clone.update_puzzle("urdl")
                    (clone_cur_row, clone_cur_col) = my_clone.current_position(1, target_col)
                    # are we in the right spot now?
                    if (clone_cur_row == 2) and (clone_cur_col == (target_col - 1)):
                        # once we have the target and zero in the right place, we do...
                        move_string += "urdlurrdluldrruld"
                        break
        # update the puzzle and we're good
        self.update_puzzle(move_string)
        #
        return move_string

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        # 
        move_string = ""
        # where is the target?
        (target_cur_row, target_cur_col) = self.current_position(1, target_col)
        # address 2 very simple cases...
        if (target_cur_row == 1) and (target_cur_col == (target_col - 1)):
            # target is to the left
            move_string = "lur"
        elif (target_cur_col == target_col) and (target_cur_row == 0):
            # target is above us
            move_string = "u"
        else:
            # create a clone for testing
            my_clone = self.clone()
            # save the expected value
            expected_val = self.get_width() + target_col
            # put zero in the end position (0, target_col)
            move_string = "u"
            #
            my_clone.update_puzzle("u")
            # cycle through the 2x3 grid until we have the target in place
            for dummy_idx in range(5):
                move_string += "lldrru"
                my_clone.update_puzzle("lldrru")
                #
                if my_clone.get_number(1, target_col) == expected_val:
                    break
        # that's all there is to it

        # update the puzzle and we're good
        self.update_puzzle(move_string)
        #
        return move_string

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
    print "Tile zero is at ", puzzle_0.current_position(0, 0)
    print
    assert puzzle_0.get_height() == height_0, "get_height: Height assertion failure!"
    assert puzzle_0.get_width() == width_0, "get_width: Width assertion failure!"
    assert puzzle_0.get_number(3, 1) == 0, "get_number: Tile zero not at (3, 1)"
    assert puzzle_0.current_position(0, 0) == (3, 1), "current_position: Tile zero not at (3, 1)"
    # 
    assert puzzle_0.lower_row_invariant(3, 1), "lower_row_invariant failure of (3, 1)"
    assert not puzzle_0.lower_row_invariant(2, 2), "lower_row_invariant failure of (2, 2)"
    # non-last row
    grid_0 = [[4, 2, 3, 5],
              [1, 9, 6, 7],
              [8, 0, 10, 11],
              [12, 13, 14, 15]]
    height_0 = 4
    width_0 = 4
    puzzle_0 = Puzzle(height_0, width_0, grid_0)
    # check a couple of basic items
    print "Basics testing - lower_row_invariant for not last row"
    print puzzle_0
    print "Tile zero is at ", puzzle_0.current_position(0, 0)
    print
    #
    assert puzzle_0.lower_row_invariant(2, 1), "lower_row_invariant failure of (2, 1)"
    assert not puzzle_0.lower_row_invariant(2, 2), "lower_row_invariant failure of (2, 2)"
    # very last entry
    grid_0 = [[4, 2, 3, 5],
              [1, 15, 6, 7],
              [8, 9, 10, 11],
              [12, 13, 14, 0]]
    height_0 = 4
    width_0 = 4
    puzzle_0 = Puzzle(height_0, width_0, grid_0)
    # check a couple of basic items
    print "Basics testing - lower_row_invariant for very last item"
    print puzzle_0
    print "Tile zero is at ", puzzle_0.current_position(0, 0)
    print
    #
    assert puzzle_0.lower_row_invariant(3, 3), "lower_row_invariant failure of (3, 3)"
    assert not puzzle_0.lower_row_invariant(2, 2), "lower_row_invariant failure of (2, 2)"
    #
    # end of row (height - 1)
    grid_0 = [[4, 2, 3, 5],
              [1, 11, 6, 7],
              [8, 9, 10, 0],
              [12, 13, 14, 15]]
    height_0 = 4
    width_0 = 4
    puzzle_0 = Puzzle(height_0, width_0, grid_0)
    # check a couple of basic items
    print "Basics testing - lower_row_invariant for very last item"
    print puzzle_0
    print "Tile zero is at ", puzzle_0.current_position(2, 3)
    print
    #
    assert puzzle_0.lower_row_invariant(2, 3), "lower_row_invariant failure of (2, 3)"
    assert not puzzle_0.lower_row_invariant(2, 2), "lower_row_invariant failure of (2, 2)"
    #
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
    grid_4 = [[4, 3, 1, 13],
              [5, 10, 2, 7],
              [8, 12, 6, 11],
              [9, 0, 14, 15]]
    height_4 = 4
    width_4 = 4
    puzzle_4 = Puzzle(height_4, width_4, grid_4)
    #
    print "solve_interior_tile - different row test - target to the right"
    print puzzle_4
    move_string_4 = puzzle_4.solve_interior_tile(3, 1)
    print "move_string_4 : ", move_string_4
    print puzzle_4
    #
    grid_5 = [[13, 3, 1, 4],
              [5, 10, 2, 7],
              [8, 12, 6, 11],
              [9, 0, 14, 15]]
    height_5 = 4
    width_5 = 4
    puzzle_5 = Puzzle(height_5, width_5, grid_5)
    #
    print "solve_interior_tile - different row test - target to the left"
    print puzzle_5
    move_string_5 = puzzle_5.solve_interior_tile(3, 1)
    print "move_string_5 : ", move_string_5
    print puzzle_5
    #
    grid_6 = [[6, 3, 1, 4],
              [5, 10, 2, 7],
              [8, 12, 13, 11],
              [9, 0, 14, 15]]
    height_6 = 4
    width_6 = 4
    puzzle_6 = Puzzle(height_6, width_6, grid_6)
    #
    print "solve_interior_tile - target one row up to right"
    print puzzle_6
    move_string_6 = puzzle_6.solve_interior_tile(3, 1)
    print "move_string_6 : ", move_string_6
    print puzzle_6
    #
    grid_7 = [[6, 3, 1, 4],
              [5, 10, 2, 7],
              [13, 12, 8, 11],
              [9, 0, 14, 15]]
    height_7 = 4
    width_7 = 4
    puzzle_7 = Puzzle(height_7, width_7, grid_7)
    #
    print "solve_interior_tile - target one row up to left"
    print puzzle_7
    move_string_7 = puzzle_7.solve_interior_tile(3, 1)
    print "move_string_7 : ", move_string_7
    print puzzle_7
    #
    # start solve_col0_tile tests
    #
    grid_8 = [[6, 3, 1, 4],
              [5, 10, 2, 7],
              [12, 9, 8, 11],
              [0, 13, 14, 15]]
    height_8 = 4
    width_8 = 4
    puzzle_8 = Puzzle(height_8, width_8, grid_8)
    #
    print "solve_col0_tile - target right above us"
    print puzzle_8
    move_string_8 = puzzle_8.solve_col0_tile(3)
    print "move_string_8 : ", move_string_8
    print puzzle_8
    #
    grid_8 = [[6, 3, 1, 4],
              [5, 10, 2, 7],
              [9, 12, 8, 11],
              [0, 13, 14, 15]]
    height_8 = 4
    width_8 = 4
    puzzle_8 = Puzzle(height_8, width_8, grid_8)
    #
    print "solve_col0_tile - target is at (2, 1)"
    print puzzle_8
    move_string_8 = puzzle_8.solve_col0_tile(3)
    print "move_string_8 : ", move_string_8
    print puzzle_8
    #
    grid_8 = [[6, 3, 1, 4],
              [5, 10, 12, 7],
              [9, 2, 8, 11],
              [0, 13, 14, 15]]
    height_8 = 4
    width_8 = 4
    puzzle_8 = Puzzle(height_8, width_8, grid_8)
    #
    print "solve_col0_tile - target is at (1, 2)"
    print puzzle_8
    move_string_8 = puzzle_8.solve_col0_tile(3)
    print "move_string_8 : ", move_string_8
    print puzzle_8
    #
    grid_8 = [[6, 3, 1, 12],
              [5, 10, 4, 7],
              [9, 2, 8, 11],
              [0, 13, 14, 15]]
    height_8 = 4
    width_8 = 4
    puzzle_8 = Puzzle(height_8, width_8, grid_8)
    #
    print "solve_col0_tile - target is at (0, 3)"
    print puzzle_8
    move_string_8 = puzzle_8.solve_col0_tile(3)
    print "move_string_8 : ", move_string_8
    print puzzle_8
    #
    grid_8 = [[12, 3, 1, 6],
              [5, 10, 4, 7],
              [9, 2, 8, 11],
              [0, 13, 14, 15]]
    height_8 = 4
    width_8 = 4
    puzzle_8 = Puzzle(height_8, width_8, grid_8)
    #
    print "solve_col0_tile - target is at (0, 0)"
    print puzzle_8
    move_string_8 = puzzle_8.solve_col0_tile(3)
    print "move_string_8 : ", move_string_8
    print puzzle_8
    #
    grid_8 = [[6, 3, 1, 4],
              [5, 10, 2, 7],
              [12, 9, 8, 11],
              [0, 13, 14, 15]]
    height_8 = 4
    width_8 = 4
    puzzle_8 = Puzzle(height_8, width_8, grid_8)
    #
    print "solve_col0_tile - target is at (2, 0)"
    print puzzle_8
    move_string_8 = puzzle_8.solve_col0_tile(3)
    print "move_string_8 : ", move_string_8
    print puzzle_8
    #
    grid_9 = [[4, 6, 1, 3],
              [5, 2, 0, 7],
              [8, 9, 10, 11],
              [12, 13, 14, 15]]
    height_9 = 4
    width_9 = 4
    puzzle_9 = Puzzle(height_9, width_9, grid_9)
    #
    print "row1_invariant testing"
    print puzzle_9
    #
    assert puzzle_9.row1_invariant(2) == True, "row1 invariant failed for column 2"
    #
    grid_9 = [[4, 6, 1, 7],
              [5, 2, 0, 3],
              [8, 9, 10, 11],
              [12, 13, 14, 15]]
    height_9 = 4
    width_9 = 4
    puzzle_9 = Puzzle(height_9, width_9, grid_9)
    #
    print "row1_invariant testing"
    print puzzle_9
    #
    assert puzzle_9.row1_invariant(2) == False, "row1 invariant failed for column 2"
    #
    grid_9 = [[4, 6, 1, 14],
              [5, 2, 0, 7],
              [8, 9, 10, 11],
              [12, 13, 3, 15]]
    height_9 = 4
    width_9 = 4
    puzzle_9 = Puzzle(height_9, width_9, grid_9)
    #
    print "row1_invariant testing"
    print puzzle_9
    #
    assert puzzle_9.row1_invariant(2) == False, "row1 invariant failed for column 2"
    #
    # row0_invariant tests
    grid_9 = [[4, 2, 0, 3],
              [5, 1, 6, 7],
              [8, 9, 10, 11],
              [12, 13, 14, 15]]
    height_9 = 4
    width_9 = 4
    puzzle_9 = Puzzle(height_9, width_9, grid_9)
    #
    print "row0_invariant testing"
    print puzzle_9
    #
    assert puzzle_9.row0_invariant(2) == True, "row0 invariant failed for column 2"
    #
    grid_9 = [[4, 2, 3, 0],
              [5, 1, 6, 7],
              [8, 9, 10, 11],
              [12, 13, 14, 15]]
    height_9 = 4
    width_9 = 4
    puzzle_9 = Puzzle(height_9, width_9, grid_9)
    #
    print "row0_invariant testing"
    print puzzle_9
    #
    assert puzzle_9.row0_invariant(3) == True, "row0 invariant failed for column 2"
    # test the solvers for row1 and row0
    grid_10 = [[4, 2, 6, 3],
              [5, 1, 0, 7],
              [8, 9, 10, 11],
              [12, 13, 14, 15]]
    height_10 = 4
    width_10 = 4
    puzzle_10 = Puzzle(height_10, width_10, grid_10)
    #
    print "solve_row1_tile - solution above"
    print puzzle_10
    #
    move_string_10 = puzzle_10.solve_row1_tile(2)
    print "move_string_10 : ", move_string_10
    print puzzle_10
    print "now try for solve_row0_tile!"
    move_string_10 = puzzle_10.solve_row0_tile(2)
    print "move_string_10 : ", move_string_10
    print puzzle_10
    #
    grid_10 = [[6, 2, 4, 3],
              [5, 1, 0, 7],
              [8, 9, 10, 11],
              [12, 13, 14, 15]]
    height_10 = 4
    width_10 = 4
    puzzle_10 = Puzzle(height_10, width_10, grid_10)
    #
    print "solve_row1_tile - go fish"
    print puzzle_10
    #
    move_string_10 = puzzle_10.solve_row1_tile(2)
    print "move_string_10 : ", move_string_10
    print puzzle_10
    #
    print "now try for solve_row0_tile!"
    move_string_10 = puzzle_10.solve_row0_tile(2)
    print "move_string_10 : ", move_string_10
    print puzzle_10
    #
    grid_10 = [[6, 2, 1, 3],
              [5, 6, 0, 7],
              [8, 9, 10, 11],
              [12, 13, 14, 15]]
    height_10 = 4
    width_10 = 4
    puzzle_10 = Puzzle(height_10, width_10, grid_10)
    #
    print "solve_row1_tile - leftie"
    print puzzle_10
    #
    move_string_10 = puzzle_10.solve_row1_tile(2)
    print "move_string_10 : ", move_string_10
    print puzzle_10
    #
    print "now try for solve_row0_tile!"
    move_string_10 = puzzle_10.solve_row0_tile(2)
    print "move_string_10 : ", move_string_10
    print puzzle_10
#
test_puzzle()
