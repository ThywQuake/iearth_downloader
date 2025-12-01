"""
Download module for handling file downloads and logging.
"""

import os
import requests
import threading  # For type hinting Optional[threading.Lock]
from typing import Dict, Any, Optional
from iearth_downloader.utils.encrypt_utils import encrypt4long

# Import constants from config that are NOT user credentials
from iearth_downloader.config.config import RESOURCE_ID

# TOKEN and USER_ACCOUNT are no longer imported directly from config
# FINISHED_LOG_FILE is also not needed here anymore as Logger gets its path from download_processor

from iearth_downloader.system.const import sys_config  # Import sys_config

# Import the auth module to access its getter functions for credentials
from iearth_downloader.utils import auth


class Downloader:
    """Handles file downloading and related operations."""

    def __init__(self, resource_id: int = None):
        """
        Initialize the Downloader.

        Args:
            resource_id: Optional resource ID to use. If None, uses the default from config.
        """
        self.resource_id = resource_id if resource_id is not None else RESOURCE_ID

    def download_file(self, fullpath: str, filename: str, local_path: str) -> bool:
        """
        Download a file using the encrypted fullpath and save it in the specified local path.
        Uses the token obtained from auth.py for authorization.
        """
        current_token = auth.get_token()  # Get token from auth module
        if not current_token:
            # This error should ideally be logged by the calling function in download_processor
            # print("Error in Downloader: No authentication token found. Please login first.")
            return False

        try:
            os.makedirs(local_path, exist_ok=True)
            local_file_path = os.path.join(local_path, filename)
            encrypt_fullpath = encrypt4long({"objectKey": fullpath})
            payload = {
                "objectKey": fullpath,
                "resourceId": str(self.resource_id),
                "userAccount": auth.get_user_account(),  # Get user_account from auth module
                "resourceType": "REMOTE_SENSING",
                "country": "Japan",
            }

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {current_token}",  # Use the retrieved token
            }

            # The print for starting download is now in download_processor's worker thread
            # New api call to get signed URL
            response = requests.post(
                sys_config.download_api, json=payload, headers=headers
            )
            signed_url = response.json()["signedUrl"]
            site = signed_url.split("/")[2].split(":")[0]
            params = signed_url.split("?")[1]
            signed_url = f"https://{site}/{fullpath}?{params}"
            # Decode the url from url encoding
            signed_url = requests.utils.unquote(signed_url)

            with open(local_file_path, "wb") as f:
                r = requests.get(signed_url, stream=True)
                for chunk in r.iter_content(chunk_size=sys_config.chunk_size):
                    if chunk:
                        f.write(chunk)

            # The print for successful download is now in download_processor's worker thread
            print(f"Successfully downloaded: {local_file_path}")
            return True

        except Exception as ex:
            # Errors (including print statements) are now handled by the calling worker in download_processor
            print(f"Error downloading file {filename}: {ex}")
            return False

    def record_download_info(self, fullpath: str, filename: str, size: int) -> bool:
        """
        Record download information by calling the API.
        Uses token and user_account obtained from auth.py.
        """
        current_token = auth.get_token()
        current_user_account = auth.get_user_account()

        if not current_token or not current_user_account:
            # This error should be logged by the calling function in download_processor
            # print("Error in Downloader: Missing token/user_account for recording. Ensure login was successful.")
            return False

        payload = {
            "resource_id": str(self.resource_id),
            "objectKey": fullpath,
            "token": current_token,  # Use retrieved token
            "userAccount": current_user_account,  # Use retrieved user_account
            "country": "China",
            "file_size": size,
            "file_name": filename,
            "resource_type": "REMOTE_SENSING",
        }

        try:
            # The print for starting recording is now in download_processor's worker thread
            response = requests.post(sys_config.record_api, json=payload)
            response.raise_for_status()
            # The print for successful recording is now in download_processor's worker thread
            return True

        except Exception:
            # Errors (including print statements) are now handled by the calling worker in download_processor
            return False


class Logger:
    """Handles logging operations for downloaded files."""

    def __init__(self, log_file: str, lock: Optional[threading.Lock] = None) -> None:
        """Initialize the logger with a log file and an optional lock."""
        self.log_file = log_file
        self.lock: Optional[threading.Lock] = lock  # Type hint for instance variable

    def initialize_fullpath_log(self) -> None:
        """Initialize or clear the log file."""
        try:
            if self.lock:
                self.lock.acquire()
            with open(self.log_file, "w", encoding="utf-8") as f:
                f.write("")
            # Initialization print is now handled by download_processor
        except Exception:
            # Errors (including print statements) are now handled by the calling download_processor
            pass  # Let the caller handle logging of this error
        finally:
            if self.lock and self.lock.locked():
                self.lock.release()

    def log_to_fullpath(self, fullpath: str) -> None:
        """
        Log the modified fullpath to the log file.
        Removes the first two directory levels from the path.
        """
        try:
            path_parts = fullpath.split("/")
            if len(path_parts) > 2:
                modified_fullpath = "/".join(path_parts[2:])
            else:
                modified_fullpath = fullpath

            if self.lock:
                self.lock.acquire()
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(f"{modified_fullpath}\n")
        except Exception:
            # Errors (including print statements) are now handled by the calling download_processor
            pass  # Let the caller handle logging of this error
        finally:
            if self.lock and self.lock.locked():
                self.lock.release()
