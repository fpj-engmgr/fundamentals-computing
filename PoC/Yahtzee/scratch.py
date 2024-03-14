
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

def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    # initalize the set
    hold_set = set()
    # hold none
    no_hold = ()
    #
    hold_set.add(tuple(no_hold))
    for first_idx in range(len(hand)):
        # hold one die
        die_0 = [hand[first_idx]]
        hold_set.add(tuple(die_0))
        # hold two dice
        if (first_idx < (len(hand) - 1)):
            for second_idx in range(first_idx + 1, len(hand)):
                new_seq = [hand[first_idx],
                           hand[second_idx]]
                hold_set.add(tuple(new_seq))
        # hold three dice
        if (first_idx < (len(hand) - 2)):
            for second_idx in range(first_idx + 1, (len(hand) - 1)):
                for third_idx in range(second_idx + 1, len(hand)):
                    new_seq = [hand[first_idx],
                               hand[second_idx],
                               hand[third_idx]]
                    hold_set.add(tuple(new_seq))
        # hold four dice
        if (first_idx < (len(hand) - 3)):
            for second_idx in range(first_idx + 1, (len(hand) - 2)):
                for third_idx in range(second_idx + 1, (len(hand) - 1)):
                    for fourth_idx in range(third_idx + 1, len(hand)):
                        new_seq = [hand[first_idx],
                                   hand[second_idx],
                                   hand[third_idx],
                                   hand[fourth_idx]]
                        hold_set.add(tuple(new_seq))
    # add hold all to the options
    hold_all = [hand[0], hand[1], hand[2], hand[3], hand[4]]
    #
    hold_set.add(tuple(hold_all))
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