from typing import Optional


class LibraryCatalog:
    """A small in-memory library catalogue."""

    def __init__(self):
        self.books: list[dict] = []

    def add_book(self, title: str, author: str, isbn: str, year: int) -> None:
        """Add a book. Raise ValueError if ISBN already exists."""

        if self.find_by_isbn(isbn) is not None:
            raise ValueError("A book with this ISBN already exists.")

        book = {
            "title": title,
            "author": author,
            "isbn": isbn,
            "year": year,
            "available": True
        }

        self.books.append(book)

    def remove_book(self, isbn: str) -> bool:
        """Remove a book by ISBN."""

        book = self.find_by_isbn(isbn)

        if book is None:
            return False

        self.books.remove(book)
        return True

    def find_by_author(self, author: str) -> list[dict]:
        """Find books by author, ignoring letter case."""

        return [
            book for book in self.books
            if book["author"].lower() == author.lower()
        ]

    def find_by_isbn(self, isbn: str) -> Optional[dict]:
        """Find a book by ISBN."""

        for book in self.books:
            if book["isbn"] == isbn:
                return book

        return None

    def borrow(self, isbn: str) -> None:
        """Borrow a book."""

        book = self.find_by_isbn(isbn)

        if book is None:
            raise ValueError("Book not found.")

        if not book["available"]:
            raise ValueError("Book is already borrowed.")

        book["available"] = False

    def return_book(self, isbn: str) -> None:
        """Return a book. Raise ValueError if ISBN is unknown."""

        book = self.find_by_isbn(isbn)

        if book is None:
            raise ValueError("Book not found.")

        book["available"] = True

    def available_books(self) -> list[dict]:
        """Return all available books."""

        return [
            book for book in self.books
            if book["available"]
        ]

    def count(self) -> int:
        """Return the total number of books."""

        return len(self.books)


def is_even(number: int) -> bool:
    """Return True if the number is even."""

    return number % 2 == 0
