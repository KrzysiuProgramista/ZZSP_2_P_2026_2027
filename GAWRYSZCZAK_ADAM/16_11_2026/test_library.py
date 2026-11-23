import sys
import unittest
from library import LibraryCatalog, is_even


class TestAddingBooks(unittest.TestCase):

    def setUp(self):
        self.catalog = LibraryCatalog()
        self.catalog.add_book("Wiedźmin", "Andrzej Sapkowski", "111", 1993)
        self.catalog.add_book("Lalka", "Bolesław Prus", "222", 1890)
        self.catalog.add_book("Hobbit", "J.R.R. Tolkien", "333", 1937)

    def test_add_book_success(self):
        self.catalog.add_book("Dune", "Frank Herbert", "444", 1965)
        self.assertEqual(self.catalog.count(), 4)

    def test_add_book_duplicate_isbn_fails_and_leaves_unchanged(self):
        with self.assertRaises(ValueError):
            self.catalog.add_book("Inny tytuł", "Inny autor", "111", 2020)
        self.assertEqual(self.catalog.count(), 3)


class TestRemovingBooks(unittest.TestCase):

    def setUp(self):
        self.catalog = LibraryCatalog()
        self.catalog.add_book("Wiedźmin", "Andrzej Sapkowski", "111", 1993)
        self.catalog.add_book("Lalka", "Bolesław Prus", "222", 1890)
        self.catalog.add_book("Hobbit", "J.R.R. Tolkien", "333", 1937)

    def test_remove_book_success(self):
        result = self.catalog.remove_book("222")
        self.assertTrue(result)
        self.assertEqual(self.catalog.count(), 2)

    def test_remove_book_unknown_isbn(self):
        result = self.catalog.remove_book("999")
        self.assertFalse(result)
        self.assertEqual(self.catalog.count(), 3)


class TestSearching(unittest.TestCase):

    def setUp(self):
        self.catalog = LibraryCatalog()
        self.catalog.add_book("Wiedźmin", "Andrzej Sapkowski", "111", 1993)
        self.catalog.add_book("Miecz przeznaczenia", "Andrzej Sapkowski", "112", 1992)
        self.catalog.add_book("Hobbit", "J.R.R. Tolkien", "333", 1937)

    def test_find_by_author_case_insensitive(self):
        books = self.catalog.find_by_author("andrzej sapkowski")
        self.assertEqual(len(books), 2)

    def test_find_by_author_not_found(self):
        books = self.catalog.find_by_author("Adam Mickiewicz")
        self.assertEqual(books, [])

    def test_find_by_isbn_found(self):
        book = self.catalog.find_by_isbn("333")
        self.assertIsNotNone(book)
        self.assertEqual(book["title"], "Hobbit")

    def test_find_by_isbn_not_found(self):
        book = self.catalog.find_by_isbn("000")
        self.assertIsNone(book)


class TestBorrowing(unittest.TestCase):

    def setUp(self):
        self.catalog = LibraryCatalog()
        self.catalog.add_book("Wiedźmin", "Andrzej Sapkowski", "111", 1993)
        self.catalog.add_book("Lalka", "Bolesław Prus", "222", 1890)
        self.catalog.add_book("Hobbit", "J.R.R. Tolkien", "333", 1937)

    def test_borrow_and_return_restores_availability(self):
        self.catalog.borrow("111")
        self.assertEqual(len(self.catalog.available_books()), 2)

        self.catalog.return_book("111")
        self.assertEqual(len(self.catalog.available_books()), 3)

    def test_borrow_already_borrowed_raises_error(self):
        self.catalog.borrow("111")
        with self.assertRaises(ValueError):
            self.catalog.borrow("111")

    def test_borrow_unknown_isbn_raises_error(self):
        with self.assertRaises(ValueError):
            self.catalog.borrow("999")

    def test_return_unknown_isbn_raises_error(self):
        with self.assertRaises(ValueError):
            self.catalog.return_book("999")


class TestExtras(unittest.TestCase):

    def test_is_even_with_subtest(self):
        test_cases = [
            (2, True),
            (4, True),
            (0, True),
            (-6, True),
            (3, False),
            (-5, False),
        ]
        for number, expected in test_cases:
            with self.subTest(number=number):
                self.assertEqual(is_even(number), expected)

    @unittest.skip("not implemented yet")
    def test_future_feature(self):
        self.fail("Ten test nie powinien się wykonać")

    @unittest.skipIf(sys.platform == "win32", "posix only")
    def test_linux_mac_only_feature(self):
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()