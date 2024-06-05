"""
Application to find global and local alignment in genomic sequences

"""

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """
    Function to build a scoring matrix for a given alphabet of bases

    Args:
        alphabet (set of char): string of bases
        diag_score (int): Score for matching (diagonal) bases
        off_diag_score (int): non-matching base score
        dash_score (int): matching base to dash score
    Return:
        scoring_matrix (dict of dict): Scoring matrix
    """
    # create the outer dict
    scoring_matrix = {}
    # add a '-' to the alphabet for building
    all_chars = set([])
    #
    for base_char in alphabet:
        all_chars.add(base_char)
    #
    all_chars.add('-')
    # loop through all_chars
    for row_char in all_chars:
        # initialize the inner dict
        inner_dict = {}
        for col_char in all_chars:
            # build the inner_dict
            if col_char == row_char:
                # match, so diag_score
                if col_char == '-':
                    inner_dict[col_char] = dash_score
                else:
                    inner_dict[col_char] = diag_score
            elif col_char != row_char:
                # no match, so...
                if (row_char == '-') or (col_char == '-'):
                    # dash in either, so dash_score
                    inner_dict[col_char] = dash_score
                else:
                    # off_diag_score
                    inner_dict[col_char] = off_diag_score
        # we've build inner_dict, so put it in scoring_matrix
        scoring_matrix[row_char] = inner_dict
    # all done
    return scoring_matrix

def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """
    Function to compute either a local or global alignment matrix for 2 given sequences

    Args:
        seq_x (string): sequence X
        seq_y (string): sequence Y
        scoring_matrix (dict of dicts): scoring matrix for alignment evaluation
        global_flag (bool): True: compute global False: compute local
    Return:
        dp_table (matrix): global/local alignment matrix
    """
    seq_x_len = len(seq_x) + 1
    seq_y_len = len(seq_y) + 1
    # initalize the table
    dp_table = [['' for _ in range(seq_y_len)] for _ in range(seq_x_len)]
    dp_table[0][0] = 0
    # take care of the matrix edges first
    for idx in range(1, seq_x_len):
        if global_flag:
            dp_table[idx][0] = dp_table[idx - 1][0] + scoring_matrix[seq_x[idx - 1]]['-']
        else:
            dp_table[idx][0] = max(dp_table[idx - 1][0] + scoring_matrix[seq_x[idx - 1]]['-'], 0)
    #
    for idx in range(1, seq_y_len):
        if global_flag:
            dp_table[0][idx] = dp_table[0][idx - 1] + scoring_matrix['-'][seq_y[idx - 1]]
        else:
            dp_table[0][idx] = max(dp_table[0][idx - 1] + scoring_matrix['-'][seq_y[idx - 1]], 0)
    #
    for idx_i in range(1, seq_x_len):
        for idx_j in range(1, seq_y_len):
            if global_flag:
                dp_table[idx_i][idx_j] = max(dp_table[idx_i - 1][idx_j - 1] + scoring_matrix[seq_x[idx_i - 1]][seq_y[idx_j - 1]],
                                             dp_table[idx_i - 1][idx_j] + scoring_matrix[seq_x[idx_i - 1]]['-'],
                                             dp_table[idx_i][idx_j - 1] + scoring_matrix['-'][seq_y[idx_j - 1]])
            else:
                dp_table[idx_i][idx_j] = max(dp_table[idx_i - 1][idx_j - 1] + scoring_matrix[seq_x[idx_i - 1]][seq_y[idx_j - 1]],
                                             dp_table[idx_i - 1][idx_j] + scoring_matrix[seq_x[idx_i - 1]]['-'],
                                             dp_table[idx_i][idx_j - 1] + scoring_matrix['-'][seq_y[idx_j - 1]],
                                             0)
    #
    return dp_table

###################################
# quick test
#
# detailed tests
#
print("Test 0 : build_scoring_matrix")
scm0 = build_scoring_matrix(set(['A', 'C', 'T', 'G']), 6, 2, -4)
#
for row in scm0:
    print(row, ":", scm0[row])
#
print("Test 1 : compute_alignment_matrix (global)")
scm1 =  {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2},
         'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, 
         '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4},
         'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 
         'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}
dpt1 = compute_alignment_matrix('ATG', 'ACG', scm1, True)
#
for row_num in range(len(dpt1)):
    print(row_num, ":", dpt1[row_num])
#
print("Test 2 : compute_alignment_matrix (local)")
scm2 =  {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2},
         'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, 
         '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4},
         'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 
         'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}
dpt2 = compute_alignment_matrix('ATG', 'ACG', scm2, False)
#
for row_num in range(len(dpt2)):
    print(row_num, ":", dpt2[row_num])
    