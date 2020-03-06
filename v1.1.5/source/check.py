from os import system, listdir
from pathlib import Path
from json import dump, load


class check:

    def __init__(self):
        check_dirlist = ['options', 'backup']  # 检查文件夹的列表
        self.__check_filelist = ['black_user.json', 'config.json']  # 检查文件的列表

        for i in check_dirlist:
            if not self.__exists(i):
                self.__create('dir', i)

        for i in self.__check_filelist:
            if not self.__exists(i):
                self.__create('file', i)

        self.__check_json()

    def get_config(self):
        with open('config.json', 'r', encoding='utf-8') as f:
            return load(f)

    def set_skip(self):
        self.__create('file', 'options\\skip.dll')

    def check_skip(self):
        return self.__exists('options\\skip.dll')

    def set_black_add(self):
        config = self.get_config()
        with open('config.json', 'w', encoding='utf-8') as f:
            config['blackadd'] = not config['blackadd']
            dump(config, f, ensure_ascii=False)

    def check_black_add(self):
        return self.get_config()['blackadd']

    def __check_json(self):  # 检查文件是否可以读取
        for i in self.__check_filelist:
            with open(i, 'r', encoding='utf-8') as f:
                try:
                    load(f)
                except Exception:
                    self.__file_init(i)

    def __file_init(self, file):  # 对不同文件进行初始化
        if file == 'black_user.json':
            self.__black_user_init()
        elif file == 'config.json':
            self.config_init()

    def __black_user_init(self):  # 对黑名单进行初始化
        with open('black_user.json', 'w', encoding='utf-8') as f:
            dump([], f)

    def config_init(self):  # 对配置文件进行初始化
        config = {}
        while True:
            print('仓库路径--为你最终存放图片的文件夹的绝对路径')
            s = input('请输入仓库路径:')
            if self.__set_config(config, s, 'warehouse', False):
                break
        while True:
            print('下载路径--为你下载排行图片的文件夹的绝对路径')
            s = input('请输入下载路径:')
            if self.__set_config(config, s, 'down_dir', False):
                break
        while True:
            print('黑名单路径--为你下载排行图片后认为不好看的图片需要将画师添加黑名单的文件夹的绝对路径,必须是空的目录')
            s = input('请输入黑名单路径:')
            if self.__set_config(config, s, 'blackdir', True):
                break
        config['blackadd'] = False
        with open('config.json', 'w', encoding='utf-8') as f:
            dump(config, f, ensure_ascii=False)

    def __set_config(self, config, s, key, empty):
        if s:  # 不为空
            if ':\\' in s:  # 绝对路径
                if self.__exists(s):  # 文件夹存在
                    if empty:  # 判断空文件夹
                        if not self.__get_dir(s):  # 判断空文件夹
                            config[key] = s
                            return True
                        else:
                            print('请输入空的文件夹(此文件夹下不要存放任何的文件或者文件夹)')
                            return False
                    else:
                        config[key] = s
                        return True
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

    def __exists(self, file_path):
        return Path(file_path).exists()

    def __get_dir(self, path):
        return listdir(path)
