"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set

def combinations(iterable, run_length):
    """
    combinations function (from itertools)
    
    returns a generator for a set of tuples of each
    combination of length run_length in iterable
    """
    pool = tuple(iterable)
    num_items = len(pool)
    if run_length > num_items:
        return
    indices = list(range(run_length))
    yield tuple(pool[idx] for idx in indices)
    while True:
        idx = 0
        for idx in reversed(range(run_length)):
            if indices[idx] != idx + num_items - run_length:
                break
        else:
            return
        indices[idx] += 1
        for jdx in range(idx + 1, run_length):
            indices[jdx] = indices[jdx - 1] + 1
        yield tuple(pool[idx] for idx in indices)


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    upper_scores = {}
    hand_size = len(hand)
    # step through the hand and add the value of the die
    for idx in range(hand_size):
        die_val = hand[idx]
        if die_val in upper_scores:
            upper_scores[die_val] += die_val
        else:
            upper_scores[die_val] = die_val
    # identify the largest score option
    max_score = 0
    for key in upper_scores:
        if upper_scores[key] > max_score:
            max_score = upper_scores[key]
    #
    return max_score


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    #
    outcomes = [idx for idx in range(1, num_die_sides + 1)]
    exp_value = 0.0
    #
    all_rolls = gen_all_sequences(outcomes, num_free_dice)
    #
    num_seqs = len(all_rolls) * 1.0
    #
    for new_roll in all_rolls:
        new_hand = list(held_dice)
        for die in new_roll:
            new_hand.append(die)
        new_hand.sort()
        #
        exp_value += score(new_hand)
    #
    exp_value /= num_seqs
    #
    return exp_value


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    #
    num_dice = len(hand)
    held_dice = set()
    # create combinations for each number of dice held
    for held_num in range(num_dice + 1):
        for combo in combinations(hand, held_num):
            held_dice.add(combo)
    #
    return held_dice


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    # imp thoughts:
    # - generate all possible holds
    # - get expected value of each hold and append it to list of values
    # - get the index of the max value
    # - return value and hold
    all_holds = set()
    all_vals = list()
    hold_list = list()
    #
    all_holds = gen_all_holds(hand)
    #
    for held_dice in all_holds:
        num_free_dice = len(hand) - len(held_dice)
        exp_val = expected_value(held_dice, num_die_sides, num_free_dice)
        #
        all_vals.append(exp_val)
        hold_list.append(held_dice)
        print held_dice, " : ", exp_val
    #
    max_val = max(all_vals)
    idx_max = all_vals.index(max_val)
    #
    return (all_vals[idx_max], hold_list[idx_max])


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    hand = (1, 4, 4, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
#run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)

