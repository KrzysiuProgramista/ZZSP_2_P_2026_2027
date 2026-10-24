import logging
import sys
from copy import deepcopy

# Configure logging to write all application events to app.log.
logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    force=True,
)

log = logging.getLogger(__name__)


class EquipmentCheckout:
    def __init__(self):
        self.equipment = {
            101: {"name": "Laptop", "available": True},
            102: {"name": "Projector", "available": True},
            103: {"name": "Camera", "available": True},
        }

    def show_state(self):
        log.debug("Current equipment state: %s", self.equipment)

    def register_equipment(self, item_id, name):
        if not isinstance(item_id, int) or item_id <= 0:
            log.warning("Invalid equipment ID for registration: %r", item_id)
            return False

        if item_id in self.equipment:
            log.warning("Equipment ID already exists: %s", item_id)
            return False

        self.equipment[item_id] = {
            "name": name,
            "available": True,
        }

        log.info(
            "Equipment registered successfully: ID=%s, name=%s",
            item_id, name,
        )
        self.show_state()
        return True

    def borrow_equipment(self, item_id):
        if not isinstance(item_id, int) or item_id <= 0:
            log.warning("Invalid equipment ID for borrowing: %r", item_id)
            return False

        if item_id not in self.equipment:
            log.warning("Equipment ID does not exist: %s", item_id)
            return False

        try:
            item = self.equipment[item_id]

            if not item["available"]:
                log.warning(
                    "Attempt to borrow unavailable equipment: ID=%s, name=%s",
                    item_id, item.get("name", "Unknown"),
                )
                return False

            item["available"] = False
            log.info(
                "Equipment borrowed successfully: ID=%s, name=%s",
                item_id, item["name"],
            )
            self.show_state()
            return True

        except Exception:
            log.exception(
                "Unexpected failure while borrowing equipment ID=%s",
                item_id,
            )
            return False

    def return_equipment(self, item_id):
        if not isinstance(item_id, int) or item_id <= 0:
            log.warning("Invalid equipment ID for return: %r", item_id)
            return False

        if item_id not in self.equipment:
            log.warning("Equipment ID does not exist: %s", item_id)
            return False

        try:
            item = self.equipment[item_id]

            if item["available"]:
                log.warning(
                    "Attempt to return equipment that is not borrowed: "
                    "ID=%s, name=%s",
                    item_id, item.get("name", "Unknown"),
                )
                return False

            item["available"] = True
            log.info(
                "Equipment returned successfully: ID=%s, name=%s",
                item_id, item["name"],
            )
            self.show_state()
            return True

        except Exception:
            log.exception(
                "Unexpected failure while returning equipment ID=%s",
                item_id,
            )
            return False

    def display_equipment(self):
        print("\nEquipment inventory")
        print("-" * 48)

        for item_id, item in sorted(self.equipment.items()):
            status = "Available" if item.get("available") else "Borrowed"
            print(f"ID: {item_id} | {item.get('name', 'Unknown')} "
                  f"| Status: {status}")

    def run(self):
        log.info("Application started")

        try:
            while True:
                print(
                    "\n1. Display equipment"
                    "\n2. Register equipment"
                    "\n3. Borrow equipment"
                    "\n4. Return equipment"
                    "\n5. Exit"
                )

                choice = input("Choose an option: ").strip()

                if choice == "1":
                    self.display_equipment()
                elif choice == "2":
                    try:
                        item_id = int(input("Enter equipment ID: "))
                    except ValueError:
                        log.warning("Invalid equipment ID entered")
                        print("The ID must be an integer.")
                        continue

                    name = input("Enter equipment name: ").strip()
                    if name:
                        self.register_equipment(item_id, name)
                    else:
                        log.warning("Equipment name cannot be empty")
                elif choice == "3":
                    try:
                        item_id = int(input("Enter equipment ID: "))
                    except ValueError:
                        log.warning("Invalid equipment ID entered")
                        print("The ID must be an integer.")
                        continue

                    self.borrow_equipment(item_id)
                elif choice == "4":
                    try:
                        item_id = int(input("Enter equipment ID: "))
                    except ValueError:
                        log.warning("Invalid equipment ID entered")
                        print("The ID must be an integer.")
                        continue

                    self.return_equipment(item_id)
                elif choice == "5":
                    break
                else:
                    log.warning("Invalid menu option: %r", choice)
                    print("Invalid option. Please try again.")

        except Exception:
            log.exception("Unexpected application failure")
        finally:
            log.info("Application shut down")


def run_demo():
    app = EquipmentCheckout()
    log.info("Application started (automated test mode)")

    try:
        # Successful operation 1: register equipment.
        app.register_equipment(104, "Tablet")

        # Successful operation 2: borrow equipment.
        app.borrow_equipment(101)

        # Successful operation 3: return equipment.
        app.return_equipment(101)

        # Successful operation 4: borrow newly registered equipment.
        app.borrow_equipment(104)

        # Successful operation 5: return the tablet.
        app.return_equipment(104)

        # Successful operation 6: register another item.
        app.register_equipment(105, "Microphone")

        # Invalid operation 1: unavailable equipment.
        app.borrow_equipment(101)
        app.borrow_equipment(101)

        # Invalid operation 2: return an item that is not borrowed.
        app.return_equipment(102)

        # Invalid operation 3: unknown equipment ID.
        app.borrow_equipment(999)

        # Invalid operation 4: invalid menu choice.
        log.warning("Invalid menu option: '9'")

        # Invalid operation 5: malformed equipment ID.
        app.borrow_equipment(-5)

        # Test an unexpected internal failure. This deliberately
        # simulates corrupted inventory data to test the traceback.
        app.equipment[106] = {"name": "Faulty Scanner"}
        app.borrow_equipment(106)

    except Exception:
        log.exception("Unexpected failure during automated tests")
    finally:
        log.info("Application shut down (automated test mode)")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        run_demo()
    else:
        EquipmentCheckout().run()