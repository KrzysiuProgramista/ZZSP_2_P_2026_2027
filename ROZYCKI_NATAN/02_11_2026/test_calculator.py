import unittest
from calculator import add, subtract, multiply, divide


class TestCalculator(unittest.TestCase):

    def test_add_two_positives(self):
        self.assertEqual(add(2, 3), 5)

    def test_add_positive_and_negative(self):
        self.assertEqual(add(5, -3), 2)

    def test_add_two_zeros(self):
        self.assertEqual(add(0, 0), 0)

    def test_subtract(self):
        self.assertEqual(subtract(10, 4), 6)

    def test_multiply_by_zero(self):
        self.assertEqual(multiply(7, 0), 0)

    def test_divide_evenly(self):
        self.assertEqual(divide(10, 2), 5.0)

    def test_divide_fractional_result(self):
        self.assertAlmostEqual(divide(1, 3), 0.3333333, places=6)

    def test_divide_by_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            divide(1, 0)

    def test_divide_by_zero_message(self):
        with self.assertRaises(ValueError) as ctx:
            divide(1, 0)
        self.assertIn("zero", str(ctx.exception))

    def test_non_numeric_input_raises_type_error(self):
        with self.assertRaises(TypeError):
            add("five", 3)
        with self.assertRaises(TypeError):
            divide(10, None)
        with self.assertRaises(TypeError):
            multiply(True, 4)


if __name__ == "__main__":
    unittest.main()