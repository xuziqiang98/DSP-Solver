from pathlib import Path
import logging
from src.configs.config_base import ConfigBase

class PathConfig(ConfigBase):
    root = Path(__file__).resolve().parents[2]
    src = root / 'src'
    data = root / 'data'
    scripts = root / 'scripts'
    tests = root / 'tests'
    logs = data / 'logs'

    def __post__init__(self) -> None:
        # create directories
        for path in vars(self).values():
            path.mkdir(parents = True, exist_ok = True)
    
class LoggerConfig(ConfigBase):
    level = logging.INFO
    logs_dir = PathConfig().logs