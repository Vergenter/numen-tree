import main_bfs
import numpy as np
import ordering.hungarianord as hunord


def dag_to_biadjacency_matrix(graph: main_bfs.DAGSN) -> np.ndarray:
    """Convert DAGSN graph"""
    arr = np.zeros((32, 32), dtype=int)
    row = 0
    row_map = {}
    column = 0
    column_map = {}
    for idx, node in enumerate(graph.nodes):
        if node == 0:
            continue
        tier = graph.get_tier(idx)
        if tier % 2 == 0:
            row_map[idx] = row
            # append node
            if tier > 0:
                for child in graph.get_children_for_index(idx):
                    arr[row][column_map[child]] = 1
            row += 1
        else:
            column_map[idx] = column

            for child in graph.get_children_for_index(idx):
                arr[row_map[child]][column] = 1
            # apppend itself to children
            column += 1
    return arr[:row, :max(1, column)]


def get_canonical_form(graph: main_bfs.DAGSN) -> str:
    """Return the canonical form of the graph using pynauty."""
    result = str(hunord.get_minimized(dag_to_biadjacency_matrix(graph)))
    return result
