# json-tool

'json-tool' is a CLI-based program that facilitates the management process of JSON file in terms of create, read, update, and delete. As for now as I'm busy with other things, this tool is available only for direct changing on JSON file by directly giving input to the command line. In the future, features like read/write content in bulk from text file (.txt) will be introduced.

## Tech Stack

- **CLI:** Only Python

- **CI/CD:** GitHub Actions

## Scope

- **Developer:** Able to manage their JSON file privately on local machine as they can download the json-tool.exe program.

## Usage & Options
### How to Start:
  ```bash
    json-tool [commands]
  ```

### Commands Available:
  ```bash
    start               Start the json-tool CLI [json-tool start]
    help                Show help message [json-tool help]
  ```

### Helpers Available:
  ```bash
    -o key=value        Create an object with key-value pairs [-o key1=-s value1 key2=-i 42 key3=-b true]
    -s value            Create a string value [-s John]
    -i value            Create an integer value [-i 123]
    -f value            Create a float value [-f 9.8]
    -b value            Create a boolean value [-b true]
    -c value            Create a character value [-c j]
    -a value            Create an array [-a]
  ```

### Read/Write JSON File:
  ```bash
    JSON file:
        read            Read JSON file [DRIVE:/path-to-json-file/.json] or [DRIVE:\path-to-json-file\.json]
        write           No need to think. Automatically write and save

    JSON object:
        nested key      Use '.' to specify nested keys in object [user.profile.name]
  ```


