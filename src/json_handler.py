# import json

# class JSONHandler:
#     def __init__(self, file_path):
#         self.file_path = file_path

#     # Load JSON file
#     def load_json(self):
#         "Load JSON file."
#         try:
#             with open(self.file_path, "r", encoding="utf-8") as file:
#                 return json.load(file)
#         except (FileNotFoundError, json.JSONDecodeError):
#             return []
        
#     # Save JSON file
#     def save_json(self, data):
#         "Save JSON data to file."
#         with open(self.file_path, "w", encoding="utf-8") as file:
#             json.dump(data, file, indent=4)

#     # Add new attribute based on its primary key
#     def add_attribute(self, primary_key, key, value):
#         "Add new attribute."
#         data = self.load_json()
#         for obj in data:
#             if obj.get("id") == primary_key:
#                 obj[key] = value
#                 self.save_json(data)
#                 return f"Successfully added '{key}' attribute to '{primary_key}' object."
#         return f"No object with ID:{primary_key} is found."

#     # Update existing attribute based on its primary key
#     def update_attribute(self, primary_key, key, value):
#         "Update an attribute based on its primary key."
#         data = self.load_json()
#         for obj in data:
#             if obj.get("id") == primary_key:
#                 if key in obj:
#                     obj[key] = value
#                     self.save_json(data)
#                     return f"Successfully updated '{key}' attribute to '{primary_key}' object."
#                 return f"Key '{key}' is not found in '{primary_key}' object."
#         return f"No object with ID:{primary_key} is found."

#     # Read specific object based on its primary key
#     def read_object(self, primary_key):
#         "Read object based on its primary key."
#         data = self.load_json()
#         for obj in data:
#             if obj.get("id") == primary_key:
#                 return json.dumps(obj, indent=4)
#         return f"No object with ID:{primary_key} is found."

#     # Delete specific object based on its primary key
#     def delete_object(self, primary_key):
#         "Delete an object based on its primary key."
#         data = self.load_json()
#         new_data = [obj for obj in data if obj.get("id") != primary_key]
#         if len(new_data) == len(data):
#             return f"No object with ID:{primary_key} is found."
#         self.save_json(new_data)
#         return f"Successfully delete '{primary_key}' object."

#     # Get all primary keys
#     def read_all_primary_keys(self):
#         "Read all primary keys."
#         data = self.load_json()
#         return [obj.get("id") for obj in data if "id" in obj]

        
import json

class JSONHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        print(f"Using file path: {self.file_path}")

    # Load JSON file
    def load_json(self):
        """Load JSON file."""
        print(f"Using file path: {self.file_path}")
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return None  # Returning None if the file is empty or invalid

    # Save JSON file
    def save_json(self, data):
        print(f"Using file path: {self.file_path}")
        """Save JSON data to file."""
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    # Recursive function to handle nested structures (dicts, lists, etc.)
    def _handle_nested_structure(self, obj, primary_key, key, value):
        """Recursively find and add/update the attribute in nested structures."""
        if isinstance(obj, dict):
            # Check if the current dictionary has the primary key
            if obj.get("id") == primary_key:
                obj[key] = value
                return True  # Found and updated
            # Otherwise, recurse through the dictionary values
            for nested_key, nested_value in obj.items():
                if isinstance(nested_value, (dict, list)):
                    if self._handle_nested_structure(nested_value, primary_key, key, value):
                        return True
        elif isinstance(obj, list):
            # Recurse through each item in the list
            for item in obj:
                if isinstance(item, (dict, list)):
                    if self._handle_nested_structure(item, primary_key, key, value):
                        return True
        return False  # If no match found in the structure

    # Add new attribute based on its primary key
    def add_attribute(self, primary_key, key, value):
        """Add a new attribute to an object based on its primary key."""
        data = self.load_json()
        if isinstance(data, list):  # Only proceed if the data is a list
            for obj in data:
                if isinstance(obj, dict) and obj.get("id") == primary_key:
                    obj[key] = value
                    self.save_json(data)
                    return f"Successfully added '{key}' attribute to '{primary_key}' object."
                # If primary key not found at top level, handle nested structures
                if self._handle_nested_structure(obj, primary_key, key, value):
                    self.save_json(data)
                    return f"Successfully added '{key}' attribute to nested object with ID '{primary_key}'."
        return f"No object with ID:{primary_key} is found or data is in an unsupported format."

    # Update existing attribute based on its primary key
    def update_attribute(self, primary_key, key, value):
        """Update an attribute based on its primary key."""
        data = self.load_json()
        if isinstance(data, list):  # Only proceed if the data is a list
            for obj in data:
                if isinstance(obj, dict) and obj.get("id") == primary_key:
                    if key in obj:
                        obj[key] = value
                        self.save_json(data)
                        return f"Successfully updated '{key}' attribute to '{primary_key}' object."
                # If primary key not found at top level, handle nested structures
                if self._handle_nested_structure(obj, primary_key, key, value):
                    self.save_json(data)
                    return f"Successfully updated '{key}' attribute in nested object with ID '{primary_key}'."
        return f"No object with ID:{primary_key} is found or data is in an unsupported format."

    # Read specific object based on its primary key
    def read_object(self, primary_key):
        """Read object based on its primary key."""
        data = self.load_json()
        if isinstance(data, list):  # Only proceed if the data is a list
            for obj in data:
                if isinstance(obj, dict) and obj.get("id") == primary_key:
                    return json.dumps(obj, indent=4)
                # If primary key not found at top level, handle nested structures
                result = self._handle_nested_structure(obj, primary_key, key=None, value=None)
                if result:
                    return json.dumps(result, indent=4)
        return f"No object with ID:{primary_key} is found or data is in an unsupported format."

    # Delete specific object based on its primary key
    def delete_object(self, primary_key):
        """Delete an object based on its primary key."""
        data = self.load_json()
        if isinstance(data, list):  # Only proceed if the data is a list
            new_data = [obj for obj in data if isinstance(obj, dict) and obj.get("id") != primary_key]
            if len(new_data) == len(data):
                return f"No object with ID:{primary_key} is found."
            self.save_json(new_data)
            return f"Successfully deleted '{primary_key}' object."
        return f"Data is in an unsupported format."

    # Get all primary keys
    def read_all_primary_keys(self):
        """Read all primary keys."""
        data = self.load_json()
        if isinstance(data, list):  # Only proceed if the data is a list
            return [obj.get("id") for obj in data if isinstance(obj, dict) and "id" in obj]
        return []

