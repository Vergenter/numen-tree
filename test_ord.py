import unittest
import numpy as np
import ordering.ord as ord


def bit_difference(col1, col2):
    return np.sum(col1 != col2)


class Ordering_test(unittest.TestCase):
    PERFECT_ARRAY = np.array(
        [[0, 0, 0, 1], [0, 0, 1, 1], [0, 1, 1, 1], [1, 1, 1, 1]])

    def test_single(self):
        arr1 = np.array([[1, 1, 1, 1], [1, 0, 1, 1],
                        [1, 0, 1, 0], [1, 0, 0, 0]])
        expected_difference = 0
        self.assertEqual(bit_difference(
            Ordering_test.PERFECT_ARRAY, ord.best_matches(arr1)), expected_difference)

    def test_difference(self):
        arr1 = np.array([[1, 1, 1, 1], [0, 1, 1, 1],
                        [1, 0, 1, 0], [1, 0, 0, 0]])
        expected_difference = 2
        self.assertEqual(bit_difference(
            Ordering_test.PERFECT_ARRAY, ord.best_matches(arr1)), expected_difference)

    def test_canonical(self):
        arr1 = np.array([[1, 1, 1, 1], [1, 0, 1, 1], [0, 1, 1, 1], [
                        1, 0, 1, 0], [1, 0, 0, 0]], dtype=int)

        arr2 = np.array([[1, 1, 1, 1],  [0, 1, 1, 1], [1, 0, 1, 1], [
                        1, 0, 1, 0], [1, 0, 0, 0]], dtype=int)
        self.assertTrue(np.array_equal(
            ord.best_matches(arr1), ord.best_matches(arr2)))


if __name__ == '__main__':
    unittest.main()
