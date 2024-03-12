"""
Functions to enumerate sequences of outcomes
Repetition of outcomes is allowed
"""


def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length
    """
    
    ans = set([()])
    for dummy_idx in range(length):
        temp = set()
        for seq in ans:
            for item in outcomes:
                new_seq = list(seq)
                new_seq.append(item)
                temp.add(tuple(new_seq))
        ans = temp
    return ans

def max_repeats(seq):
    """
    Determine the maximum number 
    """
    item_count = [seq.count(item) for item in seq]
    return max(item_count)

# example for digits
def run_example1():
    """
    Example of all sequences
    """
    outcomes = set([1, 2, 3, 4, 5, 6])
    #outcomes = set([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    #outcomes = set(["Red", "Green", "Blue"])
    #outcomes = set(["Sunday", "Mondy", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
    
    length = 3
    seq_outcomes = gen_all_sequences(outcomes, length)
    print "Computed", len(seq_outcomes), "sequences of", str(length), "outcomes"
    print "Sequences were", seq_outcomes
    # initialize gambling
    bet_cost = len(seq_outcomes) * 10
    # calculate the expected return 
    bet_win = 0
    for seq in seq_outcomes:
        reps = max_repeats(seq)
        if reps == 2:
            bet_win += 10
        elif reps == 3:
            bet_win += 200
    # share our ROI
    print "Betting cost you $" + str(bet_cost)
    print "Winnings are.... $" + str(bet_win)
    print "Expected value:  $" + str(float(bet_win)/float(len(seq_outcomes)))

run_example1()


#
#def gen_sorted_sequences(outcomes, length):
#    """
#    Function that creates all sorted sequences via gen_all_sequences
#    """    
#    all_sequences = gen_all_sequences(outcomes, length)
#    sorted_sequences = [tuple(sorted(sequence)) for sequence in all_sequences]
#    return set(sorted_sequences)
#
#
#def run_example2():
#    """
#    Examples of sorted sequences of outcomes
#    """
#    # example for digits
#    outcomes = set([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
#    #outcomes = set(["Red", "Green", "Blue"])
#    #outcomes = set(["Sunday", "Mondy", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
#    
#    length = 2
#    seq_outcomes = gen_sorted_sequences(outcomes, length)
#    print "Computed", len(seq_outcomes), "sorted sequences of", str(length) ,"outcomes"
#    print "Sequences were", seq_outcomes
#    
#run_example2()