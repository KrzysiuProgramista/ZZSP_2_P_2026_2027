from typing import Optional


class LibraryCatalog:
    """A small in-memory library catalogue.

    Each book is stored as a dictionary with these keys:
    title, author, isbn, year, available.
    """

    def __init__(self):
        self.books: list[dict] = []

    def add_book(self, title: str, author: str, isbn: str, year: int) -> None:
        """Add a book. Raise ValueError if the ISBN already exists."""
        if self.find_by_isbn(isbn) is not None:
            raise ValueError(f"A book with ISBN {isbn!r} already exists.")
        self.books.append(
            {
                "title": title,
                "author": author,
                "isbn": isbn,
                "year": year,
                "available": True,
            }
        )

    def remove_book(self, isbn: str) -> bool:
        """Remove a book by ISBN. Return True if removed, otherwise False."""
        book = self.find_by_isbn(isbn)
        if book is None:
            return False
        self.books.remove(book)
        return True

    def find_by_author(self, author: str) -> list[dict]:
        """Return books by author; the search must ignore letter case."""
        needle = author.lower()
        return [book for book in self.books if book["author"].lower() == needle]

    def find_by_isbn(self, isbn: str) -> Optional[dict]:
        """Return the matching book, or None if it does not exist."""
        for book in self.books:
            if book["isbn"] == isbn:
                return book
        return None

    def borrow(self, isbn: str) -> None:
        """Mark a book as borrowed.

        Raise ValueError if the ISBN is unknown or the book is already borrowed.
        """
        book = self.find_by_isbn(isbn)
        if book is None:
            raise ValueError(f"No book with ISBN {isbn!r}.")
        if not book["available"]:
            raise ValueError(f"Book {isbn!r} is already borrowed.")
        book["available"] = False

    def return_book(self, isbn: str) -> None:
        """Mark a book as available again.

        An unknown ISBN raises ValueError (consistent with borrow());
        returning a book that is already available is a harmless no-op.
        """
        book = self.find_by_isbn(isbn)
        if book is None:
            raise ValueError(f"No book with ISBN {isbn!r}.")
        book["available"] = True

    def available_books(self) -> list[dict]:
        """Return a list containing only available books."""
        return [book for book in self.books if book["available"]]

    def count(self) -> int:
        """Return the total number of books in the catalogue."""
        return len(self.books)


def is_even(number: int) -> bool:
    """Return True for even integers and False for odd integers."""
    return number % 2 == 0
