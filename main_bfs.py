from typing import Tuple


MAX_NODES = 31


def bit(value: int, idx: int) -> int:
    """Return the bit value at the given index in the node value."""
    return value & (1 << (idx))


def insert_0_bit(value: int, idx: int) -> int:
    """Insert a 0 bit into the specified position, shifting earlier bits left."""
    mask = (1 << idx) - 1
    # This should be correct for first tiers, because they should never use insert_0_bit.
    return ((value & mask) | ((value & ~mask) << 1))


def count_set_bits(value: int, start_index: int, end_index: int) -> int:
    """Count the number of bits that are set for the given value from start_index (inclusive) to end_index (exclusive)."""
    mask = (1 << end_index) - (1 << start_index)
    return bin(value & mask).count('1')


"""Maximal number of nodes supported by graph"""


class DAGSN:
    """A directed acyclic graph with support for tiering up and extending nodes."""

    def __init__(self, nodes: list[int] = [0]*MAX_NODES, tier_bounds: list[int] = [0, 2, 6, 14, 30, MAX_NODES]):
        """
        Initialize a new DAGSN instance.

        nodes: A list of ints representing the nodes in the graph.
               Each bit of an index i defines that node of index i is a parent of this node.
               Nodes are ordered by tier.
               The default state is all zeros.

        tier_bounds: A list of ints representing the boundaries between the different tiers of nodes.
                     The default values are calculated by the minimal number of lower tiers required for tier T,
                     defined by the equation 2**(T) and ended by MAX_NODES.
        """

        self.nodes: list[int] = nodes
        self.tier_bounds: list[int] = tier_bounds

    def find_first_empty_cell(self, tier: int) -> int:
        """
        Find the index of the first empty cell (value 0) in the specified tier of nodes,
        where an empty cell implies that all subsequent cells are also empty.

        This function uses a binary search algorithm, which has a time complexity of O(log N),
        where N is the size of the search range.

        Parameters:
        tier (int): The tier to search for the first empty cell.

        Returns:
        int: The index of the first empty cell in the specified tier. If no empty cell is found,
             the function returns the index equal to the right boundary of the tier.
        """
        left = self.tier_bounds[tier]
        right = self.tier_bounds[tier + 1]

        while left < right:
            mid = left + (right - left) // 2
            if self.nodes[mid] == 0:
                right = mid
            else:
                left = mid + 1

        return left

    def get_top_tier(self) -> int:
        """Find highest tier with nodes"""

        # If there are no nodes, return -1 as the highest tier
        if not any(self.nodes):
            return -1

        left, right = 0, len(self.tier_bounds) - 2
        while left <= right:
            mid = (left + right) // 2
            if self.nodes[self.tier_bounds[mid]] and not self.nodes[self.tier_bounds[mid+1]]:
                return mid
            elif self.nodes[self.tier_bounds[mid]]:
                left = mid + 1
            else:
                right = mid - 1

        # If there are no nodes in the tiers except the first one, return 0 as the highest tier
        return 0

    def insert_node(self, tier: int, value: int) -> "DAGSN":
        """Insert a new node into the specified tier with the given value."""
        if tier >= len(self.tier_bounds)-1:
            raise ValueError("Tier too high, cannot insert node.")
        new_nodes = self.nodes.copy()
        new_tier_bounds = self.tier_bounds.copy()

        def is_tier_full(next_tier_bound: int, nodes: list[int]):
            return nodes[next_tier_bound-1] > 0
        try:
            tier_after_empty_tier_bound = next((tier_for_end_bound for tier_for_end_bound in range(
                tier+1, len(new_tier_bounds)) if not is_tier_full(new_tier_bounds[tier_for_end_bound], new_nodes)))
        except StopIteration:
            raise ValueError("Added too many nodes, MAX_NODES exceeded.")
        # Reserverd node limit not reached
        if tier_after_empty_tier_bound == tier+1:
            new_nodes[self.find_first_empty_cell(tier)] = value
        else:
            # Reserved node limit reached, move all nodes of tier+1 to make space for new node of tier
            new_node_insert_position = new_tier_bounds[tier+1]
            for i in range(new_tier_bounds[tier_after_empty_tier_bound]-1, new_node_insert_position, -1):
                if new_nodes[i-1]:
                    # Move parents bits to work correctly with moved nodes
                    new_nodes[i] = insert_0_bit(
                        new_nodes[i-1], new_node_insert_position)
            for i in range(new_tier_bounds[tier_after_empty_tier_bound], len(new_nodes)):
                # Move parents bits to work correctly with moved nodes
                new_nodes[i] = insert_0_bit(
                    new_nodes[i], new_node_insert_position)
            # Add new node in newly created place
            new_nodes[new_node_insert_position] = value
            for i in range(tier+1, tier_after_empty_tier_bound):
                new_tier_bounds[i] += 1
        return DAGSN(new_nodes, new_tier_bounds)

    def add_node_to_tier_1(self) -> "DAGSN":
        """Add a new node to the first tier of the graph."""
        return self.insert_node(0, 1 << self.find_first_empty_cell(0))

    def get_tier(self, idx: int) -> int:
        """Return the tier of the node at the specified index."""
        for tier, (start, end) in enumerate(zip(self.tier_bounds, self.tier_bounds[1:])):
            if start <= idx < end:
                return tier
        raise ValueError("Index out of tier bound ")

    def check_separation(self, value: int, tier: int, nodes_count=2):
        """
        Check if the nodes at the specified tier have enough children to tier up.

        value: The bitwise OR of the parent nodes

        tier: The tier to check.

        nodes_count: The number of required skills for the tier up check.

        Returns: True if the nodes at the specified tier have enough children to tier up, False otherwise.
        """
        for checked_tier in range(tier-1, -1, -1):
            min_correct = nodes_count*(2**(tier-checked_tier-1))
            count = count_set_bits(
                value, start_index=self.tier_bounds[checked_tier], end_index=self.tier_bounds[checked_tier+1])
            if count < min_correct:
                return False
        return True

    def tier_up(self, idx1: int, idx2: int) -> "DAGSN":
        """
        Tier up the nodes at the specified indices.

        idx1: The index of the first node to tier up.

        idx2: The index of the second node to tier up.

        Returns: A new DAGSN instance with the nodes at the specified indices tiered up.
        """
        if idx1 == idx2:
            raise ValueError("Nodes for tier_up must be different.")
        if self.nodes[idx1] == 0 or self.nodes[idx2] == 0:
            raise ValueError("Nodes has to exist.")
        tier = self.get_tier(idx1)
        if tier != self.get_tier(idx2):
            raise ValueError("Nodes for tier_up must have same tier.")
        both = (self.nodes[idx1] | self.nodes[idx2] |
                (1 << idx1) | (1 << idx2))
        # Required number of skills for tier up check
        NODES_COUNT_FOR_CHECKING_SEPARATION = 2
        if not self.check_separation(both, tier+1, NODES_COUNT_FOR_CHECKING_SEPARATION):
            raise ValueError("Nodes have not enough childrens to tier up.")

        return self.insert_node(tier+1, both)

    def extend(self, idx1: int, idx2: int) -> "DAGSN":
        """
        Extend the node at the specified index with the node at the higher tier index.

        idx1: The index of the node to extend.

        idx2: The index of the higher tier node to extend with.

        Returns: A new DAGSN instance with the node at the specified index extended.
        """
        if idx1 == idx2:
            raise ValueError("Nodes for extend must be different.")
        if self.nodes[idx1] == 0 or self.nodes[idx2] == 0:
            raise ValueError("Nodes has to exist.")
        tier = self.get_tier(idx1)
        if tier != self.get_tier(idx2)+1:
            raise ValueError(
                "Nodes for extend should have idx1 skill node with one tier higher than idx2.")

        both = (self.nodes[idx1] | self.nodes[idx2] | (1 << idx2))
        # parents_new_idx1 is always 3 if multiple extension from same parents is enabled
        # but currently is not
        parents_count = count_set_bits(
            self.nodes[idx1], self.tier_bounds[tier-1], self.tier_bounds[tier])+1
        if not self.check_separation(both, tier, parents_count):
            raise ValueError("nodes have not enough childrens to extend")

        new_nodes = self.nodes.copy()

        new_nodes[idx1] = both
        for x in range(self.tier_bounds[tier+1], len(new_nodes)):
            if new_nodes[x] and bit(new_nodes[x], idx1):
                new_nodes[x] |= both

        return DAGSN(new_nodes, self.tier_bounds)

    def get_canonical_form(self) -> str:
        def is_sorted(list: list[Tuple[int, int]]):
            return all(list[i] <= list[i+1] for i in range(len(list)-1))

        def swap_bits(value: int, order: list[Tuple[int, int]]):
            value_cpy = value
            for destination, (source, _) in enumerate(order, self.tier_bounds[tier]):
                value &= ~(1 << destination)
                value |= (source > destination) and \
                    ((value_cpy & (1 << source)) >> (source - destination))
                value |= (source <= destination) and \
                    ((value_cpy & (1 << source)) << (destination-source))
            return value

        new_nodes = self.nodes.copy()
        first_empty_tier = self.get_top_tier()+1
        first_empty_node = self.find_first_empty_cell(first_empty_tier-1)
        are_nodes_sorted = False
        while not are_nodes_sorted:
            are_nodes_sorted = True
            for tier in range(first_empty_tier):
                sorted_indices = sorted(enumerate(
                    new_nodes[self.tier_bounds[tier]:self.tier_bounds[tier+1]], self.tier_bounds[tier]), key=lambda x: x[1])
                # sort must be stable!
                are_nodes_sorted &= is_sorted(sorted_indices)
                if not are_nodes_sorted:
                    # reoreder first tiers by sorted_indices
                    new_nodes[self.tier_bounds[tier]:self.tier_bounds[tier+1]
                              ] = list(map(lambda x: x[1], sorted_indices))
                    for i in range(0, self.tier_bounds[tier]):
                        new_nodes[i] = swap_bits(new_nodes[i], sorted_indices)
                    for i in range(self.tier_bounds[tier+1], self.find_first_empty_cell(first_empty_tier-1)):
                        new_nodes[i] = swap_bits(new_nodes[i], sorted_indices)
        return "|".join([str(node) for node in new_nodes])

    def __str__(self):
        """Return a string representation of DAGSN"""
        return self.get_canonical_form()
