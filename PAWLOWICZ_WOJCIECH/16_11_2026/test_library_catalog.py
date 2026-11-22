import sys
import unittest

from library_catalog import LibraryCatalog, is_even


def make_catalog() -> LibraryCatalog:
    """Exercise 4's setUp: a catalogue with three known books."""
    catalog = LibraryCatalog()
    catalog.add_book("Dune", "Frank Herbert", "ISBN-1", 1965)
    catalog.add_book("Foundation", "Isaac Asimov", "ISBN-2", 1951)
    catalog.add_book("Neuromancer", "William Gibson", "ISBN-3", 1984)
    return catalog


# ---------------------------------------------------------------------------
# Exercise 5: split into several TestCase classes, each with its own setUp.
# ---------------------------------------------------------------------------
class TestAddingBooks(unittest.TestCase):
    def setUp(self):
        self.catalog = make_catalog()

    def test_add_book_success(self):
        self.catalog.add_book("1984", "George Orwell", "ISBN-4", 1949)
        self.assertEqual(self.catalog.count(), 4)
        self.assertIsNotNone(self.catalog.find_by_isbn("ISBN-4"))

    def test_add_book_duplicate_isbn_raises(self):
        with self.assertRaises(ValueError):
            self.catalog.add_book("Another Dune", "Someone Else", "ISBN-1", 2000)
        # Failed operation must leave the catalogue unchanged.
        self.assertEqual(self.catalog.count(), 3)
        self.assertEqual(self.catalog.find_by_isbn("ISBN-1")["title"], "Dune")


class TestRemovingBooks(unittest.TestCase):
    def setUp(self):
        self.catalog = make_catalog()

    def test_remove_existing_book_returns_true(self):
        self.assertTrue(self.catalog.remove_book("ISBN-1"))
        self.assertEqual(self.catalog.count(), 2)
        self.assertIsNone(self.catalog.find_by_isbn("ISBN-1"))

    def test_remove_unknown_book_returns_false(self):
        self.assertFalse(self.catalog.remove_book("NO-SUCH-ISBN"))
        # Failed operation must leave the catalogue unchanged.
        self.assertEqual(self.catalog.count(), 3)


class TestSearching(unittest.TestCase):
    def setUp(self):
        self.catalog = make_catalog()

    def test_find_by_author_case_insensitive(self):
        results = self.catalog.find_by_author("frank herbert")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Dune")

    def test_find_by_author_no_match(self):
        self.assertEqual(self.catalog.find_by_author("Nobody"), [])

    def test_find_by_isbn_found(self):
        book = self.catalog.find_by_isbn("ISBN-2")
        self.assertEqual(book["title"], "Foundation")

    def test_find_by_isbn_not_found(self):
        self.assertIsNone(self.catalog.find_by_isbn("NO-SUCH-ISBN"))


class TestBorrowing(unittest.TestCase):
    def setUp(self):
        self.catalog = make_catalog()

    def test_borrow_success(self):
        self.catalog.borrow("ISBN-1")
        self.assertFalse(self.catalog.find_by_isbn("ISBN-1")["available"])

    def test_borrow_unknown_isbn_raises(self):
        with self.assertRaises(ValueError):
            self.catalog.borrow("NO-SUCH-ISBN")

    def test_borrow_already_borrowed_raises(self):
        self.catalog.borrow("ISBN-1")
        with self.assertRaises(ValueError):
            self.catalog.borrow("ISBN-1")
        # Failed operation must leave the catalogue unchanged (still
        # borrowed, not double-counted or reverted).
        self.assertFalse(self.catalog.find_by_isbn("ISBN-1")["available"])

    def test_return_success(self):
        self.catalog.borrow("ISBN-1")
        self.catalog.return_book("ISBN-1")
        self.assertTrue(self.catalog.find_by_isbn("ISBN-1")["available"])

    def test_return_unknown_isbn_raises(self):
        with self.assertRaises(ValueError):
            self.catalog.return_book("NO-SUCH-ISBN")

    def test_borrow_then_return_restores_availability(self):
        isbn = "ISBN-2"
        self.assertTrue(self.catalog.find_by_isbn(isbn)["available"])
        self.catalog.borrow(isbn)
        self.assertFalse(self.catalog.find_by_isbn(isbn)["available"])
        self.catalog.return_book(isbn)
        self.assertTrue(self.catalog.find_by_isbn(isbn)["available"])

    def test_available_books_excludes_borrowed(self):
        self.catalog.borrow("ISBN-1")
        available_isbns = {book["isbn"] for book in self.catalog.available_books()}
        self.assertNotIn("ISBN-1", available_isbns)
        self.assertIn("ISBN-2", available_isbns)
        self.assertIn("ISBN-3", available_isbns)

    def test_count(self):
        self.assertEqual(self.catalog.count(), 3)


# ---------------------------------------------------------------------------
# Exercise 6: subTest over many inputs.
# ---------------------------------------------------------------------------
class TestIsEven(unittest.TestCase):
    def test_is_even_over_many_inputs(self):
        cases = [
            (-4, True),
            (-3, False),
            (-2, True),
            (-1, False),
            (0, True),
            (1, False),
            (2, True),
            (3, False),
            (10, True),
            (7, False),
        ]
        for n, expected in cases:
            with self.subTest(n=n):
                self.assertEqual(is_even(n), expected)


# ---------------------------------------------------------------------------
# Exercise 7: skip and expectedFailure.
# ---------------------------------------------------------------------------
class TestNotYetImplemented(unittest.TestCase):
    @unittest.skip("not implemented yet")
    def test_future_feature_reserve_book(self):
        # Placeholder for a "reserve a borrowed book" feature that doesn't
        # exist yet.
        self.fail("reserve_book is not implemented")

    @unittest.skipIf(sys.platform == "win32", "posix only")
    def test_posix_only_behavior(self):
        # A stand-in for a check that only makes sense on POSIX systems.
        self.assertTrue(True)

    @unittest.expectedFailure
    def test_known_bug_duplicate_title_different_case(self):
        # Demonstrates expectedFailure: add_book() only rejects duplicate
        # ISBNs, not duplicate titles, so adding the same title twice
        # under a different ISBN currently succeeds -- which this test
        # (deliberately, as a documented known limitation) asserts should
        # NOT happen. It fails today, as expected.
        catalog = make_catalog()
        catalog.add_book("Dune", "Frank Herbert", "ISBN-999", 1965)
        duplicates = [b for b in catalog.books if b["title"] == "Dune"]
        self.assertEqual(len(duplicates), 1)


if __name__ == "__main__":
    unittest.main()
