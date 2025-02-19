import argparse
import textwrap
from json_handler import JSONHandler
import os

# Display actions menu
def actions_menu():
    menu = """
    [Welcome to json-tool]

    [1] Add Attribute
    [2] Update Attribute
    [3] Delete Attribute
    [4] Read Attribute
    [5] Show All Reference IDs
    [6] Exit
    """
    print(textwrap.dedent(menu))

def helps_menu():
    help_text = """
    Commands:
        start               Start the json-tool CLI [json-tool start]
        help                Show help message [json-tool help]

    How to:
        JSON file:
            read            Read JSON file [DRIVE:/path-to-json-file/.json] or [DRIVE:\\path-to-json-file\\.json]
            write           No need to think. Automatically write and save

        JSON object:
            nested key      Use '.' to specify nested keys in object [user.profile.name]

    Helpers:
        -o key=value        Create an object with key-value pairs [-o key1=-s value1 key2=-i 42 key3=-b true]
        -s value            Create a string value [-s John]
        -i value            Create an integer value [-i 123]
        -f value            Create a float value [-f 9.8]
        -b value            Create a boolean value [-b true]
        -c value            Create a character value [-c j]
        -a value            Create an array [-a]

    """
    print(textwrap.dedent(help_text))

def parse_input_value(input_str):
    parts = input_str.strip().split(" ", 1)
    if len(parts) == 2 and parts[0] in ["-s", "-i", "-f", "-b", "-c", "-o", "-a"]:
        return parts[0], parts[1]
    return None, input_str 

# Handle actions menu
def handle_actions_menu():
    file_path = input("\nPlease specify directory path of JSON file> ").strip()
    if not os.path.exists(file_path):
        print(f"Error: The file [{file_path}] does not exist.")
        return
    else:
        print(f"[{file_path}] is identified. Let's start!")

    handler = JSONHandler(file_path)
    # handler = JSONHandler("examples/sample.json")
    
    while True:
        actions_menu()
        choice = input("Select any option and press Enter to continue> ").strip()

        if choice == "1":  # Add a new attribute
            id = input("\nPlease specify reference ID of object> ").strip()
            key = input(f"[{id}] - Please specify key to add> ").strip()
            value_input = input(f"[{id}] - Please specify new value for [{key}]> ").strip()
            flag, value = parse_input_value(value_input)
            print(handler.add_attribute(id, key, flag, value))

        elif choice == "2":  # Update an existing attribute
            id = input("\nPlease specify reference ID of object> ").strip()
            key = input(f"[{id}] - Please specify key to update> ").strip()
            value_input = input(f"[{id}] - Please specify new value for [{key}]> ").strip()
            flag, value = parse_input_value(value_input)
            print(handler.update_attribute(id, key, flag, value))

        elif choice == "3":  # Delete an object
            id = input("\nPlease specify reference ID of object> ").strip()
            print(handler.delete_attribute(id))

        elif choice == "4":  # Read an object
            id = input("\nPlease specify reference ID of object> ").strip()
            print(handler.read_attribute(id))

        elif choice == "5":  # Show all reference IDs
            primary_keys = handler.read_all_reference_ids()
            print("All Reference IDs:")
            for index, key in enumerate(primary_keys, start=1):
                print(f"[{index}] {key}")

        elif choice == "6":  # Show help menu
            print("\nExiting... Bye Bye!")
            break

        else:
            print("\nInvalid option. Please try again.")

def main():
    parser = argparse.ArgumentParser(description="JSON Tool CLI")
    parser.add_argument("command", nargs="?", help="Command to execute", choices=["start", "help"])

    args = parser.parse_args()

    if args.command == "start":
        handle_actions_menu()
    elif args.command == "help":
        helps_menu()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
