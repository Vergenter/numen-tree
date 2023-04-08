import unittest
from main_bfs import DAGSN

from typing import Callable, TypeVar

T = TypeVar('T')

def repeat(G: T, method: Callable[[T], T], n: int) -> T:
    """Apply the given method to the given object n times.

    Args:
        G: The initial object to apply the method to.
        method: A callable method that takes an object of the same type as G and returns an updated object.
        n: The number of times to apply the method to G.

    Returns:
        The object G after the method has been applied n times.
    """
    for i in range(n):
        G = method(G)
    return G


class DAGSN_tier_up_test(unittest.TestCase):
    def test_single(self):
        g1 = DAGSN().add_node_to_tier_1().add_node_to_tier_1()
        self.assertEqual(g1.nodes[g1.tier_bounds[1]],0)
        g1=g1.tier_up(0, 1)
        self.assertGreater(g1.nodes[g1.tier_bounds[1]],0)

    def test_multiple(self):
        g1 = DAGSN().add_node_to_tier_1().add_node_to_tier_1()
        self.assertEqual(g1.nodes[g1.tier_bounds[1]],0)
        self.assertEqual(g1.nodes[g1.tier_bounds[1]+1],0)
        g1=g1.tier_up(0, 1)
        self.assertGreater(g1.nodes[g1.tier_bounds[1]],0)
        self.assertEqual(g1.nodes[g1.tier_bounds[1]+1],0)
        g1=g1.tier_up(0, 1)
        self.assertGreater(g1.nodes[g1.tier_bounds[1]],0)
        self.assertGreater(g1.nodes[g1.tier_bounds[1]+1],0)

    def test_tier_up_to_tier_3(self):
        g1 = repeat(DAGSN(),DAGSN.add_node_to_tier_1,4).tier_up(0, 1).tier_up(2, 3)
        self.assertEqual(g1.nodes[g1.tier_bounds[2]],0)
        g1=g1.tier_up(4, 5)
        self.assertGreater(g1.nodes[g1.tier_bounds[2]],0)

    def test_tier_up_to_tier_4(self):
        g1 = repeat(DAGSN(),DAGSN.add_node_to_tier_1,8)\
            .tier_up(0, 1).tier_up(2, 3).tier_up(4, 5).tier_up(6, 7)\
            .tier_up(8, 9).tier_up(10, 11)
        self.assertEqual(g1.nodes[g1.tier_bounds[3]],0)
        g1=g1.tier_up(12, 13)
        self.assertGreater(g1.nodes[g1.tier_bounds[3]],0)

    def test_tier_up_move_correctly(self):
        g1 = DAGSN().add_node_to_tier_1().add_node_to_tier_1()
        tier = 1 # counted from 0
        number_of_tier_up = 3
        self.assertTrue(all(node==0 for node in g1.nodes[g1.tier_bounds[tier]:g1.tier_bounds[tier]+number_of_tier_up]))
        g1 = g1.tier_up(0, 1).tier_up(0, 1).tier_up(0, 1)
        self.assertTrue(all(node>0 for node in g1.nodes[g1.tier_bounds[tier]:g1.tier_bounds[tier]+number_of_tier_up]))
        g1 = g1.add_node_to_tier_1().add_node_to_tier_1()
        self.assertTrue(all(node>0 for node in g1.nodes[g1.tier_bounds[tier]:g1.tier_bounds[tier]+number_of_tier_up]))

    def test_mixed_tier_up_and_moving(self):
        g1 = DAGSN().add_node_to_tier_1().add_node_to_tier_1()
        tier = 1 # counted from 0
        number_of_tier_up = 2
        self.assertTrue(all(node==0 for node in g1.nodes[g1.tier_bounds[tier]:g1.tier_bounds[tier]+number_of_tier_up]))
        g1 = g1.tier_up(0, 1).tier_up(0, 1)
        self.assertTrue(all(node>0 for node in g1.nodes[g1.tier_bounds[tier]:g1.tier_bounds[tier]+number_of_tier_up]))
        self.assertEqual(g1.nodes[g1.tier_bounds[tier]+3],0)
        g1 = g1.add_node_to_tier_1().add_node_to_tier_1()
        self.assertTrue(all(node>0 for node in g1.nodes[g1.tier_bounds[tier]:g1.tier_bounds[tier]+number_of_tier_up]))
        g1 = g1.tier_up(1, 2)
        self.assertTrue(all(node>0 for node in g1.nodes[g1.tier_bounds[tier]:g1.tier_bounds[tier]+number_of_tier_up+1]))

        
