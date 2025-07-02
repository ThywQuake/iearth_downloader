#!/usr/bin/env python3
"""
Command line usage examples for the data download script.
This file demonstrates how to use command line arguments to override config.py settings.
"""

def show_usage_examples():
    """Display various usage examples for the command line interface."""
    
    print("=== Data Download Script Command Line Arguments Usage Examples ===\n")
    
    print("1. Run with default configuration:")
    print("   python iearth_downloader.py")
    print("   # Use all default settings from config.py\n")
    
    print("2. Specify download path only:")
    print("   python iearth_downloader.py --download-path \"./my_downloads\"")
    print("   # Use custom download path, other settings use default values\n")
    
    print("3. Specify resource ID:")
    print("   python iearth_downloader.py --resource-id 9")
    print("   # Download dataset with resource ID 9\n")
    
    print("4. Specify number of threads:")
    print("   python iearth_downloader.py --max-threads 8")
    print("   # Use 8 threads for downloading\n")
    
    print("5. Specify target sub-path filter:")
    print("   python iearth_downloader.py --target-sub-path \"MODISwater2001-2022/2008\"")
    print("   # Only download files with paths starting with 'MODISwater2001-2022/2008'\n")
    
    print("6. Combine multiple parameters:")
    print("   python iearth_downloader.py --resource-id 26 --max-threads 3 --download-path \"D:\\\\Data\" --target-sub-path \"MODISwater2001-2022/2021\"")
    print("   # Specify resource ID, thread count, download path and sub-path filter simultaneously\n")
    
    print("7. Windows path example:")
    print("   python iearth_downloader.py --download-path \"C:\\\\Users\\\\YourName\\\\Downloads\\\\dataset\"")
    print("   # Windows absolute path\n")
    
    print("8. Linux/Mac path example:")
    print("   python iearth_downloader.py --download-path \"/home/username/downloads/dataset\"")
    print("   # Linux/Mac absolute path\n")
    
    print("9. Relative path example:")
    print("   python iearth_downloader.py --download-path \"./data/downloads\"")
    print("   # Path relative to current directory\n")
    
    print("10. View help information:")
    print("    python iearth_downloader.py --help")
    print("    # Display all available command line arguments\n")
    
    print("=== Parameter Description ===")
    print("--download-path   : Specify download directory path")
    print("--max-threads     : Specify concurrent download thread count (recommended not to exceed 10)")
    print("--resource-id     : Specify dataset resource ID to download")
    print("--target-sub-path : Specify sub-path filter, only download matching paths")
    print("\nAll parameters are optional. If not specified, default values from config.py will be used.")
    print("Command line arguments have higher priority than settings in the configuration file.")


if __name__ == "__main__":
    show_usage_examples() 