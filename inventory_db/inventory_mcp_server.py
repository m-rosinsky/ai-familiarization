import os
import sqlite3
from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("warehouse-inventory")


def _get_db_path() -> Path:
    if env_path := os.environ.get("WAREHOUSE_DB_PATH"):
        return Path(env_path).expanduser().resolve()

    return (Path(__file__).parent / "warehouse.db").resolve()


def _validate_db_path() -> Path:
    db_path = _get_db_path()
    if not db_path.exists():
        raise FileNotFoundError(
            f"Warehouse database not found at {db_path}. "
            "Ensure init_db.py has been executed and WAREHOUSE_DB_PATH is set correctly."
        )
    return db_path


@mcp.tool()
def query_warehouse_items() -> list[str]:
    """Queries the local SQLite database to check what items are entered into the warehouse inventory system."""
    try:
        conn = sqlite3.connect(_validate_db_path())
        cursor = conn.cursor()
        cursor.execute("SELECT item_name FROM inventory ORDER BY item_name")
        items = [row[0] for row in cursor.fetchall()]
        conn.close()
        return items
    except sqlite3.Error as e:
        raise RuntimeError(f"An error occurred while querying the database: {e}") from e


@mcp.tool()
def query_item_details(item_name: str) -> str:
    """Look up an item's quantity and warehouse location by name."""
    try:
        conn = sqlite3.connect(_validate_db_path())
        cursor = conn.cursor()
        cursor.execute(
            "SELECT item_name, quantity, location FROM inventory WHERE LOWER(item_name) = LOWER(?)",
            (item_name,),
        )
        result = cursor.fetchone()
        conn.close()

        if result:
            name, quantity, location = result
            return f"Item: {name} | Quantity in stock: {quantity} | Location: {location}"
        return f"Item '{item_name}' was not found in the inventory database."
    except sqlite3.Error as e:
        raise RuntimeError(f"An error occurred while querying the database: {e}") from e


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
