"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for human in self._human_list:
            yield human
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        # get the dimensions of the grid
        height = self.get_grid_height()
        width  = self.get_grid_width()
        # visited is an empty grid
        visited = poc_grid.Grid(height, width)
        # create distance_field and initialize
        distance_field = [[height * width for dummy_idx1 in range(width)]
                          for dummy_idx2 in range(height)]
        # create a queue to traverse
        boundary = poc_queue.Queue()
        # copy the appropriate list into boundary based on the entity_type
        if entity_type == ZOMBIE:
            for zombie in self._zombie_list:
                boundary.enqueue(zombie)
                visited.set_full(zombie[0], zombie[1])
                distance_field[zombie[0]][zombie[1]] = 0
        elif entity_type == HUMAN:
            for human in self._human_list:
                boundary.enqueue(human)
                visited.set_full(human[0], human[1])
                distance_field[human[0]][human[1]] = 0
                
        # start traversing the boundary
        while len(boundary) > 0:
            current_cell = boundary.dequeue()
            # four neighbors works great
            for neighbor_cell in visited.four_neighbors(current_cell[0], current_cell[1]):
                # check for obstacles in the main grid
                if self.is_empty(neighbor_cell[0], neighbor_cell[1]) == False:
                    continue
                if visited.is_empty(neighbor_cell[0], neighbor_cell[1]):
                    visited.set_full(neighbor_cell[0], neighbor_cell[1])
                    boundary.enqueue(neighbor_cell)
                    #
                    distance_field[neighbor_cell[0]][neighbor_cell[1]] = distance_field[current_cell[0]][current_cell[1]] + 1
        # all done
        return distance_field
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        # create a list of new locations
        new_human_list = poc_queue.Queue()
        # step through our queue of zombies
        for human in self._human_list:
            zombie_dist = zombie_distance_field[human[0]][human[1]]
            move_cells = []
            # look at the eight neighbors for the human's location
            for neighbor_cell in poc_grid.Grid.eight_neighbors(self, human[0], human[1]):
                if self.is_empty(neighbor_cell[0], neighbor_cell[1]) == False:
                    continue
                cell_dist = zombie_distance_field[neighbor_cell[0]][neighbor_cell[1]]
                # if we get a new shortest distance make that preferred
                if cell_dist > zombie_dist:
                    zombie_dist = cell_dist
                    move_cells = [neighbor_cell]
                # if it's the same distance add this neighbor for random selection
                elif cell_dist == zombie_dist:
                    move_cells.append(neighbor_cell)
            # let's choose randomly from among potential moves
            if len(move_cells) > 0:
                move_target = random.choice(move_cells)
                new_human_list.enqueue(move_target)
        # update the human list now that we're done
        if len(new_human_list) > 0:
            self._human_list = []
            #
            for dummy_idx in range(len(new_human_list)):
                self._human_list.append(new_human_list.dequeue())
        # that's all there is to it
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        # create a list of new locations
        new_zombie_list = poc_queue.Queue()
        # step through our queue of zombies
        for zombie in self._zombie_list:
            human_dist = human_distance_field[zombie[0]][zombie[1]]
            move_cells = []
            # look at the four neighbors for the zombie's location
            for neighbor_cell in poc_grid.Grid.four_neighbors(self, zombie[0], zombie[1]):
                if self.is_empty(neighbor_cell[0], neighbor_cell[1]) == False:
                    continue
                cell_dist = human_distance_field[neighbor_cell[0]][neighbor_cell[1]]
                # if we get a new shortest distance make that preferred
                if cell_dist < human_dist:
                    human_dist = cell_dist
                    move_cells = [neighbor_cell]
                # if it's the same distance add this neighbor for random selection
                elif cell_dist == human_dist:
                    move_cells.append(neighbor_cell)
            # let's choose randomly from among potential moves
            if len(move_cells) > 0:
                move_target = random.choice(move_cells)
                new_zombie_list.enqueue(move_target)
        # update the zombie list now that we're done
        if len(new_zombie_list) > 0:
            self._zombie_list = []
            #
            for dummy_idx in range(len(new_zombie_list)):
                self._zombie_list.append(new_zombie_list.dequeue())
        # that's all there is to it

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

