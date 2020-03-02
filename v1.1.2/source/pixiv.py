
from os import system
from json import load
from pathlib import Path
from requests import session
from requests.adapters import HTTPAdapter


# p站下载主类
class pixiv:

    def __init__(self, file_reset):
        self.file_reset = file_reset
        self.rank_url = "https://www.pixiv.net/ranking.php?mode=daily&p=%d&format=json"  # 排行URL
        self.rank_header = {"referer": "https://www.pixiv.net/ranking.php?mode=daily"}  # 头部跳转信息 注:应对P站防盗链,headers只需要加referer即可获得返回数据
        self.warehouse, self.down_dir = self.__get_path()  # 读取路径
        self.black_user = self.__get_black_user()  # 读取黑名单
        self.s = session()  # 实例化进程对象
        # 设置超时重试次数
        self.s.mount('http://', HTTPAdapter(max_retries=3))
        self.s.mount('https://', HTTPAdapter(max_retries=3))
        self.s.keep_alive = False  # 设置保持连接为否
        self.del_li = ['/', '|', '\t', '"', ':', '*', '\\', '<', '>', '?']  # windows目录删除的字符
        self.native_data = []  # 存放原始数据

    def down_start(self):
        self.__get_native_data()
        self.__down_p0()

    def __get_native_data(self):
        for p in range(1, 11):  # 循环获取10页数据
            # print("开始处理:", i)  # 调试输出
            r = self.s.get(self.rank_url % p, headers=self.rank_header, timeout=10)  # timeout设置超时10秒
            r = r.json()['contents']  # 获得排行原始数据
            for data in r:  # 遍历数据
                if data['user_id'] not in self.black_user:  # 判断不在黑名单
                    self.native_data.append(  # 保存必要数据
                        {'url': data['url'].replace('/c/240x480', ''),  # 下载地址
                         'header': {"referer": f"https://www.pixiv.net/artworks/{data['illust_id']}"},  # 跳转头
                         'p_name': self.__get_p_name(data['url']),  # 图片名称
                         'dir_name': self.__get_dir_path(data["user_name"], data["user_id"])}  # 目录名称
                    )
        print("排行数据处理完成!")

    def __down_p0(self):
        for data in self.native_data:  # 遍历原始数据
            if 'p0' in data['p_name']:  # 判断是否有p0
                p = 0
                while True:
                    data['url'] = data['url'].replace('p0', f'p{p}')
                    data['p_name'] = data['p_name'].replace('p0', f'p{p}')
                    if not self.__download_init(data):
                        break
                    p += 1
            else:
                self.__download_init(data)

    def __download_init(self, data):
        if not self.__exists(f'{self.warehouse}\\{data["dir_name"]}\\{data["p_name"]}'):  # 仓库是否有此图片
            if not self.__exists(f'{self.down_dir}\\{data["dir_name"]}\\{data["p_name"]}'):  # 下载路径是否有此图片
                if not self.__exists(f'{self.down_dir}\\{data["dir_name"]}'):  # 是否有画师的目录
                    if self.__create_dir(f'{self.down_dir}\\{data["dir_name"]}'):  # 创建目录
                        if not self.__download(data):
                            return False
                else:
                    if not self.__download(data):
                        return False

    def __download(self, data):
        img = self.s.get(data['url'], headers=data['header'], timeout=10)  # 下载图片
        if img.status_code == 404:
            return False
        if img.status_code == 200:
            with open(f'{self.down_dir}\\{data["dir_name"]}\\{data["p_name"]}', 'wb') as f:
                f.write(img.content)  # 保存图片
                return True

    def __get_black_user(self):
        try:
            with open('black_user.json', 'r') as f:
                return load(f)
        except Exception as e:
            print(e)
            print('黑名单文件已损坏!开始重置黑名单')
            self.file_reset.black_user_init()

    def __get_path(self):
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                r = load(f)
                return r['warehouse'], r['downdir']
        except Exception as e:
            print(e)
            print('配置文件已损坏!开始重置')
            self.file_reset.config_init()

    def __get_user_name(self, name):
        for i in self.del_li:
            name.replace(i, '')
        return name

    def __get_p_name(self, url):
        return url.split("/")[-1].replace("_master1200", "")

    def __get_dir_path(self, u_name, id):
        return f"{self.__get_user_name(u_name)} {id}"

    def __exists(self, file_path):
        return Path(file_path).exists()

    def __create_dir(self, dir_path):
        return self.__system(f'mkdir "{dir_path}"')

    def __system(self, cmd):
        r = system(cmd)
        if r == 0:
            return True
        else:
            return False
