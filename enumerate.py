from typing import Callable, Optional
from main_bfs import DAGSN, MAX_NODES
from nauty_canonic import get_canonical_form
import time


def enumerate_graphs(graph: DAGSN, nodes_count: Optional[int] = None):

    if not nodes_count:
        nodes_count = sum(1 for node in graph.nodes if node > 0)
    # Generate all possible tier_ups
    for idx1 in range(nodes_count):
        for idx2 in range(idx1 + 1, nodes_count):
            try:
                new_graph = graph.tier_up(idx1, idx2)
                yield new_graph
            except ValueError:
                pass

    # Generate all possible extensions
    for idx1 in range(nodes_count):
        for idx2 in range(idx1):
            try:
                new_graph = graph.extend(idx1, idx2)
                yield new_graph
            except ValueError:
                pass

    # Add a node to the first tier
    try:
        new_graph = graph.add_node_to_tier_1()
        yield new_graph
    except ValueError:
        pass


def main():
    graph = DAGSN()
    target_action_count = 13
    unique_graphs: list[dict[str, DAGSN]] = [
        {"": DAGSN()}]+[dict() for _ in range(target_action_count)]
    start_time = time.monotonic()
    for action_number in range(target_action_count):
        for graph in unique_graphs[action_number].values():
            for new_graph in enumerate_graphs(graph):
                unique_graphs[action_number +
                              1][get_canonical_form(new_graph)] = new_graph
    end_time = time.monotonic()
    # print the elapsed time with 6 decimal places
    print(f"Elapsed time: {end_time - start_time:.6f} seconds")

    # Reverse d1 and d2 so that keys become values and values become keys

    for i in range(target_action_count+1):
        print(
            f"actions{i} graphs: {len(unique_graphs[i])}")


if __name__ == "__main__":
    main()
