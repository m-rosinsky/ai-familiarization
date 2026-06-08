import os
import sqlite3
from pathlib import Path

from pydantic import BaseModel, Field


class Tools:
    def __init__(self):
        self.valves = self.Valves()

    class Valves(BaseModel):
        db_path: str = Field(
            default="",
            description="Full path to warehouse.db on your machine (e.g. C:/code/ai-familiarization/inventory_db/warehouse.db)",
        )

    def _get_db_path(self) -> Path:
        if self.valves.db_path.strip():
            return Path(self.valves.db_path.strip()).expanduser().resolve()

        if env_path := os.environ.get("WAREHOUSE_DB_PATH"):
            return Path(env_path).expanduser().resolve()

        raise FileNotFoundError(
            "Database path not configured. Open the tool's Valves settings and set db_path "
            "to the full path of warehouse.db."
        )

    def _validate_db_path(self) -> Path:
        db_path = self._get_db_path()
        if not db_path.exists():
            raise FileNotFoundError(
                f"Warehouse database not found at {db_path}. "
                "Ensure init_db.py has been executed and db_path is set correctly in the tool Valves."
            )
        return db_path

    def query_warehouse_items(self) -> list[str]:
        """
        Queries the local SQLite database to check what items are entered into the warehouse inventory system.
        :return: A list of strings detailing the item names.
        """
        try:
            conn = sqlite3.connect(self._validate_db_path())
            cursor = conn.cursor()
            cursor.execute("SELECT item_name FROM inventory ORDER BY item_name")
            items = [row[0] for row in cursor.fetchall()]
            conn.close()
            return items
        except sqlite3.Error as e:
            raise RuntimeError(f"An error occurred while querying the database: {e}") from e

    def query_item_details(self, item_name: str) -> str:
        """
        Look up an item's quantity and warehouse location by name.
        :param item_name: The name of the inventory item to look up.
        :return: A string describing the item's quantity and location.
        """
        try:
            conn = sqlite3.connect(self._validate_db_path())
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
