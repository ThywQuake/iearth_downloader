"""
Download processor module for coordinating the entire download workflow.
"""

import os
import time
import threading
import queue

from iearth_downloader.core.catalog_manager import CatalogManager
from iearth_downloader.core.file_manager import FileManager
from iearth_downloader.core.downloader import Downloader, Logger
from iearth_downloader.config.config import (
    DEFAULT_DOWNLOAD_PATH,
    MAX_DOWNLOAD_THREADS,
    TARGET_SUB_PATH,
    RESOURCE_ID,
)
from ..system.const import get_system_config


def get_download_path():
    """
    Get the configured download path.

    Returns:
        str: Absolute path to the download directory
    """
    if DEFAULT_DOWNLOAD_PATH is None:
        # Use current working directory
        return os.path.abspath(os.getcwd())
    elif os.path.isabs(DEFAULT_DOWNLOAD_PATH):
        # Use absolute path as is
        return DEFAULT_DOWNLOAD_PATH
    else:
        # Convert relative path to absolute path
        return os.path.abspath(DEFAULT_DOWNLOAD_PATH)


class DownloadProcessor:
    """Coordinates the entire download process."""

    def __init__(self, custom_download_path: str = None, config_overrides: dict = None):
        """
        Initialize the download processor.

        Args:
            custom_download_path: Optional custom download path to override config
            config_overrides: Optional dictionary to override config values
                Supported keys: 'max_threads', 'resource_id', 'target_sub_path'
        """
        # Apply configuration overrides
        if config_overrides is None:
            config_overrides = {}

        # Override configuration values
        self.max_threads = config_overrides.get("max_threads", MAX_DOWNLOAD_THREADS)
        self.resource_id = config_overrides.get("resource_id", RESOURCE_ID)
        self.target_sub_path = config_overrides.get("target_sub_path", TARGET_SUB_PATH)

        # Determine download base path first
        self.download_base_path = custom_download_path or get_download_path()

        # Load system configurations based on (possibly overridden) resource_id
        self._system_configs = get_system_config(self.resource_id)
        self.sleep_interval = self._system_configs["SLEEP_INTERVAL"]
        self.sleep_after_files = self._system_configs["SLEEP_AFTER_FILES"]

        # Set catalog and log files to be in the download directory
        catalog_filename = self._system_configs["CATALOG_FILE"]
        finished_log_filename = self._system_configs["FINISHED_LOG_FILE"]
        self.catalog_file = os.path.join(self.download_base_path, catalog_filename)
        self.finished_log_file = os.path.join(
            self.download_base_path, finished_log_filename
        )

        # Ensure download directory exists before initializing components
        os.makedirs(self.download_base_path, exist_ok=True)

        # Initialize components
        self.catalog_manager = CatalogManager(
            self.catalog_file, resource_id=self.resource_id
        )
        self.file_manager = FileManager()
        self.downloader = Downloader(resource_id=self.resource_id)
        self.log_lock = threading.Lock()
        self.logger = Logger(log_file=self.finished_log_file, lock=self.log_lock)
        self.download_queue = queue.Queue(maxsize=self.max_threads * 2)
        self.downloaded_files_count = 0
        self.lock_download_count = threading.Lock()

        # Print configuration being used
        print(f"Configuration being used:")
        print(f"  - Resource ID: {self.resource_id}")
        print(f"  - Max Threads: {self.max_threads}")
        print(
            f"  - Target Sub Path: '{self.target_sub_path}' (empty means process all)"
        )
        print(f"  - Download Path: {self.download_base_path}")
        print(f"  - Catalog File: {self.catalog_file}")
        print(f"  - Log File: {self.finished_log_file}")

    def _download_worker(self):
        """Worker function for download threads."""
        while True:
            task = self.download_queue.get()

            if task is None:
                self.download_queue.task_done()
                break

            fullpath, filename, local_path, size = task

            current_thread_id = threading.get_ident()
            print(f"Thread {current_thread_id}: Starting download for {filename}")
            if self.downloader.download_file(fullpath, filename, local_path):
                self.logger.log_to_fullpath(fullpath)

                with self.lock_download_count:
                    self.downloaded_files_count += 1
                    current_total_downloaded_by_all_threads = (
                        self.downloaded_files_count
                    )

                if not self.downloader.record_download_info(fullpath, filename, size):
                    print(
                        f"Thread {current_thread_id}: Failed to record download information for: {filename}"
                    )

                if (
                    current_total_downloaded_by_all_threads % self.sleep_after_files
                    == 0
                    and current_total_downloaded_by_all_threads > 0
                ):
                    print(
                        f"Thread {current_thread_id}: Pausing for {self.sleep_interval} second(s) after {current_total_downloaded_by_all_threads} total downloads by the process..."
                    )
                    time.sleep(self.sleep_interval)
            else:
                print(f"Thread {current_thread_id}: Failed to download: {filename}")

            self.download_queue.task_done()

    def process_catalog_and_download(self) -> None:
        """
        Main function to process catalog paths and download files to local directories using multiple threads.
        The main thread acts as a producer, adding download tasks to a queue.
        Worker threads consume tasks from the queue.
        Filters paths based on target_sub_path if provided.
        """
        catalog_data = self.catalog_manager.load_catalog_data()
        if not catalog_data:
            print("Failed to load catalog data.")
            return

        all_catalog_paths = self.catalog_manager.get_paths()
        table = self.catalog_manager.get_table()
        data_type = self.catalog_manager.get_data_type()

        if not all_catalog_paths:
            print("No paths found in catalog data.")
            return

        # Filter paths based on target_sub_path (either from config or override)
        paths_to_process = []
        if self.target_sub_path and self.target_sub_path.strip():
            normalized_target_sub_path = self.target_sub_path.strip().replace(
                "\\", "/"
            )  # Normalize slashes
            print(
                f"Filtering catalog paths by TARGET_SUB_PATH: '{normalized_target_sub_path}'"
            )
            for p in all_catalog_paths:
                normalized_catalog_path = p.replace(
                    "\\", "/"
                )  # Normalize slashes for comparison
                if normalized_catalog_path.startswith(normalized_target_sub_path):
                    paths_to_process.append(p)
            if not paths_to_process:
                print(
                    f"No paths in the catalog match the TARGET_SUB_PATH: '{normalized_target_sub_path}'. No files will be downloaded."
                )
                # Optionally, print completion message here or let it flow to the end
                # For now, let it flow, so it prints the standard completion message with 0 files.
        else:
            print("TARGET_SUB_PATH is not set. Processing all paths from the catalog.")
            paths_to_process = all_catalog_paths

        if not paths_to_process:
            print("No paths to process after filtering (or catalog was empty).")
            # Print a more specific completion message if needed, or let it flow
            # For consistency, we let it flow to the standard completion reporting.
            # The tasks_added_to_queue will be 0, and the final report will reflect that.

        print(
            f"Processing {len(paths_to_process)} paths using up to {self.max_threads} threads..."
        )
        print(f"Table: {table}")
        print(f"Type: {data_type}")

        print(f"Base download directory: {self.download_base_path}")

        self.logger.initialize_fullpath_log()

        threads = []
        for _ in range(self.max_threads):
            thread = threading.Thread(target=self._download_worker)
            thread.daemon = (
                True  # Allows main program to exit even if threads are still running
            )
            thread.start()
            threads.append(thread)

        tasks_added_to_queue = 0
        for i, path in enumerate(paths_to_process, 1):
            print(f"Producer: Processing path {i}/{len(paths_to_process)}: {path}")
            local_path = os.path.join(self.download_base_path, path)
            file_list = self.file_manager.fetch_file_list(table, path)
            if not file_list:
                print(f"Producer: No files found in path: {path}")
                continue

            for file_info in file_list:
                filename = file_info.get("file", "")
                size = file_info.get("size", 0)
                fullpath = f"shared-dataset/{data_type}/{path}/{filename}"
                if fullpath and filename:
                    # The put() call will block if the queue is full (if maxsize was set and reached)
                    self.download_queue.put((fullpath, filename, local_path, size))
                    tasks_added_to_queue += 1
            print(
                f"Producer: Queued {len(file_list)} files from path: {path}. Total tasks queued so far: {tasks_added_to_queue}"
            )

        print(
            f"Producer: All {tasks_added_to_queue} download tasks have been added to the queue."
        )

        # Signal worker threads to stop by sending sentinel values
        print(
            f"Producer: Sending {self.max_threads} sentinel values to stop worker threads..."
        )
        for _ in range(self.max_threads):
            self.download_queue.put(None)

        # Wait for all tasks in the queue to be processed by worker threads
        # This includes the sentinel None values, as workers call task_done() for them too.
        print(
            "Producer: Waiting for all tasks in queue to be processed (including sentinels)..."
        )
        self.download_queue.join()
        print("Producer: All tasks in queue have been processed.")

        # Wait for all worker threads to finish their execution
        print("Producer: Waiting for worker threads to terminate...")
        for thread in threads:
            thread.join()
        print("Producer: All worker threads have terminated.")

        print(f"\n=== Processing completed ===")
        print(f"Total files identified and queued for download: {tasks_added_to_queue}")
        print(
            f"Total files successfully downloaded: {self.downloaded_files_count}"
        )  # This count is from workers
        if tasks_added_to_queue > 0:
            success_rate = self.downloaded_files_count / tasks_added_to_queue * 100
            print(f"Download success rate: {success_rate:.1f}%")
        else:
            print("No files were scheduled for download.")
        print(f"Files downloaded to: {self.download_base_path}")

    def run_full_process(self) -> None:
        """
        Run the complete process: fetch catalog data and then download files.
        """
        print("Starting data processing and download...")
        print(f"Download base directory: {self.download_base_path}")

        print("\n=== Step 1: Fetching catalog data ===")
        if not self.catalog_manager.fetch_catalog_data():
            print("Failed to fetch catalog data. Exiting.")
            return

        print("\n=== Step 2: Processing paths and downloading files ===")
        self.process_catalog_and_download()

        print("\n=== Processing completed ===")
        print("Files generated:")
        print(f"- {self.catalog_file}: Contains catalog structure and paths")
        print(f"- {self.finished_log_file}: Contains downloaded file information")
        print(
            f"- Downloaded files: Organized in subdirectories under {self.download_base_path}"
        )
