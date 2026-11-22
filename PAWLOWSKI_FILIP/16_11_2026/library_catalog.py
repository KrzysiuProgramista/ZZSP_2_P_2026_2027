from typing import Optional


class LibraryCatalog:
    
    def __init__(self) -> None:
        self.books: list[dict] = []

    def add_book(self, title: str, author: str, isbn: str, year: int) -> None:
        if self.find_by_isbn(isbn) is not None:
            raise ValueError(f"ISBN {isbn} is already in the catalogue.")

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
        book = self.find_by_isbn(isbn)

        if book is None:
            return False

        self.books.remove(book)
        return True

    def find_by_author(self, author: str) -> list[dict]:
        wanted = author.casefold()
        return [b for b in self.books if b["author"].casefold() == wanted]

    def find_by_isbn(self, isbn: str) -> Optional[dict]:
        for book in self.books:
            if book["isbn"] == isbn:
                return book
        return None

    def borrow(self, isbn: str) -> None:
        book = self._get_or_raise(isbn)

        if not book["available"]:
            raise ValueError(f"Book {isbn} is already borrowed.")

        book["available"] = False

    def return_book(self, isbn: str) -> None:
        book = self._get_or_raise(isbn)
        book["available"] = True

    def available_books(self) -> list[dict]:
        return [b for b in self.books if b["available"]]

    def count(self) -> int:
        return len(self.books)

    def _get_or_raise(self, isbn: str) -> dict:
        book = self.find_by_isbn(isbn)

        if book is None:
            raise ValueError(f"No book with ISBN {isbn}.")

        return book
