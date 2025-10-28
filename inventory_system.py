"""
Inventory System Module

This module manages stock items by providing functions to add, remove,
and retrieve item quantities. It also allows saving/loading data
to/from a JSON file.
"""

import json
from datetime import datetime
import ast

# Global variable to store inventory data
stock_data = {}


def add_item(item="default", qty=0, logs=None):
    """
    Add a specified quantity of an item to the inventory.

    Args:
        item (str): The name of the item to add.
        qty (int): The quantity to add.
        logs (list, optional): A list for storing log entries.
    """
    if logs is None:
        logs = []
    if not isinstance(item, str) or not isinstance(qty, (int, float)):
        raise ValueError(
            "Item must be a string and quantity must be a number."
        )

    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")


def remove_item(item, qty):
    """
    Remove a specified quantity of an item from the inventory.

    Args:
        item (str): The name of the item to remove.
        qty (int): The quantity to remove.
    """
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except KeyError:
        print(f"Warning: '{item}' not found in inventory.")
    except TypeError:
        print("Error: Invalid quantity type.")


def get_qty(item):
    """
    Retrieve the quantity of a specific item.

    Args:
        item (str): The item name.

    Returns:
        int: Quantity available.
    """
    return stock_data.get(item, 0)


def load_data(file_path="inventory.json"):
    """
    Load stock data from a JSON file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        dict: Loaded stock data.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(
            f"File '{file_path}' not found. "
            "Starting with empty inventory."
        )
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON from '{file_path}'.")
        return {}


def save_data(file_path="inventory.json"):
    """
    Save stock data to a JSON file.

    Args:
        file_path (str): Path to the JSON file.
    """
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(stock_data, file, indent=4)


def print_data():
    """
    Print the current inventory data in a readable format.
    """
    print("\nItems Report:")
    for item, quantity in stock_data.items():
        print(f"{item} -> {quantity}")


def check_low_items(threshold=5):
    """
    Return a list of items with quantity below a given threshold.

    Args:
        threshold (int): The minimum quantity threshold.

    Returns:
        list: Items with quantity less than threshold.
    """
    return [item for item, qty in stock_data.items() if qty < threshold]


def main():
    """
    Main function to demonstrate inventory operations.
    """
    logs = []

    add_item("apple", 10, logs)
    add_item("banana", 2, logs)
    remove_item("apple", 3)
    remove_item("orange", 1)

    print(f"Apple stock: {get_qty('apple')}")
    print(f"Low items: {check_low_items()}")

    save_data()

    # Load data and assign to global dictionary
    data = load_data()
    stock_data.clear()
    stock_data.update(data)

    print_data()

    # Example of safe evaluation using ast.literal_eval
    expression = "{'note': 'safe eval example'}"
    result = ast.literal_eval(expression)
    print("Safe eval result:", result)

    print("\nLogs:")
    for entry in logs:
        print(entry)


if __name__ == "__main__":
    main()
