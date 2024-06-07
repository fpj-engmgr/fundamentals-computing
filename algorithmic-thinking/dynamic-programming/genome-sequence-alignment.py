"""
Application to find global and local alignment in genomic sequences

"""
import math
import random
#
import matplotlib.pyplot as plt
import numpy as np
#
FILE_DIR = "/Users/fpj/Development/python/fundamentals-computing/algorithmic-thinking/dynamic-programming/data/"
PAM50_FILE = "alg_PAM50.txt"
HUMAN_FILE = "alg_HumanEyelessProtein.txt"
FRUIT_FILE = "alg_FruitflyEyelessProtein.txt"
PAX_DOMAIN = "alg_ConsensusPAXDomain.txt"

##################################################################
#   Helper functions
#
def load_scoring_matrix(file_name):
    """
    Helper function to load a scoring matrix from a given file

    Args:
        file_name (string): file where the scoring matrix is stored
    Returns:
        scoring_matrix (dict of dicts): Scoring matrix
    """
    data_file = open(file_name)
    matrix_lines = data_file.read().splitlines()
    # initialize the scoring matrix
    scoring_matrix = {}
    # the first line read will have the base chars
    alphabet = matrix_lines[0]
    # build a set of chars
    base_chars = []
    #
    for bchar in alphabet:
        if (bchar != ' ') and (bchar != '\n'):
            base_chars.append(bchar)
    # read the rest of the lines
    for row_idx in range(1, len(matrix_lines)):
        matrix_line = matrix_lines[row_idx].split(" ")
        row_char = matrix_line[0]
        # clean up any cruft
        clean_line = []
        for idx in range(1, len(matrix_line)):
            if (matrix_line[idx] != '') and (matrix_line[idx] != '\n'):
                clean_line.append(matrix_line[idx])
        #
        inner_dict = {}
        # read the line and store the scores by basepair
        for col_idx in range(0, len(clean_line)):
            inner_dict[base_chars[col_idx]] = int(clean_line[col_idx])
        #
        scoring_matrix[row_char] = inner_dict
    #
    return (scoring_matrix, set(base_chars))
#
def load_genome_file(file_name):
    """
    Helper to load the genome sequence from a file

    Args:
        file_name (file name): location of the file to be opened
    Returns:
        genome (str) : genome sequence as a string
    """
    data_file = open(file_name)
    #
    genome = data_file.read().splitlines()
    #
    return genome[0]
#
def calc_match_percentage(seq_x, seq_y):
    """
    Helper function to compute the percentage of alignments that match
    between two genome sequences of identical length

    Args:
        seq_x (str): genome sequence
        seq_y (str): genome sequence

    Returns:
        float: percentage of alignments as part of entire sequence
    """
    seq_length = len(seq_x)
    #
    match_count = 0
    for idx in range(seq_length):
        if seq_x[idx] == seq_y[idx]:
            match_count += 1
    #
    return float(match_count)/float(seq_length)
#
def calc_mean(score_dist: dict):
    """
    Calculate the mean score of a given score distribution

    Args:
        score_dist (dict): score distribution

    Returns:
        float: arithmetic mean
    """
    sum_total = 0
    num_reslt = 0
    #
    for score in score_dist.keys():
        rslts = score_dist[score]
        num_reslt += rslts
        sum_total += (rslts * score)
    #
    return float(sum_total) / float(num_reslt)
#
def calc_stddev(score_dist: dict, mean: float):
    """
    Calculate the standard deviation against a given mean for
    a score distribution

    Args:
        score_dist (dict): score distribution
        mean (float): mean for score distribution

    Returns:
        (float): standard deviation
    """
    sum_devs = 0.0
    num_trials = 0
    #
    for score in score_dist.keys():
        rslts = score_dist[score]
        dev_sqrd = (score - mean) ** 2.0
        sum_devs += (rslts * dev_sqrd)
        num_trials += rslts
    #
    sigma_squared = sum_devs / float(num_trials)
    #
    return math.sqrt(sigma_squared)
