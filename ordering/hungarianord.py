import numpy as np


def best_matches(arr: np.ndarray):
    # Step 1: Sort rows by number of set bits in row
    arr_sorted = arr[np.argsort(np.sum(arr, axis=1))]
    ordered_bit_counts = np.sum(arr_sorted, axis=1)

    # count cost of every column

    # Compute the binary values for each row
    binary_values = np.packbits(
        arr_sorted, axis=1).flatten()

    # Create a sorting index based on binary values and ordered_numbers
    sorting_index = np.lexsort((ordered_bit_counts, binary_values))

    # Sort the rows of the array based on the sorting index
    return arr_sorted[sorting_index]


arr = np.array([[True, False, True],
                [False, True, False],
                [True, True, False],
                [False, False, True]])

print(best_matches(arr))
