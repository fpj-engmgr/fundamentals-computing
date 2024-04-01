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
    # the logic:
    # 1. check if the board is done (i.e. win/loss/draw, so no more moves) and
    #    return result based on SCORES dictionary

    # check if this board is done
    board_result = board.check_win()
    if board_result != None:
        # is the winner our current player?
        board_score = SCORES[board_result]
        # return the result as a win/draw and no more moves
        return board_score, (-1, -1)
    # 2. generate a list of empty squares and initialize best move and score
    empty_squares_list = board.get_empty_squares()
    # set best move and step through the list of empty squares
    best_move = (-1, -1)
    best_score = -1
    # 3. loop through empty squares
    for empty_square in empty_squares_list:
        # 3.1 clone the board
        test_board = board.clone()
        # 3.2 update the board with the first empty square and player
        test_board.move(empty_square[0], empty_square[1], player)
        # 3.3 call mm_move for this board with the next player
        test_result = mm_move(test_board, provided.switch_player(player))
        # 3.4 set min_max for the current player
        min_max = SCORES[player]
        current_score = min_max * test_result[0]
        # 3.5 if the board score is more than the best_score
        if current_score > best_score:
            best_score = current_score
            best_move = empty_square
        # 3.6 if best_score is maxed out, no need to look further
        if best_score == 1:
            break
        # end of for loop
    # all done and no winning strategy, so return best move
    return min_max * best_score, best_move

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
poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)

#
# Test code
#
def test_ttt():
    """
    Testing code for TTT
    """
    #
#    tst_brd_1 = provided.TTTBoard(3, False)
#    tst_brd_1.move(0, 1, provided.PLAYERX)
#    tst_brd_1.move(1, 0, provided.PLAYERO)
#    tst_brd_1.move(1, 1, provided.PLAYERX)
#    tst_brd_1.move(2, 0, provided.PLAYERO)
#    #
#    result1 = mm_move(tst_brd_1, provided.PLAYERX)
#    #
#    print "Test board 1 - PLAYERX"
#    print "- before"
#    print tst_brd_1
#    tst_brd_1.move(result1[1][0], result1[1][1], provided.PLAYERX)
#    print "- after"
#    print tst_brd_1
#    print "Result : ", result1
    #
#    tst_brd_2 = provided.TTTBoard(3, False)
#    tst_brd_2.move(0, 0, provided.PLAYERX)
#    tst_brd_2.move(0, 1, provided.PLAYERX)
#    tst_brd_2.move(0, 2, provided.PLAYERO)
#    tst_brd_2.move(1, 1, provided.PLAYERO)
#    tst_brd_2.move(1, 2, provided.PLAYERX)
#    tst_brd_2.move(2, 0, provided.PLAYERX)
#    tst_brd_2.move(2, 2, provided.PLAYERO)
#    #
#    result2 = mm_move(tst_brd_2, provided.PLAYERO)
#    #
#    print
#    print "Test board 2 - PLAYERO"
#    print "- before"
#    print tst_brd_2
#    tst_brd_2.move(result2[1][0], result2[1][1], provided.PLAYERO)
#    print "- after"
#    print tst_brd_2
#    print "Result : ", result2
#    #
#    tst_brd_3 = provided.TTTBoard(3, False)
#    tst_brd_3.move(0, 0, provided.PLAYERX)
##    tst_brd_3.move(0, 1, provided.PLAYERX)
#    tst_brd_3.move(0, 2, provided.PLAYERO)
#    tst_brd_3.move(1, 0, provided.PLAYERO)
#    tst_brd_3.move(1, 1, provided.PLAYERO)
##    tst_brd_3.move(1, 2, provided.PLAYERX)
#    tst_brd_3.move(2, 0, provided.PLAYERX)
#    tst_brd_3.move(2, 2, provided.PLAYERX)
#    #
#    result3 = mm_move(tst_brd_3, provided.PLAYERX)
#    #
#    print
#    print "Test board 3 - PLAYERX"
#    print "- before"
#    print tst_brd_3
#    tst_brd_3.move(result3[1][0], result3[1][1], provided.PLAYERX)
#    print "- after"
#    print tst_brd_3
#    print "Result : ", result3
#    #
#    print
#    tst_brd_4 = provided.TTTBoard(3, False)
#    tst_brd_4.move(0, 0, provided.PLAYERX)
#    tst_brd_4.move(0, 1, provided.PLAYERX)
#    tst_brd_4.move(0, 2, provided.PLAYERO)
##    tst_brd_4.move(1, 1, provided.PLAYERX)
#    tst_brd_4.move(1, 2, provided.PLAYERX)
#    tst_brd_4.move(2, 0, provided.PLAYERO)
#    tst_brd_4.move(2, 2, provided.PLAYERO)
#    #
#    result4 = mm_move(tst_brd_4, provided.PLAYERX)
#    #
#    print "Test board 4 - PLAYERX"
#    print
#    print tst_brd_4
#    print "Result : ", result4
    #
    tst_brd_5 = provided.TTTBoard(3, False)
    #
    result5 = mm_move(tst_brd_5, provided.PLAYERX)
    #
    tst_brd_5.move(result5[1][0], result5[1][1], provided.PLAYERX)
    #
    print "Test board 5 - PLAYERX"
    print
    print tst_brd_5
    print "Result : ", result5
    #
    #
    tst_brd_6 = tst_brd_5.clone()
    #
    result6 = mm_move(tst_brd_6, provided.PLAYERO)
    #
    tst_brd_6.move(result6[1][0], result6[1][1], provided.PLAYERO)
    #
    print "Test board 6 - PLAYERO"
    print
    print tst_brd_6
    print "Result : ", result6
    #
    tst_brd_7 = tst_brd_6.clone()
    #
    result7 = mm_move(tst_brd_7, provided.PLAYERX)
    #
    tst_brd_7.move(result7[1][0], result7[1][1], provided.PLAYERX)
    #
    print "Test board 7 - PLAYERX"
    print
    print tst_brd_7
    print "Result : ", result7
    #
    tst_brd_8 = tst_brd_7.clone()
    #
    result8 = mm_move(tst_brd_8, provided.PLAYERO)
    #
    tst_brd_8.move(result8[1][0], result8[1][1], provided.PLAYERO)
    #
    print "Test board 8 - PLAYERO"
    print
    print tst_brd_8
    print "Result : ", result8
    #
    tst_brd_9 = tst_brd_8.clone()
    #
    result9 = mm_move(tst_brd_9, provided.PLAYERX)
    #
    tst_brd_9.move(result9[1][0], result9[1][1], provided.PLAYERX)
    #
    print "Test board 8 - PLAYERO"
    print
    print tst_brd_9
    print "Result : ", result9
# test_ttt()