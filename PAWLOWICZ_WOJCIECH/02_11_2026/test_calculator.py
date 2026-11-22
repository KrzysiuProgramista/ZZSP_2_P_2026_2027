import unittest

from calculator import add, subtract, multiply, divide, safe_add


class TestCalculator(unittest.TestCase):
    def test_adding_two_positives(self):
        self.assertEqual(add(2, 3), 5)

    def test_adding_a_positive_and_a_negative(self):
        self.assertEqual(add(5, -2), 3)

    def test_adding_two_zeros(self):
        self.assertEqual(add(0, 0), 0)

    def test_subtracting(self):
        self.assertEqual(subtract(10, 4), 6)

    def test_multiplying_by_zero(self):
        self.assertEqual(multiply(7, 0), 0)

    def test_dividing_evenly(self):
        self.assertEqual(divide(10, 2), 5)

    def test_dividing_with_fractional_result(self):
        self.assertAlmostEqual(divide(1, 3), 0.3333333333, places=9)

    def test_dividing_by_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            divide(1, 0)

    # Exercise 3: assertRaises + checking the message
    def test_dividing_by_zero_message(self):
        with self.assertRaises(ValueError) as ctx:
            divide(1, 0)
        self.assertIn("zero", str(ctx.exception))

    def test_safe_add_raises_type_error_on_non_numeric(self):
        with self.assertRaises(TypeError):
            safe_add(1, "two")


if __name__ == "__main__":
    unittest.main()
