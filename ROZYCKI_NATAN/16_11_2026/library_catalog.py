from typing import Optional


class LibraryCatalog:
    """A small in-memory library catalogue.

    Each book is stored as a dictionary with these keys:
    title, author, isbn, year, available.
    """

    def __init__(self) -> None:
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
        for index, book in enumerate(self.books):
            if book["isbn"] == isbn:
                del self.books[index]
                return True
        return False

    def find_by_author(self, author: str) -> list[dict]:
        """Return books by author; the search must ignore letter case."""
        target = author.casefold()
        return [book for book in self.books if book["author"].casefold() == target]

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
            raise ValueError(f"Unknown ISBN: {isbn!r}")
        if not book["available"]:
            raise ValueError(f"Book with ISBN {isbn!r} is already borrowed.")
        book["available"] = False

    def return_book(self, isbn: str) -> None:
        """Mark a book as available again.

        Raises ValueError if the ISBN is unknown in the catalogue.
        """
        book = self.find_by_isbn(isbn)
        if book is None:
            raise ValueError(f"Unknown ISBN: {isbn!r}")
        book["available"] = True

    def available_books(self) -> list[dict]:
        """Return a list containing only available books."""
        return [book for book in self.books if book["available"]]

    def count(self) -> int:
        """Return the total number of books in the catalogue."""
        return len(self.books)