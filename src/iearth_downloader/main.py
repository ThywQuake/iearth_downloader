from __future__ import annotations

import typer
import sys
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from iearth_downloader.core.download_processor import DownloadProcessor
    from iearth_downloader.utils import auth

app = typer.Typer(help="iEarth Data Download CLI")


def _init_imports():
    globals()["DownloadProcessor"] = __import__(
        "iearth_downloader.core.download_processor", fromlist=["DownloadProcessor"]
    ).DownloadProcessor
    globals()["auth"] = __import__("iearth_downloader.utils.auth", fromlist=["auth"])


@app.command()
def download(
    download_path: str | None = typer.Option(
        None,
        "--download-path",
        "-to",
        help="Custom download path (overrides config.py setting)",
    ),
    max_threads: int | None = typer.Option(
        None,
        "--max-threads",
        "-m",
        help="Number of concurrent download threads (default from config.py)",
    ),
    resource_id: int | None = typer.Option(
        None,
        "--resource-id",
        "-id",
        help="Resource ID for the dataset to download (default from config.py)",
    ),
    target_sub_path: str | None = typer.Option(
        None,
        "--target-sub-path",
        "-sp",
        help="Specify a sub-path to filter downloads from the catalog (default from config.py)",
    ),
):
    """
        Command to run the data download process.
        === Data Download Script Command Line Arguments Usage Examples ===

    1. Run with default configuration:

        iearth

        # Use all default settings from config.py

    2. Specify download path only:

        iearth --download-path "./my_downloads"

        # Use custom download path, other settings use default values

    3. Specify resource ID:

        iearth --resource-id 9
        # Download dataset with resource ID 9

    4. Specify number of threads:

        iearth --max-threads 8

        # Use 8 threads for downloading

    5. Specify target sub-path filter:

        iearth --target-sub-path "MODISwater2001-2022/2008"

        # Only download files with paths starting with 'MODISwater2001-2022/2008'

    6. Combine multiple parameters:

        iearth --resource-id 26 --max-threads 3 --download-path "D:\\Data" --target-sub-path "MODISwater2001-2022/2021"

        # Specify resource ID, thread count, download path and sub-path filter simultaneously

    7. Windows path example:

        iearth --download-path "C:\\Users\\YourName\\Downloads\\dataset"

        # Windows absolute path

    8. Linux/Mac path example:

        iearth --download-path "/home/username/downloads/dataset"

        # Linux/Mac absolute path

    9. Relative path example:

        iearth --download-path "./data/downloads"

        # Path relative to current directory

    10. View help information:

        iearth --help

        # Display all available command line arguments
    """
    _init_imports()

    # User authentication
    typer.echo("=== User authentication ===")
    while not auth.login():
        typer.echo("Authentication failed, unable to continue downloading task")
        os.remove("credential.toml")

    typer.echo("\nAuthentication successful！")

    confirmation = (
        typer.prompt("Whether to start downloading task immediately？([y]/n): ")
        .strip()
        .lower()
    )

    if confirmation in ("n", "no"):
        typer.echo("Operation canceled")
        sys.exit(0)

    typer.echo("\n=== Start download task ===")

    # Prepare configuration overrides
    config_overrides = {}
    if download_path is not None:
        config_overrides["download_path"] = download_path
    if max_threads is not None:
        config_overrides["max_threads"] = max_threads
    if resource_id is not None:
        config_overrides["resource_id"] = resource_id
    if target_sub_path is not None:
        config_overrides["target_sub_path"] = target_sub_path

    # Initialize and run the download processor
    processor = DownloadProcessor(
        custom_download_path=download_path, config_overrides=config_overrides
    )
    processor.run_full_process()


if __name__ == "__main__":
    app()