#
def plot_score_comparison(score_dist: dict):
    """
    Plot a bar graph depicting the normalized distrubtion of scores

    Args:
        score_dist (dict): unnormalized score distribution
    """
    # create a sorted list of the scores
    list_scores = list(score_dist.keys())
    list_scores.sort()
    # Step through the sorted list and create a list of trial counts
    # and get the total number of trials run
    num_trials = 0
    trial_counts = []
    #
    for score in list_scores:
        trial_counts.append(score_dist[score])
        num_trials += score_dist[score]
    # normalize trial_counts
    for idx in range(len(trial_counts)):
        trial_counts[idx] = float(trial_counts[idx]) / float(num_trials)
    #
    fig, ax = plt.subplots(figsize=(16, 10))
    suptitle_str = 'Null distribution for hypothesis testing for ' + str(num_trials) +' trials'
    fig.suptitle(suptitle_str)
    #
    ax.set_xlabel('Scores')
    ax.set_ylabel('Fraction of trials')
    #
    x = np.array(list_scores)
    y = np.array(trial_counts)
    #
    plt.bar(x, y)
    plt.show()
#
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

def compute_global_alignment(sequence_x, sequence_y, scoring_matrix, dp_table):
    """
    Function to compute and return a global pairwise alignment

    Args:
        sequence_x (string): X sequence of nucleotides
        sequence_y (string): Y sequence of nucleotides
        scoring_matrix (matrix): scoring matrix for positional matching of nucleotides
        dp_table (matrix): alignment matrix
    Returns:
        gpsa (string): global pairwise alignment of sequences X and Y
    """
    seq_x_len = len(sequence_x)
    seq_y_len = len(sequence_y)
    #
    x_align = ''
    y_align = ''
    #
    while (seq_x_len != 0) and (seq_y_len != 0):
        row_char = sequence_x[seq_x_len - 1]
        col_char = sequence_y[seq_y_len - 1]
        if dp_table[seq_x_len][seq_y_len] == dp_table[seq_x_len - 1][seq_y_len - 1] + scoring_matrix[row_char][col_char]:
            x_align = sequence_x[seq_x_len - 1] + x_align
            y_align = sequence_y[seq_y_len - 1] + y_align
            seq_x_len -= 1
            seq_y_len -= 1
        else:
            if dp_table[seq_x_len][seq_y_len] == dp_table[seq_x_len - 1][seq_y_len] + scoring_matrix[row_char]['-']:
                x_align = sequence_x[seq_x_len - 1] + x_align
                y_align = '-' + y_align
                seq_x_len -= 1
            else:
                x_align = '-' + x_align
                y_align = sequence_y[seq_y_len - 1] + y_align
                seq_y_len -= 1
    #
    # copy the remainer from the longest sequence
    while (seq_x_len != 0):
        x_align = sequence_x[seq_x_len - 1] + x_align
        y_align = '-' + y_align
        seq_x_len -= 1
    #
    while (seq_y_len != 0):
        x_align = '-' + x_align
        y_align = sequence_y[seq_y_len - 1] + y_align
        seq_y_len -= 1
    # calculate the score
    score = 0
    #
    for idx in range(len(x_align)):
        score += scoring_matrix[x_align[idx]][y_align[idx]]
    #
    return (score, x_align, y_align)

def compute_local_alignment(sequence_x, sequence_y, scoring_matrix, align_matrix):
    """
    Function to compute and return a global pairwise alignment

    Args:
        sequence_x (string): X sequence of nucleotides
        sequence_y (string): Y sequence of nucleotides
        scoring_matrix (matrix): scoring matrix for positional matching of nucleotides
        align_matrix (matrix): alignment matrix
    Returns:
       (score, align_x, align_y): local pairwise alignment of sequences X and Y
    """
    # initalize X' and Y'
    align_x = ''
    align_y = ''
    # find the entry in the alignment matrix that is the highest
    max_val = -1
    max_row = -1
    max_col = -1
    #
    for row_idx in range(len(align_matrix)):
        tst_val = max(align_matrix[row_idx])
        if tst_val > max_val:
            max_val = tst_val
            max_row = row_idx
            max_col = align_matrix[row_idx].index(max_val)
    # start at the highest score row_col and go until our score is zero
    while max_row != 0 and max_col != 0:
        #
        row_char = sequence_x[max_row - 1]
        col_char = sequence_y[max_col - 1]
        #
        if align_matrix[max_row][max_col] == align_matrix[max_row - 1][max_col - 1] + scoring_matrix[row_char][col_char]:
            align_x = sequence_x[max_row - 1] + align_x
            align_y = sequence_y[max_col - 1] + align_y
            max_row -= 1
            max_col -= 1
        else:
            if align_matrix[max_row][max_col] == align_matrix[max_row - 1][max_col] + scoring_matrix[row_char]['-']:
                align_x = sequence_x[max_row - 1] + align_x
                align_y = '-' + align_y
                max_row -= 1
            else:
                align_x = '-' + align_x
                align_y = sequence_y[max_col - 1] + align_y
                max_col -= 1
        # if we encounter an alignment matrix entry of value 0, we're done
        if align_matrix[max_row][max_col] == 0:
            break
    #
    # calculate the score
    score = 0
    #
    for idx in range(len(align_x)):
        score += scoring_matrix[align_x[idx]][align_y[idx]]
    #
    return (score, align_x, align_y)
