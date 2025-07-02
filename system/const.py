"""
System configuration loader module.
This module loads fixed system configurations from system.ini file.
"""

import configparser
import os


class SystemConfig:
    """System configuration singleton class."""
    
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        """Load configuration from ini file."""
        self._config = configparser.ConfigParser()
        config_file = os.path.join(os.path.dirname(__file__), 'system.ini')
        
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"System configuration file not found: {config_file}")
        
        self._config.read(config_file, encoding='utf-8')
    
    def get_catalog_file(self, resource_id):
        """Get catalog file name based on resource ID."""
        pattern = self._config.get('file_configuration', 'catalog_file_pattern')
        return pattern.format(resource_id)
    
    def get_finished_log_file(self, resource_id):
        """Get finished log file name based on resource ID."""
        pattern = self._config.get('file_configuration', 'finished_log_file_pattern')
        return pattern.format(resource_id)
    
    @property
    def chunk_size(self):
        return self._config.getint('download_configuration', 'chunk_size')
    
    @property
    def sleep_interval(self):
        return self._config.getint('download_configuration', 'sleep_interval')
    
    @property
    def sleep_after_files(self):
        return self._config.getint('download_configuration', 'sleep_after_files')
    
    @property
    def base_url(self):
        return self._config.get('api_configuration', 'base_url')
    
    @property
    def catalog_api(self):
        return self._config.get('api_configuration', 'catalog_api')
    
    @property
    def file_list_api(self):
        return self._config.get('api_configuration', 'file_list_api')
    
    @property
    def download_api(self):
        return self._config.get('api_configuration', 'download_api')
    
    @property
    def record_api(self):
        return self._config.get('api_configuration', 'record_api')
    
    @property
    def login_api_url(self):
        return self._config.get('api_configuration', 'login_api_url')


# Create singleton instance
sys_config = SystemConfig()

# Export system configuration values
def get_system_config(resource_id):
    """
    Get all system configuration values.
    
    Args:
        resource_id: Resource ID for file name formatting
        
    Returns:
        dict: Dictionary containing all system configuration values
    """
    return {
        'CATALOG_FILE': sys_config.get_catalog_file(resource_id),
        'FINISHED_LOG_FILE': sys_config.get_finished_log_file(resource_id),
        'CHUNK_SIZE': sys_config.chunk_size,
        'SLEEP_INTERVAL': sys_config.sleep_interval,
        'SLEEP_AFTER_FILES': sys_config.sleep_after_files,
        'BASE_URL': sys_config.base_url,
        'CATALOG_API': sys_config.catalog_api,
        'FILE_LIST_API': sys_config.file_list_api,
        'DOWNLOAD_API': sys_config.download_api,
        'RECORD_API': sys_config.record_api,
        'LOGIN_API_URL': sys_config.login_api_url,
    } 