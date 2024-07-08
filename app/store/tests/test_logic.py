import unittest

from store.logic import operations


class LogicTestCase(unittest.TestCase):
    def test_plus(self):
        result = operations(6, 13, '+')
        self.assertEqual(19, result)

    def test_minus(self):
        result = operations(15, 7, '-')
        self.assertEqual(8, result)

    def test_multiply(self):
        result = operations(4, 5, '*')
        self.assertEqual(20, result)


if __name__ == '__main__':
    unittest.main()
