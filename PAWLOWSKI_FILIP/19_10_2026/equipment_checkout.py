import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

LOG_FILE = Path(__file__).resolve().parent / "app.log"

log = logging.getLogger("equipment")


class EquipmentError(Exception):
    pass


@dataclass
class Equipment:
    item_id: int
    name: str
    available: bool = True
    borrower: Optional[str] = None


class EquipmentManager:
    def __init__(self):
        self.items = {}
        for item_id, name in ((1, "Laptop"), (2, "Projector"), (3, "Camera")):
            self.items[item_id] = Equipment(item_id, name)
        log.info("Loaded %d default items", len(self.items))
        self._log_state()

    def _log_state(self):
        state = ", ".join(
            f"{i.item_id}={'available' if i.available else 'borrowed'}"
            for i in self.items.values()
        )
        log.debug("State: %s", state or "(empty)")

    def _get(self, item_id):
        if item_id not in self.items:
            log.warning("Invalid ID: no equipment with id=%d", item_id)
            raise EquipmentError(f"No equipment with ID {item_id}.")
        return self.items[item_id]

    @staticmethod
    def _maybe_fail(operation):
        if os.environ.get("SIMULATE_FAILURE") == operation:
            raise RuntimeError(f"Simulated failure during '{operation}'")

    def add(self, item_id, name):
        if item_id in self.items:
            log.warning("Duplicate ID rejected: id=%d already exists", item_id)
            raise EquipmentError(f"ID {item_id} is already in use.")
        self.items[item_id] = Equipment(item_id, name)
        log.info("Registered new equipment: id=%d name=%r", item_id, name)
        self._log_state()

    def borrow(self, item_id, student):
        item = self._get(item_id)
        if not item.available:
            log.warning("Borrow refused: id=%d is held by %s", item_id, item.borrower)
            raise EquipmentError(f"{item.name} is already borrowed.")
        self._maybe_fail("borrow")
        item.available, item.borrower = False, student
        log.info("Borrowed: id=%d name=%r by %s", item_id, item.name, student)
        self._log_state()

    def return_item(self, item_id):
        item = self._get(item_id)
        if item.available:
            log.warning("Return refused: id=%d is not borrowed", item_id)
            raise EquipmentError(f"{item.name} is not currently borrowed.")
        student = item.borrower
        item.available, item.borrower = True, None
        log.info("Returned: id=%d name=%r by %s", item_id, item.name, student)
        self._log_state()


MENU = """
=== Student Equipment Borrowing ===
1. Display available equipment
2. Borrow an item
3. Return an item
4. Add new equipment
5. Display status of all equipment
6. Exit
"""


def ask_id(prompt="Equipment ID: "):
    text = input(prompt).strip()
    try:
        value = int(text)
        if value <= 0:
            raise ValueError
        return value
    except ValueError:
        log.warning("Invalid ID entered (must be a positive integer): %r", text)
        raise EquipmentError("ID must be a positive whole number.")


def show(items):
    if not items:
        print("  (nothing to show)")
    for i in items:
        status = "available" if i.available else f"borrowed by {i.borrower}"
        print(f"  [{i.item_id}] {i.name} - {status}")


def handle(choice, mgr):
    if choice == "1":
        show([i for i in mgr.items.values() if i.available])
    elif choice == "2":
        item_id = ask_id()
        student = input("Student name: ").strip()
        if not student:
            log.warning("Borrow refused: empty student name")
            raise EquipmentError("Student name is required.")
        mgr.borrow(item_id, student)
        print("Item borrowed.")
    elif choice == "3":
        mgr.return_item(ask_id())
        print("Item returned.")
    elif choice == "4":
        item_id = ask_id("New equipment ID: ")
        name = input("Equipment name: ").strip()
        if not name:
            log.warning("Add refused: empty equipment name")
            raise EquipmentError("Equipment name is required.")
        mgr.add(item_id, name)
        print("Equipment added.")
    elif choice == "5":
        show(list(mgr.items.values()))
    elif choice == "6":
        return False
    else:
        log.warning("Invalid menu option: %r", choice)
        print("Invalid option, please choose 1-6.")
    return True


def main():
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.DEBUG,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )
    log.info("Application started")
    mgr = EquipmentManager()
    running = True
    while running:
        print(MENU)
        try:
            running = handle(input("Choose an option: ").strip(), mgr)
        except EquipmentError as err:
            print(f"Error: {err}")
        except EOFError:
            log.info("Input stream closed")
            break
        except Exception:
            log.exception("Unexpected failure while handling the request")
            print("Unexpected error - see app.log for details.")
    log.info("Application shut down")


if __name__ == "__main__":
    main()
