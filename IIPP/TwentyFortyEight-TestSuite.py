"""
Testing suite for TwentyFortyEight
"""

import poc_simpletest

def run_suite(game_class):
    """
    Some informal testing code
    """
    
    # create a TestSuite object
    suite = poc_simpletest.TestSuite()    
    
    # create a grid of 4 rows and 5 columns
    game = game_class(4, 5)
    
    # add tests using suite.run_test(....) here

    # test the initial configuration of the board using the str method
    suite.run_test(str(game), "[[0, 0, 0, 0, 0][0, 0, 0, 0, 0][0, 0, 0, 0, 0][0, 0, 0, 0, 0]]", "Test #0: init")

    # test basic methods for the class
    suite.run_test(game.get_grid_height(), 4, "Test #1: get_grid_height")
    suite.run_test(game.get_grid_width(), 5, "Test #2: get_grid_width")
    
    # set a tile value and check it afterwards
    suite.run_test(game.set_tile(2, 3, 8), None, "Test #3: set_tile")
    suite.run_test(game.get_tile(2, 3), 8, "Test #4: get_tile")
    # check the str and get_num_seeds methods
    
    # report number of tests and failures
    suite.report_results()
