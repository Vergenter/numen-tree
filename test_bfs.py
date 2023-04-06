import unittest
from main_bfs import DAGSN

class DAGSNTest(unittest.TestCase):

    def test_add_node_to_tier_1(self):
        g1 = DAGSN().add_node_to_tier_1()
        self.assertEqual(str(g1), '1|||')

    def test_tier_up(self):
        g1 = DAGSN().add_node_to_tier_1().add_node_to_tier_1().tier_up(0, 1).add_node_to_tier_1()
        self.assertEqual(str(g1), '3|2||')
        g2= DAGSN().add_node_to_tier_1().add_node_to_tier_1().tier_up(0, 1).tier_up(0, 1)
        self.assertEqual(str(g2), '2|22||')
        g3= DAGSN().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().tier_up(0, 1).tier_up(2, 3).tier_up(4, 5)
        self.assertEqual(str(g3), '4|22|2|')
        g4= DAGSN().add_node_to_tier_1().add_node_to_tier_1().tier_up(0, 1).tier_up(0, 1).tier_up(0, 1)
        self.assertEqual(str(g4), '2|222||')
        g5= DAGSN().add_node_to_tier_1().add_node_to_tier_1().tier_up(0, 1).tier_up(0, 1).tier_up(0, 1).add_node_to_tier_1().add_node_to_tier_1()
        self.assertEqual(str(g5), '4|222||')
        g6= DAGSN().add_node_to_tier_1().add_node_to_tier_1().tier_up(0, 1).tier_up(0, 1).add_node_to_tier_1().add_node_to_tier_1().tier_up(1, 2)
        self.assertNotEqual(str(g5),str(g6))

    def test_extend(self):
        g1 = DAGSN().add_node_to_tier_1().add_node_to_tier_1().tier_up(0, 1).add_node_to_tier_1().extend(3, 2).add_node_to_tier_1().extend(4, 3)
        self.assertEqual(str(g1), '4|4||')

    def test_get_canonical_form(self):

        g1= DAGSN().add_node_to_tier_1().add_node_to_tier_1().tier_up(0,1).add_node_to_tier_1().extend(3,2).add_node_to_tier_1()
        g2 = DAGSN().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().tier_up(0,2).add_node_to_tier_1().extend(4,3)
        self.assertEqual(str(g1), str(g2))

        g3= DAGSN().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().tier_up(0, 1).tier_up(0, 1)
        g4= DAGSN().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().tier_up(0, 1).tier_up(1, 2)
        self.assertNotEqual(str(g3),str(g4))

        g3= DAGSN().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().tier_up(0, 1).tier_up(0, 1)
        g4= DAGSN().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().tier_up(0, 1).tier_up(1, 2)
        self.assertNotEqual(str(g3),str(g4))

    def test_get_tier(self):
        g1 = DAGSN().add_node_to_tier_1().add_node_to_tier_1().tier_up(0, 1).add_node_to_tier_1().extend(3, 2).add_node_to_tier_1().extend(4, 3)
        self.assertEqual(g1.get_tier(0), 0)
        self.assertEqual(g1.get_tier(1), 0)
        self.assertEqual(g1.get_tier(2), 0)
        self.assertEqual(g1.get_tier(3), 0)
        self.assertEqual(g1.get_tier(4), 1)
        self.assertEqual(g1.get_tier(5), 1)
        self.assertEqual(g1.get_tier(6), 1)



if __name__ == '__main__':
    unittest.main()


    # g1 = DAGSN().add_node_to_tier_1().add_node_to_tier_1().tier_up(0,1).add_node_to_tier_1().extend(3,2).add_node_to_tier_1()
# print(g1)
# g2 = DAGSN().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().tier_up(0,2).add_node_to_tier_1().extend(4,3)
# print(g2)