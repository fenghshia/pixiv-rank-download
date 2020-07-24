from os import system, listdir
from json import dump, load
from pathlib import Path
from datetime import datetime


class check:

    def __init__(self):
        # 路径
        self.config_path = "config/config.json"
        self.cookie_path = "config/cookie.json"
        self.socks_path = "config/socks.json"
        self.__check_config()

    def __check_config(self):
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
        elif file_name == "config/cookie.json":
            self.__cookie_init(need_set)
        elif file_name == "config/socks.json":
            self.__socks_init(need_set)

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
                if config["dir"]:
                    config["old_dirs"].append({"dir": config["dir"],
                                               "change_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                               "data_moved": False})
                config["dir"] = dir_path
                break
        with open(self.config_path, 'w', encoding='utf-8') as f:
            dump(config, f, ensure_ascii=False, indent=4)
        self.__classify_init(dir_path)
        self.__create("dir", dir_path+"/pixiv_storage/daily_rank")
        self.__create("dir", dir_path+"/pixiv_storage/r18_rank")
        self.__create("dir", dir_path+"/pixiv_storage/artist")
        self.__create("dir", dir_path+"/blacklist")

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

    def __classify_init(self, dir_path):
        with open("ResNet/class_names_6000.json", "r", encoding="utf-8") as f:
            classify_list = load(f)
        for name in classify_list:
            print(f"初始化分类文件目录:{name}                        ", end="\r")
            self.__create("dir", dir_path+"/classify/"+name)

    def __cookie_init(self, need_set):
        with open(self.cookie_path, 'w', encoding='utf-8') as f:
            dump({"history": [], "cookie": ""}, f, indent=4)
        if need_set:
            self.set_cookie()

    def set_cookie(self):
        cookie = self.__check_json(self.cookie_path, False)
        new_cookie = input("请输入你的pixiv登录cookie:")
        if new_cookie:
            if cookie["cookie"]:
                cookie["history"].append({"cookie": cookie["cookie"],
                                          "change_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
            cookie["cookie"] = new_cookie
            with open(self.cookie_path, "w", encoding='utf-8') as f:
                dump(cookie, f, ensure_ascii=False, indent=4)
        else:
            print("当前输入为空, 不设置")

    def check_cookie_exist(self):
        if not self.__exist(self.cookie_path):
            self.__file_init(self.cookie_path, False)
            return False
        cookie = self.__check_json(self.cookie_path, False)
        if cookie["cookie"]:
            return True
        else:
            return False

    def __socks_init(self, need_set):
        with open(self.socks_path, 'w', encoding='utf-8') as f:
            dump({"history": [], "socks": ""}, f, indent=4)
        if need_set:
            self.set_socks()

    def set_socks(self):
        socks = self.__check_json(self.socks_path, False)
        new_socks = {"type": "socks5"}
        host = input("请输入代理的IP地址:")
        if host:
            new_socks["host"] = host
            while True:
                port = input("请输入代理的端口:")
                if port:
                    try:
                        new_socks["port"] = int(port)
                        if socks["socks"]:
                            socks["history"].append({"socks": socks["socks"],
                                                     "change_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                        socks["socks"] = new_socks
                        with open(self.socks_path, "w", encoding='utf-8') as f:
                            dump(socks, f, ensure_ascii=False, indent=4)
                        break
                    except Exception:
                        print("你输入的不是数字")
                else:
                    print("你的输入为空不设置")
                    break
        else:
            print("你的输入为空不设置")

    def check_socks_exist(self):
        if not self.__exist(self.socks_path):
            self.__file_init(self.socks_path, False)
            return False
        socks = self.__check_json(self.socks_path, False)
        if socks["socks"]:
            return True
        else:
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