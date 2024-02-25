"""
Student facing implement of solitaire version of Mancala - Tchoukaillon

Goal: Move as many seeds from given houses into the store

In GUI, you make ask computer AI to make move or click to attempt a legal move
"""


class SolitaireMancala:
    """
    Simple class that implements Solitaire Mancala
    """
    
    def __init__(self):
        """
        Create Mancala game with empty store and no houses
        """
        self.houses = [0]
    
    def set_board(self, configuration):
        """
        Take the list configuration of initial number of seeds for given houses
        house zero corresponds to the store and is on right
        houses are number in ascending order from right to left
        """
        for house_num in range(6):
            self.houses.append(configuration[house_num + 1])
    
    def __str__(self):
        """
        Return string representation for Mancala board
        """
        house_string = "["
        for idx in range(len(self.houses) - 1, -1, -1):
            if idx == (len(self.houses) -1):
                house_string = house_string + str(self.houses[idx])
            else:
                house_string = house_string + ", " + str(self.houses[idx])
                                          
        return house_string + "]"
    
    def get_num_seeds(self, house_num):
        """
        Return the number of seeds in given house on board
        """
        return self.houses[house_num]

    def is_game_won(self):
        """
        Check to see if all houses but house zero are empty
        """
        for house_num in range(1, len(self.houses)):
            if self.houses[house_num] <> 0:
                return False

        return True
    
    def is_legal_move(self, house_num):
        """
        Check whether a given move is legal
        """
        if self.houses[house_num] > house_num:
            return False
        return True

    
    def apply_move(self, house_num):
        """
        Move all of the stones from house to lower/left houses
        Last seed must be played in the store (house zero)
        """
        seeds = self.houses[house_num]
        self.houses[house_num] = 0
        for house_idx in range(seeds - 1, -1, -1):
            self.houses[house_idx] += 1
#            print "Index: ", str(house_idx)

    def choose_move(self):
        """
        Return the house for the next shortest legal move
        Shortest means legal move from house closest to store
        Note that using a longer legal move would make smaller illegal
        If no legal move, return house zero
        """
        for house_num in range(1, len(self.houses)):
            if self.houses[house_num] == house_num:
                return house_num
        return 0
    
    def plan_moves(self):
        """
        Return a sequence (list) of legal moves based on the following heuristic: 
        After each move, move the seeds in the house closest to the store 
        when given a choice of legal moves
        Not used in GUI version, only for machine testing
        """
        move_list = []
#        print move_list
#        house_num = self.choose_move()
#        print "House num :", str(house_num)
#        print self.houses
#        if house_num > 0:
#            self.apply_move(house_num)
#        print self.houses
#        move_list.append(house_num)
#        print self.is_game_won()
        while True:
            if self.is_game_won():
                print "We've won!"
                break
            # check if there is a move
            house_num = self.choose_move()
            if house_num > 0:
                self.apply_move(house_num)
                move_list.append(house_num)
            else:
                return move_list
        return move_list
 

# Create tests to check the correctness of your code

def test_mancala():
    """
    Test code for Solitaire Mancala
    """
    
    my_game = SolitaireMancala()
    print "Testing init - Computed:", my_game, "Expected: [0]"
    
    config1 = [0, 0, 1, 1, 3, 5, 0]    
    my_game.set_board(config1)   
    
    print "Testing set_board - Computed:", str(my_game), "Expected:", str([0, 5, 3, 1, 1, 0, 0])
    print "Testing get_num_seeds - Computed:", my_game.get_num_seeds(1), "Expected:", config1[1]
    print "Testing get_num_seeds - Computed:", my_game.get_num_seeds(3), "Expected:", config1[3]
    print "Testing get_num_seeds - Computed:", my_game.get_num_seeds(5), "Expected:", config1[5]

    # add more tests here
    print "Testing a move plan - ", str(my_game.plan_moves())
    print "The ending board is ", str(my_game)
    print "Has the game been won? ", str(my_game.is_game_won())
    
test_mancala()


# Import GUI code once you feel your code is correct
# import poc_mancala_gui
# poc_mancala_gui.run_gui(SolitaireMancala())
