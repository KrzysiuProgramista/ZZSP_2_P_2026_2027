import copy
import unittest
from library_catalog import LibraryCatalog


class TestLibraryCatalog(unittest.TestCase):
    def setUp(self) -> None:
        self.catalog = LibraryCatalog()
        self.catalog.add_book("Dune", "Frank Herbert", "978-0441172719", 1965)
        self.catalog.add_book("Dune Messiah", "Frank Herbert", "978-0593098233", 1969)
        self.catalog.add_book("1984", "George Orwell", "978-0451524935", 1949)

    def test_add_book_success(self) -> None:
        self.catalog.add_book("Foundation", "Isaac Asimov", "978-0553293357", 1951)
        self.assertEqual(self.catalog.count(), 4)
        added = self.catalog.find_by_isbn("978-0553293357")
        self.assertIsNotNone(added)
        self.assertTrue(added["available"])

    def test_add_book_duplicate_isbn_raises(self) -> None:
        with self.assertRaises(ValueError):
            self.catalog.add_book("Duplicate", "Someone", "978-0451524935", 2000)

    def test_remove_book_success(self) -> None:
        self.assertTrue(self.catalog.remove_book("978-0451524935"))
        self.assertEqual(self.catalog.count(), 2)
        self.assertIsNone(self.catalog.find_by_isbn("978-0451524935"))

    def test_remove_book_unknown_returns_false(self) -> None:
        self.assertFalse(self.catalog.remove_book("000-0000000000"))
        self.assertEqual(self.catalog.count(), 3)

    def test_find_by_author_case_insensitive(self) -> None:
        results = self.catalog.find_by_author("fRaNk HeRbErT")
        self.assertEqual(len(results), 2)
        self.assertEqual({b["title"] for b in results}, {"Dune", "Dune Messiah"})

    def test_find_by_author_missing_returns_empty(self) -> None:
        self.assertEqual(self.catalog.find_by_author("Unknown Author"), [])

    def test_find_by_isbn_success(self) -> None:
        book = self.catalog.find_by_isbn("978-0441172719")
        self.assertIsNotNone(book)
        self.assertEqual(book["title"], "Dune")

    def test_find_by_isbn_missing_returns_none(self) -> None:
        self.assertIsNone(self.catalog.find_by_isbn("999-9999999999"))

    def test_borrow_success(self) -> None:
        self.catalog.borrow("978-0441172719")
        book = self.catalog.find_by_isbn("978-0441172719")
        self.assertFalse(book["available"])

    def test_borrow_unknown_isbn_raises(self) -> None:
        with self.assertRaises(ValueError):
            self.catalog.borrow("000-0000000000")

    def test_borrow_already_borrowed_raises(self) -> None:
        self.catalog.borrow("978-0441172719")
        with self.assertRaises(ValueError):
            self.catalog.borrow("978-0441172719")

    def test_return_book_success(self) -> None:
        self.catalog.borrow("978-0441172719")
        self.catalog.return_book("978-0441172719")
        self.assertTrue(self.catalog.find_by_isbn("978-0441172719")["available"])

    def test_return_book_unknown_isbn_raises(self) -> None:
        with self.assertRaises(ValueError):
            self.catalog.return_book("000-0000000000")

    def test_available_books_excludes_borrowed(self) -> None:
        self.catalog.borrow("978-0451524935")
        available_isbns = {b["isbn"] for b in self.catalog.available_books()}
        self.assertEqual(available_isbns, {"978-0441172719", "978-0593098233"})

    def test_available_books_when_all_borrowed_returns_empty(self) -> None:
        for book in self.catalog.books:
            self.catalog.borrow(book["isbn"])
        self.assertEqual(self.catalog.available_books(), [])

    def test_count_returns_book_total(self) -> None:
        self.assertEqual(self.catalog.count(), 3)

    def test_count_empty_catalogue_is_zero(self) -> None:
        empty = LibraryCatalog()
        self.assertEqual(empty.count(), 0)
        
    def test_borrow_then_return_restores_availability(self) -> None:
        isbn = "978-0441172719"
        self.assertIn(isbn, {b["isbn"] for b in self.catalog.available_books()})

        self.catalog.borrow(isbn)
        self.assertNotIn(isbn, {b["isbn"] for b in self.catalog.available_books()})

        self.catalog.return_book(isbn)
        self.assertIn(isbn, {b["isbn"] for b in self.catalog.available_books()})

    def test_failed_operations_leave_catalogue_unchanged(self) -> None:
        snapshot = copy.deepcopy(self.catalog.books)

        with self.assertRaises(ValueError):
            self.catalog.add_book("Dune Copy", "Someone", "978-0441172719", 2020)
        self.assertEqual(self.catalog.books, snapshot)

        self.assertFalse(self.catalog.remove_book("000-0000000000"))
        self.assertEqual(self.catalog.books, snapshot)

        with self.assertRaises(ValueError):
            self.catalog.borrow("000-0000000000")
        self.assertEqual(self.catalog.books, snapshot)

        with self.assertRaises(ValueError):
            self.catalog.return_book("000-0000000000")
        self.assertEqual(self.catalog.books, snapshot)


if __name__ == "__main__":
    unittest.main()