
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

def gen_sorted_sequences(outcomes, length):
    """
    Function that creates all sorted sequences via gen_all_sequences
    """    
    all_sequences = gen_all_sequences(outcomes, length)
    sorted_sequences = [tuple(sorted(sequence)) for sequence in all_sequences]
    return set(sorted_sequences)

def combinations(iterable, r):
    # combinations('ABCD', 2) → AB AC AD BC BD CD
    # combinations(range(4), 3) → 012 013 023 123
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)


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
            hold_set.add(combo)
    #
    return hold_set


num_die_sides = 6
hand = (1, 1, 1, 5, 6)

hold_one = gen_all_sequences(hand, 1)
hold_two = gen_all_sequences(hand, 2)
hold_thr = gen_all_sequences(hand, 3)

print "Unsorted ---"
print "One    : ", len(hold_one), hold_one
print "Two    : ", len(hold_two), hold_two
print "Three  : ", len(hold_thr), hold_thr

sort_one = gen_sorted_sequences(hand, 1)
sort_two = gen_sorted_sequences(hand, 2)
sort_thr = gen_sorted_sequences(hand, 3)

print "Sorted ---"
print "One    : ", len(sort_one), sort_one
print "Two    : ", len(sort_two), sort_two
print "Three  : ", len(sort_thr), sort_thr


all_holds = gen_all_holds(hand)

print "Holds ---"
print "Number possible : ", len(all_holds)
print all_holds

print hand, " : ", score(hand)
hand = (1, 2, 4, 4, 6)
print hand, " : ", score(hand)
hand = (1, 2, 4, 4, 6)
print hand, " : ", score(hand)
hand = (1, 4, 4, 4, 6)
print hand, " : ", score(hand)
hand = (1, 2, 4, 4, 5, 5, 5, 6, 6)
print hand, " : ", score(hand)

print "((3, 3), 8, 5)", expected_value((3, 3), 8, 5)
