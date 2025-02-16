import os
import tomllib

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH = os.path.join(
    CURRENT_DIR,     
    "..",   
    "..",   
    "config", 
    "settings.toml"
)

_commands_cache = None 

def _load_settings(settings_file: str = CONFIG_PATH) -> dict:
    global _commands_cache
    if _commands_cache is None:
       with open(settings_file, 'rb') as f:
           _commands_cache = tomllib.load(f)
    return _commands_cache
    

def get_config(key: str, default=None):
    return _load_settings().get(key, default)

def reload_config():
    """Config cache'ini temizleyerek tekrar yüklemeyi sağlar."""
    global _commands_cache
    _commands_cache = None
    return _load_settings() 


    