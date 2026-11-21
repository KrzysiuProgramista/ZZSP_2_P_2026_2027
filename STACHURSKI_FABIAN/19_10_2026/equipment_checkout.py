import logging

logging.basicConfig(
    filename="app.log",
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

items = {
    "1": ["Laptop", False],
    "2": ["Projector", False],
    "3": ["Camera", False],
}


def log_state():
    logging.debug(str(items))


def main():
    logging.info("Start")
    log_state()

    while True:
        print("\n1.Available 2.Borrow 3.Return 4.Add 5.Status 6.Exit")
        c = input("> ").strip()

        try:
            if c == "1":
                for k, v in items.items():
                    if not v[1]:
                        print(k, v[0])
                logging.info("Listed available")

            elif c == "2":
                i = input("ID: ").strip()
                if i not in items or items[i][1]:
                    print("Cannot borrow")
                    logging.warning(f"Cannot borrow {i}")
                else:
                    items[i][1] = True
                    print("Borrowed")
                    logging.info(f"Borrowed {i}")
                    log_state()

            elif c == "3":
                i = input("ID: ").strip()
                if i not in items or not items[i][1]:
                    print("Cannot return")
                    logging.warning(f"Cannot return {i}")
                else:
                    items[i][1] = False
                    print("Returned")
                    logging.info(f"Returned {i}")
                    log_state()

            elif c == "4":
                i = input("ID: ").strip()
                n = input("Name: ").strip()
                if not i or not n or i in items:
                    print("Bad ID")
                    logging.warning(f"Bad ID {i}")
                else:
                    items[i] = [n, False]
                    print("Added")
                    logging.info(f"Added {i}")
                    log_state()

            elif c == "5":
                for k, v in items.items():
                    print(k, v[0], "borrowed" if v[1] else "available")
                logging.info("Listed all")

            elif c == "6":
                break

            elif c == "99":
                1 / 0

            else:
                print("Invalid choice")
                logging.warning(f"Invalid choice {c}")

        except Exception:
            print("Error")
            logging.exception("Error")

    logging.info("Stop")


main()