"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 1         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.
def mc_trial(board, player):
    """
    Function to play a game starting with the board given, alternating between
    playerX and playerO. Random moves are made and the function finishes when
    the game is over. The board will be updated, as the function has no return.
    """
    
def mc_update_scores(scores, board, player):
    """
    Take a grid of scores and a completed board and update the scores based on
    the outcome of the game.
    """

def get_best_move(board, scores):
    """
    Function that looks at all the empty squares and returns a tuple (row, column)
    indicating the square that has the highest chance of a winning move.
    """
    
def mc_move(board, player, trials):
    """
    Given the current board and machine player, run Monte Carlo simulation using
    trials count and returns the best move to be found.
    """
    

# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

provided.play_game(mc_move, NTRIALS, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)

