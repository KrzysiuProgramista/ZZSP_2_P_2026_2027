import logging

log = logging.getLogger("equipment_checkout")

# inventory maps ID -> {"name": ..., "available": True/False, "borrower": ...}
inventory = {}


def setup_logging():
    logging.basicConfig(
        filename="app.log",
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def state_snapshot():
    snapshot = {}
    for item_id, item in inventory.items():
        snapshot[item_id] = "available" if item["available"] else "borrowed"
    return snapshot


def ask_id(prompt):
    raw = input(prompt)
    item_id = raw.strip().upper()
    if item_id == "" or " " in item_id:
        log.warning("Invalid equipment ID entered: %r", raw)
        print("Invalid ID. It cannot be empty or contain spaces.")
        return None
    return item_id


def add_item(item_id, name):
    if item_id in inventory:
        log.warning("Attempt to add duplicate equipment ID %s", item_id)
        print("An item with ID", item_id, "already exists.")
        return
    inventory[item_id] = {"name": name, "available": True, "borrower": None}
    log.info("Registered new equipment %s (%s)", item_id, name)
    log.debug("State after add: %s", state_snapshot())
    print("Added", name, "with ID", item_id)


def borrow_item(item_id, student):
    if item_id not in inventory:
        log.warning("Borrow attempted with unknown ID %s", item_id)
        print("No equipment with ID", item_id)
        return
    item = inventory[item_id]
    if not item["available"]:
        log.warning("Borrow attempted for unavailable item %s (held by %s)",
                    item_id, item["borrower"])
        print(item["name"], "is already borrowed.")
        return
    item["available"] = False
    item["borrower"] = student
    log.info("Item %s (%s) borrowed by %s", item_id, item["name"], student)
    log.debug("State after borrow: %s", state_snapshot())
    print(student, "borrowed", item["name"])


def return_item(item_id):
    if item_id not in inventory:
        log.warning("Return attempted with unknown ID %s", item_id)
        print("No equipment with ID", item_id)
        return
    item = inventory[item_id]
    if item["available"]:
        log.warning("Return attempted for item %s which is not borrowed", item_id)
        print(item["name"], "is not currently borrowed.")
        return
    student = item["borrower"]
    item["available"] = True
    item["borrower"] = None
    log.info("Item %s (%s) returned by %s", item_id, item["name"], student)
    log.debug("State after return: %s", state_snapshot())
    print(item["name"], "returned. Thank you,", student)


def display_available():
    print("\nAvailable equipment:")
    count = 0
    for item_id, item in inventory.items():
        if item["available"]:
            print(" ", item_id, "-", item["name"])
            count += 1
    if count == 0:
        print("  (none)")
    log.debug("Displayed %d available item(s)", count)


def display_status():
    print("\nEquipment status:")
    for item_id, item in inventory.items():
        if item["available"]:
            status = "Available"
        else:
            status = "Borrowed by " + item["borrower"]
        print(" ", item_id, "-", item["name"], "-", status)
    log.debug("Displayed status of %d item(s)", len(inventory))


def handle_borrow():
    item_id = ask_id("Equipment ID to borrow: ")
    if item_id is None:
        return
    student = input("Student name: ").strip()
    if student == "":
        log.warning("Borrow attempted for %s with empty student name", item_id)
        print("Student name cannot be empty.")
        return
    borrow_item(item_id, student)


def handle_return():
    item_id = ask_id("Equipment ID to return: ")
    if item_id is not None:
        return_item(item_id)


def handle_add():
    item_id = ask_id("New equipment ID: ")
    if item_id is None:
        return
    name = input("Equipment name: ").strip()
    if name == "":
        log.warning("Add attempted for %s with empty name", item_id)
        print("Name cannot be empty.")
        return
    add_item(item_id, name)


def main():
    setup_logging()
    log.info("Application started")
    add_item("L-001", "Laptop")
    add_item("P-001", "Projector")
    add_item("C-001", "Camera")

    while True:
        print("\n=== Equipment Checkout ===")
        print("1. Display available equipment")
        print("2. Borrow an item")
        print("3. Return a borrowed item")
        print("4. Add new equipment")
        print("5. Display status of all equipment")
        print("6. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "6":
            break
        try:
            match choice:
                case "1":
                    display_available()
                case "2":
                    handle_borrow()
                case "3":
                    handle_return()
                case "4":
                    handle_add()
                case "5":
                    display_status()
                case _:
                    log.warning("Invalid menu option: %r", choice)
                    print("Invalid option. Please enter a number from 1 to 6.")
        except Exception:
            log.exception("Unexpected failure while running menu option %s", choice)
            print("Something went wrong. Details were written to the log.")

    log.info("Application shut down")
    print("Goodbye!")


if __name__ == "__main__":
    main()