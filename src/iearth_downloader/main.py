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
        None, help="Custom download path (overrides config.py setting)"
    ),
    max_threads: int | None = typer.Option(
        None, help="Number of concurrent download threads (default from config.py)"
    ),
    resource_id: int | None = typer.Option(
        None, help="Resource ID for the dataset to download (default from config.py)"
    ),
    target_sub_path: str | None = typer.Option(
        None,
        help="Specify a sub-path to filter downloads from the catalog (default from config.py)",
    ),
):
    """
    Command to run the data download process.
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
