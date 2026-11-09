import unittest
from calculator import add, subtract, multiply, divide, strict_multiply

class TestCalculator(unittest.TestCase):
    def test_positive_addition(self):
        self.assertEqual(add(3, 6), 9)

    def test_mixed_addition(self):
        self.assertEqual(add(-5, 2), -3)

    def test_two_zero_addition(self):
        self.assertEqual(add(0, 0), 0)

    def test_subtraction(self):
        self.assertEqual(subtract(8, 7), 1)

    def test_multiplication_by_zero(self):
        self.assertEqual(multiply(5, 0), 0)

    def test_even_division(self):
        self.assertEqual(divide(4, 2), 2)

    def test_fractional_division(self):
        self.assertAlmostEqual(divide(5, 2), 2.5)

    def test_division_by_zero(self):
        with self.assertRaises(ValueError):
            divide(1, 0)
    
    def test_division_by_zero_message(self):
        with self.assertRaises(ValueError) as ctx:
            divide(1, 0)
        self.assertIn("zero", str(ctx.exception))
    
    def test_strict_multiply(self):
        with self.assertRaises(TypeError):
            strict_multiply("3", "4")