#
def generate_null_distribution(seq_x, seq_y, scoring_matrix, num_trials):
    """
    

    Args:
        seq_x (str): genome sequence
        seq_y (str): genome sequence
        scoring_matrix (dict of dicts): scoring matrix
        num_trials (int): number of trials to run
    Return:
        score_dist (dict): scoring distribution
    """
    score_dist = {}
    #
    for _ in range(num_trials):
        list_seq_y = list(seq_y)
        random.shuffle(list_seq_y)
        rand_y = "".join(list_seq_y)
        gnd_align_mtrx = compute_alignment_matrix(seq_x, rand_y, scoring_matrix, False)
        (score, align_x, align_y) = compute_local_alignment(seq_x, rand_y, scoring_matrix, gnd_align_mtrx)
        #
        if score in score_dist:
            score_dist[score] += 1
        else:
            score_dist[score] = 1
    #
    return score_dist

###################################
# quick test
#
# detailed tests
#
#print("Test 0 : build_scoring_matrix")
#scm0 = build_scoring_matrix(set(['A', 'C', 'T', 'G']), 6, 2, -4)
#
#for row in scm0:
#    print(row, ":", scm0[row])
#
#print("Test 1 : compute_alignment_matrix (global)")
#scm1 =  {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2},
#         'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, 
#         '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4},
#         'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 
#         'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}
#dpt1 = compute_alignment_matrix('ATG', 'ACG', scm1, True)
#
#for row_num in range(len(dpt1)):
#    print(row_num, ":", dpt1[row_num])
#
#print("Test 2 : compute_alignment_matrix (local)")
#scm2 =  {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2},
#         'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, 
#         '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4},
#         'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 
#         'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}
#dpt2 = compute_alignment_matrix('ATG', 'ACG', scm2, False)
#
#for row_num in range(len(dpt2)):
#    print(row_num, ":", dpt2[row_num])
#
#seq_x = 'ACCTG-CA-C'
#seq_y = 'CGTGCTAGTC'
#
#dpt3 = compute_alignment_matrix(seq_x, seq_y, scm2, True)
#
#(score, x_prime, y_prime) = compute_global_alignment(seq_x, seq_y, scm2, dpt3)
#
#print("X-prime : ", x_prime)
#print("Y-prime : ", y_prime)
#print("score   : ", score)
#
#print("Test 5 : compute_global_alignment")
#
scm5 = {'A': {'A': 2, 'C': 1, '-': 0, 'T': 1, 'G': 1},
        'C': {'A': 1, 'C': 2, '-': 0, 'T': 1, 'G': 1},
        '-': {'A': 0, 'C': 0, '-': 0, 'T': 0, 'G': 0},
        'T': {'A': 1, 'C': 1, '-': 0, 'T': 2, 'G': 1},
        'G': {'A': 1, 'C': 1, '-': 0, 'T': 1, 'G': 2}}
