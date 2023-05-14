
import numpy as np
from typing import List, Tuple


def minimize_binary_value(arr: np.ndarray) -> Tuple[np.ndarray, List[int], List[int]]:
    n, m = arr.shape
    optimization_variants = [(list(range(n)), list(range(m)))]  # initial state
    splits = [m]  # initial split at the end of the row

    def count_zeros(row: np.ndarray, splits: List[int]) -> Tuple[int, ...]:
        zeros = []
        prev_split = 0
        for split in splits:
            zeros.append((row[prev_split:split] == 0).sum())
            prev_split = split
        return tuple(zeros)

    def find_splits(row: np.ndarray, splits: List[int]) -> List[int]:
        row_as_int = row.astype(int)
        new_splits = list(np.where(np.diff(row_as_int) == 1)[0] + 1)
        # merge and sort old and new splits
        return sorted(list(set(splits + new_splits)))

    for i in range(n):
        new_variants = []
        for rows_indices, columns_indices in optimization_variants:
            # Rearrange the array according to the current indices
            temp_arr = arr[np.ix_(rows_indices, columns_indices)]
            zero_counts = [count_zeros(row, splits) for row in temp_arr[i:]]
            max_zeros_rows = np.array([
                idx + i for idx, zc in enumerate(zero_counts) if zc == max(zero_counts)])
            # Get unique max_zeros_rows
            _, idxs = np.unique(
                temp_arr[max_zeros_rows], axis=0, return_index=True)
            # Add all unique max_zeros_rows to new variants
            for max_zeros_row in max_zeros_rows[idxs]:
                new_rows_indices = rows_indices[:i] + [rows_indices[max_zeros_row]] + \
                    rows_indices[i:max_zeros_row] + \
                    rows_indices[max_zeros_row+1:]
                new_variants.append((new_rows_indices, columns_indices))
                if i > 0 and np.array_equal(temp_arr[new_rows_indices[i]], temp_arr[new_rows_indices[i-1]]):
                    break
        # Filter the new variants
        max_zero_count = max_zero_count = max([count_zeros(arr[np.ix_(x[0], x[1])][i], splits)
                                               for x in new_variants])
        optimization_variants = [x for x in new_variants if count_zeros(
            arr[np.ix_(x[0], x[1])][i], splits) == max_zero_count]
        print("variants after filter", len(optimization_variants))

        # Update splits and sort columns
        for j in range(len(optimization_variants)):
            rows_indices, columns_indices = optimization_variants[j]
            temp_arr = arr[np.ix_(rows_indices, columns_indices)]
            for start, end in zip([0] + splits, splits + [m]):
                # Sort columns in each part separately
                part_indices = np.argsort(temp_arr[i, start:end]).tolist()
                part_indices = [start + idx for idx in part_indices]
                columns_indices[start:end] = [columns_indices[idx]
                                              for idx in part_indices]
            # call find_splits on sorted part of the array
            splits = find_splits(temp_arr[i, columns_indices], splits)
            optimization_variants[j] = (rows_indices, columns_indices)

    # Return the best variant
    best_rows_indices, best_columns_indices = optimization_variants[0]
    return arr[np.ix_(best_rows_indices, best_columns_indices)], best_rows_indices, best_columns_indices


# Example usage
# arr = np.array([[1, 0, 1],
#                 [0, 1, 0],
#                 [0, 1, 0],
#                 [1, 1, 0],], dtype=bool)

# # minimized_arr, row_order, col_order = minimize_binary_value(arr)
# print(minimized_arr)


arr1 = np.array([[0, 1],
                [0, 1],
                 [1, 0],
                 [1, 1]], dtype=bool)
minimized_arr, row_order, col_order = minimize_binary_value(arr1)
print(minimized_arr)
arr2 = np.array([[0, 1],
                [1, 1],
                 [1, 0],
                 [1, 0]], dtype=bool)
minimized_arr, row_order, col_order = minimize_binary_value(arr2)
print(minimized_arr)