# poc_zombie_gui.run_gui(Apocalypse(30, 40))
# test code
#obj = Apocalypse(3, 3, [], [], [(2, 2)])
#hum_dst_field = obj.compute_distance_field(HUMAN)
#print hum_dst_field[0]
#print hum_dst_field[1]
#print hum_dst_field[2]

#obj = Apocalypse(3, 3, [], [(1, 1)], [(1, 1)])
#hum_dst_field = obj.compute_distance_field(HUMAN)
#print hum_dst_field[0]
#print hum_dst_field[1]
#print hum_dst_field[2]
#dist = [[2, 1, 2], [1, 0, 1], [2, 1, 2]]
#obj.move_zombies(dist)
#for zombie in obj.zombies():
#    print zombie

# ZOMBIE init
#obstacles = [(2, 7), (3, 7), (5, 6)]
#HEIGHT = 8
#WIDTH = 10
#mini_clip = Apocalypse(HEIGHT, WIDTH, obstacles)
#print mini_clip
#mini_clip.add_zombie(6, 6)
#mini_clip.add_zombie(3, 2)
#print "Num zombies : ", mini_clip.num_zombies()
#for zombie in mini_clip.zombies():
#    print "Z : ", zombie
#zombie_dist_fld = mini_clip.compute_distance_field(ZOMBIE)
#for idx in range(HEIGHT):
#    print zombie_dist_fld[idx]
## HUMAN init
#mini_clip.add_human(1, 0)
#mini_clip.add_human(2, 3)
#print "Num humans : ", mini_clip.num_humans()
#for human in mini_clip.humans():
#    print "H start: ", human
#human_dist_fld = mini_clip.compute_distance_field(HUMAN)
#for idx in range(HEIGHT):
#    print human_dist_fld[idx]
## select a number of moves to execute
#NUM_MOVES = 12
#for idx in range(NUM_MOVES):
#    # move the zombies and see where they appear
#    mini_clip.move_zombies(human_dist_fld)
#    # see where they are now
#    print "Num zombies : ", mini_clip.num_zombies()
#    for zombie in mini_clip.zombies():
#        print "Z #", idx, zombie
#    # create a new distance field
#    zombie_dist_fld = mini_clip.compute_distance_field(ZOMBIE)
#    for idx in range(HEIGHT): 
#        print zombie_dist_fld[idx]
#    # move the humans and see how they flee!
#    mini_clip.move_humans(zombie_dist_fld)
#    print "Num humans : ", mini_clip.num_humans()
#    for human in mini_clip.humans():
#        print "H # ", idx, human
#    human_dist_fld = mini_clip.compute_distance_field(HUMAN)
#    for idx in range(HEIGHT):
#        print human_dist_fld[idx]
#
#        
#humans = [(12, 15), (10, 17)]
#zombies = [(3, 17), (11, 13)]
#obstacles = [(9, 11), (9, 12), (9, 13), (11,17), (12, 17), (13, 17), (14, 17)]
#
#apocalyptica = Apocalypse(15, 25, obstacles, zombies, humans)
#print apocalyptica
#print "Number of zombies : ", apocalyptica.num_zombies()
#print "Number of humans  : ", apocalyptica.num_humans()
#for zombie in apocalyptica.zombies():
#    print "Z : ", zombie
#for human in apocalyptica.humans():
#    print "H : ", human
#apocalyptica.add_zombie(7, 7)
#apocalyptica.add_human(13, 2)
#print "Number of zombies : ", apocalyptica.num_zombies()
#print "Number of humans  : ", apocalyptica.num_humans()
#for zombie in apocalyptica.zombies():
#    print "Z : ", zombie
#for human in apocalyptica.humans():
#    print "H : ", human
#print "Clearing..."
#apocalyptica.clear()
#print apocalyptica
#print "Number of zombies : ", apocalyptica.num_zombies()
#print "Number of humans  : ", apocalyptica.num_humans()

