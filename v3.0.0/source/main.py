from time import sleep
from check import check


class mune:

    def __init__(self, check):
        self.check = check
        while True:
            self.__menu()
            s = input('请输入你执行的操作的数字:')
            try:  # 转换为整数
                s = int(s)
            except Exception:  # 为非数字的时候
                print('请输入数字!' * 3)
            if s > 6:  # 输入不存在的选项时
                print('请输入存在的选项!' * 3)
            elif s == 1:
                print('爬虫已完成')
                sleep(3)
                break
            elif s == 2:
                self.__black_user_operate()
            elif s == 3:
                self.check.set_cookie()
                print("已保存输入的cookie")
                sleep(3)
            elif s == 4:
                self.__config_operate()
            elif s == 5:
                break

    def __menu(self):
        print('-' * 60)
        print('pixiv自动下载程序')
        print('-' * 60)
        print('1.爬取开始')
        print('2.黑名单操作')
        print(f'3.cookie设置({self.__cookie_state()})')
        print('4.配置修改')
        print('5.退出')
        print('-' * 60)

    def __black_user_menu(self):
        print('-' * 60)
        print('黑名单操作')
        print('-' * 60)
        print('1.黑名单添加')
        print('2.黑名单自运行(当前设置:)')
        print('3.黑名单删除')
        print('4.返回主菜单')
        print('-' * 60)

    def __black_user_operate(self):
        self.__black_user_menu()
        s = input('请输入你执行的操作的数字:')
        try:  # 转换为整数
            s = int(s)
        except Exception:  # 为非数字的时候
            print('请输入数字!' * 3)
        if s > 4:  # 输入不存在的选项时
            print('请输入存在的选项!' * 3)
        elif s == 1:
            print('黑名单已添加')
        elif s == 2:
            print("黑名单自运行设置已修改")
        elif s == 3:
            print("黑名单已删除")
        elif s == 4:
            pass

    def __config_menu(self):
        print('-' * 60)
        print('配置修改操作')
        print('-' * 60)
        print('1.配置目录调整\n----修改后前面下载的数据如果迁移将无法使用classcifi下的lnk\n----如果要迁移数据请运行下面旧数据迁移选项')
        print(f'2.socket配置({self.__socks_state()})')
        print('3.旧数据迁移\n----数据迁移会花费大量时间---慎重考虑!')
        print('4.返回主菜单')
        print('-' * 60)

    def __config_operate(self):
        self.__config_menu()
        s = input('请输入你执行的操作的数字:')
        try:  # 转换为整数
            s = int(s)
        except Exception:  # 为非数字的时候
            print('请输入数字!' * 3)
        if s > 4:  # 输入不存在的选项时
            print('请输入存在的选项!' * 3)
        elif s == 1:
            self.check.set_config()
        elif s == 2:
            self.check.set_socks()
            print("socket配置已生效")
            sleep(3)
        elif s == 3:
            print("数据已迁移完成")
        elif s == 4:
            pass

    def __socks_state(self):
        if self.check.check_socks_exist():
            return "已配置socks代理"
        else:
            return "未配置socks代理"

    def __cookie_state(self):
        if self.check.check_cookie_exist():
            return "当前已配置cookie"
        else:
            return "当前未配置cookie"


if __name__ == '__main__':
    mune(check())
