from os import _exit
from pixiv import pixiv
from firstRun import firstRun
from blackUserAdd import black_user_add


if __name__ == '__main__':
    m = '''*******************************************
*     欢迎使用PIXIV自动化排行下载程序     *
*               1.下载开始                *
*               2.修改配置                *
*         3.下次运行跳过主菜单选项        *
*                 4.退出                  *
*******************************************'''
    f = firstRun()
    f.check_options()
    b = black_user_add()
    b.add()
    p = pixiv(f)
    if f.skip:
        try:
            p.down_start()
        except Exception as e:
            print(e)
            print("下载出现了以上错误:请检查你的网络情况!如果可以翻墙正常,那么重启程序即可")
    else:
        print(m)
        while True:
            n = input('输入你要执行的操作的数字:')
            try:
                n = int(n)
            except Exception:
                print('请输入数字--', end='')
            else:
                if n == 1:
                    try:
                        p.down_start()
                    except Exception as e:
                        print(e)
                        print("下载出现了以上错误:请检查你的网络情况!如果可以翻墙正常,那么重启程序即可")
                elif n == 2:
                    f.config_init()
                elif n == 3:
                    f.create('file', 'options\\pass.dll')
                elif n == 4:
                    _exit(0)
                else:
                    print('不存在这个选项--', end='')
