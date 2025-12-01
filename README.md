# iEarth Data Download Script

This is a Python script for downloading files from [iEarth datahub](https://data-starcloud.pcl.ac.cn/iearthdata/), supporting user authentication, directory structure retrieval, file list queries, and batch download functionality.

## Project Structure

```
data_tool/
├── iearth_downloader.py        # Main program entry
├── example_usage_cli.py        # Command line usage examples
├── requirements.txt            # Dependency list
├── README.md                   # Project documentation
├── config/                     # Configuration module directory
│   └── config.py              # User configuration file
├── system/                     # System configuration module directory
│   ├── system.ini             # System configuration file
│   └── const.py               # System constants and configuration loader
├── core/                       # Core functionality module directory
│   ├── catalog_manager.py     # Catalog management module
│   ├── file_manager.py        # File management module
│   ├── downloader.py          # Downloader module
│   └── download_processor.py  # Download processor module
└── utils/                      # Utility module directory
    ├── auth.py                # User authentication module
    └── encrypt_utils.py       # Encryption utility module
```

## Installation and Usage

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Parameters

#### User Configuration
Edit the `config/config.py` file to set defaults for:
- Resource ID corresponding to data (see: **RESOURCE_ID and Data Name Reference Table**) (RESOURCE_ID)
- Number of download threads (MAX_DOWNLOAD_THREADS)
- Target sub-path filtering (TARGET_SUB_PATH)
- Download path (DEFAULT_DOWNLOAD_PATH)

#### RESOURCE_ID and Data Name Reference Table
| Resource ID | Data Name                                                                                     |
|-------------|----------------------------------------------------------------------------------------------|
| 1           | 10-m Resolution Global Land Cover in 2017                                                    |
| 2           | 30-m Resolution Global Land Cover 2017                                                       |
| 3           | 30-m Resolution Global Land Cover 2015                                                       |
| 4           | Global Land Cover-Hierarchy                                                                   |
| 6           | 250-m Resolution Global Land Cover                                                           |
| 7           | Essential Urban Land Use Categories Map for China                                            |
| 8           | Improved Version of FROM-GLC Water Layer                                                     |
| 9           | Global daily 500m waterbody from 2001 to 2023(Version 2023)                                  |
| 10          | Global Cropland mapping data 2010                                                            |
| 11          | 40-year human settlement changes in China (Urban data only)                                  |
| 12          | 40-year human settlement changes in China (Urban and rural data)                            |
| 13          | Global Artificial Impervious Area (GAIA) data (Version 2024)                                 |
| 14          | Global urban boundaries data                                                                 |
| 15          | 30-m Resolution Forest Map for China                                                         |
| 16          | 34-year-long annual dynamics of global land cover (GLASS-GLC) at 5 km resolution             |
| 18          | 30-m Resolution Chilean Land Cover 2016                                                      |
| 19          | African land Cover                                                                           |
| 26          | Global 30-m seamless data cube (2000-2022) of land surface reflectance generated from Landsat-5,7,8,9 and MODIS Terra constellations |
| 27          | Global Land Surface Reflectance Seamless Data Cube based on MODIS data                      |
| 28          | Global 0.05 degree MODIS reflectance and normalized difference vegetation index (NDVI) seamless data cube |
| 54          | The First All-season Sample Set based on Landsat-8 data                                      |
| 55          | Multi-scale building height products and GF-7 building roof dataset                          |
| 57          | Fine-grained Urban Semantic Understanding (FUSU) dataset                                     |

### 3. Command Line Usage (Recommended)

#### Available Command Line Arguments

| Argument | Type | Description | Corresponding Config Variable |
|----------|------|-------------|------------------------------|
| `--download-path` | String | Data storage path | `DEFAULT_DOWNLOAD_PATH` |
| `--max-threads` | Integer | Concurrent download threads (⚠️ recommended not to exceed 10) | `MAX_DOWNLOAD_THREADS` |
| `--resource-id` | Integer | Data resource ID (see: **RESOURCE_ID and Data Name Reference Table**) | `RESOURCE_ID` |
| `--target-sub-path` | String | Sub-path filtering, only download matching paths | `TARGET_SUB_PATH` |

#### Basic Usage
```bash
# Use default configuration (will prompt for user login first)
python iearth_downloader.py

# View all available arguments
python iearth_downloader.py --help
```

#### Single Parameter Examples
```bash
# Specify download path
python iearth_downloader.py --download-path "./my_downloads"

# Specify data resource ID
python iearth_downloader.py --resource-id 9

# Specify thread count
python iearth_downloader.py --max-threads 8

# Specify sub-path filtering（download data where the catalog path starts with "MODISwater2001-2022/2008".）
python iearth_downloader.py --target-sub-path "MODISwater2001-2022/2008"
```

#### Combined Parameter Examples
```bash
# Combine multiple parameters
python iearth_downloader.py --resource-id 9 --max-threads 3 --download-path "D:\\Data" --target-sub-path "MODISwater2001-2022/2021"

# Windows path example
python iearth_downloader.py --resource-id 9 --download-path "C:\\Users\\YourName\\Downloads\\dataset"

# Linux/Mac path example
python iearth_downloader.py --resource-id 9 --download-path "/home/username/downloads/dataset"
```

#### Configuration Priority
1. **Command line arguments** - Highest priority
2. **User configuration file** (`config/config.py`) - Default values

## Usage Examples

### View Detailed Usage Examples
```bash
python example_usage_cli.py
```

### Common Use Cases

#### Scenario 1: Download complete dataset for specific resource ID
```bash
python iearth_downloader.py --resource-id 9 --download-path "./water_data"
```

#### Scenario 2: High-speed download (increase thread count)
```bash
python iearth_downloader.py --max-threads 8 --download-path "./downloads"
```

#### Scenario 3: Download data for specific year (using target-sub-path to set sub-path)
```bash
python iearth_downloader.py --target-sub-path "MODISwater2001-2022/2008" --download-path "./2008_data"
```

#### Scenario 4: Fully customized configuration
```bash
python iearth_downloader.py --resource-id 9 --max-threads 5 --download-path "/data/modis_water" --target-sub-path "MODISwater2001-2022/2020"
```

## Workflow

1. **User Authentication**: The program first performs user login verification when started
2. **Parameter Parsing**: Parse command line arguments, overriding configuration file settings
3. **Directory Structure Retrieval**: Get complete directory tree structure from API
4. **Save Directory Information**: Save directory information to `catalog_id_{resource_id}.json`
5. **Determine Download Path**: Determine base download path based on configuration or parameters
6. **Path Filtering**: Filter paths based on `target_sub_path` (if specified)
7. **Multi-threaded Download**: Use specified number of threads for concurrent file downloads
8. **Record Information**: Record download information to `downloaded_files_id_{resource_id}.txt`

## Output Files

- `catalog_id_{resource_id}.json`: Contains directory structure and path information (stored in download directory)
- `downloaded_files_id_{resource_id}.txt`: Contains downloaded file path information (stored in download directory)
- Downloaded files: Organized in the original directory structure within the configured download directory

## Directory Structure Example

Assuming the command `python iearth_downloader.py --download-path "/data/downloads" --resource-id 9` is used, the directory structure after download would be:

```
/data/downloads/
├── catalog_id_9.json           # Directory structure file
├── downloaded_files_id_9.txt   # Download log file
├── MODISwater2001-2022/        # Actual data files
│   ├── 2008/
│   │   ├── h00v09/
│   │   │   ├── 2008h00v09001_qc.tif
│   │   │   ├── 2008h00v09001_water.tif
│   │   │   └── 2008h00v09002_qc.tif
│   │   └── h01v09/
│   │       ├── 2008h01v09001_qc.tif
│   │       └── 2008h01v09001_water.tif
│   └── 2009/
│       └── ...
```

**Note**: All files (including catalog and log files) will be stored in the specified download directory for unified management.

## Important Notes

1. **Authentication Required**: The program requires valid user account and password when starting
2. Ensure all dependency modules are correctly installed and configured
3. Check network connection and API access permissions
4. **Ensure the specified download path has sufficient disk space and write permissions**
5. **Download path will be automatically created if it doesn't exist**
6. Automatic delays are added during bulk file downloads to avoid overload
7. **Thread count is recommended not to exceed 10 to avoid excessive server pressure**

## Error Handling

The script includes comprehensive error handling mechanisms:
- User authentication failure handling
- Network request exception handling
- JSON parsing error handling
- File operation exception handling
- Path creation failure handling
- Download failure retry mechanism
- **Command line argument validation**

## Performance Recommendations

1. **Thread Count Setting**: Adjust based on network environment, typically 3-8 threads work well
2. **Path Filtering**: Using `--target-sub-path` can significantly reduce download time
3. **Storage Location**: Choosing SSD drives can improve download write speed
4. **Network Environment**: Ensure stable network connection
5. **Authentication Information**: Ensure valid login credentials are used

## Troubleshooting

### Common Issues

1. **Authentication Failure**: Check if username and password are correct, and network connection status
2. **Module Import Error**: Ensure all modules are in the correct directory structure
3. **Path Does Not Exist**: Ensure the specified download path is valid and has write permissions
4. **Download Interruption**: The program supports resume downloads, just run again
5. **Insufficient Memory**: Reduce thread count or use a machine with more memory

### Debugging Tips

```bash
# Use single thread for debugging
python iearth_downloader.py --max-threads 1 --target-sub-path "small_dataset_path"

# View detailed configuration information
# The program will display all current configuration parameters when starting
```
