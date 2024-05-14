def merge_inversions(left_array, right_array, array_ints):
    """
    Function to count the number of inversions and merge

    Args:
        left_array (_type_): _description_
        right_array (_type_): _description_
        array_ints (_type_): _description_
    """
    inversion_count = 0
    idx_left = 0
    idx_right = 0
    idx_merge = 0
    #
    len_left = len(left_array)
    len_right = len(right_array)
    #
    while (idx_left < len_left) and (idx_right < len_right):
        if left_array[idx_left] <= right_array[idx_right]:
            array_ints[idx_merge] = left_array[idx_left]
            idx_left += 1
        else:
            array_ints[idx_merge] = right_array[idx_right]
            idx_right += 1
            inversion_count += (len_left - idx_left)
        #
        idx_merge += 1
    if idx_left == len_left:
        array_ints[idx_merge:(len_right + len_left - 1)] = right_array[idx_right:]
    else:
        array_ints[idx_merge:(len_right + len_left - 1)] = left_array[idx_left:]
    #
    return inversion_count
        
def count_inversions(array_ints):
    """
    Function to count the number of inversions in a given array of integers

    Args:
        array_ints (list): Array of integers
    """
    # if we're of length 1 there are no inversions
    if len(array_ints) == 1:
        return 0
    else:
        mid_point = len(array_ints) // 2
        left_array = array_ints[:mid_point]
        right_array = array_ints[mid_point:]
        #
        inversions_left  = count_inversions(left_array)
        inversions_right = count_inversions(right_array)
        inversions_merge = merge_inversions(left_array, right_array, array_ints)
        #
        return inversions_left + inversions_right + inversions_merge

array0 = [0, 1, 3, 2]
count0 = count_inversions(array0)
print("inversions : ", count0)

array1 = [0, 1, 3, 6, 5, 2]
count1 = count_inversions(array1)
print("inversions : ", count1)