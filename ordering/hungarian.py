from typing import Tuple
import numpy as np


def subtract_arrays(a: np.ndarray, b: np.ndarray, L: np.ndarray) -> np.ndarray:
    result = np.zeros_like(a)
    borrow = np.zeros_like(a)

    for i in range(a.shape[0]-1, -1, -1):
        diff = a[i] - b[i] - borrow[i]

        if diff < 0:
            if abs(diff) > L[i]:
                raise ValueError("Subtraction would result in negative value")

            diff += L[i]
            borrow[i-1] = 1
        else:
            borrow[i-1] = 0

        result[i] = diff

    return result


def add_arrays(a: np.ndarray, b: np.ndarray, L: np.ndarray) -> np.ndarray:
    result = np.zeros_like(a)
    carry = 0

    for i in range(a.shape[0]-1, -1, -1):
        summation = a[i] + b[i] + carry

        if summation >= L[i]:
            carry = 1
            result[i] = summation - L[i]
        else:
            carry = 0
            result[i] = summation

    if carry > 0:
        raise ValueError("Addition would result in value exceeding limit")

    return result


def min_array(arrays: np.ndarray) -> np.ndarray:
    min_idx = np.lexsort(np.rot90(arrays, axes=(0, 1)))
    return arrays[min_idx[0]]


def calculate_L(cost_matrix: np.ndarray) -> np.ndarray:
    L = np.max(cost_matrix, axis=1)
    return np.sum(L, axis=0)+1


def augmenting_path(nc: int, cost: np.ndarray, u: np.ndarray, v: np.ndarray, path: np.ndarray, row4col: np.ndarray,
                    shortestPathCosts: np.ndarray, i: int, SR: np.ndarray, SC: np.ndarray,
                    remaining: np.ndarray, L: np.ndarray) -> Tuple[int, np.ndarray]:

    minVal: np.ndarray = np.zeros_like(L)
    num_remaining: int = nc
    remaining = np.arange(nc)[::-1]
    SR = np.zeros(nc, dtype=bool)
    SC = np.zeros(nc, dtype=bool)
    shortestPathCosts = np.full((nc, len(L)), np.inf)

    sink: int = -1
    while sink == -1:
        index: int = -1
        lowest: np.ndarray = np.full(len(L), np.inf)
        SR[i] = True

        for it in range(num_remaining):
            j: int = remaining[it]
            r: np.ndarray = subtract_arrays(add_arrays(
                minVal, cost[i, j], L), add_arrays(u[i], v[j], L), L)
            if np.array_equal(r, min_array(np.array([r, shortestPathCosts[j]]))):
                path[j] = i
                shortestPathCosts[j] = r

            if np.array_equal(shortestPathCosts[j], min_array(np.array([shortestPathCosts[j], lowest]))) or (np.array_equal(shortestPathCosts[j], lowest) and row4col[j] == -1):
                lowest = shortestPathCosts[j]
                index = it

        minVal = lowest
        if np.all(minVal == np.inf):  # infeasible cost matrix
            return -1, np.full(len(L), -1)

        j: int = remaining[index]
        if row4col[j] == -1:
            sink = j
        else:
            i = row4col[j]

        SC[j] = True
        remaining = np.delete(remaining, index)
        num_remaining -= 1

    return sink, minVal


def solve_rectangular_linear_sum_assignment(cost_matrix: np.ndarray, maximize: bool = False) -> Tuple[np.ndarray, np.ndarray]:
    nr: int
    nc: int
    nr, nc = cost_matrix.shape[0], cost_matrix.shape[1]

    # If necessary, transpose the cost matrix to make it square
    if nr < nc:
        cost_matrix = cost_matrix
        cost_matrix = cost_matrix.transpose((1, 0, 2))
        nr, nc = nc, nr

    # If necessary, negate the cost matrix to make the problem a minimization
    if maximize:
        cost_matrix = -cost_matrix

    # Calculate L
    L = calculate_L(cost_matrix)

    # Initialize variables
    u = np.zeros((nr, len(L)))
    v = np.zeros((nc, len(L)))
    shortestPathCosts = np.full((nc, len(L)), np.inf)
    path = np.full(nc, -1, dtype=np.int_)
    col4row = np.full(nr, -1, dtype=np.int_)
    row4col = np.full(nc, -1, dtype=np.int_)
    SR = np.zeros(nr, dtype=np.bool_)
    SC = np.zeros(nc, dtype=np.bool_)
    remaining = np.arange(nc)

    # Iteratively build the solution
    for curRow in range(nr):
        # Find an augmenting path from curRow to some column in the remaining set
        sink, minVal = augmenting_path(
            nc, cost_matrix, u, v, path, row4col, shortestPathCosts, curRow, SR, SC, remaining, L)
        if sink == -1:
            raise ValueError("Infeasible cost matrix")

        # Update dual variables
        u[curRow] = add_arrays(u[curRow], minVal, L)
        for i in range(nr):
            if SR[i] and i != curRow:
                u[i] = add_arrays(u[i], subtract_arrays(
                    minVal, shortestPathCosts[col4row[i]], L), L)
        for j in range(nc):
            if SC[j]:
                v[j] = subtract_arrays(v[j], subtract_arrays(
                    minVal, shortestPathCosts[j], L), L)

        # Augment the solution along the path from curRow to sink
        while True:
            i = path[sink]
            row4col[sink] = i
            col4row[i], sink = sink, col4row[i]
            if i == curRow:
                break

    # If the cost matrix was originally transposed, the solution is untransposed before it's returned
    if nr < nc:
        return row4col, np.arange(nr)
    else:
        return np.arange(nr), col4row


# cost_matrix = np.array([
#     [[1, 2, 1], [2, 3, 1], [4, 1, 3]],
#     [[4, 5, 6], [11, 18, 3], [5, 4, 6]],
#     [[7, 5, 9], [8, 9, 7], [23, 7, 9]]
# ])

# print(solve_rectangular_linear_sum_assignment(cost_matrix))
# array([1, 2, 0]
# [2, 3, 1]+[5, 4, 6]+[7, 5, 9]=14,12,16
# x, 1, 2

# 0, 2, 1 <=> [1, 2, 1]+[5, 4, 6]+[8, 9, 7]=14,15,14
# 2, 0, 1 <=> [4, 1, 3]+[4, 5, 6]+[8, 9, 7]=16,15,16
# 1, 2, 0 <=> [2, 3, 1]+[5, 4, 6]+[7, 5, 9]=14,12,16


# cost_matrix = np.array([[[0, 0, 0, 2, 0, 0],
#                          [0, 0, 0, 0, 2, 0],
#                          [0, 0, 0, 0, 0, 2]],

#                         [[1, 0, 0, 1, 0, 0],
#                          [0, 1, 0, 0, 1, 0],
#                          [0, 0, 1, 0, 0, 1]],

#                         [[1, 0, 0, 1, 0, 0],
#                          [0, 1, 0, 0, 1, 0],
#                          [0, 0, 1, 0, 0, 1]]])

# print(solve_rectangular_linear_sum_assignment(cost_matrix))


