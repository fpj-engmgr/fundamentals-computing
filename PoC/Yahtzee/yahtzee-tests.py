"""
Template testing suite for Yahtzee
"""

import poc_simpletest

# define a list of TEST_CASES
TEST_CASES = [[0, 0, 1, 1, 3, 5, 0],
              [0, 1, 2, 0, 4, 0, 0],
              [0, 0, 0, 4, 3, 5, 0],
              [0, 1, 0, 0, 0, 0, 0],
              [0, 2, 3, 1, 4, 0, 0]]

CHS_MOV_RSLTS = [5,
                 1,
                 5,
                 1]

PLN_MOV_RSLTS = [[5, 1, 2, 1, 4, 1, 3, 1, 2, 1],
                 [1, 2, 1, 4, 1],
                 [5, 1, 4, 1, 2, 1],
                 [1]]

def run_suite(game_class):
    """
    Some informal testing code
    """
    
    # create a TestSuite object
    suite = poc_simpletest.TestSuite()    
    
    # create a game
    game = game_class()
    
    # define a set of boards
    # add tests using suite.run_test(....) here

    # test the initial configuration of the board using the str method
    suite.run_test(str(game), str([0]), "Test #0: init")

    # check the str and get_num_seeds methods  
    game.set_board(TEST_CASES[0])   
    suite.run_test(str(game), str([0, 5, 3, 1, 1, 0, 0]), "Test #1a: str")
    suite.run_test(game.get_num_seeds(1), TEST_CASES[0][1], "Test #1b: get_num_seeds")
    suite.run_test(game.get_num_seeds(3), TEST_CASES[0][3], "Test #1c: get_num_seeds")
    suite.run_test(game.get_num_seeds(5), TEST_CASES[0][5], "Test #1d: get_num_seeds")
    
    # check the choose_move method
    game.reset_board(TEST_CASES[0])
    suite.run_test(game.choose_move(), CHS_MOV_RSLTS[0], "Test #2a: choose_move")
    game.reset_board(TEST_CASES[1])
    suite.run_test(game.choose_move(), CHS_MOV_RSLTS[1], "Test #2b: choose_move")
    
    # plan_moves test
    game.reset_board(TEST_CASES[0])
    suite.run_test(game.plan_moves(), PLN_MOV_RSLTS[0], "Test #3a: plan_moves")
    game.reset_board(TEST_CASES[1])
    suite.run_test(game.plan_moves(), PLN_MOV_RSLTS[1], "Test #3b: plan_moves")
    game.reset_board(TEST_CASES[2])
    suite.run_test(game.plan_moves(), PLN_MOV_RSLTS[2], "Test #3c: plan_moves")
    game.reset_board(TEST_CASES[3])
    suite.run_test(game.plan_moves(), PLN_MOV_RSLTS[3], "Test #3c: plan_moves")
    # report number of tests and failures
    suite.report_results()