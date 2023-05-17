import numpy as np
from ordering.hungarian import solve_rectangular_linear_sum_assignment


def get_cost(col: np.ndarray, column_index: int, width: int, cost_size: int, indices_where_cost_change: np.ndarray) -> np.ndarray:
    """
    Calculate cost for column at position column_index using ordered_bit_count and width
    Result is a vector(flattened matrix) ordered by bit_count and column_index
    Set bits in col for rows with same bit_count are summed
    """
    result = np.zeros(cost_size, dtype=np.int_)
    for i, item in enumerate(col):
        index = np.searchsorted(indices_where_cost_change, i, side='right')
        result[index * width + column_index] += item

    return result


def get_minimized(arr: np.ndarray):
    # Step 1: Sort rows by number of set bits in row
    arr_sorted = arr[np.argsort(np.sum(arr, axis=1))]
    width = arr_sorted.shape[1]
    ordered_bit_counts = np.sum(arr_sorted, axis=1)
    unique_bit_counts, counts = np.unique(
        ordered_bit_counts, return_counts=True)
    cost_size = len(unique_bit_counts) * width
    indices_where_cost_change = np.cumsum(counts)
    # Initialize empty cost matrix
    cost_matrix = np.empty((width, width, cost_size), dtype=np.int_)

    # Calculate cost for each column at each position
    for i in range(width):
        for j in range(width):
            cost_matrix[i, j] = get_cost(
                arr_sorted[:, i], j, width, cost_size, indices_where_cost_change)

    row4col, col4row = solve_rectangular_linear_sum_assignment(cost_matrix)
    inverse_col_ind = np.argsort(col4row)
    arr_sorted_with_columns = arr_sorted[:, inverse_col_ind]

    binary_values = np.packbits(
        arr_sorted_with_columns, axis=1).flatten()

    # Create a sorting index based on binary values and ordered_numbers
    sorting_index = np.lexsort((ordered_bit_counts, binary_values))

    # Sort the rows of the array based on the sorting index
    return arr_sorted_with_columns[sorting_index]


# array([[0, 1, 1],
#        [1, 0, 0],
#        [1, 1, 1]])


# array([[0, 1, 0],
#        [1, 0, 1],
#        [1, 1, 1]])

