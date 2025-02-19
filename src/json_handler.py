import json
import os

class JSONHandler:
    # Init function
    def __init__(self, file_path):
        self.file_path = file_path

    # Load file function
    def load_json(self):
        if not os.path.exists(self.file_path):
            print(f"[Error] The file '{self.file_path}' does not exist.")
            return None
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"[Error] Couldn't load this JSON file: {str(e)}")
            return None

    # Save file function
    def save_json(self, data):
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
        except (TypeError, ValueError):
            return None

    # Convert value function
    def convert_value(self, flag, value):
        try:
            if flag == "-o":
                if value:
                    data_dict = {}
                    key_value_pairs = value.split()
                    i = 0

                    while i < len(key_value_pairs):
                        pair = key_value_pairs[i]
                        try:
                            key, val = pair.split("=")
                            if val.startswith('-'):
                                flag_type = val
                                value = key_value_pairs[i + 1]
                                data_dict[key] = self.convert_value(flag_type, value) 
                            else:
                                data_dict[key] = val
                            i += 2
                        except ValueError:
                            print(f"[Error] Invalid key=value pair '{pair}'")
                            break 
                    return data_dict  
                return {}
            elif flag == "-a":
                return []
            elif flag == "-s":
                return str(value)
            elif flag == "-i":
                return int(value)
            elif flag == "-f":
                return float(value)
            elif flag == "-b":
                return value.lower() in ("true", "1", "yes")
            elif flag == "-c":
                return value[0] if value else ""
            else:
                return value
        except ValueError as e:
            return None

    # Identify reference ID function
    def set_identity(self, id):
        try:
            if ":" in id:
                key, value = id.split(":")
                return key.strip(), value.strip()  
            return None, None
        except (TypeError, ValueError):
            return None, None
    
    # Add nested key function
    def _add_nested_key(self, obj, key_path, value):
        keys = key_path.split(".")
        current = obj
        
        if current:
            for k in keys[:-1]:
                if isinstance(current, dict) and k in current:
                    if k not in current:
                        current[k] = {}
                    current = current[k]
                else:
                    return False
                
            last_key = keys[-1]

            if isinstance(current, dict):
                current[last_key] = value
                return True
            return False
        return False
    
    # Update nested key function
    def _update_nested_key(self, obj, key_path, value):
        keys = key_path.split(".")
        current = obj

        for k in keys[:-1]:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return False
            
        last_key = keys[-1]

        if isinstance(current, dict) and last_key in current:
            current[last_key] = value
            return True
        return False

    # Add attribute function
    def add_attribute(self, primary_key, key_path, flag, value):
        value = self.convert_value(flag, value)
        if value is None:
            print(f"[Error] Unable to add key-value pair because that value with flag '{flag}' is invalid.")  
            return "[Error] Operation aborted due to invalid value."

        data = self.load_json()

        if isinstance(data, list):
            for obj in data:
                if isinstance(obj, dict) and obj.get("id") == primary_key:
                    if self._add_nested_key(obj, key_path, value):
                        self.save_json(data)
                        return f"[Success] Successfully added value to key [{key_path}]:[{value}] under reference key [{primary_key}]."
        return f"No object with ID:{primary_key} found."

    # Update attribute function
    def update_attribute(self, primary_key, key_path, flag, value):
        value = self.convert_value(flag, value) 
        if value is None:
            print(f"[Error] Unable to update key-value pair because that value with flag '{flag}' is invalid.")  
            return "[Error] Operation aborted due to invalid value."
        
        data = self.load_json()

        if isinstance(data, list):
            for obj in data:
                if isinstance(obj, dict) and obj.get("id") == primary_key:
                    if self._update_nested_key(obj, key_path, value):
                        self.save_json(data)
                        return f"[Success] Successfully updated value [{value}] to key [{key_path}] under reference key [{primary_key}]."
                    else:
                        return f"Invalid key path '{key_path}' for ID '{primary_key}'."
        return f"No object with ID:{primary_key} found."

    # def update_attribute(self, identifier, key_path, flag, value):
    #     key, primary_value = self.set_identity(identifier)  # Extract key and value
    #     if not key or not primary_value:
    #         return "Invalid reference format."

    #     value = self.convert_value(flag, value)  # Convert value
    #     data = self.load_json()  # Load JSON file

    #     if isinstance(data, list):
    #         for obj in data:
    #             if isinstance(obj, dict) and obj.get(key) == primary_value:  # Match key
    #                 if self._update_nested_key(obj, key_path, value):
    #                     self.save_json(data)  # Save changes
    #                     return f"Updated [{key_path}] with [{value}] for {key} [{primary_value}]."
    #                 else:
    #                     return f"Invalid key path '{key_path}' for {key} '{primary_value}'."
    #     return f"No object with {key}='{primary_value}' found."

    # Read attribute function
    def read_attribute(self, primary_key):
        data = self.load_json()
        if isinstance(data, list):
            for obj in data:
                if isinstance(obj, dict) and obj.get("id") == primary_key:
                    return json.dumps(obj, indent=4)
        return f"No object with ID:{primary_key} found."

    # Delete attribute function
    def delete_attribute(self, primary_key):
        data = self.load_json()
        if isinstance(data, list):
            new_data = [obj for obj in data if isinstance(obj, dict) and obj.get("id") != primary_key]
            if len(new_data) == len(data):
                return f"[Error] No object with reference key={primary_key} found."
            self.save_json(new_data)
            return f"[Success] Successfully deleted object with reference key='{primary_key}'."
        return f"[Error] Data is in an unsupported format."

    # Read all reference IDs
    def read_all_reference_ids(self):
        data = self.load_json()
        if isinstance(data, list):
            return [obj.get("id") for obj in data if isinstance(obj, dict) and "id" in obj]
        return []
