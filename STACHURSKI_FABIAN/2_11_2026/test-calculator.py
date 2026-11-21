import unittest
from calculator import add, subtract, multiply, divide, strict_add


class TestCalculator(unittest.TestCase):
    def test_add_two_positives(self):
        self.assertEqual(add(3, 5), 8)

    def test_add_positive_and_negative(self):
        self.assertEqual(add(10, -4), 6)

    def test_add_two_zeros(self):
        self.assertEqual(add(0, 0), 0)

    def test_subtract(self):
        self.assertEqual(subtract(10, 4), 6)

    def test_multiply_by_zero(self):
        self.assertEqual(multiply(7, 0), 0)

    def test_divide_evenly(self):
        self.assertEqual(divide(12, 4), 3)

    def test_divide_fractional(self):
        self.assertAlmostEqual(divide(1, 3), 0.3333333, places=6)

    def test_divide_by_zero_raises(self):
        with self.assertRaises(ValueError):
            divide(1, 0)

    def test_divide_by_zero_message(self):
        with self.assertRaises(ValueError) as ctx:
            divide(1, 0)
        self.assertIn("zero", str(ctx.exception).lower())

    def test_strict_add_non_numeric_raises_type_error(self):
        with self.assertRaises(TypeError):
            strict_add("5", 2)


if __name__ == "__main__":
    unittest.main()