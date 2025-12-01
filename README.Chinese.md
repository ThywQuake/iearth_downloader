# iEarth数据下载脚本

这是一个用于从[iEarth datahub](https://data-starcloud.pcl.ac.cn/iearthdata/)下载文件的Python脚本，支持用户认证、目录结构获取、文件列表查询和批量下载功能。

## 项目结构

```
data_tool/
├── iearth_downloader.py        # 主程序入口
├── example_usage_cli.py        # 命令行参数使用示例
├── requirements.txt            # 依赖包列表
├── README.md                   # 项目说明文档
├── config/                     # 配置模块目录
│   └── config.py              # 用户配置文件
├── system/                     # 系统配置模块目录
│   ├── system.ini             # 系统配置文件
│   └── const.py               # 系统常量和配置加载器
├── core/                       # 核心功能模块目录
│   ├── catalog_manager.py     # 目录管理模块
│   ├── file_manager.py        # 文件管理模块
│   ├── downloader.py          # 下载器模块
│   └── download_processor.py  # 下载处理器模块
└── utils/                      # 工具模块目录
    ├── auth.py                # 用户认证模块
    └── encrypt_utils.py       # 加密工具模块
```



## 安装和使用

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置参数

#### 用户配置
编辑 `config/config.py` 文件，设置默认的：
- 数据资源对应的id(详见：**RESOURCE_ID与数据名称对照表**) (RESOURCE_ID)
- 下载线程数 (MAX_DOWNLOAD_THREADS)
- 目标子路径过滤 (TARGET_SUB_PATH)
- 下载存储路径 (DEFAULT_DOWNLOAD_PATH)

#### RESOURCE_ID与数据名称对照表
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
| 16          | 34-year-long annual dynamics of global land cover (GLASS-GLC) at 5 km resolution             |
| 18          | 30-m Resolution Chilean Land Cover 2016                                                      |
| 19          | African land Cover                                                                           |
| 26          | Global 30-m seamless data cube (2000-2022) of land surface reflectance generated from Landsat-5,7,8,9 and MODIS Terra constellations |
| 27          | Global Land Surface Reflectance Seamless Data Cube based on MODIS data                      |
| 28          | Global 0.05 degree MODIS reflectance and normalized difference vegetation index (NDVI) seamless data cube |
| 54          | The First All-season Sample Set based on Landsat-8 data                                      |
| 55          | Multi-scale building height products and GF-7 building roof dataset                          |
| 57          | Fine-grained Urban Semantic Understanding (FUSU) dataset                                     |

### 3. 使用命令行（推荐）


#### 可用的命令行参数

| 参数 | 类型 | 说明 | 对应配置文件变量 |
|------|------|------|------------------|
| `--download-path` | 字符串 | 数据存储路径 | `DEFAULT_DOWNLOAD_PATH` |
| `--max-threads` | 整数 | 并发下载线程数 (⚠️建议不超过10) | `MAX_DOWNLOAD_THREADS` |
| `--resource-id` | 整数 | 数据资源id(详见：**RESOURCE_ID与数据名称对照表**) | `RESOURCE_ID` |
| `--target-sub-path` | 字符串 | 子路径过滤，只下载匹配的路径中的数据 | `TARGET_SUB_PATH` |


#### 基本用法
```bash
# 使用默认配置（会先要求用户登录）
python iearth_downloader.py

# 查看所有可用参数
python iearth_downloader.py --help
```

#### 单个参数示例
```bash
# 指定下载路径
python iearth_downloader.py --download-path "./my_downloads"

# 指定数据资源ID
python iearth_downloader.py --resource-id 9

# 指定线程数
python iearth_downloader.py --max-threads 8

# 指定子路径过滤（只下载 "MODISwater2001-2022/2008"目录下的数据）
python iearth_downloader.py --target-sub-path "MODISwater2001-2022/2008"
```

#### 组合参数示例
```bash
# 组合多个参数
python iearth_downloader.py --resource-id 9 --max-threads 3 --download-path "D:\\Data" --target-sub-path "MODISwater2001-2022/2021"

# Windows 路径示例
python iearth_downloader.py --resource-id 9 --download-path "C:\\Users\\YourName\\Downloads\\dataset"

# Linux/Mac 路径示例
python iearth_downloader.py --resource-id 9 --download-path "/home/username/downloads/dataset"
```

#### 配置优先级
1. **命令行参数** - 最高优先级
2. **用户配置文件** (`config/config.py`) - 默认值



## 使用示例

### 查看详细使用示例
```bash
python example_usage_cli.py
```

### 常见使用场景

#### 场景1：下载特定资源ID的完整数据集
```bash
python iearth_downloader.py --resource-id 9 --download-path "./water_data"
```

#### 场景2：高速下载（增加线程数）
```bash
python iearth_downloader.py --max-threads 8 --download-path "./downloads"
```

#### 场景3：下载特定年份的数据（通过target-sub-path设置子路径）
```bash
python iearth_downloader.py --target-sub-path "MODISwater2001-2022/2008" --download-path "./2008_data"
```

#### 场景4：完全自定义配置
```bash
python iearth_downloader.py --resource-id 9 --max-threads 5 --download-path "/data/modis_water" --target-sub-path "MODISwater2001-2022/2020"
```

## 工作流程

1. **用户认证**: 程序启动时首先进行用户登录验证
2. **参数解析**: 解析命令行参数，覆盖配置文件设置
3. **获取目录结构**: 从API获取完整的目录树结构
4. **保存目录信息**: 将目录信息保存到 `catalog_id_{resource_id}.json`
5. **确定下载路径**: 根据配置或参数确定下载基础路径
6. **路径过滤**: 根据 `target_sub_path` 过滤路径（如果指定）
7. **多线程下载**: 使用指定数量的线程并发下载文件
8. **记录信息**: 记录下载信息到 `downloaded_files_id_{resource_id}.txt`

## 输出文件

- `catalog_id_{resource_id}.json`: 包含目录结构和路径信息（存储在下载目录中）
- `downloaded_files_id_{resource_id}.txt`: 包含已下载文件的路径信息（存储在下载目录中）
- 下载的文件: 按照原始目录结构组织在配置的下载目录中

## 目录结构示例

假设使用命令 `python iearth_downloader.py --download-path "/data/downloads" --resource-id 9`，下载后的目录结构如下：

```
/data/downloads/
├── catalog_id_9.json           # 目录结构文件
├── downloaded_files_id_9.txt   # 下载记录文件
├── MODISwater2001-2022/        # 实际数据文件
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

**注意**: 所有文件（包括 catalog 和 log 文件）都会存储在指定的下载目录中，便于统一管理。

## 注意事项

1. **认证要求**: 程序启动时需要提供有效的用户账号和密码
2. 确保所有依赖模块正确安装和配置
3. 检查网络连接和API访问权限
4. **确保指定的下载路径有足够的磁盘空间和写入权限**
5. **下载路径会自动创建，如果不存在的话**
6. 大量文件下载时会自动添加延时以避免过载
7. **线程数建议不超过10，避免对服务器造成过大压力**

## 错误处理

脚本包含完善的错误处理机制：
- 用户认证失败处理
- 网络请求异常处理
- JSON解析错误处理
- 文件操作异常处理
- 路径创建失败处理
- 下载失败重试机制
- **命令行参数验证**

## 性能建议

1. **线程数设置**: 根据网络环境调整，通常3-8个线程较为合适
2. **路径过滤**: 使用 `--target-sub-path` 可以显著减少下载时间
3. **存储位置**: 选择SSD硬盘可以提高下载写入速度
4. **网络环境**: 确保稳定的网络连接
5. **认证信息**: 确保使用有效的登录凭据

## 故障排除

### 常见问题

1. **认证失败**: 检查用户名和密码是否正确，以及网络连接状态
2. **模块导入错误**: 确保所有模块都在正确的目录结构中
3. **路径不存在**: 确保指定的下载路径有效且有写入权限
4. **下载中断**: 程序支持断点续传，重新运行即可
5. **内存不足**: 减少线程数或使用更大内存的机器

### 调试技巧

```bash
# 使用单线程调试
python iearth_downloader.py --max-threads 1 --target-sub-path "small_dataset_path"

# 查看详细配置信息
# 程序启动时会显示当前使用的所有配置参数
```