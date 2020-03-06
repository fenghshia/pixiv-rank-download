from os import listdir, system
from json import load, dump


class black_user_add:

    def __init__(self):
        with open('config.json', 'r', encoding='utf-8') as f:
            config = load(f)
            self.blackdir = config['blackdir']
        self.__add()

    def __add(self):
        dirlist = self.__get_dir()
        if dirlist:
            print(f'读取到需要添加黑名单的目录,总数:{len(dirlist)}')
            with open('black_user.json', 'r', encoding='utf-8') as fr:
                black_user = load(fr)
            for name in dirlist:
                id = self.__get_id(name)
                black_user.append(id)
            with open('black_user.json', 'w', encoding='utf-8') as fw:
                dump(black_user, fw, ensure_ascii=False)
                self.__system(f'rd /s /q "{self.blackdir}"')
                self.__create()
        else:
            print('未读取到需要添加黑名单的目录')

    def __get_id(self, name):
        return int(name.split(" ")[-1])

    def __get_dir(self):
        return listdir(self.blackdir)

    def __create(self):
        self.__system(f'mkdir "{self.blackdir}"')

    def __system(self, cmd):
        r = system(cmd)
        if r == 0:
            return True
        else:
            return False