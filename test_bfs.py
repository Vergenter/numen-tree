import unittest
from main_bfs import DAGSN


class DAGSN_tier_up_test(unittest.TestCase):
    def test_tier_up_1(self):
        g1 = DAGSN().add_node_to_tier_1().add_node_to_tier_1().tier_up(0, 1).add_node_to_tier_1()
        self.assertEqual(str(g1), '3|011|0||')

    def test_tier_up_2(self):
        g2 = DAGSN().add_node_to_tier_1().add_node_to_tier_1().tier_up(0, 1).tier_up(0, 1)
        self.assertEqual(str(g2), '2|22|00||')

    def test_tier_up_3(self):
        g3 = DAGSN().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().tier_up(0, 1).tier_up(2, 3).tier_up(4, 5)
        self.assertEqual(str(g3), '4|1111|11|0|')

    def test_tier_up_4(self):
        g4 = DAGSN().add_node_to_tier_1().add_node_to_tier_1().tier_up(0, 1).tier_up(0, 1).tier_up(0, 1)
        self.assertEqual(str(g4), '2|33|000||')

    def test_tier_up_5(self):
        g5 = DAGSN().add_node_to_tier_1().add_node_to_tier_1().tier_up(0, 1).tier_up(0, 1).tier_up(0, 1).add_node_to_tier_1().add_node_to_tier_1()
        self.assertEqual(str(g5), '4|0033|000||')

    def test_tier_up_6(self):
        g6 = DAGSN().add_node_to_tier_1().add_node_to_tier_1().tier_up(0, 1).tier_up(0, 1).add_node_to_tier_1().add_node_to_tier_1().tier_up(1, 2)
        self.assertEqual(str(g6), '4|0123|000||')

    def test_tier_up_7(self):
        g6 = DAGSN().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1()\
        .tier_up(0, 1).tier_up(3, 4).extend(7,2).tier_up(4,5).tier_up(4,5)\
        .tier_up(6,7).tier_up(7,9).tier_up(7,9)
        self.assertEqual(str(g6), '6|111123|0123|000|')

    def test_tier_up_8(self):
        g6 = DAGSN().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1()\
        .tier_up(0, 1).tier_up(0, 1).tier_up(2,3).tier_up(4,5).tier_up(4,5)\
        .tier_up(6,8).tier_up(7,8).tier_up(7,9).tier_up(8,10)
        
        self.assertEqual(str(g6), '6|112222|11123|0000|')


    def test_tier_up_9(self):
        g6 = DAGSN().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1()\
        .tier_up(1, 2).extend(4,0).tier_up(1, 2).extend(5,3).tier_up(0,3).tier_up(0,3)\
        .tier_up(4,5).tier_up(5,7)
        self.assertEqual(str(g6), '4|2233|0112|00|')
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
            .tier_up(7,8)
        g2= DAGSN().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1()\
            .tier_up(0, 1).tier_up(2, 3).tier_up(4, 5).extend(9,6)\
            .tier_up(8,9)
        self.assertNotEqual(str(g1),str(g2))

    def test_get_canonical_form_6(self):
        g1= DAGSN().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1()\
            .tier_up(0, 1).tier_up(0, 1).tier_up(2, 3).tier_up(4, 5)\
            .tier_up(6,8)
        
        g2= DAGSN().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1().add_node_to_tier_1()\
            .tier_up(0, 1).tier_up(0, 1).tier_up(2, 3).tier_up(4, 5)\
            .tier_up(8,9)
        self.assertNotEqual(str(g1),str(g2))


class DAGSNTest(unittest.TestCase):

    def test_add_node_to_tier_1(self):
        g1 = DAGSN().add_node_to_tier_1()
        self.assertEqual(str(g1), '1|0|||')

    def test_extend(self):
        g1 = DAGSN().add_node_to_tier_1().add_node_to_tier_1().tier_up(0, 1).add_node_to_tier_1().extend(3, 2).add_node_to_tier_1().extend(4, 3)
        self.assertEqual(str(g1), '4|1111|0||')

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