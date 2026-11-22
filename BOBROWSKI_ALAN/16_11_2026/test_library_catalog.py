import unittest
import sys

from library_catalog import LibraryCatalog, is_even


class TestAddingBooks(unittest.TestCase):

    def setUp(self):
        self.catalog = LibraryCatalog()

        self.catalog.add_book("1984", "George Orwell", "111", 1949)
        self.catalog.add_book("Hamlet", "William Shakespeare", "222", 1603)
        self.catalog.add_book("Animal Farm", "George Orwell", "333", 1945)

    def test_add_book_success(self):
        self.catalog.add_book("The Hobbit", "J.R.R. Tolkien", "444", 1937)

        self.assertEqual(self.catalog.count(), 4)

    def test_add_duplicate_isbn(self):
        with self.assertRaises(ValueError):
            self.catalog.add_book(
                "Another Book", "Someone", "111", 2020
            )

    def test_count(self):
        self.assertEqual(self.catalog.count(), 3)

    def test_count_empty_catalog(self):
        empty = LibraryCatalog()
        self.assertEqual(empty.count(), 0)


class TestRemovingBooks(unittest.TestCase):

    def setUp(self):
        self.catalog = LibraryCatalog()

        self.catalog.add_book("1984", "George Orwell", "111", 1949)
        self.catalog.add_book("Hamlet", "William Shakespeare", "222", 1603)
        self.catalog.add_book("Animal Farm", "George Orwell", "333", 1945)

    def test_remove_existing_book(self):
        result = self.catalog.remove_book("111")

        self.assertTrue(result)
        self.assertEqual(self.catalog.count(), 2)

    def test_remove_unknown_book(self):
        result = self.catalog.remove_book("999")

        self.assertFalse(result)
        self.assertEqual(self.catalog.count(), 3)


class TestSearching(unittest.TestCase):

    def setUp(self):
        self.catalog = LibraryCatalog()

        self.catalog.add_book("1984", "George Orwell", "111", 1949)
        self.catalog.add_book("Hamlet", "William Shakespeare", "222", 1603)
        self.catalog.add_book("Animal Farm", "George Orwell", "333", 1945)

    def test_find_by_author_success(self):
        result = self.catalog.find_by_author("george orwell")

        self.assertEqual(len(result), 2)

    def test_find_by_author_unknown(self):
        result = self.catalog.find_by_author("J.K. Rowling")

        self.assertEqual(result, [])

    def test_find_by_isbn_success(self):
        result = self.catalog.find_by_isbn("111")

        self.assertIsNotNone(result)
        self.assertEqual(result["title"], "1984")

    def test_find_by_isbn_unknown(self):
        result = self.catalog.find_by_isbn("999")

        self.assertIsNone(result)

    def test_available_books(self):
        self.catalog.borrow("111")

        available = self.catalog.available_books()

        self.assertEqual(len(available), 2)

    def test_available_books_all_available(self):
        self.assertEqual(len(self.catalog.available_books()), 3)


class TestBorrowing(unittest.TestCase):

    def setUp(self):
        self.catalog = LibraryCatalog()

        self.catalog.add_book("1984", "George Orwell", "111", 1949)
        self.catalog.add_book("Hamlet", "William Shakespeare", "222", 1603)
        self.catalog.add_book("Animal Farm", "George Orwell", "333", 1945)

    def test_borrow_success(self):
        self.catalog.borrow("111")

        book = self.catalog.find_by_isbn("111")

        self.assertFalse(book["available"])

    def test_borrow_already_borrowed(self):
        self.catalog.borrow("111")

        with self.assertRaises(ValueError):
            self.catalog.borrow("111")

    def test_borrow_unknown_isbn(self):
        with self.assertRaises(ValueError):
            self.catalog.borrow("999")

    def test_return_book_success(self):
        self.catalog.borrow("111")
        self.catalog.return_book("111")

        book = self.catalog.find_by_isbn("111")

        self.assertTrue(book["available"])

    def test_return_unknown_book(self):
        with self.assertRaises(ValueError):
            self.catalog.return_book("999")

    def test_borrow_then_return_restores_availability(self):
        self.catalog.borrow("111")

        self.assertFalse(
            self.catalog.find_by_isbn("111")["available"]
        )

        self.catalog.return_book("111")

        self.assertTrue(
            self.catalog.find_by_isbn("111")["available"]
        )

    def test_failed_borrow_does_not_change_catalog(self):
        before = [book.copy() for book in self.catalog.books]

        with self.assertRaises(ValueError):
            self.catalog.borrow("999")

        self.assertEqual(self.catalog.books, before)

    def test_failed_duplicate_add_does_not_change_catalog(self):
        before = [book.copy() for book in self.catalog.books]

        with self.assertRaises(ValueError):
            self.catalog.add_book(
                "Duplicate", "Someone", "111", 2020
            )

        self.assertEqual(self.catalog.books, before)


class TestSubTest(unittest.TestCase):

    def test_is_even(self):
        test_cases = [
            (2, True),
            (4, True),
            (6, True),
            (8, True),
            (1, False),
            (3, False),
            (-2, True),
            (-5, False),
            (0, True)
        ]

        for number, expected in test_cases:
            with self.subTest(number=number):
                self.assertEqual(is_even(number), expected)


class TestSkipping(unittest.TestCase):

    @unittest.skip("not implemented yet")
    def test_future_feature(self):
        self.assertTrue(False)

    @unittest.skipIf(sys.platform == "win32", "posix only")
    def test_posix_only(self):
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
