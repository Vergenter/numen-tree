MAX_NODES=31
INT32_MAX = 2147483647
FIRST_TIER_NODE_VALUE= 1<<MAX_NODES

def bit(value:int, idx:int):
    return value&(1<<(idx))

def insert_0_bit(value:int,idx:int):
    """insert 0 into position idx moving earlier bits left"""
    mask = (1 << idx) - 1
    # limit for INT32_MAX to prevent python from increasing type size
    # it should be correct for first tiers, because they should be never insert_0_bit
    return ((value & mask) | ((value & ~mask) << 1)) & INT32_MAX

def count_set_bits(value:int,start:int,end:int):
    """return number of bits that is set for value from start inclusive to end exclusive"""
    mask = (1 << end) - (1 << start)
    return bin(value & mask).count('1')

"""Maximal number of nodes supported by graph"""
class DAGSN:
    def __init__(self,nodes:list[int]=[0]*MAX_NODES,tier_bounds:list[int] = [0,2,6,14,30]):
        
        self.nodes:list[int] = nodes
        """
        REQUIREMENTS nodes<32 for int32 and nodes<64 for int64
        it's array of ints
        where bit of index i defines that node of index i is parent of this node 
        nodes are ordered by tier
        last bit is set if node is 1st tier
        Default state is all zeros
        """
        self.tier_bounds:list[int] = tier_bounds
        """
        tier_bounds are dynamic 
        for example if there are more that two 1st tier nodes, 
        all bounds from index 1 should be moved by number of additional tier 1's
        default values are calculated by minimal number of lower tier required for tier T defined by equation 2**(T)
        """

    def insert_node(self,tier:int,value:int=FIRST_TIER_NODE_VALUE):
        """tier is counted from 0"""
        new_nodes = self.nodes.copy()
        new_tier_bounds= self.tier_bounds.copy()
        # reserverd node limit not reached
        if not new_nodes[new_tier_bounds[tier+1]-1]:
            # can be optimized to binary search
            for x in range(new_tier_bounds[tier+1]-1,new_tier_bounds[tier],-1):
                # add node to x position if next node is set
                if new_nodes[x-1]>0:
                    new_nodes[x]=value
                    break
            else: 
                # add node to new_tier_bounds[tier] position if there is no nodes in tier
                new_nodes[new_tier_bounds[tier]]= value
        else: # reserverd node limit reached
            # move all nodes of tier+1 to make place for new node of tier
            for i in range(len(new_nodes)-1,new_tier_bounds[tier+1],-1):
                if new_nodes[i-1]:
                    new_nodes[i] = insert_0_bit(new_nodes[i-1],new_tier_bounds[tier+1])
            # move parents bits to work correctly with move nodes
            for i in range(tier+1,(len(new_tier_bounds))):
                new_tier_bounds[i]+=1
            # add new node in newly created place
            new_nodes[new_tier_bounds[tier+1]-1]=value
        return DAGSN(new_nodes,new_tier_bounds)

    def add_node_to_tier_1(self):
        return self.insert_node(0,FIRST_TIER_NODE_VALUE)

    def get_tier(self,idx:int):
        for tier,(start,end) in enumerate(zip(self.tier_bounds,self.tier_bounds[1:])):
            if start<=idx<end:
                return tier
        raise ValueError("index out of tier bound ")



    def tier_up(self,idx1:int,idx2:int):
        if idx1==idx2:
            raise ValueError("nodes for tier_up must be different")
        tier = self.get_tier(idx1)
        if tier!=self.get_tier(idx2):
            raise ValueError("nodes for tier_up must have same tier")
        both = self.nodes[idx1] | self.nodes[idx2]
        for checked_tier in range(tier-1,-1,-1):
            min_correct = 2*(2**tier-checked_tier)
            count = count_set_bits(both,start=self.tier_bounds[checked_tier],end=self.tier_bounds[checked_tier+1])
            if count<min_correct:
                raise ValueError("nodes have not enough childrens to tier up")
        
        return self.insert_node(tier+1,both | (1<<idx1) | (1<<idx2))

    def extend(self,idx1:int,idx2:int):
        if idx1==idx2:
            raise ValueError("nodes for extend must be different")

        tier = self.get_tier(idx1)
        if tier!=self.get_tier(idx2)+1:
            raise ValueError("nodes for extend should have idx1 skill node with one tier higher than idx2")

        both = self.nodes[idx1] | self.nodes[idx2] | (1<<idx2)
        # parents_new_idx1 is always 3 if multiple extension from same parents is enabled
        # but currently is not
        parents_new_idx1=count_set_bits(self.nodes[idx1],self.tier_bounds[tier-1],self.tier_bounds[tier])+1
        for checked_tier in range(tier-1,-1,-1):
            min_correct = parents_new_idx1*(2**tier-checked_tier-1)
            count = count_set_bits(both,start=self.tier_bounds[checked_tier],end=self.tier_bounds[checked_tier+1])
            if count<min_correct:
                raise ValueError("nodes have not enough childrens to extend")
            
        new_nodes = self.nodes.copy()

        new_nodes[idx1]=both
        for x in range(self.tier_bounds[tier+1],len(new_nodes)):
            if new_nodes[x] and bit(new_nodes[x],idx1):
                new_nodes[x]|=both
        
        return DAGSN(new_nodes,self.tier_bounds)
        
    def get_canonical_form(self) -> str:
        # Initialize an empty list to hold the ordered tiers
        ordered_tiers = []

        # add all first tiers indegree for connection to root node(that doesn't exist)
        # as all first tiers are same we can write them as single value 
        ordered_tiers.append(len([1 for node in self.nodes[self.tier_bounds[0]:self.tier_bounds[1]] if node]))
        ordered_tiers.append('|')
        # add sorted indegree for all next tiers
        for tier,(start_tier, end_tier) in enumerate(zip(self.tier_bounds[1:-1], self.tier_bounds[2:])): 
            ordered_tiers.extend(sorted([sum(bit(node,node_idx)>0 for node in self.nodes[start_tier:end_tier]) for node_idx in range(self.tier_bounds[tier],self.tier_bounds[tier+1]) if self.nodes[node_idx]])) 
            ordered_tiers.append('|')

        return "".join([str(node) for node in ordered_tiers])

    def __str__(self):
        return self.get_canonical_form()


print(DAGSN().add_node_to_tier_1())