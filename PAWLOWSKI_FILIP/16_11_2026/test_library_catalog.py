import copy
import sys
import unittest

from library_catalog import LibraryCatalog
from number_utils import is_even


def make_catalog() -> LibraryCatalog:
    catalog = LibraryCatalog()
    catalog.add_book("Dune", "Frank Herbert", "978-001", 1965)
    catalog.add_book("The Trial", "Franz Kafka", "978-002", 1925)
    catalog.add_book("The Castle", "Franz Kafka", "978-003", 1926)
    return catalog



class TestAddingBooks(unittest.TestCase):

    def setUp(self):
        self.catalog = make_catalog()

    def test_add_book_success(self):
        self.catalog.add_book("Solaris", "Stanisław Lem", "978-004", 1961)

        self.assertEqual(self.catalog.count(), 4)
        self.assertIsNotNone(self.catalog.find_by_isbn("978-004"))

    def test_new_book_is_available(self):
        self.catalog.add_book("Solaris", "Stanisław Lem", "978-004", 1961)

        self.assertTrue(self.catalog.find_by_isbn("978-004")["available"])

    def test_add_duplicate_isbn_raises(self):
        with self.assertRaises(ValueError):
            self.catalog.add_book("Another Dune", "Someone Else", "978-001", 2001)

    def test_failed_add_leaves_catalog_unchanged(self):
        before = copy.deepcopy(self.catalog.books)

        with self.assertRaises(ValueError):
            self.catalog.add_book("Another Dune", "Someone Else", "978-001", 2001)

        self.assertEqual(self.catalog.books, before)

    def test_count_with_three_books(self):
        self.assertEqual(self.catalog.count(), 3)

    def test_count_of_empty_catalog(self):
        self.assertEqual(LibraryCatalog().count(), 0)


class TestRemovingBooks(unittest.TestCase):

    def setUp(self):
        self.catalog = make_catalog()

    def test_remove_existing_book(self):
        self.assertTrue(self.catalog.remove_book("978-001"))

        self.assertEqual(self.catalog.count(), 2)
        self.assertIsNone(self.catalog.find_by_isbn("978-001"))

    def test_remove_unknown_book(self):
        self.assertFalse(self.catalog.remove_book("000-000"))

        self.assertEqual(self.catalog.count(), 3)

    def test_remove_same_book_twice(self):
        self.assertTrue(self.catalog.remove_book("978-002"))
        self.assertFalse(self.catalog.remove_book("978-002"))


class TestSearching(unittest.TestCase):

    def setUp(self):
        self.catalog = make_catalog()

    def test_find_by_author_ignores_case(self):
        found = self.catalog.find_by_author("FRANZ kafka")

        self.assertEqual(len(found), 2)
        self.assertEqual({b["isbn"] for b in found}, {"978-002", "978-003"})

    def test_find_by_author_unknown(self):
        self.assertEqual(self.catalog.find_by_author("Jane Austen"), [])

    def test_find_by_isbn_success(self):
        book = self.catalog.find_by_isbn("978-001")

        self.assertIsNotNone(book)
        self.assertEqual(book["title"], "Dune")

    def test_find_by_isbn_unknown(self):
        self.assertIsNone(self.catalog.find_by_isbn("000-000"))

    def test_available_books_skips_borrowed(self):
        self.catalog.borrow("978-001")

        titles = [b["title"] for b in self.catalog.available_books()]

        self.assertEqual(titles, ["The Trial", "The Castle"])

    def test_available_books_when_nothing_is_borrowed(self):
        self.assertEqual(len(self.catalog.available_books()), 3)


class TestBorrowing(unittest.TestCase):

    def setUp(self):
        self.catalog = make_catalog()

    def test_borrow_success(self):
        self.catalog.borrow("978-002")

        self.assertFalse(self.catalog.find_by_isbn("978-002")["available"])

    def test_borrow_already_borrowed_raises(self):
        self.catalog.borrow("978-002")

        with self.assertRaises(ValueError):
            self.catalog.borrow("978-002")

    def test_borrow_unknown_isbn_raises(self):
        with self.assertRaises(ValueError):
            self.catalog.borrow("000-000")

    def test_return_book_success(self):
        self.catalog.borrow("978-003")
        self.catalog.return_book("978-003")

        self.assertTrue(self.catalog.find_by_isbn("978-003")["available"])

    def test_return_unknown_isbn_raises(self):
        with self.assertRaises(ValueError):
            self.catalog.return_book("000-000")

    def test_borrow_then_return_restores_availability(self):
        available_before = len(self.catalog.available_books())

        self.catalog.borrow("978-001")
        self.assertEqual(len(self.catalog.available_books()), available_before - 1)

        self.catalog.return_book("978-001")
        self.assertEqual(len(self.catalog.available_books()), available_before)
        self.assertTrue(self.catalog.find_by_isbn("978-001")["available"])

    def test_failed_borrow_leaves_catalog_unchanged(self):
        before = copy.deepcopy(self.catalog.books)

        with self.assertRaises(ValueError):
            self.catalog.borrow("000-000")

        self.assertEqual(self.catalog.books, before)

    def test_borrowing_twice_leaves_book_borrowed(self):
        self.catalog.borrow("978-001")
        before = copy.deepcopy(self.catalog.books)

        with self.assertRaises(ValueError):
            self.catalog.borrow("978-001")

        self.assertEqual(self.catalog.books, before)



class TestSubTest(unittest.TestCase):

    def test_is_even_for_many_inputs(self):
        cases = [
            (0, True),
            (2, True),
            (10, True),
            (100, True),
            (-4, True),
            (1, False),
            (7, False),
            (99, False),
            (-3, False),
        ]

        for number, expected in cases:
            with self.subTest(number=number, expected=expected):
                self.assertEqual(is_even(number), expected)



class TestSkipping(unittest.TestCase):

    @unittest.skip("not implemented yet")
    def test_export_to_csv(self):
        self.fail("This would fail, but it is never executed.")

    @unittest.skipIf(sys.platform == "win32", "posix only")
    def test_posix_only(self):
        self.assertNotEqual(sys.platform, "win32")

    @unittest.expectedFailure
    def test_known_bug_title_search(self):
        self.assertEqual(LibraryCatalog().find_by_title("Dune"), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
