#zad 4
import unittest


class LibraryCatalog:
    """A simple catalogue of books stored as dictionaries."""

    def __init__(self):
        self.books = []

    def add_book(self, title, author, isbn, year):
        if self.find_by_isbn(isbn) is not None:
            raise ValueError(f"Book with ISBN {isbn} already exists.")
        book = {
            "title": title,
            "author": author,
            "isbn": isbn,
            "year": year,
            "available": True,
        }
        self.books.append(book)
        return book

    def remove_book(self, isbn):
        book = self.find_by_isbn(isbn)
        if book is None:
            return False
        self.books.remove(book)
        return True

    def find_by_author(self, author):
        author_lower = author.casefold()
        return [
            book for book in self.books
            if book["author"].casefold() == author_lower
        ]

    def find_by_isbn(self, isbn):
        for book in self.books:
            if book["isbn"] == isbn:
                return book
        return None

    def borrow(self, isbn):
        book = self.find_by_isbn(isbn)
        if book is None:
            raise ValueError(f"Book with ISBN {isbn} does not exist.")
        if not book["available"]:
            raise ValueError(f"Book with ISBN {isbn} is already borrowed.")
        book["available"] = False
        return book

    def return_book(self, isbn):
        book = self.find_by_isbn(isbn)
        if book is None:
            raise ValueError(f"Book with ISBN {isbn} does not exist.")
        book["available"] = True
        return book

    def available_books(self):
        return [book for book in self.books if book["available"]]

    def count(self):
        return len(self.books)


class TestLibraryCatalog(unittest.TestCase):
    def setUp(self):
        self.catalog = LibraryCatalog()
        self.catalog.add_book("The Hobbit", "J.R.R. Tolkien", "111", 1937)
        self.catalog.add_book("1984", "George Orwell", "222", 1949)
        self.catalog.add_book("Animal Farm", "George Orwell", "333", 1945)

    def test_add_book_success(self):
        book = self.catalog.add_book("Dune", "Frank Herbert", "444", 1965)
        self.assertEqual(book["title"], "Dune")
        self.assertTrue(book["available"])
        self.assertEqual(self.catalog.count(), 4)

    def test_add_book_duplicate_isbn(self):
        before = [book.copy() for book in self.catalog.books]
        with self.assertRaises(ValueError):
            self.catalog.add_book("Different title", "Someone", "111", 2020)
        self.assertEqual(self.catalog.books, before)

    def test_remove_book_success(self):
        self.assertTrue(self.catalog.remove_book("111"))
        self.assertIsNone(self.catalog.find_by_isbn("111"))
        self.assertEqual(self.catalog.count(), 2)

    def test_remove_book_missing(self):
        self.assertFalse(self.catalog.remove_book("999"))
        self.assertEqual(self.catalog.count(), 3)

    def test_find_by_author_case_insensitive(self):
        found = self.catalog.find_by_author("gEoRgE oRwElL")
        self.assertEqual({book["isbn"] for book in found}, {"222", "333"})

    def test_find_by_author_no_matches(self):
        self.assertEqual(self.catalog.find_by_author("Nobody"), [])

    def test_find_by_isbn_found(self):
        self.assertEqual(self.catalog.find_by_isbn("222")["title"], "1984")

    def test_find_by_isbn_missing(self):
        self.assertIsNone(self.catalog.find_by_isbn("999"))

    def test_borrow_success(self):
        book = self.catalog.borrow("111")
        self.assertFalse(book["available"])

    def test_borrow_unknown_isbn(self):
        before = [book.copy() for book in self.catalog.books]
        with self.assertRaises(ValueError):
            self.catalog.borrow("999")
        self.assertEqual(self.catalog.books, before)

    def test_borrow_already_borrowed(self):
        self.catalog.borrow("111")
        before = [book.copy() for book in self.catalog.books]
        with self.assertRaises(ValueError):
            self.catalog.borrow("111")
        self.assertEqual(self.catalog.books, before)

    def test_return_book_success(self):
        self.catalog.borrow("111")
        book = self.catalog.return_book("111")
        self.assertTrue(book["available"])

    def test_return_unknown_isbn(self):
        before = [book.copy() for book in self.catalog.books]
        with self.assertRaises(ValueError):
            self.catalog.return_book("999")
        self.assertEqual(self.catalog.books, before)

    def test_borrow_then_return_restores_availability(self):
        self.catalog.borrow("222")
        self.assertFalse(self.catalog.find_by_isbn("222")["available"])
        self.catalog.return_book("222")
        self.assertTrue(self.catalog.find_by_isbn("222")["available"])

    def test_available_books(self):
        self.catalog.borrow("111")
        available_isbns = {book["isbn"] for book in self.catalog.available_books()}
        self.assertEqual(available_isbns, {"222", "333"})

    def test_count(self):
        self.assertEqual(self.catalog.count(), 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
