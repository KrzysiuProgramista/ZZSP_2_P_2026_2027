from typing import Optional


class LibraryCatalog:
    def __init__(self):
        self.books: list[dict] = []

    def add_book(self, title: str, author: str, isbn: str, year: int) -> None:
        if self.find_by_isbn(isbn) is not None:
            raise ValueError("Book with this ISBN already exists")

        book = {
            "title": title,
            "author": author,
            "isbn": isbn,
            "year": year,
            "available": True
        }
        self.books.append(book)

    def remove_book(self, isbn: str) -> bool:
        for book in self.books:
            if book["isbn"] == isbn:
                self.books.remove(book)
                return True
        return False

    def find_by_author(self, author: str) -> list[dict]:
        result = []
        for book in self.books:
            if book["author"].lower() == author.lower():
                result.append(book)
        return result

    def find_by_isbn(self, isbn: str) -> Optional[dict]:
        for book in self.books:
            if book["isbn"] == isbn:
                return book
        return None

    def borrow(self, isbn: str) -> None:
        book = self.find_by_isbn(isbn)
        if book is None:
            raise ValueError("Unknown ISBN")
        if not book["available"]:
            raise ValueError("Book is already borrowed")

        book["available"] = False

    def return_book(self, isbn: str) -> None:
        book = self.find_by_isbn(isbn)
        if book is None:
            raise ValueError("Unknown ISBN")

        book["available"] = True

    def available_books(self) -> list[dict]:
        result = []
        for book in self.books:
            if book["available"]:
                result.append(book)
        return result

    def count(self) -> int:
        return len(self.books)


def is_even(number: int) -> bool:
    if number % 2 == 0:
        return True
    else:
        return False