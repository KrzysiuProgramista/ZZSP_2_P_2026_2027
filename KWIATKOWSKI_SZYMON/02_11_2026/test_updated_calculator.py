import unittest
from calculator import add, divide, multiply, subtract


class TestCalculator(unittest.TestCase):

    def test_add_two_positives(self):
        self.assertEqual(add(3, 5), 8)

    def test_add_positive_and_negative(self):
        self.assertEqual(add(7, -3), 4)

    def test_add_two_zeros(self):
        self.assertEqual(add(0, 0), 0)

    def test_subtract(self):
        self.assertEqual(subtract(10, 4), 6)

    def test_multiply_by_zero(self):
        self.assertEqual(multiply(5, 0), 0)

    def test_divide_evenly(self):
        self.assertEqual(divide(10, 2), 5)

    def test_divide_fractional_result(self):
        self.assertAlmostEqual(divide(1, 3), 0.3333333, places=6)

    def test_divide_by_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            divide(5, 0)

    def test_divide_by_zero_message(self):
        with self.assertRaises(ValueError) as ctx:
            divide(1, 0)
        self.assertIn("zero", str(ctx.exception))

    def test_type_error_non_numeric(self):
        with self.assertRaises(TypeError):
            add("5", 3)


if __name__ == "__main__":
    unittest.main()