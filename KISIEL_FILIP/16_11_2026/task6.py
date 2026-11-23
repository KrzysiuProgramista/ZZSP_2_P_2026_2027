#zad 6
import unittest


def is_even(number):
    return number % 2 == 0


class TestSubTest(unittest.TestCase):
    def test_is_even_for_many_inputs(self):
        for number in [2, 4, 6, 7, 8, 10]:
            with self.subTest(number=number):
                self.assertTrue(is_even(number), f"{number} should be even")


if __name__ == "__main__":
    unittest.main(verbosity=2)
