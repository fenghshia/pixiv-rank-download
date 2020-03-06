from check import check
from blackUserAdd import black_user_add
from download import download
from time import sleep


class mune:

    def __mune(self):
        print('-' * 60)
        print('pixiv自动下载程序')
        print('-' * 60)
        print('1.爬取开始')
        print('2.黑名单添加')
        print(f'3.自动添加黑名单(当前设置为:{self.check.check_black_add()})')
        print('4.配置修改')
        print('5.下次直接运行爬虫')
        print('6.退出')
        print('-' * 60)

    def __init__(self, check):
        self.check = check
        while True:
            self.__mune()
            s = input('请输入你执行的操作的数字:')
            try:  # 转换为整数
                s = int(s)
            except Exception:  # 为非数字的时候
                print('请输入数字!' * 3)
            if s > 6:  # 输入不存在的选项时
                print('请输入存在的选项!' * 3)
            elif s == 1:
                download(self.check.get_config())
                print('爬虫已完成')
            elif s == 2:
                black_user_add()
                print('黑名单已更新')
            elif s == 3:
                self.check.set_black_add()
                print('设置已保存')
            elif s == 4:
                self.check.config_init()
                print('设置已保存')
            elif s == 5:
                self.check.set_skip()
                print('设置已保存')
            elif s == 6:
                break


if __name__ == '__main__':
    check = check()
    if check.check_black_add():  # 自动更新黑名单
        black_user_add()
        print('黑名单已更新')
    if check.check_skip():  # 自动爬虫
        download(check.get_config())
        print('爬虫已完成,3秒后退出')
        sleep(3)
    else:
        mune(check)
