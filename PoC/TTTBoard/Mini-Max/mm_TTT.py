"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    # check if this board is done
    board_result = board.check_win()
    print "mm_move : ", player, board_result
    print board
    if board_result != None:
        # is the winner our current player?
        board_score = SCORES[board_result]
        if player == board_result:
            board_score = SCORES[board_result] * SCORES[board_result]
        elif board_result == provided.PLAYERX:
            board_score = -1 * SCORES[board_result]
        # return the result as a win/draw and no more moves
        print "Score : ", board_score, player, board_result
        return board_score, (-1, -1)
    # we don't have a completed game, so find empty squares
    empty_squares_list = board.get_empty_squares()
    print "Empty squares : ", empty_squares_list
    # set best move and step through the list of empty squares
    best_move = (-1, -1)
    #
    for empty_square in empty_squares_list:
        # clone the board
        test_board = board.clone()
        # fill the empty square in the test_board
        test_board.move(empty_square[0], empty_square[1], player)
        #
        print "Player is : ", player
        test_result = mm_move(test_board, provided.switch_player(player))
        # if we get a score of 1 then we have a best move
        print "Square : ", empty_square, " result : ", test_result, player
        if test_result[0] == 1:
            return test_result[0], empty_square
        else:
            best_move = empty_square
        # end of for loop
    # all done and no winning strategy, so return best move
    return 0, best_move

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)

#
# Test code
#
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
#    tst_brd_1 = provided.TTTBoard(3, False)
#    tst_brd_1.move(0, 1, provided.PLAYERX)
#    tst_brd_1.move(1, 0, provided.PLAYERO)
#    tst_brd_1.move(1, 1, provided.PLAYERX)
#    tst_brd_1.move(2, 0, provided.PLAYERO)
#    #
#    result1 = mm_move(tst_brd_1, provided.PLAYERX)
#    #
#    print "Test board 1"
#    print
#    print tst_brd_1
#    print "Result : ", result1
    #
#    tst_brd_2 = provided.TTTBoard(3, False)
#    tst_brd_2.move(0, 0, provided.PLAYERX)
#    tst_brd_2.move(0, 1, provided.PLAYERX)
#    tst_brd_2.move(0, 2, provided.PLAYERO)
#    tst_brd_2.move(1, 1, provided.PLAYERX)
#    tst_brd_2.move(1, 2, provided.PLAYERX)
#    tst_brd_2.move(2, 0, provided.PLAYERO)
#    tst_brd_2.move(2, 2, provided.PLAYERO)
#    #
#    result2 = mm_move(tst_brd_2, provided.PLAYERO)
#    #
#    print
#    print "Test board 2 - PLAYERO"
#    print
#    print tst_brd_2
#    print "Result : ", result2
    #
#    tst_brd_3 = provided.TTTBoard(3, False)
#    tst_brd_3.move(0, 0, provided.PLAYERX)
#    tst_brd_3.move(0, 1, provided.PLAYERX)
#    tst_brd_3.move(0, 2, provided.PLAYERO)
##    tst_brd_3.move(1, 1, provided.PLAYERX)
#    tst_brd_3.move(1, 2, provided.PLAYERX)
#    tst_brd_3.move(2, 0, provided.PLAYERO)
#    tst_brd_3.move(2, 2, provided.PLAYERO)
#    #
#    result3 = mm_move(tst_brd_3, provided.PLAYERX)
#    #
#    print
#    print "Test board 3 - PLAYERX"
#    print
#    print tst_brd_3
#    print "Result : ", result3
    #
    print
    tst_brd_4 = provided.TTTBoard(3, False)
    tst_brd_4.move(0, 0, provided.PLAYERX)
    tst_brd_4.move(0, 1, provided.PLAYERX)
    tst_brd_4.move(0, 2, provided.PLAYERO)
    tst_brd_4.move(1, 1, provided.PLAYERX)
    tst_brd_4.move(1, 2, provided.PLAYERX)
    tst_brd_4.move(2, 0, provided.PLAYERO)
    tst_brd_4.move(2, 2, provided.PLAYERO)
    #
    result4 = mm_move(tst_brd_4, provided.PLAYERO)
    #
    print "Test board 4 - PLAYERO"
    print
    print tst_brd_4
    print "Result : ", result4
    
test_ttt()