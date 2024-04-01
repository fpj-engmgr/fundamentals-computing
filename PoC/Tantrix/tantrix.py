"""
Student facing code for Tantrix Solitaire
http://www.jaapsch.net/puzzles/tantrix.htm

Game is played on a grid of hexagonal tiles.
All ten tiles for Tantrix Solitaire and place in a corner of the grid.
Click on a tile to rotate it.  Cick and drag to move a tile.

Goal is to position the 10 provided tiles to form
a yellow, red or  blue loop of length 10
"""



# Core modeling idea - a triangular grid of hexagonal tiles are 
# model by integer tuples of the form (i, j, k) 
# where i + j + k == size and i, j, k >= 0.

# Each hexagon has a neighbor in one of six directions
# These directions are modeled by the differences between the 
# tuples of these adjacent tiles

# Numbered directions for hexagonal grid, ordered clockwise at 60 degree intervals
DIRECTIONS = {0 : (-1, 0, 1), 1 : (-1, 1, 0), 2 : (0, 1, -1), 
              3 : (1, 0, -1), 4 : (1, -1, 0), 5 : (0,  -1, 1)}

def reverse_direction(direction):
    """
    Helper function that returns opposite direction on hexagonal grid
    """
    num_directions = len(DIRECTIONS)
    return (direction + num_directions / 2) % num_directions



# Color codes for ten tiles in Tantrix Solitaire
# "B" denotes "Blue", "R" denotes "Red", "Y" denotes "Yellow"
SOLITAIRE_CODES = ["BBRRYY", "BBRYYR", "BBYRRY", "BRYBYR", "RBYRYB",
                "YBRYRB", "BBRYRY", "BBYRYR", "YYBRBR", "YYRBRB"]


# Minimal size of grid to allow placement of 10 tiles
MINIMAL_GRID_SIZE = 4



class Tantrix:
    """
    Basic Tantrix game class
    """
    
    def __init__(self, size):
        """
        Create a triangular grid of hexagons with size + 1 tiles on each side.
        """
        assert size >= MINIMAL_GRID_SIZE
        pass

        # Initialize dictionary tile_value to contain codes for ten
        # tiles in Solitaire Tantrix in one 4x4 corner of grid
        pass

    def __str__(self):
        """
        Return string of dictionary of tile positions and values
        """
        return ""
        
    def get_tiling_size(self):
        """
        Return size of board for GUI
        """
        return 0
    
    def tile_exists(self, index):
        """
        Return whether a tile with given index exists
        """
        return False
    
    def place_tile(self, index, code):
        """
        Play a tile with code at cell with given index
        """
        pass       

    def remove_tile(self, index):
        """
        Remove a tile at cell with given index
        and return the code value for that tile        """
        pass
               
    def rotate_tile(self, index):
        """
        Rotate a tile clockwise at cell with given index
        """
        pass

    def get_code(self, index):
        """
        Return the code of the tile at cell with given index
        """
        return self._tile_value[index]

    def get_neighbor(self, index, direction):
        """
        Return the index of the tile neighboring the tile with given index in given direction
        """
        return ()

    def is_legal(self):
        """
        Check whether a tile configuration obeys color matching rules for adjacent tiles
        """
        return False
            
    def has_loop(self, color):
        """
        Check whether a tile configuration has a loop of size 10 of given color
        """
        return False

    
# run GUI for Tantrix
import poc_tantrix_gui
poc_tantrix_gui.TantrixGUI(Tantrix(6))