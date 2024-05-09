def mystery(int_array, left_bound, right_bound):
    """
    Mystery algorithm....

    Args:
        int_array (list): Array of distinct integers
        left_bound (int): Left boundary
        right_bound (int): Right boundary
    """
    if left_bound > right_bound:
        return -1
        
    mid_point = (left_bound + right_bound) // 2
    #
    if int_array[mid_point] == mid_point:
        return mid_point
    else:
        if int_array[mid_point] < mid_point:
            return mystery(int_array, mid_point + 1, right_bound)
        else:
            return mystery(int_array, left_bound, mid_point - 1)

print("mystery ; ", mystery([-2, 0, 1, 4, 7, 12, 15], 0, 6))
