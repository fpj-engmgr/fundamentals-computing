"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
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

# test code
line1 = [2, 0, 2, 2]
merge1 = merge(line1)
print line1, merge1

line2 = [2, 0, 2, 4]
merge2 = merge(line2)
print line2, merge2

line3 = [2, 0, 2, 2, 4, 0, 4, 8, 0]
merge3 = merge(line3)
print line3, merge3