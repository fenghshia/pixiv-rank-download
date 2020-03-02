from os import system, listdir
from pathlib import Path
from json import dump


class firstRun:

    def __init__(self):
        check_dirlist = ['options', 'backup']  # 检查文件夹的列表
        check_filelist = ['black_user.json', 'config.json']  # 检查文件的列表
        self.miss = []  # 需要初始化的文件
        for i in check_dirlist:
            if not self.__exists(i):
                self.create('dir', i)
        for i in check_filelist:
            if not self.__exists(i):
                self.create('file', i)
                self.miss.append(i)
        print("运行前检查结束")

    def check_options(self):
        if not self.__exists("options\\run.dll"):
            print('开始初始化程序设置')
            self.create('file', 'options\\run.dll')
            self.__file_init()
        if self.__exists('options\\pass.dll'):
            self.skip = True
        else:
            self.skip = False

    def __file_init(self):
        self.black_user_init()
        self.config_init()

    def black_user_init(self):
        with open('black_user.json', 'w', encoding='utf-8') as f:
            dump([], f)

    def config_init(self):
        config = {}
        while True:
            print('仓库路径--为你最终存放图片的文件夹的绝对路径')
            s = input('请输入仓库路径:')
            if self.__exists(s):
                config['warehouse'] = s
                break
            else:
                print('你输入的目录不存在,请重新输入')
        while True:
            print('下载路径--为你下载排行图片的文件夹的绝对路径')
            s = input('请输入下载路径:')
            if self.__exists(s):
                config['downdir'] = s
                break
            else:
                print('你输入的目录不存在,请重新输入')
        while True:
            print('黑名单路径--为你下载排行图片后认为不好看的图片需要将画师添加黑名单的文件夹的绝对路径,必须是空的目录')
            s = input('请输入黑名单路径:')
            if self.__exists(s):
                if not self.__get_dir(s):
                    config['blackdir'] = s
                    break
                else:
                    print('你输入的目录不是空目录')
            else:
                print('你输入的目录不存在,请重新输入')
        with open('config.json', 'w', encoding='utf-8') as f:
            dump(config, f, ensure_ascii=False)

    def create(self, f_type, path):
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
