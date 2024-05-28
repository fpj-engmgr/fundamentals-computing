"""
    Solve for the Global Pairwise Alignment Problem
"""


#######################################
#   Helper functions
#
def compute_global_alignment_scores(sequence_x, sequence_y, scoring_matrix):
    """
    Function to compute a global alignment matrix S whose entries S[i, j] are
    the maximum scores over all possible global alignments of the sequences
    X and Y

    Args:
        sequence_x (string): X sequence of nucleotides
        sequence_y (string): Y sequence of nucleotides
        scoring_matrix (matrix): scoring matrix for positional matching of nucleotides
    
    Returns:
        dp_table (matrix): dynamic programming table 
    """
    x_len = len(sequence_x)
    y_len = len(sequence_y)
    #
    dp_table = [['' for _ in range(y_len)] for _ in range(x_len)]
    #
    return dp_table
    
    
# scoring_matrix for ACTG-
scoring_matrix = [[10, 5, 7, 3, -6],
                  [5, 10, 6, 5, -5],
                  [5, 1, 15, 1, -3],
                  [8, 4, 2, 15, -1],
                  [-4, -4, -2, -2, 'N/A']]

seq_x = 'ACCTG-CA'
seq_y = 'CGT-GCTAGTC'

dp_tab = compute_global_alignment_scores(seq_x, seq_y, scoring_matrix)
#
for row_num in range(len(dp_tab)):
    print(dp_tab[row_num])
