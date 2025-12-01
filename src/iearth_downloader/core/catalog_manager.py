"""
Catalog management module for handling catalog data operations.
"""

import json
import requests
from typing import List, Dict, Any
from iearth_downloader.config.config import RESOURCE_ID
from iearth_downloader.system.const import sys_config


class CatalogManager:
    """Manages catalog data operations including fetching and processing."""

    def __init__(self, catalog_file_path: str, resource_id: int = None):
        self.catalog_data = {}
        self.catalog_file = catalog_file_path
        self.resource_id = resource_id if resource_id is not None else RESOURCE_ID

    def flatten_catalog_paths(
        self, catalog_data: List[Dict[str, Any]], parent_path: str = ""
    ) -> List[str]:
        """
        Recursively flatten the catalog structure to generate paths.

        Args:
            catalog_data: List of catalog items with potential children
            parent_path: Current path prefix

        Returns:
            List of flattened paths
        """
        paths = []

        for item in catalog_data:
            current_path = (
                f"{parent_path}/{item['label']}" if parent_path else item["label"]
            )

            if "children" in item and item["children"]:
                # Recursively process children
                paths.extend(self.flatten_catalog_paths(item["children"], current_path))
            else:
                # This is a leaf node, add the path
                paths.append(current_path)

        return paths

    def fetch_catalog_data(self) -> bool:
        """
        Fetch catalog data from API and save to JSON file.

        Returns:
            bool: True if successful, False otherwise
        """
        url = f"{sys_config.catalog_api}?id={self.resource_id}"

        try:
            print("Fetching catalog data from API...")
            response = requests.get(url)
            response.raise_for_status()

            # Parse the JSON response
            data = response.json()

            # Extract catalog, table, and type
            catalog = data.get("catalog", [])
            table = data.get("table", "")
            data_type = data.get("type", "")

            # Flatten the catalog to generate paths
            print("Processing catalog structure...")
            paths = self.flatten_catalog_paths(catalog)

            # Create the output structure
            output = {"path": paths, "table": table, "type": data_type}

            # Write to catalog.json
            with open(self.catalog_file, "w", encoding="utf-8") as f:
                json.dump(output, f, indent=2, ensure_ascii=False)

            print(f"Successfully wrote {len(paths)} paths to {self.catalog_file}")
            print(f"Table: {table}")
            print(f"Type: {data_type}")

            self.catalog_data = output
            return True

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from API: {e}")
            return False
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False

    def load_catalog_data(self) -> Dict[str, Any]:
        """
        Load catalog data from catalog.json file.

        Returns:
            Dictionary containing catalog data with paths, table, and type
        """
        try:
            with open(self.catalog_file, "r", encoding="utf-8") as f:
                catalog_data = json.load(f)
            self.catalog_data = catalog_data
            return catalog_data
        except FileNotFoundError:
            print(
                f"Error: {self.catalog_file} file not found. Please run fetch_catalog_data() first."
            )
            return {}
        except json.JSONDecodeError as e:
            print(f"Error parsing {self.catalog_file}: {e}")
            return {}

    def get_paths(self) -> List[str]:
        """Get the list of paths from loaded catalog data."""
        return self.catalog_data.get("path", [])

    def get_table(self) -> str:
        """Get the table name from loaded catalog data."""
        return self.catalog_data.get("table", "")

    def get_data_type(self) -> str:
        """Get the data type from loaded catalog data."""
        return self.catalog_data.get("type", "")
