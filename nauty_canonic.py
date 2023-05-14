import pynauty
from main_bfs import DAGSN


def dag_to_pynauty(graph: DAGSN) -> pynauty.Graph:
    """Convert DAGSN graph to networkx.DiGraph."""
    vertex_coloring = [{idx for tier in range(0, graph.get_top_tier()+1, 2) for idx in range(graph.tier_bounds[tier], graph.find_first_empty_cell(
        tier))}, {idx for tier in range(1, graph.get_top_tier()+1, 2) for idx in range(graph.tier_bounds[tier], graph.find_first_empty_cell(
            tier))}]
    vertex_coloring = [{idx for idx in range(graph.tier_bounds[tier], graph.find_first_empty_cell(
        tier))} for tier in range(graph.get_top_tier()+1)]

    adjacency_dict = {idx: graph.get_children_for_index(
        idx) for idx, node in enumerate(graph.nodes) if node != 0}
    number_of_vertices = len([node for node in graph.nodes if node > 0])
    g = pynauty.Graph(number_of_vertices=number_of_vertices, directed=False,
                      adjacency_dict=adjacency_dict, vertex_coloring=vertex_coloring)
    return g


def get_canonical_form(graph: DAGSN) -> str:
    """Return the canonical form of the graph using pynauty."""
    canonical_labeling = pynauty.certificate(dag_to_pynauty(graph))
    return "".join(str(node) for node in canonical_labeling)
