"""
equipment_checkout.py

A menu-driven application that manages equipment borrowed by students
(laptops, projectors, cameras, etc.).

Menu:
  1. Display all available equipment.
  2. Borrow an item.
  3. Return a borrowed item.
  4. Add a new equipment item.
  5. Display the current status of all equipment.
  6. Exit the application.

Logging:
  - All diagnostic information goes to app.log (never print()).
  - DEBUG: internal state (item ids + availability) after every successful
    change.
  - INFO: startup/shutdown, successful borrow/return, new item registered.
  - WARNING: invalid menu choice, borrowing an unavailable item, returning
    an item that isn't borrowed, invalid/unknown ids.
  - ERROR: unexpected failures, logged with log.exception() to capture the
    traceback.
"""

import logging

logging.basicConfig(
    filename="app.log",
    filemode="a",
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

log = logging.getLogger("equipment_checkout")


class DuplicateIdError(Exception):
    """Raised when adding an item whose id already exists."""


class EquipmentNotFoundError(Exception):
    """Raised when an id does not match any known item."""


class EquipmentCatalog:
    """Holds equipment items as a list of dicts:
    {id, name, available}.
    """

    def __init__(self):
        self.items: list[dict] = []

    # -- internal helpers ----------------------------------------------
    def _find(self, item_id: str) -> dict:
        for item in self.items:
            if item["id"] == item_id:
                return item
        log.warning("Invalid/unknown equipment id requested: %r", item_id)
        raise EquipmentNotFoundError(f"Unknown equipment id: {item_id!r}")

    def _log_state(self) -> None:
        state = [(i["id"], i["available"]) for i in self.items]
        log.debug("Current state: %s", state)

    # -- public API ------------------------------------------------------
    def add_item(self, item_id: str, name: str) -> None:
        if any(i["id"] == item_id for i in self.items):
            log.warning("Attempt to add duplicate id=%s (name=%s)", item_id, name)
            raise DuplicateIdError(f"Equipment id already exists: {item_id!r}")
        self.items.append({"id": item_id, "name": name, "available": True})
        log.info("Registered new equipment: id=%s name=%s", item_id, name)
        self._log_state()

    def borrow(self, item_id: str) -> None:
        item = self._find(item_id)
        if not item["available"]:
            log.warning("Attempt to borrow unavailable item id=%s name=%s", item_id, item["name"])
            raise ValueError(f"Item {item_id!r} is already borrowed.")
        item["available"] = False
        log.info("Borrowed: id=%s name=%s", item_id, item["name"])
        self._log_state()

    def return_item(self, item_id: str) -> None:
        item = self._find(item_id)
        if item["available"]:
            log.warning("Attempt to return item that isn't borrowed id=%s name=%s", item_id, item["name"])
            raise ValueError(f"Item {item_id!r} was not borrowed.")
        item["available"] = True
        log.info("Returned: id=%s name=%s", item_id, item["name"])
        self._log_state()

    def available_items(self) -> list[dict]:
        return [i for i in self.items if i["available"]]

    def all_items(self) -> list[dict]:
        return list(self.items)


def seed_catalog(catalog: EquipmentCatalog) -> None:
    catalog.add_item("L1", "Laptop - Dell XPS")
    catalog.add_item("L2", "Laptop - MacBook Air")
    catalog.add_item("P1", "Projector - Epson")
    catalog.add_item("C1", "Camera - Canon EOS")


def print_menu() -> None:
    print(
        "\nEquipment Checkout\n"
        "1. Display available equipment\n"
        "2. Borrow an item\n"
        "3. Return a borrowed item\n"
        "4. Add a new equipment item\n"
        "5. Display status of all equipment\n"
        "6. Exit"
    )


def format_item(item: dict) -> str:
    status = "available" if item["available"] else "borrowed"
    return f"  {item['id']:<4} {item['name']:<28} [{status}]"


def run(catalog: EquipmentCatalog, inputs=None) -> None:
    """Run the menu loop. If `inputs` is given, it's used instead of
    interactive input() -- this lets the automated test run below drive
    the application without a human typing at a terminal."""

    def get_input(prompt: str) -> str:
        if inputs is not None:
            try:
                value = next(inputs)
            except StopIteration:
                value = "6"
            print(prompt + value)
            return value
        return input(prompt)

    log.info("Application starting up.")

    while True:
        print_menu()
        choice = get_input("Choose an option (1-6): ").strip()

        try:
            if choice == "1":
                items = catalog.available_items()
                if not items:
                    print("No equipment is currently available.")
                else:
                    print("Available equipment:")
                    for item in items:
                        print(format_item(item))

            elif choice == "2":
                item_id = get_input("Enter the id of the item to borrow: ").strip()
                catalog.borrow(item_id)
                print(f"Borrowed {item_id}.")

            elif choice == "3":
                item_id = get_input("Enter the id of the item to return: ").strip()
                catalog.return_item(item_id)
                print(f"Returned {item_id}.")

            elif choice == "4":
                item_id = get_input("New item id: ").strip()
                name = get_input("New item name: ").strip()
                catalog.add_item(item_id, name)
                print(f"Added {item_id} ({name}).")

            elif choice == "5":
                print("All equipment:")
                for item in catalog.all_items():
                    print(format_item(item))

            elif choice == "6":
                log.info("Application shutting down.")
                print("Goodbye.")
                break

            else:
                log.warning("Invalid menu option entered: %r", choice)
                print("Invalid option. Please choose 1-6.")

        except (DuplicateIdError, EquipmentNotFoundError, ValueError) as exc:
            # Expected, user-facing failures: already logged as WARNING
            # inside the catalog methods. Just report to the user here.
            print(f"Error: {exc}")

        except Exception:
            # Unexpected failure: capture the full traceback.
            log.exception("Unexpected error while handling option %r", choice)
            print("An unexpected error occurred. See app.log for details.")


def _force_unexpected_error(catalog: EquipmentCatalog) -> None:
    """Deliberately trigger and log one unexpected exception, to satisfy
    the 'at least one exception logged with its traceback' requirement."""
    try:
        # item["available"] on None -> TypeError, something that isn't a
        # normal, already-handled catalog error.
        broken_item = None
        _ = broken_item["available"]
    except Exception:
        log.exception("Unexpected error encountered during a forced test")


def automated_demo() -> None:
    """Run >=10 operations automatically: >=5 successful, >=3 invalid,
    and 1 that triggers a logged exception with a traceback."""
    catalog = EquipmentCatalog()
    seed_catalog(catalog)  # 4 successful "add" operations, logged already

    scripted_inputs = iter([
        "1",            # display available
        "2", "L1",      # borrow L1 -> success (5th op overall)
        "2", "L1",      # borrow L1 again -> invalid (already borrowed)
        "3", "L1",      # return L1 -> success
        "3", "P1",      # return P1 (not borrowed) -> invalid
        "2", "ZZZ",     # borrow unknown id -> invalid
        "4", "C2", "Camera - Sony A7",  # add new item -> success
        "5",            # display status
        "9",            # invalid menu option -> invalid
        "6",            # exit
    ])

    run(catalog, inputs=scripted_inputs)

    # One deliberate, unexpected (non-catalog) exception with traceback.
    _force_unexpected_error(catalog)


if __name__ == "__main__":
    automated_demo()
