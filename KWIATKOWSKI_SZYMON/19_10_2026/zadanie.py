import logging

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

equipment = [
    {"id": "1", "name": "Laptop", "available": True},
    {"id": "2", "name": "Projector", "available": True},
    {"id": "3", "name": "Camera", "available": False},
]

def display_available():
  print()
  print("--- AVAILABLE EQUIPMENT ---")
  count = 0
  for item in equipment:
    if item["available"] == True:
      print("ID:", item["id"], "| Name:", item["name"])
      count = count + 1
  if count == 0:
    print("No equipment available.")
  logging.info("Displayed available equipment list.")


def borrow_equipment():
  print()
  print("--- BORROW EQUIPMENT ---")
  search_id = input("Enter equipment ID to borrow: ")

  found = False
  for item in equipment:
    if item["id"] == search_id:
      found = True
      if item["available"] == True:
        item["available"] = False
        print("Success! Borrowed:", item["name"])
        logging.info("Borrowed equipment with ID: " + search_id)
      else:
        print("Error: This equipment is already borrowed!")
        logging.warning("Attempted to borrow unavailable equipment ID: " + search_id)

  if found == False:
    print("Error: Equipment with this ID was not found.")
    logging.warning("Equipment ID not found: " + search_id)

def return_equipment():
  print()
  print("--- RETURN EQUIPMENT ---")
  search_id = input("Enter equipment ID to return: ")

  found = False
  for item in equipment:
    if item["id"] == search_id:
      found = True
      if item["available"] == False:
        item["available"] = True
        print("Success! Returned:", item["name"])
        logging.info("Returned equipment with ID: " + search_id)
      else:
        print("Error: This equipment was not borrowed!")
        logging.warning("Attempted to return available equipment ID: " + search_id)

  if found == False:
    print("Error: Equipment with this ID was not found.")
    logging.warning("Equipment ID not found: " + search_id)


def add_equipment():
  print()
  print("--- ADD NEW EQUIPMENT ---")
  new_id = input("Enter unique ID for new equipment: ")

  duplicate = False
  for item in equipment:
    if item["id"] == new_id:
      duplicate = True

  if duplicate == True:
    print("Error: Equipment with this ID already exists!")
    logging.error("Attempted to add equipment with duplicate ID: " + new_id)
  else:
    new_name = input("Enter equipment name: ")
    new_item = {"id": new_id, "name": new_name, "available": True}
    equipment.append(new_item)
    print("Success! Added new equipment:", new_name)
    logging.info("Added new equipment with ID: " + new_id)

def display_status():
  print()
  print("--- ALL EQUIPMENT STATUS ---")
  for item in equipment:
    if item["available"] == True:
      status = "Available"
    else:
      status = "Borrowed"
    print("ID:", item["id"], "| Name:", item["name"], "| Status:", status)
  logging.info("Displayed full equipment status.")


logging.info("Application started.")

while True:
  print()
  print("===============================")
  print(" EQUIPMENT MANAGEMENT SYSTEM ")
  print("===============================")
  print("1. Display available equipment")
  print("2. Borrow equipment")
  print("3. Return equipment")
  print("4. Add new equipment")
  print("5. Display all equipment status")
  print("6. Exit")

  choice = input("Select an option (1-6): ")

  if choice == "1":
    display_available()
  elif choice == "2":
    borrow_equipment()
  elif choice == "3":
    return_equipment()
  elif choice == "4":
    add_equipment()
  elif choice == "5":
    display_status()
  elif choice == "6":
    print("Program ended. Goodbye!")
    logging.info("Application closed.")
    break
  else:
    print("Error: Please select an option from 1 to 6.")
    logging.warning("Invalid menu option selected.")