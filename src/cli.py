import click
import json

@click.command()
@click.option("--file", required=True, help="Path to JSON file")
@click.option("--action", required=True, type=click.Choice(["add", "update", "delete", "read", "list"]), help="Action to perform")
@click.option("--id", help="Primary key of the object")
@click.option("--key", help="Attribute key to add or update")
@click.option("--value", help="Value to add or update")
def main(file, action, id, key, value):
    """JSON CLI Tool"""
    # Read the JSON data from the file
    with open(file, "r") as f:
        data = json.load(f)
    
    if action == "add":
        # Ensure the ID exists
        if id not in data:
            data[id] = {}
            click.echo("ID or key not found.")
            return
        
        # Add the new key-value pair
        data[id][key] = value
    
    elif action == "update":
        # Update an existing key-value pair
        if id in data and key in data[id]:
            data[id][key] = value
        else:
            click.echo("ID or key not found.")
            return

    elif action == "delete":
        # Delete the key-value pair
        if id in data and key in data[id]:
            del data[id][key]
        else:
            click.echo("ID or key not found.")
            return

    elif action == "read":
        # Read and display the contents
        click.echo(json.dumps(data, indent=4))

    elif action == "list":
        # List all keys for the given ID
        if id in data:
            click.echo(json.dumps(data[id], indent=4))
        else:
            click.echo("ID not found.")
            return

    # Write the updated data back to the file
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

    click.echo(f"Executed {action} on {file} with ID={id}, KEY={key}, VALUE={value}")

if __name__ == "__main__":
    main()
