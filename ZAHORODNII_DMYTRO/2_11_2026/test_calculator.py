import unittest
from calculator import add, subtract, multiply, divide


class TestCalculator(unittest.TestCase):
   
    def test_assert_raises(self):
        with self.assertRaises(ValueError):
            divide(1, 0)

    def test_assert_raises_message(self):
        with self.assertRaises(ValueError) as ctx:
            divide(1, 0)

        self.assertIn("zero", str(ctx.exception))

    def test_non_numeric_input(self):
        with self.assertRaises(TypeError):
            add("hello", 5)

    def test_add_two_positives(self):
        self.assertEqual(add(2, 3), 5)

    def test_add_positive_and_negative(self):
        self.assertEqual(add(5, -3), 2)

    def test_add_two_zeros(self):
        self.assertEqual(add(0, 0), 0)

    def test_subtract(self):
        self.assertEqual(subtract(10, 4), 6)

    def test_multiply_by_zero(self):
        self.assertEqual(multiply(5, 0), 0)

    def test_divide_evenly(self):
        self.assertEqual(divide(10, 2), 5)

    def test_divide_fractional(self):
        self.assertAlmostEqual(divide(10, 3), 3.333333, places=5)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            divide(10, 0)


if __name__ == "__main__":
    unittest.main()
