"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

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

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # create a list of lists of height rows and width columns
        self._height = grid_height
        self._width = grid_width
        # set all entries in the grid to zero first
        self._grid = [[0 for dummy_col in range(grid_width)] 
                         for dummy_row in range(grid_height)]

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        # replace with your code
        pass

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # create a string to give a list of lists
        print_string = "["
        
        for row in range(self._height):
            print_string = print_string + "["
            for col in range(self._width):
                if col = 0:
                    print_string = print_string + str(self._grid[row][col])
                else:
                    print_string = print_string + ", " + str(self._grid[row][col])
            print_string = print_string + "]"
            
        print_string = print_string +"]"
        
        return print_string

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code
        return 0

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return 0

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # replace with your code
        pass

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # replace with your code
        pass

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        # replace with your code
        pass

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        # replace with your code
        return 0


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