class DAGSN_canonical(unittest.TestCase):

    def test_get_canonical_form_1(self):
        g1= DAGSN().add_node_to_tier_1().add_node_to_tier_1().tier_up(0,1).add_node_to_tier_1().extend(3,2).add_node_to_tier_1()
        g2 = DAGSN().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().tier_up(0,2).add_node_to_tier_1().extend(4,3)
        self.assertEqual(str(g1), str(g2))

    def test_get_canonical_form_2(self):
        g3= DAGSN().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().tier_up(0, 1).tier_up(0, 1)
        g4= DAGSN().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().tier_up(0, 1).tier_up(1, 2)
        self.assertNotEqual(str(g3),str(g4))

    def test_get_canonical_form_3(self):
        g3= DAGSN().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().tier_up(0, 1).tier_up(0, 1)
        g4= DAGSN().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().tier_up(0, 1).tier_up(1, 2)
        self.assertNotEqual(str(g3),str(g4))

    def test_get_canonical_form_4(self):
        g1= DAGSN().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().tier_up(0, 1).extend(4, 2).extend(4, 3)
        g2= DAGSN().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().tier_up(0, 1).tier_up(2, 3)
        self.assertNotEqual(str(g1),str(g2))

    def test_get_canonical_form_5(self):
        g1= DAGSN().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1()\
            .tier_up(0, 1).tier_up(2, 3).tier_up(4, 5).extend(9,6)\
            .tier_up(7,8) # tier_up skill without extension
        g2= DAGSN().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1()\
            .tier_up(0, 1).tier_up(2, 3).tier_up(4, 5).extend(9,6)\
            .tier_up(8,9) # tier_up skill with extension
        self.assertNotEqual(str(g1),str(g2))

    def test_get_canonical_form_6(self):
        g1= DAGSN().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1()\
            .tier_up(0, 1).tier_up(0, 1).tier_up(2, 3).tier_up(4, 5)\
            .tier_up(6,8) # tier_up skill that have exactly same copy
        
        g2= DAGSN().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1()\
            .tier_up(0, 1).tier_up(0, 1).tier_up(2, 3).tier_up(4, 5)\
            .tier_up(8,9) # tier_up skills that are unique
        self.assertNotEqual(str(g1),str(g2))

    def test_get_canonical_form_7(self):
        # test if structural differences are differenciated
        g1= DAGSN().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1()\
            .tier_up(0, 1).extend(4, 2).tier_up(2, 3).tier_up(1, 3) # both tier up have different node from tier up with extension
        
        g2= DAGSN().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1()\
            .tier_up(0, 1).extend(4, 2).tier_up(0, 2).tier_up(1, 3) # one tier up contained in other with extension
        self.assertNotEqual(str(g1),str(g2))

    def test_get_canonical_form_8(self):
        # test if structural differences are differenciated between multiple tier tier3 tier to tier4 diff in tier 2
        g1= repeat(DAGSN(),DAGSN.add_node_to_tier_1,13)\
            .tier_up(0,1).extend(13,2).tier_up(3,4).tier_up(5,6).tier_up(7,8).tier_up(9,10).tier_up(11,12)\
            .tier_up(13,14).tier_up(15,16).tier_up(17,18)\
            .tier_up(19,20) # tier up from skill that tier_up from extended node
            
        g2= repeat(DAGSN(),DAGSN.add_node_to_tier_1,13)\
            .tier_up(0,1).extend(13,2).tier_up(3,4).tier_up(5,6).tier_up(7,8).tier_up(9,10).tier_up(11,12)\
            .tier_up(13,14).tier_up(15,16).tier_up(17,18)\
            .tier_up(20,21) # tier up from tier ups that aren't from extended node
        self.assertNotEqual(str(g1),str(g2))


class DAGSNTest(unittest.TestCase):

    def test_add_node_to_tier_1(self):
        g1 = DAGSN()
        self.assertEqual(g1.nodes[g1.tier_bounds[0]],0)
        g1=g1.add_node_to_tier_1()
        self.assertGreater(g1.nodes[g1.tier_bounds[0]],0)

    def test_extend(self):
        g1 = DAGSN().add_node_to_tier_1().add_node_to_tier_1()\
        .tier_up(0, 1).add_node_to_tier_1()\
        .extend(3, 2)\
        .add_node_to_tier_1()\
        .extend(4, 3)
        self.assertTrue(g1.nodes[g1.tier_bounds[1]]>0 and g1.nodes[g1.tier_bounds[1]+1]==0)
        with self.assertRaises(ValueError):
            g1.extend(g1.tier_bounds[1],g1.tier_bounds[1])
        with self.assertRaises(ValueError):
            g1.extend(g1.tier_bounds[1],g1.tier_bounds[1]+1)
        with self.assertRaises(ValueError):
            g1.extend(g1.tier_bounds[1],g1.tier_bounds[1]-1)

    def test_get_tier(self):
        g1 = DAGSN().add_node_to_tier_1().add_node_to_tier_1().tier_up(0, 1).add_node_to_tier_1().extend(3, 2).add_node_to_tier_1().extend(4, 3)
        self.assertEqual(g1.get_tier(0), 0)
        self.assertEqual(g1.get_tier(1), 0)
        self.assertEqual(g1.get_tier(2), 0)
        self.assertEqual(g1.get_tier(3), 0)
        self.assertEqual(g1.get_tier(4), 1)

    def test_example_player_tree_1(self):
        DAGSN().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1()\
        .tier_up(0, 1).tier_up(3, 4).extend(7,2).tier_up(4,5).tier_up(4,5)\
        .tier_up(6,7).tier_up(7,9).tier_up(7,9)

    def test_example_player_tree_2(self):
        DAGSN().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1()\
        .tier_up(0, 1).tier_up(0, 1).tier_up(2,3).tier_up(4,5).tier_up(4,5)\
        .tier_up(6,8).tier_up(7,8).tier_up(7,9).tier_up(8,10)
        

    def test_example_player_tree_3(self):
        DAGSN().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1()\
        .tier_up(1, 2).extend(4,0).tier_up(1, 2).extend(5,3).tier_up(0,3).tier_up(0,3)\
        .tier_up(4,5).tier_up(5,7)



if __name__ == '__main__':
    unittest.main()


    # g1 = DAGSN().add_node_to_tier_1().add_node_to_tier_1().tier_up(0,1).add_node_to_tier_1().extend(3,2).add_node_to_tier_1()
# print(g1)
# g2 = DAGSN().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().tier_up(0,2).add_node_to_tier_1().extend(4,3)
# print(g2)