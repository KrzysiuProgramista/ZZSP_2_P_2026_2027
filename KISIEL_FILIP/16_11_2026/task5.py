#zad 5
import unittest


class LibraryCatalog:
    def __init__(self):
        self.books = []

    def add_book(self, title, author, isbn, year):
        if self.find_by_isbn(isbn) is not None:
            raise ValueError(f"Duplicate ISBN: {isbn}")
        book = {"title": title, "author": author, "isbn": isbn,
                "year": year, "available": True}
        self.books.append(book)
        return book

    def remove_book(self, isbn):
        book = self.find_by_isbn(isbn)
        if book is None:
            return False
        self.books.remove(book)
        return True

    def find_by_author(self, author):
        return [b for b in self.books if b["author"].casefold() == author.casefold()]

    def find_by_isbn(self, isbn):
        return next((b for b in self.books if b["isbn"] == isbn), None)

    def borrow(self, isbn):
        book = self.find_by_isbn(isbn)
        if book is None:
            raise ValueError(f"Unknown ISBN: {isbn}")
        if not book["available"]:
            raise ValueError(f"Already borrowed: {isbn}")
        book["available"] = False
        return book

    def return_book(self, isbn):
        book = self.find_by_isbn(isbn)
        if book is None:
            raise ValueError(f"Unknown ISBN: {isbn}")
        book["available"] = True
        return book

    def available_books(self):
        return [b for b in self.books if b["available"]]

    def count(self):
        return len(self.books)


class TestAddingBooks(unittest.TestCase):
    def setUp(self):
        self.catalog = LibraryCatalog()
        self.catalog.add_book("The Hobbit", "J.R.R. Tolkien", "111", 1937)
        self.catalog.add_book("1984", "George Orwell", "222", 1949)
        self.catalog.add_book("Animal Farm", "George Orwell", "333", 1945)

    def test_add_success(self):
        self.catalog.add_book("Dune", "Frank Herbert", "444", 1965)
        self.assertEqual(self.catalog.count(), 4)

    def test_add_duplicate_isbn_fails_without_change(self):
        before = [b.copy() for b in self.catalog.books]
        with self.assertRaises(ValueError):
            self.catalog.add_book("Other", "Author", "111", 2020)
        self.assertEqual(self.catalog.books, before)


class TestRemovingBooks(unittest.TestCase):
    def setUp(self):
        self.catalog = LibraryCatalog()
        self.catalog.add_book("The Hobbit", "J.R.R. Tolkien", "111", 1937)
        self.catalog.add_book("1984", "George Orwell", "222", 1949)
        self.catalog.add_book("Animal Farm", "George Orwell", "333", 1945)

    def test_remove_existing(self):
        self.assertTrue(self.catalog.remove_book("111"))
        self.assertEqual(self.catalog.count(), 2)

    def test_remove_missing(self):
        self.assertFalse(self.catalog.remove_book("999"))
        self.assertEqual(self.catalog.count(), 3)


class TestSearching(unittest.TestCase):
    def setUp(self):
        self.catalog = LibraryCatalog()
        self.catalog.add_book("The Hobbit", "J.R.R. Tolkien", "111", 1937)
        self.catalog.add_book("1984", "George Orwell", "222", 1949)
        self.catalog.add_book("Animal Farm", "George Orwell", "333", 1945)

    def test_find_author_case_insensitive(self):
        self.assertEqual(len(self.catalog.find_by_author("GEORGE ORWELL")), 2)

    def test_find_author_no_match(self):
        self.assertEqual(self.catalog.find_by_author("Nobody"), [])

    def test_find_isbn_found(self):
        self.assertEqual(self.catalog.find_by_isbn("222")["title"], "1984")

    def test_find_isbn_missing(self):
        self.assertIsNone(self.catalog.find_by_isbn("999"))

    def test_available_books_and_count(self):
        self.catalog.borrow("111")
        self.assertEqual(len(self.catalog.available_books()), 2)
        self.assertEqual(self.catalog.count(), 3)


class TestBorrowing(unittest.TestCase):
    def setUp(self):
        self.catalog = LibraryCatalog()
        self.catalog.add_book("The Hobbit", "J.R.R. Tolkien", "111", 1937)
        self.catalog.add_book("1984", "George Orwell", "222", 1949)
        self.catalog.add_book("Animal Farm", "George Orwell", "333", 1945)

    def test_borrow_and_return(self):
        self.catalog.borrow("111")
        self.assertFalse(self.catalog.find_by_isbn("111")["available"])
        self.catalog.return_book("111")
        self.assertTrue(self.catalog.find_by_isbn("111")["available"])

    def test_borrow_already_borrowed_fails_without_change(self):
        self.catalog.borrow("111")
        before = [b.copy() for b in self.catalog.books]
        with self.assertRaises(ValueError):
            self.catalog.borrow("111")
        self.assertEqual(self.catalog.books, before)

    def test_borrow_unknown_isbn(self):
        before = [b.copy() for b in self.catalog.books]
        with self.assertRaises(ValueError):
            self.catalog.borrow("999")
        self.assertEqual(self.catalog.books, before)

    def test_return_unknown_isbn(self):
        with self.assertRaises(ValueError):
            self.catalog.return_book("999")


if __name__ == "__main__":
    unittest.main(verbosity=2)
