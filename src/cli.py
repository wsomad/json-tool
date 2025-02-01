# import click
# import json

# @click.command()
# @click.option("--file", required=True, help="Path to JSON file")
# @click.option("--action", required=True, type=click.Choice(["add", "update", "delete", "read", "list"]), help="Action to perform")
# @click.option("--id", help="Primary key of the object")
# @click.option("--key", help="Attribute key to add or update")
# @click.option("--value", help="Value to add or update")
# def main(file, action, id, key, value):
#     """JSON CLI Tool"""
#     # Read the JSON data from the file
#     with open(file, "r") as f:
#         data = json.load(f)
    
#     if action == "add":
#         # Ensure the ID exists
#         if id not in data:
#             data[id] = {}
#             click.echo("ID or key not found.")
#             return
        
#         # Add the new key-value pair
#         data[id][key] = value
    
#     elif action == "update":
#         # Update an existing key-value pair
#         if id in data and key in data[id]:
#             data[id][key] = value
#         else:
#             click.echo("ID or key not found.")
#             return

#     elif action == "delete":
#         # Delete the key-value pair
#         if id in data and key in data[id]:
#             del data[id][key]
#         else:
#             click.echo("ID or key not found.")
#             return

#     elif action == "read":
#         # Read and display the contents
#         click.echo(json.dumps(data, indent=4))

#     elif action == "list":
#         # List all keys for the given ID
#         if id in data:
#             click.echo(json.dumps(data[id], indent=4))
#         else:
#             click.echo("ID not found.")
#             return

#     # Write the updated data back to the file
#     with open(file, "w") as f:
#         json.dump(data, f, indent=4)

#     click.echo(f"Executed {action} on {file} with ID={id}, KEY={key}, VALUE={value}")

# if __name__ == "__main__":
#     main()

# import argparse
# import json_handler

# def print_menu():
#     """Displays the available commands when the tool is run with 'start'."""
#     menu = """
#     🛠️ JSON CLI Tool 🛠️
#     ------------------------------------
#     Select an action:

#     [1] Add a new attribute to an object
#     [2] Update an existing attribute
#     [3] Delete an object based on primary key
#     [4] Read an object by primary key
#     [5] List all primary keys in the JSON file
#     [6] Exit

#     Type the number and press Enter to continue.
#     """

#     print(menu)

# def handle_selection():
#     """Handles user selection from the menu."""
#     handler = json_handler("examples/sample.json")  # Your JSON file
#     while True:
#         print_menu()
#         choice = input("👉 Enter your choice: ").strip()

#         if choice == "1":
#             pk = input("Enter primary key: ").strip()
#             key = input("Enter key to add: ").strip()
#             value = input("Enter value: ").strip()
#             handler.add_attribute(pk, key, value)
#             print("✅ Attribute added successfully!")

#         elif choice == "2":
#             pk = input("Enter primary key: ").strip()
#             key = input("Enter key to update: ").strip()
#             value = input("Enter new value: ").strip()
#             handler.update_attribute(pk, key, value)
#             print("✅ Attribute updated successfully!")

#         elif choice == "3":
#             pk = input("Enter primary key: ").strip()
#             handler.delete_object(pk)
#             print("✅ Object deleted successfully!")

#         elif choice == "4":
#             pk = input("Enter primary key: ").strip()
#             obj = handler.read_object(pk)
#             print(f"📄 Object Data: {obj}" if obj else "❌ Object not found.")

#         elif choice == "5":
#             primary_keys = handler.list_primary_keys()
#             print("📌 Primary Keys:")
#             for index, key in enumerate(primary_keys, start=1):
#                 print(f"  [{index}] {key}")

#         elif choice == "6":
#             print("👋 Exiting...")
#             break

#         else:
#             print("❌ Invalid choice. Please try again.")

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="JSON Tool CLI")
#     parser.add_argument("action", help="Command to execute", nargs="?")

#     args = parser.parse_args()

#     if args.action == "json-tool start":
#         handle_selection()
#     else:
#         print("❌ Unknown command. Use 'json-tool start' to begin.")

# import sys
# print("Arguments received:", sys.argv)

import argparse
import sys
from json_handler import JSONHandler # Ensure correct import

def print_menu():
    """Displays the available commands when the tool is run with 'start'."""
    menu = """
    🛠️ JSON CLI Tool 🛠️
    ------------------------------------
    Select an action:

    [1] Add a new attribute to an object
    [2] Update an existing attribute
    [3] Delete an object based on primary key
    [4] Read an object by primary key
    [5] List all primary keys in the JSON file
    [6] Exit

    Type the number and press Enter to continue.
    """
    print(menu)

def handle_selection():
    """Handles user selection from the menu."""
    handler = JSONHandler("examples/sample.json")  # Ensure this is a class in json_handler.py
    
    while True:
        print_menu()
        choice = input("👉 Enter your choice: ").strip()

        if choice == "1":
            pk = input("Enter primary key: ").strip()
            key = input("Enter key to add: ").strip()
            value = input("Enter value: ").strip()
            handler.add_attribute(pk, key, value)
            print("✅ Attribute added successfully!")

        elif choice == "2":
            pk = input("Enter primary key: ").strip()
            key = input("Enter key to update: ").strip()
            value = input("Enter new value: ").strip()
            handler.update_attribute(pk, key, value)
            print("✅ Attribute updated successfully!")

        elif choice == "3":
            pk = input("Enter primary key: ").strip()
            handler.delete_object(pk)
            print("✅ Object deleted successfully!")

        elif choice == "4":
            pk = input("Enter primary key: ").strip()
            obj = handler.read_object(pk)
            print(f"📄 Object Data: {obj}" if obj else "❌ Object not found.")

        elif choice == "5":
            primary_keys = handler.list_primary_keys()
            print("📌 Primary Keys:")
            for index, key in enumerate(primary_keys, start=1):
                print(f"  [{index}] {key}")

        elif choice == "6":
            print("👋 Exiting...")
            break

        else:
            print("❌ Invalid choice. Please try again.")

def main():
    parser = argparse.ArgumentParser(description="JSON Tool CLI")
    parser.add_argument("action", help="Command to execute", nargs="?")

    args = parser.parse_args()

    if args.action == "json-tool start":  # FIXED
        handle_selection()
    else:
        print("❌ Unknown command. Use 'json-tool start' to begin.")

if __name__ == "__main__":
    main()


