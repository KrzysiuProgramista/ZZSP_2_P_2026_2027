import unittest


def is_even(number: int) -> bool:
    """Return True for even integers and False for odd integers."""
    return number % 2 == 0


class TestIsEven(unittest.TestCase):
    def test_is_even_multiple_inputs(self) -> None:
        cases = [
            (0, True),
            (2, True),
            (-4, True),
            (1, False),
            (-7, False),
            (100, True),
            (101, False),
        ]
        for number, expected in cases:
            with self.subTest(number=number, expected=expected):
                self.assertEqual(is_even(number), expected)


if __name__ == "__main__":
    unittest.main()