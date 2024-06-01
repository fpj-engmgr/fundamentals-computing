"""
    Solve for the Global Pairwise Alignment Problem
"""
###################################
#   Constants
#
# DNA letter assignments in scoring matrix
#
DNA_MAP = {'A': 0,
           'C': 1,
           'G': 2,
           'T': 3,
           '-': 4}
DASH_VAL = 4
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
    x_len = len(sequence_x) + 1
    y_len = len(sequence_y) + 1
    #
    dp_table = [['' for _ in range(y_len)] for _ in range(x_len)]
    #
    dp_table[0][0] = 0
    #
    for idx in range(1, x_len):
        dp_table[idx][0] = dp_table[idx - 1][0] + scoring_matrix[DNA_MAP[sequence_x[idx - 1]]][DASH_VAL]
    #
    for idx in range(1, y_len):
        dp_table[0][idx] = dp_table[0][idx - 1] + scoring_matrix[DASH_VAL][DNA_MAP[sequence_y[idx - 1]]]
    #
    for idx_i in range(1, x_len):
        for idx_j in range(1, y_len):
            idx_x = DNA_MAP[sequence_x[idx_i - 1]]
            idx_y = DNA_MAP[sequence_y[idx_j - 1]]
            dp_table[idx_i][idx_j] = max((dp_table[idx_i - 1][idx_j - 1] + scoring_matrix[idx_x][idx_y]),
                                         dp_table[idx_i - 1][idx_j],
                                         dp_table[idx_i][idx_j - 1])
    #
    return dp_table

def compute_local_alignment_scores(sequence_x, sequence_y, scoring_matrix):
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
    x_len = len(sequence_x) + 1
    y_len = len(sequence_y) + 1
    #
    dp_table = [['' for _ in range(y_len)] for _ in range(x_len)]
    #
    dp_table[0][0] = 0
    #
    for idx in range(1, x_len):
        dp_table[idx][0] = max(scoring_matrix[DNA_MAP[sequence_x[idx - 1]]][DASH_VAL], 0)
    #
    for idx in range(1, y_len):
        dp_table[0][idx] = max(scoring_matrix[DASH_VAL][DNA_MAP[sequence_y[idx - 1]]], 0)
    #
    for idx_i in range(1, x_len):
        for idx_j in range(1, y_len):
            idx_x = DNA_MAP[sequence_x[idx_i - 1]]
            idx_y = DNA_MAP[sequence_y[idx_j - 1]]
            dp_table[idx_i][idx_j] = max((dp_table[idx_i - 1][idx_j - 1] + scoring_matrix[idx_x][idx_y]),
                                         dp_table[idx_i - 1][idx_j],
                                         dp_table[idx_i][idx_j - 1],
                                         0)
    #
    return dp_table


def compute_alignment(sequence_x, sequence_y, scoring_matrix, dp_table):
    """
    Function to compute and return a global pairwise alignment

    Args:
        sequence_x (string): X sequence of nucleotides
        sequence_y (string): Y sequence of nucleotides
        scoring_matrix (matrix): scoring matrix for positional matching of nucleotides
        dp_table (matrix): dynamic programming table
    Returns:
        gpsa (string): global pairwise alignment of sequences X and Y
    """
    x_len = len(sequence_x)
    y_len = len(sequence_y)
    #
    x_align = ''
    y_align = ''
    #
    while (x_len > 0) and (y_len > 0):
        idx_x = DNA_MAP[sequence_x[x_len - 1]]
        idx_y = DNA_MAP[sequence_y[y_len - 1]]
        if dp_table[x_len][y_len] == dp_table[x_len - 1][y_len - 1] + scoring_matrix[idx_x][idx_y]:
            x_align = sequence_x[x_len - 1] + x_align
            y_align = sequence_y[y_len - 1] + y_align
            x_len -= 1
            y_len -= 1
        else:
            if dp_table[x_len][y_len] == dp_table[x_len - 1][y_len] + scoring_matrix[idx_x][DASH_VAL]:
                x_align = sequence_x[x_len - 1] + x_align
                y_align = '-' + y_align
                x_len -= 1
            else:
                x_align = '-' + x_align
                y_align = sequence_y[y_len - 1] + y_align
                y_len -= 1
    #
    return (x_align, y_align)
