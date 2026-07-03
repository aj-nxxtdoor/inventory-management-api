import requests
import sys

BASE_URL = "http://127.0.0.1:5000"


def list_items():
    response = requests.get(f"{BASE_URL}/items")
    items = response.json()

    if not items:
        print("No items in inventory.")
        return

    for item in items:
        print(f"[{item['id']}] {item['name']} | Qty: {item['quantity']} | Price: {item['price']} | Barcode: {item['barcode']}")


def add_item():
    name = input("Item name: ")
    barcode = input("Barcode (optional): ")
    category = input("Category (optional): ")
    quantity = input("Quantity: ")
    price = input("Price: ")

    payload = {
        "name": name,
        "barcode": barcode or None,
        "category": category or None,
        "quantity": int(quantity) if quantity else 0,
        "price": float(price) if price else None
    }

    response = requests.post(f"{BASE_URL}/items", json=payload)

    if response.status_code == 201:
        print("Item added successfully:")
        print(response.json())
    else:
        print("Error adding item:", response.json())


def update_item():
    item_id = input("Item ID to update: ")
    field = input("Field to update (name/barcode/category/quantity/price): ")
    value = input(f"New value for {field}: ")

    if field in ["quantity"]:
        value = int(value)
    elif field in ["price"]:
        value = float(value)

    payload = {field: value}

    response = requests.patch(f"{BASE_URL}/items/{item_id}", json=payload)

    if response.status_code == 200:
        print("Item updated successfully:")
        print(response.json())
    else:
        print("Error updating item:", response.json())


def delete_item():
    item_id = input("Item ID to delete: ")
    response = requests.delete(f"{BASE_URL}/items/{item_id}")

    if response.status_code == 200:
        print(response.json())
    else:
        print("Error deleting item:", response.json())


def import_from_barcode():
    barcode = input("Barcode to import: ")
    quantity = input("Quantity: ")
    price = input("Price: ")

    payload = {
        "barcode": barcode,
        "quantity": int(quantity) if quantity else 0,
        "price": float(price) if price else None
    }

    response = requests.post(f"{BASE_URL}/items/import", json=payload)

    if response.status_code == 201:
        print("Product imported successfully:")
        print(response.json())
    else:
        print("Error importing product:", response.json())


def main_menu():
    while True:
        print("\n--- Inventory Management CLI ---")
        print("1. List all items")
        print("2. Add new item")
        print("3. Update an item")
        print("4. Delete an item")
        print("5. Import item from barcode (OpenFoodFacts)")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            list_items()
        elif choice == "2":
            add_item()
        elif choice == "3":
            update_item()
        elif choice == "4":
            delete_item()
        elif choice == "5":
            import_from_barcode()
        elif choice == "6":
            print("Goodbye!")
            sys.exit()
        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main_menu()