#!/opt/homebrew/bin/python3

"""
Clone of 2048 game.
"""

#import poc_2048_gui
#import user51_3QVviOCgxh_0 as poc_2048_gui

import random
import math

# test suite
#import user51_6HKgraqrNV_4 as poc_test_suite

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

# helper functions
# - merge
def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    # iterate over the input list and slide all non-zero tiles into slide_line
    slide_line = []
    for tile in line:
        if tile > 0:
            slide_line.append(tile)
    # now check for matching neigbor pairs in slide_line and merge them
    return_line = []
    num_slided_tiles = len(slide_line)
    # iterate over all tiles in slide_line
    for tile_num in range(num_slided_tiles):
        # make sure our index doesn't go out of bounds
        if tile_num < (num_slided_tiles - 1):
            # compare the tiles
            if slide_line[tile_num] == slide_line[tile_num + 1]:
                # match: double value and append
                return_line.append(2 * slide_line[tile_num])
                # set next tile to zero, so we don't match again
                slide_line[tile_num + 1] = 0
            else:
                # no match: append the tile if it is non-zero
                if slide_line[tile_num] > 0:
                    return_line.append(slide_line[tile_num])
        else:
            # on the last tile, just append it, even if it is zero
            return_line.append(slide_line[tile_num])
    # pad the return_line with zero elements to match the length of the input line
    pad_length = len(line) - len(return_line)
    for dummy_idx in range(pad_length):
        return_line.append(0)
        
    return return_line
