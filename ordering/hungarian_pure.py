import numpy as np
from typing import Tuple


def augmenting_path(nc: int, cost: np.ndarray, u: np.ndarray, v: np.ndarray, path: np.ndarray, row4col: np.ndarray,
                    shortestPathCosts: np.ndarray, i: int, SR: np.ndarray, SC: np.ndarray,
                    remaining: np.ndarray) -> Tuple[int, float]:

    minVal: float = 0
    num_remaining: int = nc
    remaining = np.arange(nc)[::-1]
    SR = np.zeros(nc, dtype=bool)
    SC = np.zeros(nc, dtype=bool)
    shortestPathCosts = np.full(nc, np.inf)

    sink: int = -1
    while sink == -1:
        index: int = -1
        lowest: float = np.inf
        SR[i] = True

        for it in range(num_remaining):
            j: int = remaining[it]
            r: float = minVal + cost[i, j] - u[i] - v[j]
            if r < shortestPathCosts[j]:
                path[j] = i
                shortestPathCosts[j] = r

            if shortestPathCosts[j] < lowest or (shortestPathCosts[j] == lowest and row4col[j] == -1):
                lowest = shortestPathCosts[j]
                index = it

        minVal = lowest
        if minVal == np.inf:  # infeasible cost matrix
            return -1, -1

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
    nr, nc = cost_matrix.shape

    # If necessary, transpose the cost matrix to make it square
    if nr < nc:
        cost_matrix = cost_matrix.T
        nr, nc = nc, nr

    # If necessary, negate the cost matrix to make the problem a minimization
    if maximize:
        cost_matrix = -cost_matrix

    # Initialize variables
    u = np.zeros(nr)
    v = np.zeros(nc)
    shortestPathCosts = np.full(nc, np.inf)
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
            nc, cost_matrix, u, v, path, row4col, shortestPathCosts, curRow, SR, SC, remaining)
        if sink == -1:
            raise ValueError("Infeasible cost matrix")

        # Update dual variables
        u[curRow] += minVal
        for i in range(nr):
            if SR[i] and i != curRow:
                u[i] += minVal - shortestPathCosts[col4row[i]]
        for j in range(nc):
            if SC[j]:
                v[j] -= minVal - shortestPathCosts[j]

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


cost_matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(solve_rectangular_linear_sum_assignment(cost_matrix))
# Expected Output: (array([0, 1, 2]), array([0, 1, 2]))
cost_matrix = np.array([[1, 3, 2], [2, 3, 1], [2, 1, 3]])
print(solve_rectangular_linear_sum_assignment(cost_matrix))
# Expected Output: (array([0, 1, 2]), array([0, 2, 1]))
cost_matrix = np.array([[4, 1, 3], [2, 0, 5], [3, 2, 2]])
print(solve_rectangular_linear_sum_assignment(cost_matrix))
# Expected Output: (array([0, 1, 2]), array([1, 0, 2]))
cost_matrix = np.array([[10, 10, 8], [9, 8, 1], [9, 7, 4]])
print(solve_rectangular_linear_sum_assignment(cost_matrix, maximize=True))
# Expected Output: (array([0, 1, 2]), array([2, 1, 0]))