dpt5 =  [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
         [0, 1, 2, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
         [0, 1, 2, 3, 4, 6, 6, 6, 6, 6, 6, 6, 6, 6],
         [0, 1, 2, 4, 4, 6, 7, 7, 7, 7, 7, 7, 7, 7],
         [0, 1, 2, 4, 6, 6, 7, 9, 9, 9, 9, 9, 9, 9],
         [0, 1, 2, 4, 6, 8, 8, 9, 11, 11, 11, 11, 11, 11]]
seq5_x = 'ACTACT'
seq5_y = 'GGACTGCTTCTGG'
#
#(scr5, alx5, aly5) = compute_global_alignment(seq5_x, seq5_y, scm5, dpt5)
#
#print("X-prime : ", alx5)
#print("Y-prime : ", aly5)
#print("score   : ", scr5)
#
#print("Test 6 : compute_local_alignment")
#
scm6 = {'A': {'A': 2, 'C': 1, '-': 0, 'T': 1, 'G': 1},
        'C': {'A': 1, 'C': 2, '-': 0, 'T': 1, 'G': 1},
        '-': {'A': 0, 'C': 0, '-': 0, 'T': 0, 'G': 0},
        'T': {'A': 1, 'C': 1, '-': 0, 'T': 2, 'G': 1},
        'G': {'A': 1, 'C': 1, '-': 0, 'T': 1, 'G': 2}}
dpt6 =  [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
         [0, 1, 2, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
         [0, 1, 2, 3, 4, 6, 6, 6, 6, 6, 6, 6, 6, 6],
         [0, 1, 2, 4, 4, 6, 7, 7, 7, 7, 7, 7, 7, 7],
         [0, 1, 2, 4, 6, 6, 7, 9, 9, 9, 9, 9, 9, 9],
         [0, 1, 2, 4, 6, 8, 8, 9, 11, 11, 11, 11, 11, 11]]
#seq6_x = 'ACTACT'
#seq6_y = 'GGACTGCTTCTGG'
#
#(scr6, alx6, aly6) = compute_local_alignment(seq6_x, seq6_y, scm6, dpt6)
#
#print("X-prime : ", alx6)
#print("Y-prime : ", aly6)
#print("score   : ", scr6)
#
#print("Test 7 : compute_local_alignment")
#
#scm7 = {'-': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1},
#        'a': {'-': -1, 'a': 2, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1},
#        'c': {'-': -1, 'a': -1, 'c': 2, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1},
#        'b': {'-': -1, 'a': -1, 'c': -1, 'b': 2, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1},
#        'e': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': 2, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1},
#        'd': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': 2, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1},
#        'g': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': 2, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1},
#        'f': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': 2, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 
#        'i': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': 2, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 
#        'h': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': 2, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1},
#        'k': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': 2, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 
#        'j': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': 2, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 
#        'm': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': 2, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 
#        'l': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': 2, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 
#        'o': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': 2, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 
#        'n': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': 2, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 
#        'q': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': 2, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 
#        'p': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': 2, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 
#        's': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': 2, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 
#        'r': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': 2, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 
#        'u': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': 2, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 
#        't': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': 2, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 
#        'w': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': 2, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 
#        'v': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': 2, 'y': -1, 'x': -1, 'z': -1}, 
#        'y': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': 2, 'x': -1, 'z': -1}, 
#        'x': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': 2, 'z': -1}, 
#        'z': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': 2}}
#
#dpt7 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
#        [0, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
#        [0, 1, 1, 4, 3, 2, 1, 0, 0, 0, 0, 0, 0], 
#        [0, 0, 0, 3, 3, 5, 4, 3, 2, 1, 0, 0, 0], 
#        [0, 0, 0, 2, 2, 5, 7, 6, 5, 4, 3, 2, 1], 
#        [0, 0, 0, 1, 4, 4, 6, 6, 5, 4, 3, 2, 1], 
#        [0, 0, 0, 0, 3, 6, 6, 5, 5, 4, 3, 2, 1], 
#        [0, 0, 0, 0, 2, 5, 5, 8, 7, 6, 5, 4, 3], 
#        [0, 0, 0, 0, 1, 4, 4, 7, 10, 9, 8, 7, 6], 
#        [0, 0, 0, 0, 0, 3, 3, 6, 9, 9, 8, 7, 6], 
#        [0, 0, 0, 0, 0, 2, 2, 5, 8, 11, 10, 9, 8], 
#        [0, 0, 0, 0, 0, 1, 1, 4, 7, 10, 13, 12, 11]]
#
#seq7_x = 'abddcdeffgh'
#seq7_y = 'aabcddefghij'
#
#print("X : ", seq7_x)
#print("Y : ", seq7_y)
#
#(scr7, alx7, aly7) = compute_local_alignment(seq7_x, seq7_y, scm7, dpt7)
#
#print("X-prime : ", alx7)
#print("Y-prime : ", aly7)
#print("score   : ", scr7)
#
# Application #4 work
#
# Compare Eyeless proteing sequence for Human and Fruitfly
#
pam50 = FILE_DIR + PAM50_FILE
#
(scm_50, alfabet_50) = load_scoring_matrix(pam50)
#
#for row in scm_50:
#    print(row, " : ", scm_50[row])
# next read the genomes
#
fruit_file = FILE_DIR + FRUIT_FILE
human_file = FILE_DIR + HUMAN_FILE
#
ffly_seq = load_genome_file(fruit_file)
humn_seq = load_genome_file(human_file)
#
#print("Fruit-Fly : ", type(ffly_seq), ffly_seq)
#print("Human Eye : ", type(humn_seq), humn_seq)
#
dpt_eyeless = compute_alignment_matrix(ffly_seq, humn_seq, scm_50, False)
#
(scr_eyeless, ffly_align, humn_align) = compute_local_alignment(ffly_seq, humn_seq, scm_50, dpt_eyeless)
#
# Q1 answers
print("\nQ1 answers\n")
#
print("X-prime : ", ffly_align)
print("Y-prime : ", humn_align)
print("score   : ", scr_eyeless)
#
# Check against ConsensusPAX Domain
#
cpd_file = FILE_DIR + PAX_DOMAIN
conpaxdom = load_genome_file(cpd_file)
#
# remove dashes from each off the above alignments
#
ffly_strip = ffly_align.replace('-', '')
humn_strip = humn_align.replace('-', '')
# 
#print("X-prime (stripped) : ", ffly_strip)
#print("Y-prime (stripped) : ", humn_strip)
#
dpt_fly_cpd = compute_alignment_matrix(ffly_strip, conpaxdom, scm_50, True)
(scr_fstr, ffly_strp, cpd_align0) = compute_global_alignment(ffly_strip, conpaxdom, scm_50, dpt_fly_cpd)
#
dpt_hum_cpd = compute_alignment_matrix(humn_strip, conpaxdom, scm_50, True)
(scr_hstr, humn_strp, cpd_align1) = compute_global_alignment(humn_strip, conpaxdom, scm_50, dpt_hum_cpd)
#
print("\nQ2 answers\n")
#
print("X-fruit : ", ffly_strp)
print("Y-prime : ", cpd_align0)
print("score   : ", scr_fstr)
print("Match % : ", 100.0 * calc_match_percentage(ffly_strp, cpd_align0))
#
print("X-human : ", humn_strp)
print("Y-prime : ", cpd_align1)
print("score   : ", scr_hstr)
print("Match % : ", 100.0 * calc_match_percentage(humn_strp, cpd_align1))
#
# Question 4 work
#
#num_trials = 1000
#
#scr_dist = generate_null_distribution(humn_seq, ffly_seq, scm_50, num_trials)
#
#print("Result : \n\n", scr_dist)
#scr_keys = list(scr_dist.keys())
#scr_keys.sort()
#
#for key in scr_keys:
#    print("score : ", key, "\tvalue : ", scr_dist[key])
#
# The Plot is the Question 4 answer...
#
# plot_score_comparison(scr_dist)
#
# Question 5
#
#scr_mean = calc_mean(scr_dist)
#
#scr_stdev = calc_stddev(scr_dist, scr_mean)
#
#print("\nQ5 answers\n")
#
#print("mean     : ", scr_mean)
#print("std.dev. : ", scr_stdev)
#
#print("z-score  : ", ((scr_eyeless - scr_mean) / scr_stdev))
#
# Question 7 work
#
diag_score_7 = 2
off_diag_score_7 = 1
dash_score_7 = 0
#
#print("alfabet : ", alfabet_50)
#
scm_7 = build_scoring_matrix(alfabet_50, diag_score_7, off_diag_score_7, dash_score_7)
#
#for row in scm_7:
#    print(row, " : ", scm_7[row])
#
dpt_7 = compute_alignment_matrix(ffly_seq, humn_seq, scm_7, True)
#
(scr_7, ffly_align_7, humn_align_7) = compute_global_alignment(ffly_seq, humn_seq, scm_7, dpt_7)
#
# Q1 answers
print("\nQ7 answers\n")
#
print("X-prime : ", ffly_align_7)
print("Y-prime : ", humn_align_7)
print("score   : ", scr_7)
#
# Spell-check...
#
alfabet_8 = 'abcdegfhijklmnopqrstuvwxyz-'
seq_1 = 'humble'
seq_2 = 'fumble'
#
scm_8 = build_scoring_matrix(alfabet_8, diag_score_7, off_diag_score_7, dash_score_7)
#
dpt_8 = compute_alignment_matrix(seq_1, seq_2, scm_8, True)
#
(scr_8, hum_align_8, fly_align_8) = compute_global_alignment(seq_1, seq_2, scm_8, dpt_8)
#
print("\nQ7 answers\n")
#
print("X-prime : ", hum_align_8)
print("Y-prime : ", fly_align_8)
print("score   : ", scr_8)