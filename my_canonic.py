from main_bfs import DAGSN
import numpy as np


def canonic(arr: np.ndarray):
    # Step 1: Sort rows by number of set bits in row
    arr_sorted = arr[np.argsort(np.sum(arr, axis=1))]
    set_bits_rows = np.sum(arr_sorted, axis=1)

    # Step 2: Sort columns by count of set bits in column in rows with same number of bits
    unique_set_bits = np.unique(set_bits_rows)
    num_unique_set_bits = unique_set_bits.size
    col_counts = np.zeros(
        (arr_sorted.shape[1], num_unique_set_bits), dtype=int)
    for i in range(arr_sorted.shape[0]):
        row_set_bits = set_bits_rows[i]
        for j in range(arr_sorted.shape[1]):
            col_counts[j, np.where(unique_set_bits == row_set_bits)[
                0][0]] += arr_sorted[i, j]

    order = np.lexsort([col_counts[:, i]
                       for i in range(col_counts.shape[1] - 1, -1, -1)])
    arr_col_optimal = arr_sorted[:, order]

    # Step 3: Sort rows by number of set bits in row and by value
    arr_with_bits = np.c_[set_bits_rows, arr_col_optimal]
    order = np.lexsort([arr_with_bits[:, i]
                       for i in range(arr_with_bits.shape[1] - 1, -1, -1)])

    # Step 4: Return the resulting array
    canonical = arr_col_optimal[order]
    return canonical


def dag_to_biadjacency_matrix(graph: DAGSN) -> np.ndarray:
    """Convert DAGSN graph"""
    arr = np.zeros((32, 32))
    row = 0
    column = 0
    for idx, node in enumerate(graph.nodes):
        if node == 0:
            continue
        tier = graph.get_tier(idx)
        if tier % 2 == 0:
            row += 1
            # append node
            if tier > 0:
                # add its children to iself
                pass
        else:
            # apppend itself to children
            pass

    graph
    # for each node get its children
    # and bipartite it
    # even layers is rows
    # odd layer is rows
    # it will be bound to 32x32
    return g


def get_canonical_form(graph: DAGSN) -> str:
    """Return the canonical form of the graph using pynauty."""
    canonical_labeling = pynauty.certificate(dag_to_pynauty(graph))
    return "".join(str(node) for node in canonical_labeling)
