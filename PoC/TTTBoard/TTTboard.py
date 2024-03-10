"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 10         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player

#

# Add your functions here.
def mc_trial(board, player):
    """
    Function to play a game starting with the board given, alternating between
    playerX and playerO. Random moves are made and the function finishes when
    the game is over. The board will be updated, as the function has no return.
    """
    # set the current_player to player, so that we don't change player
    current_player = player
    # set the winner to None
    winner = None
    # start the moves
    while winner == None:
        # get the list of empty squares
        empty_squares = board.get_empty_squares()
        # generate a random integer based on the length of empty_squares
        next_move = empty_squares[random.randrange(0, len(empty_squares))]
        # move current_player into this square
        board.move(next_move[0], next_move[1], current_player)
        # check to see if game is done
        winner = board.check_win()
        # switch players
        current_player = provided.switch_player(current_player)
    # that's all there is to this
    
def mc_update_scores(scores, board, player):
    """
    Take a grid of scores and a completed board and update the scores based on
    the outcome of the game.
    """
    # check to see who won the game
    winner = board.check_win()
    # if we get None (game still in progress) or DRAW, there's no update
    if (winner == None) or (winner == provided.DRAW):
        return
    # if the winner is the current player
    if winner == player:
        current_score = SCORE_CURRENT
        other_score = -SCORE_OTHER
    else:
        current_score = -SCORE_CURRENT
        other_score = SCORE_OTHER
    # check to see who the other player is (switch_player function)
    other_player = provided.switch_player(player)
    # now traverse the board and scores grids
    dim = board.get_dim()
    for row in range(dim):
        for col in range(dim):
            if board.square(row, col) == player:
                scores[row][col] += current_score
            elif board.square(row, col) == other_player:
                scores[row][col] += other_score
    # all done

def get_best_move(board, scores):
    """
    Function that looks at all the empty squares and returns a tuple (row, column)
    indicating the square that has the highest chance of a winning move.
    """
    # get the list of empty squares for the current board
    empty_squares = board.get_empty_squares()
    # initialize a best_move, just in case
    best_move = empty_squares[0]
    # set the baseline for score below a draw
    high_score = scores[best_move[0]][best_move[1]]
    # step through all squares in the empty squares list
    for square_coord in empty_squares:
        # check the score at this location
        if scores[square_coord[0]][square_coord[1]] > high_score:
            high_score = scores[square_coord[0]][square_coord[1]]
            best_move = square_coord
    # all done, so return the best move
    return best_move

def mc_move(board, player, trials):
    """
    Given the current board and machine player, run Monte Carlo simulation using
    trials count and returns the best move to be found.
    """
    # initialize the scores list
    dim = board.get_dim()
    #
    scores = [[0 for dummycol in range(dim)]
              for dummyrow in range(dim)]
    #
    for dummyidx in range(trials):
        # clone the board before the trial run(s)
        trial_board = board.clone()
        # run a trial game
        mc_trial(trial_board, player)
        # update the score based on the trial board
        mc_update_scores(scores, trial_board, player)
    # all trials are complete, so get the best move and return it
    return (get_best_move(board, scores))

# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

# provided.play_game(mc_move, NTRIALS, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)

def test_ttt():
    """
    Testing code for TTT
    """
    # start with an empty 3x3 board
#    my_board = provided.TTTBoard(3, False)
#    # populate a couple of squares
#    my_board.move(1, 1, provided.PLAYERX)
#    my_board.move(0, 0, provided.PLAYERO)
#    my_board.move(0, 2, provided.PLAYERO)
#    # clone the board for later use
#    myclone = my_board.clone()
#    # print the board
#    print my_board
#    # run mc_trial on this board
#    mc_trial(my_board, provided.PLAYERX)
#    # print the board
#    print my_board
#    # check the state and print it
#    print my_board.check_win()
#    #
#    # next build a scores list
#    my_scores = [[0 for dummycol in range(3)]
#                for dummyrow in range(3)]
#    print "Scores:"
#    print my_scores
#    # update the scores
#    mc_update_scores(my_scores, my_board, provided.PLAYERO)
#    #
#    print my_scores
#    # get the best move
#    my_best_move = get_best_move(myclone, my_scores)
#    #
#    print my_best_move
#    #
#    print mc_move(myclone, provided.PLAYERO, 20)
#    # debug time
#    print "Debug time"
#    new_board = provided.TTTBoard(2, False)
#    print new_board
#    test_scores = [[0, 0],[3, 0]]
#    print get_best_move(new_board, test_scores)
    #
    # another get_best_move test
    #
    tst_brd_1 = provided.TTTBoard(3, False)
    tst_brd_1.move(0, 1, provided.PLAYERX)
    tst_brd_1.move(1, 0, provided.PLAYERO)
    tst_brd_1.move(1, 1, provided.PLAYERX)
    tst_brd_1.move(2, 0, provided.PLAYERO)
    #
    tst_scr_1 = [[-3, 6, -2], [8, 0, -3], [3, -2, -4]]
    print "get_best_move:"
    print get_best_move(tst_brd_1, tst_scr_1)
    print tst_brd_1
    print tst_scr_1
    #
    tst_brd_2 = provided.TTTBoard(3, False)
    tst_brd_2.move(0, 0, provided.PLAYERX)
    tst_brd_2.move(0, 1, provided.PLAYERX)
    tst_brd_2.move(0, 2, provided.PLAYERO)
    tst_brd_2.move(1, 1, provided.PLAYERX)
    tst_brd_2.move(1, 2, provided.PLAYERX)
    tst_brd_2.move(2, 0, provided.PLAYERO)
    tst_brd_2.move(2, 2, provided.PLAYERO)
    #
    print tst_brd_2
    print mc_move(tst_brd_2, provided.PLAYERO, NTRIALS)
             
#test_ttt()