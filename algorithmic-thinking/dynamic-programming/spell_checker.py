"""
    Spell-checking and related algorithms
"""
import time

FILE_DIR = "/Users/fpj/Development/python/fundamentals-computing/algorithmic-thinking/data/"
DICT_FILE = "assets_scrabble_words3.txt"


######################################################
#   Helper functions
#
def load_dictionary(dict_file):
    """
    Function to load a dictionary file and return a word list

    Args:
        dict_file (str): Name and location of dictionary file
    Returns:
        (set): set of all words in dict_file
    """
    data_file = open(dict_file)
    words = data_file.read().splitlines()
    #
    word_set = set([])
    word_count = 0
    #
    for word in words:
        word_set.add(word)
        word_count += 1
    #
    print("Loaded ", word_count, " words")
    #
    return word_set
#
def check_spelling(checked_word, dist, word_list):
    """
    Function to generate a set of words that are within an edit distance dist
    of the string checked_word.
    
    Edit distance refers to the number of inserts, deletes or substitutes that 
    are performed on checked_word; the resulting word is checked against the 
    word_list for inclusion.

    Args:
        checked_word (str): word to be transformed
        dist (int): edit distance
        word_list (set): dictionary of permitted words
    Returns:
        (set): all words within edit distance
    """
    alfabet = 'abcdefghijklmnopqrstuvwxyz'
    #
    check_len = len(checked_word)
    #
    word_salad = set([])
    # check insertions first
    for idx in range(check_len + 1):
        # go through the entire alphabet
        for karakter in alfabet:
            # insert in every location
            if idx < check_len:
                test_word = checked_word[:idx] + karakter + checked_word[idx:]
            else:
                test_word = checked_word[:idx] + karakter
            # check if the word is in the list
            if test_word in word_list:
                word_salad.add(test_word)
            # if we can go for more distance
            if dist > 1:
                more_words = check_spelling(test_word, (dist - 1), word_list)
                # add more distant words
                for new_word in more_words:
                    word_salad.add(new_word)
    # let's try deletions
    for idx in range(check_len):
        # delete in every location
        if idx < (check_len - 1):
            test_word = checked_word[:idx] + checked_word[idx + 1:]
        else:
            test_word = checked_word[:idx]
        # check if the word is in the list
        if test_word in word_list:
            word_salad.add(test_word)
        # is there more distance?
        if dist > 1:
            more_words = check_spelling(test_word, (dist - 1), word_list)
            # add more distant words
            for new_word in more_words:
                word_salad.add(new_word)
    # and substitutions
    for idx in range(check_len):
        # go through the entire alphabet
        for karakter in alfabet:
            # insert in every location
            if idx < (check_len - 1):
                test_word = checked_word[:idx] + karakter + checked_word[idx + 1:]
            else:
                test_word = checked_word[:idx] + karakter
            # check if the word is in the list
            if test_word in word_list:
                word_salad.add(test_word)
            # if we can go for more distance
            if dist > 1:
                more_words = check_spelling(test_word, (dist - 1), word_list)
                # add more distant words
                for new_word in more_words:
                    word_salad.add(new_word)
    #
    return word_salad
#
######################################
#
scrabble = FILE_DIR + DICT_FILE
dictionary = load_dictionary(scrabble)
#
# perf test for lookups
#
lookup_list = ['grapnels',
               'savagism',
               'spalpeen',
               'indocile',
               'catalyst',
               'zymosis',
               'quaintly',
               'joyously',
               'smilaxes',
               'witchery']
#
set_count = 0
#
lookup_count = 1000000
lookup_len = len(lookup_list)
#
#
start_time = time.time()
#
for idx in range(lookup_count):
    if lookup_list[idx % lookup_len] in dictionary:
        set_count += 1
#
set_time = time.time() -start_time
#
print("Found all ", set_count, " in dictionary set in  ", set_time)
#
seed_word0 = 'humble'
depth0 = 1
jumble_set0 = check_spelling(seed_word0, depth0, dictionary)
#
seed_word1 = 'firefly'
depth1 = 3
jumble_set1 = check_spelling(seed_word1, depth1, dictionary)
#
print("Brain salad surgery",jumble_set0)
print("Brain salad surgery",jumble_set1)