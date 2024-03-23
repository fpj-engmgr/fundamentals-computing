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
        elif entity_type == HUMAN:
            for human in self._human_list:
                boundary.enqueue(human)
        else:
            print "Bad entity type...must be HUMAN or ZOMBIE!"
            return None
        # traverse the queue and populate visited and distance_field
        for entity in boundary:
            visited.set_full(entity[0], entity[1])
            distance_field[entity[0]][entity[1]] = 0
        #
        print visited
        #
        while len(boundary) > 0:
            current_cell = boundary.dequeue()
            # Zombies cannot travel diagonally, so four neighbors only
            if entity_type == ZOMBIE:
                for neighbor_cell in visited.four_neighbors(current_cell[0], current_cell[1]):
                    if visited.is_empty(neighbor_cell[0], neighbor_cell[1]):
                        visited.set_full(neighbor_cell[0], neighbor_cell[1])
                        boundary.enqueue(neighbor_cell)
                        #
                        distance_field[neighbor_cell[0]][neighbor_cell[1]] = distance_field[current_cell[0]][current_cell[1]] + 1
            # Humans can move diagonally, so eight neighbors to visit
            elif entity_type == HUMAN: 
                for neighbor_cell in visited.eight_neighbors(current_cell[0], current_cell[1]):
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
        pass
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        pass

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

# poc_zombie_gui.run_gui(Apocalypse(30, 40))

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
# ZOMBIE test
mini_clip = Apocalypse(4, 6)
print mini_clip
mini_clip.add_zombie(1, 5)
mini_clip.add_zombie(3, 2)
print "Num zombies : ", mini_clip.num_zombies()
for zombie in mini_clip.zombies():
    print "Z : ", zombie
zombie_dist_fld = mini_clip.compute_distance_field(ZOMBIE)
print zombie_dist_fld[0]
print zombie_dist_fld[1]
print zombie_dist_fld[2]
print zombie_dist_fld[3]
# HUMAN test
mini_clip.add_human(1, 0)
mini_clip.add_human(2, 3)
print "Num humans : ", mini_clip.num_humans()
for human in mini_clip.humans():
    print "H : ", human
human_dist_fld = mini_clip.compute_distance_field(HUMAN)
print human_dist_fld[0]
print human_dist_fld[1]
print human_dist_fld[2]
print human_dist_fld[3]