# - search_grid
def search_grid(search_val, grid, start_cell, grid_height, grid_width):
    """
    Helper function that finds a value in the grid through traversing it row by row.
    
    The start_cell is a tuples denoting the location in the grid to start at. This supports
    randomizing the start location for new tile inserts.
    
    The grid is a list of lists of dimension grid_height x grid_width
    
    The grid_height and grid_width are needed to bound the search in case there are no instances
    of search_val in the grid.
    
    search_grid will return:
    - tuple of the grid location where the value is found
    - (-1, -1) if the value is not found
    """
    # calculate the maximum number of squares to search
    max_search = grid_height * grid_width
    # set search direction to row traversal
    search_direction = (0, 1)
    # start stepping through the search
    for step in range(max_search):
        # increment the row every time the column wraps
        row = (start_cell[0] + ((start_cell[1] + step) // grid_width)) % grid_height
        # increment the column and wrap for width
        col = (start_cell[1] + step * search_direction[1]) % grid_width
        # check for a match
        if (grid[row][col] == search_val):
            return (row, col)
    # none found
    return (-1, -1)
# 
# Main game class for 2048

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # create a list of lists of height rows and width columns
        self._height = grid_height
        self._width = grid_width
        # set all entries in the grid to zero first
        self._grid = [[0 for dummy_col in range(self._width)] 
                         for dummy_row in range(self._height)]
        # keep a count of the empty squares, as that can shorten
        # the search to find one as the grid becomes full
        self._empty_squares = grid_height * grid_width

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        # create the empty grid first
        self._grid = [[0 for dummy_col in range(self._width)] 
                         for dummy_row in range(self._height)]
        # add 2 new tiles
        self.new_tile()
        self.new_tile()
        # we should have 2 new tiles

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # create a string for each row

        for row in range(self._height):
            if row == 0:
                print_string = "[" + str(self._grid[row])
            else:
                print_string = print_string + "\n " + str(self._grid[row])
        # add closing bracket
        print_string = print_string + "]"
        
        return print_string

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # Basic thoughts:
        # - in direction create lists with [0] being the target of the direction
        # - call merge for each list and set move flag, if the last element is 0
        # - reassemble the grid based on the direction
        # - if move flag is set add a new tile
        move_flag = False
        # get the movement offset
        offset = OFFSETS.get(direction)
        # select starting cell based on direction:
        # - default to upper left hand corner (0, 0)
        # - if down (-1, 0) then start lower left hand corner (height - 1, 0)
        # - if right (0, -1) then start upper right hand corner (0, width - 1)
        start_cell = [0, 0]
        #
        if offset[0] == -1:
            start_cell[0] = self._height - 1
        #
        if offset[1] == -1:
            start_cell[1] = self._width -1
        # set ranges based on vertical or horizontal traversal
        # - num_steps: number of elements to build a line to move
        # - num_lines: number of lines to process to complete the grid
        if (direction == UP) or (direction == DOWN):
            num_steps = self._height
            num_lines = self._width
        else:
            num_steps = self._width
            num_lines = self._height
        # loop for each line
        for line_num in range(num_lines):
            move_line = []
            # loop to build the line to process
            for step in range(num_steps):
                # calculate the row and column in the grid
                row = start_cell[0] + step * offset[0] + line_num * int(math.fabs(offset[1]))
                col = start_cell[1] + step * offset[1] + line_num * int(math.fabs(offset[0]))
                # add this cell to move_line
                move_line.append(self._grid[row][col])
            # the line is build, so now do the merge
            new_line = merge(move_line)
            # see if the lines differ
            if new_line == move_line:
                continue
            else:
                move_flag = True
            # put this line back into the grid
            for step in range(num_steps):
                # calculate the row and column in the grid
                row = start_cell[0] + step * offset[0] + line_num * int(math.fabs(offset[1]))
                col = start_cell[1] + step * offset[1] + line_num * int(math.fabs(offset[0]))
                # 
                self._grid[row][col] = new_line[step]
        # if something was moved, add a tile
        if move_flag:
            self.new_tile()
        # that's all

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        
        Return:
        - True, if a new tile was added
        - False, if no new tile was added (no space)
        
        """
        if (random.random() >= 0.9):
            new_tile_value = 4
        else:
            new_tile_value = 2
        
        # pick a random square based on grid size and start looking
        # for an empty square by going forward from there
        start_square = random.randrange(0, self._height * self._width)
        start_cell = [start_square // self._width, start_square % self._width]
        print start_cell
        # traverse the grid, but don't go beyond the total grid size in the search
        new_location = search_grid(0, self._grid,
                                   start_cell,
                                   self._height, self._width)
        # if a location is found, put the tile in that location
        if (new_location[0] > -1):
            self.set_tile(new_location[0],
                          new_location[1],
                          new_tile_value)
            return True
        # no tile was added
        return False  

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        # put the given value into the specified location
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        # return the value of the specified location
        return self._grid[row][col]


#game = TwentyFortyEight(4, 4)
#
#poc_2048_gui.run_gui(game)

# Test the methods!
#print "Test #0: __init__"
#obj = TwentyFortyEight(4, 4)
#print obj
#
#print "Test #1: set_tile"
#obj.set_tile(0, 0, 2)
#obj.set_tile(0, 1, 4)
#obj.set_tile(0, 2, 8)
#obj.set_tile(0, 3, 16)
#obj.set_tile(1, 0, 16)
#obj.set_tile(1, 1, 8)
#obj.set_tile(1, 2, 4)
#obj.set_tile(1, 3, 2)
#obj.set_tile(2, 0, 0)
#obj.set_tile(2, 1, 0)
#obj.set_tile(2, 2, 8)
#obj.set_tile(2, 3, 16)
#obj.set_tile(3, 0, 0)
#obj.set_tile(3, 1, 0)
#obj.set_tile(3, 2, 4)
#obj.set_tile(3, 3, 2)
#
#print obj
#
## print "Test #2: move(UP)"
#obj.move(UP)
#print obj

#game1.reset()
#print game1
#
#print(" Moving tiles up")
#game1.move(UP)
#print game1
#
#print(" Moving tiles left")
#game1.move(LEFT)
#print game1
#
#print(" Moving tiles down")
#game1.move(DOWN)
#print game1
#
#print(" Moving tiles right")
#game1.move(RIGHT)
#print game1


#poc_test_suite.run_suite(TwentyFortyEight)
