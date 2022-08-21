import os
import configparser


class MyConfigParser(configparser.ConfigParser):
    """
    set ConfigParser options for case sensitive.
    """
    
    def __init__(self, defaults=None):
        configparser.ConfigParser.__init__(self, defaults=defaults)
    
    def optionxform(self, optionstr):
        return optionstr

def read_ini(config_path):
    
    conf = MyConfigParser()
    
    # 读取默认配置
    conf.read(config_path)
    # get()函数读取section里的参数值
    try:
        site_cfg = conf.items("site")
        site_cfg_data = dict(site_cfg)
    except configparser.NoSectionError:
        site_cfg_data = {}
    
    try:
        common_cfg = conf.items("common")
        common_cfg_data = dict(common_cfg)
    except configparser.NoSectionError:
        common_cfg_data = {}
        
    cfg_data = {**site_cfg_data, **common_cfg_data}
    return cfg_data


def read_cfg():
    # 当前文件路径
    current_path = os.path.split(os.path.realpath(__file__))[0]
    
    print(current_path)
    
    # 在当前文件路径下查找默认.ini文件
    default_cfg_path = os.path.join(current_path, "default_config.ini")
    cfg_data = read_ini(default_cfg_path)

    
    # 在当前路径settings目录下查找开发或生产.ini文件
    other_cfg_path = os.path.join(current_path, "settings")

    other_cfg = {}
    for files in os.listdir(other_cfg_path):
        if files.endswith(".ini"):
            print(files)  # printing file n
            other_cfg = read_ini(os.path.join(other_cfg_path, files))
            break
    # paths = Path(other_cfg_path).glob('**/*.ini')
    
    cfg_data.update(other_cfg)
    for k in cfg_data.keys():
        v = cfg_data[k]
        if v and v.lower() in ('true', 'false'):
            v = True if v.lower() == 'true' else False
            cfg_data[k] = v
        elif v and v.isdigit():
            v = int(v)
            cfg_data[k] = v
    
    return cfg_data