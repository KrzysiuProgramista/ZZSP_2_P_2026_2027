import logging

logging.basicConfig(
    level=logging.DEBUG,
    filename="app.log",
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

log = logging.getLogger(__name__)

equipment = {
    101: {"name": "Laptop", "available": True},
    102: {"name": "Projector", "available": True},
    103: {"name": "Camera", "available": True},
}


def log_internal_state():
    state = {item_id: data["available"] for item_id, data in equipment.items()}
    log.debug("Internal state updated: %s", state)


def display_available():
    print("\n--- Available Equipment ---")
    found = False
    for item_id, data in equipment.items():
        if data["available"]:
            print(f"ID: {item_id} | Name: {data['name']}")
            found = True
    if not found:
        print("No equipment available.")


def display_all_status():
    print("\n--- Current Equipment Status ---")
    for item_id, data in equipment.items():
        status = "Available" if data["available"] else "Borrowed"
        print(f"ID: {item_id} | Name: {data['name']} | Status: {status}")


def borrow_item():
    raw_id = input("Enter item ID to borrow: ").strip()
    try:
        item_id = int(raw_id)
    except ValueError:
        log.exception("Unexpected failure converting item ID: %s", raw_id)
        print("Invalid input. ID must be a number.")
        return

    if item_id not in equipment:
        log.warning("Invalid ID: %s does not exist", item_id)
        print("Item with this ID does not exist.")
        return

    if not equipment[item_id]["available"]:
        log.warning("Attempt to borrow unavailable item ID %s", item_id)
        print("This item is currently unavailable.")
        return

    equipment[item_id]["available"] = False
    log.info("Borrowed item ID %s (%s)", item_id, equipment[item_id]["name"])
    log_internal_state()
    print(f"Successfully borrowed {equipment[item_id]['name']}.")


def return_item():
    raw_id = input("Enter item ID to return: ").strip()
    try:
        item_id = int(raw_id)
    except ValueError:
        log.exception("Unexpected failure converting item ID: %s", raw_id)
        print("Invalid input. ID must be a number.")
        return

    if item_id not in equipment:
        log.warning("Invalid ID: %s does not exist", item_id)
        print("Item with this ID does not exist.")
        return

    if equipment[item_id]["available"]:
        log.warning("Attempt to return item ID %s which is not borrowed", item_id)
        print("This item was not borrowed.")
        return

    equipment[item_id]["available"] = True
    log.info("Returned item ID %s (%s)", item_id, equipment[item_id]["name"])
    log_internal_state()
    print(f"Successfully returned {equipment[item_id]['name']}.")


def add_item():
    raw_id = input("Enter new item ID: ").strip()
    try:
        item_id = int(raw_id)
    except ValueError:
        log.exception("Unexpected failure converting new item ID: %s", raw_id)
        print("Invalid input. ID must be a number.")
        return

    if item_id in equipment:
        log.warning("Invalid ID: duplicate item ID %s", item_id)
        print("An item with this ID already exists.")
        return

    name = input("Enter equipment name: ").strip()
    if not name:
        log.warning("Invalid equipment name: empty value for ID %s", item_id)
        print("Equipment name cannot be empty.")
        return

    equipment[item_id] = {"name": name, "available": True}
    log.info("Registered new equipment ID %s (%s)", item_id, name)
    log_internal_state()
    print(f"Successfully added {name} (ID: {item_id}).")


def main():
    log.info("Application started")

    while True:
        print("\n=== Equipment Checkout Menu ===")
        print("1. Display all available equipment")
        print("2. Borrow an item")
        print("3. Return a borrowed item")
        print("4. Add a new equipment item")
        print("5. Display the current status of all equipment")
        print("6. Exit the application")

        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            display_available()
        elif choice == "2":
            borrow_item()
        elif choice == "3":
            return_item()
        elif choice == "4":
            add_item()
        elif choice == "5":
            display_all_status()
        elif choice == "6":
            log.info("Application shut down")
            print("Goodbye!")
            break
        else:
            log.warning("Invalid menu option selected: %s", choice)
            print("Invalid option. Please choose between 1 and 6.")


if __name__ == "__main__":
    main()