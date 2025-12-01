# ==========Configuration file for data download script==========

# Number of concurrent download threads
# The recommended number of threads is no more than 10
MAX_DOWNLOAD_THREADS = 5  

# Which dataset to download
# For example, the RESOURCE_ID for "Global 500m of water per day from 2001 to 2023 (2023 edition)" is 9
RESOURCE_ID = 9

# Optional: Specify a sub-path to filter downloads from the catalog.
# If empty or None, all paths in the catalog will be processed.
# Example: TARGET_SUB_PATH = "MODISwater2001-2022/2001"
# This would only download data where the catalog path starts with "MODISwater2001-2022/2001".
TARGET_SUB_PATH = "" # Default to empty (download all)

# Download Path Configuration
# Set the default download directory
# Options:
# 1. Use current working directory: DEFAULT_DOWNLOAD_PATH = None
# 2. Use absolute path: DEFAULT_DOWNLOAD_PATH = "/path/to/download/folder"
# 3. Use relative path: DEFAULT_DOWNLOAD_PATH = "./downloads"
# 4. Windows path:DEFAULT_DOWNLOAD_PATH = "D:\\Data\\Downloads"
DEFAULT_DOWNLOAD_PATH = None  # Use current working directory if None

