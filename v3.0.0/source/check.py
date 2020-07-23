from os import system, listdir
from json import dump, load
from pathlib import Path


class check:

    def __init__(self):
        # 路径
        self.config_path = "config/config.json"
        self.__check_config()

    def __check_config(self):
        # 路径
        self.config_path = "config/config.json"
        # 校验文件夹存在
        if not self.__exist("config"):
            self.__create('dir', "config")
        # 校验文件存在
        if self.__exist(self.config_path):
            # 验证文件可读性 并读取内容
            self.__check_json(self.config_path, True)
        # 文件不存在的初始化操作
        else:
            self.__file_init(self.config_path, True)

    # 校验json文件的可读性 返回读取内容
    def __check_json(self, file_name, need_set):
        with open(file_name, 'r', encoding='utf-8') as f:
            try:
                return load(f)
            except Exception:
                self.__file_init(file_name, need_set)

    # 文件初始化
    def __file_init(self, file_name, need_set):
        if file_name == "config/config.json":
            self.__config_init(need_set)

    # 配置初始化
    def __config_init(self, need_set):
        with open(self.config_path, 'w', encoding='utf-8') as f:
            dump({"old_dirs": [], "dir": ""}, f, indent=4)
        if need_set:
            self.set_config()

    # 配置设置
    def set_config(self):
        # 读取配置
        config = self.__check_json(self.config_path, False)
        # 用户输入工作目录
        while True:
            print('仓库路径--为程序存放图片的文件夹的绝对路径')
            dir_path = input('请输入仓库路径:')
            if self.__check_config_dir(dir_path):
                if config["dir"] and:
                    config["old_dirs"].append(config["dir"])
                config["dir"] = dir_path
                break
        with open(self.config_path, 'w', encoding='utf-8') as f:
            dump(config, f, ensure_ascii=False, indent=4)

    def __check_config_dir(self, dir_path):
        if dir_path:  # 不为空
            if ':\\' in dir_path:  # 绝对路径
                if self.__exist(dir_path):  # 文件夹存在
                    if not self.__get_dir(dir_path):  # 判断空文件夹
                        return True
                    else:
                        print('请输入空的文件夹(此文件夹下不要存放任何的文件或者文件夹)')
                        return False
                else:
                    print('你输入的目录不存在,请重新输入')
                    return False
            else:
                print('请输入绝对路径')
                return False
        else:
            print('你的输入为空,请重新输入')
            return False

    def __create(self, f_type, path):
        if f_type == 'dir':
            self.__system(f'mkdir "{path}"')
        elif f_type == 'file':
            self.__system(f'type nul>"{path}"')

    def __system(self, cmd):
        r = system(cmd)
        if r == 0:
            return True
        else:
            return False

    # 是否存在
    def __exist(self, file_path):
        return Path(file_path).exists()

    def __get_dir(self, path):
        return listdir(path)