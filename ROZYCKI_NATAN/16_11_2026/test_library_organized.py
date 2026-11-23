import copy
import unittest
from library_catalog import LibraryCatalog


class TestAddingBooks(unittest.TestCase):
    def setUp(self) -> None:
        self.catalog = LibraryCatalog()
        self.catalog.add_book("1984", "George Orwell", "978-0451524935", 1949)

    def test_add_new_book_increases_count(self) -> None:
        self.catalog.add_book("Dune", "Frank Herbert", "978-0441172719", 1965)
        self.assertEqual(self.catalog.count(), 2)

    def test_add_duplicate_isbn_raises_and_keeps_count(self) -> None:
        with self.assertRaises(ValueError):
            self.catalog.add_book("Other", "Someone", "978-0451524935", 2000)
        self.assertEqual(self.catalog.count(), 1)


class TestRemovingBooks(unittest.TestCase):
    def setUp(self) -> None:
        self.catalog = LibraryCatalog()
        self.catalog.add_book("1984", "George Orwell", "978-0451524935", 1949)

    def test_remove_existing_book_returns_true(self) -> None:
        self.assertTrue(self.catalog.remove_book("978-0451524935"))
        self.assertEqual(self.catalog.count(), 0)

    def test_remove_missing_book_returns_false(self) -> None:
        self.assertFalse(self.catalog.remove_book("000-0000000000"))
        self.assertEqual(self.catalog.count(), 1)


class TestSearching(unittest.TestCase):
    def setUp(self) -> None:
        self.catalog = LibraryCatalog()
        self.catalog.add_book("Dune", "Frank Herbert", "978-0441172719", 1965)
        self.catalog.add_book("Dune Messiah", "Frank Herbert", "978-0593098233", 1969)
        self.catalog.add_book("1984", "George Orwell", "978-0451524935", 1949)

    def test_find_by_author_case_insensitive(self) -> None:
        results = self.catalog.find_by_author("frank herbert")
        self.assertEqual(len(results), 2)

    def test_find_by_author_missing_returns_empty(self) -> None:
        self.assertEqual(self.catalog.find_by_author("Isaac Asimov"), [])

    def test_find_by_isbn_found(self) -> None:
        self.assertEqual(self.catalog.find_by_isbn("978-0451524935")["title"], "1984")

    def test_find_by_isbn_missing_returns_none(self) -> None:
        self.assertIsNone(self.catalog.find_by_isbn("999-9999999999"))

    def test_available_books_filters_borrowed(self) -> None:
        self.catalog.borrow("978-0451524935")
        self.assertEqual(len(self.catalog.available_books()), 2)


class TestBorrowing(unittest.TestCase):
    def setUp(self) -> None:
        self.catalog = LibraryCatalog()
        self.catalog.add_book("Dune", "Frank Herbert", "978-0441172719", 1965)

    def test_borrow_and_return_restores_availability(self) -> None:
        self.catalog.borrow("978-0441172719")
        self.assertFalse(self.catalog.find_by_isbn("978-0441172719")["available"])

        self.catalog.return_book("978-0441172719")
        self.assertTrue(self.catalog.find_by_isbn("978-0441172719")["available"])

    def test_borrow_already_borrowed_raises_without_mutating(self) -> None:
        self.catalog.borrow("978-0441172719")
        snapshot = copy.deepcopy(self.catalog.books)
        with self.assertRaises(ValueError):
            self.catalog.borrow("978-0441172719")
        self.assertEqual(self.catalog.books, snapshot)

    def test_return_unknown_isbn_raises(self) -> None:
        with self.assertRaises(ValueError):
            self.catalog.return_book("000-0000000000")


if __name__ == "__main__":
    unittest.main()