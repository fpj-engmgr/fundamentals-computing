def pick_a_number(board):
    # Initialize scores for player 1 and player 2 and save board length
    p1_score = 0
    p2_score = 0
    board_length = len(board)
    #print("debug length : ", board_length, " board : ", board)
    # Base case: if the board is empty, return (0, 0)
    if board_length == 1:
        # Base case: if the board has only one element, return that element
        p1_score = board[0]
    elif board_length == 2:
        # Base case: if the board has two elements, return the larger one
        p1_score = max(board)
    else:
    # board length is 3 or more
    # Recursive case: pick the maximum of two scenarios:
    # Player 1 picks the first element and player 2 picks the optimal number from the rest of the board
        #print("debug board layouts")
        #print("debug board total", board)
        #print("debug P1_FIRST :", board[0], pick_a_number(board[1:]))
        #print("debug P1_LAST  :", board[-1], pick_a_number(board[:-1]))
        p1_score = max(board[0] + min(pick_a_number(board[1:])), 
                       board[-1] + min(pick_a_number(board[:-1])))
        #print("debug p1_score", p1_score)
    # player 2 score is the remainder
    p2_score = sum(board) - p1_score
    #
    #print("debug scores", p1_score, p2_score)
    # Return the scores
    return (p1_score, p2_score)


#######################
# TEST
#######################
board = [12, 9, 7, 3, 4, 7, 4, 7, 3, 16, 4, 8, 12, 1, 2, 7, 11, 6, 3, 9, 7, 1]
#board = [3, 5, 2, 1]

(player1, player2) = pick_a_number(board)

print("\nBoard : ", board)
print("Player 1 score:", player1)
print("Player 2 score:", player2)

board = [9, 7, 3, 4, 7, 4, 7, 3, 16, 4, 8, 12, 1, 2, 7, 11, 6, 3, 9, 7, 1]
#board = [3, 5, 2, 1]

(player1, player2) = pick_a_number(board)

print("\nBoard : ", board)
print("Player 1 score:", player1)
print("Player 2 score:", player2)

board = [7, 3, 4, 7, 4, 7, 3, 16, 4, 8, 12, 1, 2, 7, 11, 6, 3, 9, 7, 1]
#board = [3, 5, 2, 1]

(player1, player2) = pick_a_number(board)

print("\nBoard : ", board)
print("Player 1 score:", player1)
print("Player 2 score:", player2)

board = [9, 7, 3, 4, 6, 4]
#board = [3, 5, 2, 1]

(player1, player2) = pick_a_number(board)

print("\nBoard : ", board)
print("Player 1 score:", player1)
print("Player 2 score:", player2)

board = [3, 5, 2, 1]

(player1, player2) = pick_a_number(board)

print("\nBoard : ", board)
print("Player 1 score:", player1)
print("Player 2 score:", player2)

board = [3, 5, 2]

(player1, player2) = pick_a_number(board)

print("\nBoard : ", board)
print("Player 1 score:", player1)
print("Player 2 score:", player2)

board = [3, 5]

(player1, player2) = pick_a_number(board)

print("\nBoard : ", board)
print("Player 1 score:", player1)
print("Player 2 score:", player2)
