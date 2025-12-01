"""
File management module for handling file operations.
"""

import requests
import json
from typing import List, Dict, Any
from iearth_downloader.system.const import sys_config


class FileManager:
    """Manages file operations including fetching file lists."""

    def fetch_file_list(self, table: str, path: str) -> List[Dict[str, Any]]:
        """
        Fetch file list for a specific path from the API.

        Args:
            table: The table name
            path: The path to fetch files for

        Returns:
            List of file information dictionaries
        """
        payload = {
            "params": {
                "table": table,
                "path": path,
                "page": 1,
                "enableSpatialQuery": False,
                "count": 100000,
            }
        }

        try:
            print(f"Fetching file list for path: {path}")
            response = requests.post(sys_config.file_list_api, json=payload)
            response.raise_for_status()

            data = response.json()
            return data.get("response", [])

        except requests.exceptions.RequestException as e:
            print(f"Error fetching file list for path {path}: {e}")
            return []
        except json.JSONDecodeError as e:
            print(f"Error parsing response for path {path}: {e}")
            return []
