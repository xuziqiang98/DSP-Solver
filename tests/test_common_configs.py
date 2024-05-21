import path_setup

from src.configs.common_configs import PathConfig

if __name__ == '__main__':
    pathConfig = PathConfig()
    print(pathConfig.root)
    print(pathConfig.src)
    print(pathConfig.data)
    print(pathConfig.logs)