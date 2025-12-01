"""
Main entry point for the data download script.
"""

import argparse
import sys
from iearth_downloader.core.download_processor import DownloadProcessor
from iearth_downloader.utils import auth


def main():
    """
    Main function to run the data download process.
    """
    parser = argparse.ArgumentParser(description="Data Download Script")

    # Download path configuration
    parser.add_argument(
        "--download-path",
        type=str,
        help="Custom download path (overrides config.py setting)",
    )

    # Number of concurrent download threads
    parser.add_argument(
        "--max-threads",
        type=int,
        help="Number of concurrent download threads (default from config.py)",
    )

    # Resource ID for the dataset to download
    parser.add_argument(
        "--resource-id",
        type=int,
        help="Resource ID for the dataset to download (default from config.py)",
    )

    # Target sub-path filter
    parser.add_argument(
        "--target-sub-path",
        type=str,
        help="Specify a sub-path to filter downloads from the catalog (default from config.py)",
    )

    args = parser.parse_args()

    # User authentication
    print("=== User authentication ===")
    if not auth.login():
        print("Authentication failed, unable to continue downloading task")
        sys.exit(1)

    print("\nAuthentication successful！")

    confirmation = (
        input("Whether to start downloading task immediately？([y]/n): ")
        .strip()
        .lower()
    )

    if confirmation in ("n", "no"):
        print("Operation canceled")
        sys.exit(0)

    print("\n=== Start download task ===")

    # Prepare configuration overrides
    config_overrides = {}
    if args.max_threads is not None:
        config_overrides["max_threads"] = args.max_threads
    if args.resource_id is not None:
        config_overrides["resource_id"] = args.resource_id
    if args.target_sub_path is not None:
        config_overrides["target_sub_path"] = args.target_sub_path

    # Create processor with optional custom download path and config overrides
    processor = DownloadProcessor(
        custom_download_path=args.download_path, config_overrides=config_overrides
    )
    processor.run_full_process()


if __name__ == "__main__":
    main()
