
import unittest
import sys
from library_catalog import LibraryCatalog, is_even


class TestAddingBooks(unittest.TestCase):

    def setUp(self):
        self.catalog = LibraryCatalog()
        self.catalog.add_book("Harry Potter", "J.K. Rowling", "111", 1997)
        self.catalog.add_book("The Hobbit", "J.R.R. Tolkien", "222", 1937)
        self.catalog.add_book("1984", "George Orwell", "333", 1949)

    def test_add_book_success(self):
        self.catalog.add_book("Dune", "Frank Herbert", "444", 1965)
        self.assertEqual(self.catalog.count(), 4)

    def test_add_duplicate_isbn(self):
        with self.assertRaises(ValueError):
            self.catalog.add_book("Another Book", "Someone", "111", 2000)

        self.assertEqual(self.catalog.count(), 3)


class TestRemovingBooks(unittest.TestCase):

    def setUp(self):
        self.catalog = LibraryCatalog()
        self.catalog.add_book("Harry Potter", "J.K. Rowling", "111", 1997)
        self.catalog.add_book("The Hobbit", "J.R.R. Tolkien", "222", 1937)
        self.catalog.add_book("1984", "George Orwell", "333", 1949)

    def test_remove_book_success(self):
        result = self.catalog.remove_book("111")

        self.assertTrue(result)
        self.assertIsNone(self.catalog.find_by_isbn("111"))

    def test_remove_book_not_found(self):
        result = self.catalog.remove_book("999")

        self.assertFalse(result)
        self.assertEqual(self.catalog.count(), 3)


class TestSearching(unittest.TestCase):

    def setUp(self):
        self.catalog = LibraryCatalog()
        self.catalog.add_book("Harry Potter", "J.K. Rowling", "111", 1997)
        self.catalog.add_book("The Hobbit", "J.R.R. Tolkien", "222", 1937)
        self.catalog.add_book("1984", "George Orwell", "333", 1949)

    def test_find_by_author(self):
        result = self.catalog.find_by_author("j.k. rowling")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "Harry Potter")

    def test_find_by_author_not_found(self):
        result = self.catalog.find_by_author("Unknown")

        self.assertEqual(result, [])

    def test_find_by_isbn(self):
        book = self.catalog.find_by_isbn("222")

        self.assertIsNotNone(book)
        self.assertEqual(book["title"], "The Hobbit")

    def test_find_by_isbn_not_found(self):
        book = self.catalog.find_by_isbn("999")

        self.assertIsNone(book)

    def test_available_books(self):
        self.catalog.borrow("111")

        available = self.catalog.available_books()

        self.assertEqual(len(available), 2)


class TestBorrowing(unittest.TestCase):

    def setUp(self):
        self.catalog = LibraryCatalog()
        self.catalog.add_book("Harry Potter", "J.K. Rowling", "111", 1997)
        self.catalog.add_book("The Hobbit", "J.R.R. Tolkien", "222", 1937)
        self.catalog.add_book("1984", "George Orwell", "333", 1949)

    def test_borrow_success(self):
        self.catalog.borrow("111")

        self.assertFalse(
            self.catalog.find_by_isbn("111")["available"]
        )

    def test_borrow_already_borrowed(self):
        self.catalog.borrow("111")

        with self.assertRaises(ValueError):
            self.catalog.borrow("111")

    def test_borrow_unknown_isbn(self):
        before = [book.copy() for book in self.catalog.books]

        with self.assertRaises(ValueError):
            self.catalog.borrow("999")

        self.assertEqual(self.catalog.books, before)

    def test_return_book(self):
        self.catalog.borrow("111")
        self.catalog.return_book("111")

        self.assertTrue(
            self.catalog.find_by_isbn("111")["available"]
        )

    def test_return_unknown_isbn(self):
        with self.assertRaises(ValueError):
            self.catalog.return_book("999")

class TestIsEven(unittest.TestCase):

    def test_is_even(self):
        test_cases = [
            (2, True),
            (4, True),
            (6, True),
            (8, True),
            (1, False),
            (3, False),
            (-2, True),
            (-3, False),
            (0, True)
        ]

        for number, expected in test_cases:
            with self.subTest(n=number):
                self.assertEqual(is_even(number), expected)


class TestSkipping(unittest.TestCase):

    @unittest.skip("not implemented yet")
    def test_not_implemented(self):
        self.assertEqual(1 + 1, 2)

    @unittest.skipIf(sys.platform == "win32", "posix only")
    def test_posix_only(self):
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()

#6
#The subTest() method allows testing multiple inputs within one test method. I tested positive numbers, negative numbers and zero.
#I deliberately changed the expected result for one input to make the test fail. The output showed exactly which input caused the failure, 
#while the remaining inputs were still tested.

#7
#I used @unittest.skip to skip a test that is not implemented yet. I also used @unittest.skipIf to skip a test when running on Windows. 
#After running the test suite, the summary showed "OK (skipped=2)". This means that two tests were skipped and the remaining tests were executed normally.