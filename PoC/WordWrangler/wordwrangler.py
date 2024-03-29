"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    new_list = []
    #
    if len(list1) < 2:
        return list1
    elif list1[0] <> list1[1]:
        new_list.append(list1[0])
    #
    new_list += remove_duplicates(list1[1:])
    #
    return new_list

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    intersect_list = []
    # if either list is empty there is no intersection
    if (len(list1) == 0) or (len(list2) == 0):
        return []
    elif list1[0] == list2[0]:
        intersect_list.append(list1[0])
        # match, so go to next element in both lists
        intersect_list += intersect(list1[1:], list2[1:])
    elif list1[0] < list2[0]:
        # list1 is less, so bump list1
        intersect_list += intersect(list1[1:], list2)
    else:
        # list2 is less, so bump list2
        intersect_list += intersect(list1, list2[1:])
    #
    return intersect_list

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function can be iterative.
    """
    # we'll merge into a copy of list1
    list1_length = len(list1)
    list2_length = len(list2)
    # if either list (or both) are empty, return their sum
    if (list1_length == 0) or (list2_length == 0):
        return list1 + list2
    else:
        # populate the merge with a copy of list1
        merge_list = list1[:]
        merge_length = list1_length
        # we'll index through the lists
        merge_index = 0
        list2_index = 0
        # in the worst case we'll have to step through all list items
        for dummy_index in range(list1_length + list2_length):
            # if there are items in the merge list after the current index
            if merge_index < merge_length:
                if list2[list2_index] < merge_list[merge_index]:
                    # list2 item goes before the current merge_list item
                    merge_list.insert(merge_index, list2[list2_index])
                    # update both indices
                    list2_index += 1
                    merge_index += 1
                    # the merge_list length has grown
                    merge_length += 1
                else:
                    # list2 item doesn't go before, so update merge_index only
                    merge_index += 1
            else:
                # we've reach the end of the merge list and have more list2 to process
                merge_list.insert(merge_index, list2[list2_index])
                # update both indices
                list2_index += 1
                merge_index += 1
            # if we processed all of list2, we've merged everything
            if list2_index >= list2_length:
                break
            # all done
    return merge_list
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    return []

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    return []

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    return []

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
# run()

# test area
tlist0 = []
tlist1 = ['a']
tlist2 = ['a', 'a']
tlist3 = ['a', 'b', 'b', 'v']
tlist4 = ['a', 'b', 'c', 'd', 'e', 'f', 'f', 'g', 'h', 'i', 'j', 'k', 'k', 'l', 'z']
#
print "Testing remove duplicates"
print
res0 = remove_duplicates(tlist0)
print res0, " from ", tlist0
res1 = remove_duplicates(tlist1)
print res1, " from ", tlist1
res2 = remove_duplicates(tlist2)
print res2, " from ", tlist2
res3 = remove_duplicates(tlist3)
print res3, " from ", tlist3
res4 = remove_duplicates(tlist4)
print res4, " from ", tlist4
#
alist0 = []
alist1 = ['a']
alist2 = ['a', 'a']
alist3 = ['a', 'b', 'b', 'v']
alist4 = ['a', 'b', 'c', 'd', 'e', 'f', 'f', 'g', 'h', 'i', 'j', 'k', 'k', 'l', 'z']
alist5 = ['a', 'c', 'e', 'h', 'j', 'k', 'z']
#
blist0 = []
blist1 = ['a']
blist2 = ['a', 'a']
blist3 = ['a', 'b', 'd', 'v']
blist4 = ['a', 'b', 'c', 'd', 'e', 'f', 'f', 'j', 'k', 'k', 'l', 'z']
blist5 = ['c', 'd', 'g', 'h', 'i', 'k', 'l', 'o', 'p', 'q', 's', 'x', 'y', 'z']
#
print
print "Testing intersect"
print
res0 = intersect(alist0, blist0)
print res0, " from ", alist0, " and ", blist0
res1 = intersect(alist2, blist0)
print res1, " from ", alist2, " and ", blist0
res2 = intersect(alist1, blist1)
print res2, " from ", alist1, " and ", blist1
res3 = intersect(alist2, blist2)
print res3, " from ", alist2, " and ", blist2
res4 = intersect(alist3, blist2)
print res4, " from ", alist3, " and ", blist2
res5 = intersect(alist3, blist3)
print res5, " from ", alist3, " and ", blist3
res6 = intersect(alist4, blist3)
print res6, " from ", alist4, " and ", blist3
res7 = intersect(alist4, blist4)
print res7, " from ", alist4, " and ", blist4
res8 = intersect(alist5, blist5)
print res8, " from ", alist5, " and ", blist5
#
mlist0 = []
mlist1 = ['b']
mlist2 = ['a', 'c']
mlist3 = ['a', 'b', 'c', 'd']
mlist4 = ['f', 'g', 'h', 'i', 'j', 'k', 'k', 'l', 'z']
mlist5 = ['a', 'c', 'e', 'h', 'j', 'l', 'x']
#
nlist0 = []
nlist1 = ['a']
nlist2 = ['a', 'b']
nlist3 = ['e', 'f', 'g', 'h']
nlist4 = ['a', 'b', 'c', 'd', 'e', 'f']
nlist5 = ['b', 'f', 'g', 'i', 'k', 'z']
#
#
print
print "Testing merge"
print
res0 = merge(mlist0, nlist0)
print res0, " from ", mlist0, " and ", nlist0
res1 = merge(mlist0, nlist1)
print res1, " from ", mlist0, " and ", nlist1
res2 = merge(mlist1, nlist1)
print res2, " from ", mlist1, " and ", nlist1
res3 = merge(mlist2, nlist2)
print res3, " from ", mlist2, " and ", nlist2
res4 = merge(mlist3, nlist3)
print res4, " from ", mlist3, " and ", nlist3
res5 = merge(nlist3, mlist3)
print res5, " from ", nlist3, " and ", mlist3