#
def compute_local_alignment(sequence_x, sequence_y, scoring_matrix, dp_table, max_tuple):
    """
    Function to compute and return a global pairwise alignment

    Args:
        sequence_x (string): X sequence of nucleotides
        sequence_y (string): Y sequence of nucleotides
        scoring_matrix (matrix): scoring matrix for positional matching of nucleotides
        dp_table (matrix): dynamic programming table
    Returns:
        gpsa (string): global pairwise alignment of sequences X and Y
    """
    x_len = max_tuple[0]
    y_len = max_tuple[1]
    #
    x_align = ''
    y_align = ''
    #
    while (x_len > 0) and (y_len > 0):
        idx_x = DNA_MAP[sequence_x[x_len - 1]]
        idx_y = DNA_MAP[sequence_y[y_len - 1]]
        print("local : ", x_len, y_len)
        print("local : ", x_align, y_align)
        if dp_table[x_len][y_len] == dp_table[x_len - 1][y_len - 1] + scoring_matrix[idx_x][idx_y]:
            x_align = sequence_x[x_len - 1] + x_align
            y_align = sequence_y[y_len - 1] + y_align
            x_len -= 1
            y_len -= 1
        else:
            if dp_table[x_len][y_len] == dp_table[x_len - 1][y_len] + scoring_matrix[idx_x][DASH_VAL]:
                x_align = sequence_x[x_len - 1] + x_align
                y_align = '-' + y_align
                x_len -= 1
            else:
                x_align = '-' + x_align
                y_align = sequence_y[y_len - 1] + y_align
                y_len -= 1
    #
    print("local : ", x_len, y_len)
    print("local : ", x_align, y_align)
    return (x_align, y_align)
     
##########################
#   Start testing here
#
# scoring_matrix for ACGT-
scoring_matrix = [[10, 4, 4, 4, -4],
                  [4, 10, 6, 4, -4],
                  [4, 4, 10, 4, -4],
                  [4, 4, 4, 10, -4],
                  [-4, -4, -4, -4, 0]]

seq_x = 'ACCTG-CA-C'
seq_y = 'CGTGCTAGTC'

dp_tab = compute_global_alignment_scores(seq_x, seq_y, scoring_matrix)
#
for row_num in range(len(dp_tab)):
    print(dp_tab[row_num])
    
(x_prime, y_prime) = compute_alignment(seq_x, seq_y, scoring_matrix, dp_tab)

print("X-prime : ", x_prime)
print("Y-prime : ", y_prime)

seq_a = 'AA'
seq_b = 'TAAT'
scoring_metric = [[10, 4, 4, 4, -6],
                  [4, 10, 6, 4, -6],
                  [4, 4, 10, 4, -6],
                  [4, 4, 4, 10, -6],
                  [-6, -6, -6, -6, 10]]

ab_table = compute_local_alignment_scores(seq_a, seq_b, scoring_metric)
#
for row_num in range(len(ab_table)):
    print(ab_table[row_num])
#
print("S[0, 2] : ", ab_table[0][2])
print("S[2, 0] : ", ab_table[2][0])
print("S[2, 2] : ", ab_table[2][2])

(a_prime, b_prime) = compute_local_alignment(seq_a, seq_b, scoring_metric, ab_table, (2, 3))

print("A-prime : ", a_prime)
print("B-prime : ", b_prime)

(c_prime, d_prime) = compute_alignment(seq_a, seq_b, scoring_metric, ab_table)
#
print("A-prime : ", c_prime)
print("B-prime : ", d_prime)