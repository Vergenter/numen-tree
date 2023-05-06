import numpy as np
from scipy.optimize import linear_sum_assignment


def bit_difference(col1, col2):
    return np.sum(col1 != col2)


def best_matches(arr1):
    arr1_sorted = arr1[np.argsort(np.sum(arr1, axis=1))]

    n = arr1_sorted.shape[0]
    cost_matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            target_col = np.zeros(n)
            target_col[-(j+1):] = 1
            cost_matrix[i, j] = bit_difference(arr1_sorted[:, i], target_col)
    print(cost_matrix)
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    inverse_col_ind = np.argsort(col_ind)
    arr1_optimal = arr1_sorted[:, inverse_col_ind]

    return arr1_optimal
    # [3,2,1,0]
    # [0,1,2,3]
    # [2,1,0,1]
    # [1,0,1,2]
    # for i in range(n):
    #     for j in range(n):
    #         cost_matrix[i, j] = bit_difference(
    #             arr1_sorted_transposed[i], target_array[:, j])

    # row_ind, col_ind = linear_sum_assignment(cost_matrix)
    # arr1_optimal = arr1_sorted_transposed[col_ind].T

    # return arr1_optimal


# arr1 = np.array([[1, 1, 1, 1], [1, 0, 1, 1], [1, 0, 1, 0], [1, 0, 0, 0]])
# result = best_matches(arr1)
# print(result)
