from alive_progress import alive_bar
from alive_progress import config_handler
# 设置进度条类型
config_handler.set_global(length=30, bar='circles', spinner='pointer')


class rate:

    def __init__(self, counter):
        self.counter = counter

    def rank_page(self):
        with alive_bar(10) as bar:
            pagenum = 0
            while True:
                if self.counter.bar_breaker:
                    break
                if self.counter.pagenum > pagenum:
                    for i in range(self.counter.pagenum-pagenum):
                        bar(text=f"正在处理{self.counter.pagenum}页数据")
                        pagenum = self.counter.pagenum
                if pagenum == 10:
                    break

    def p_down(self, data):
        with alive_bar(self.counter.ranknum) as bar:
            p_num = 0
            t = 0
            while True:
                if self.counter.bar_breaker:
                    break
                if self.counter.down_rank_num > p_num:
                    for i in range(self.counter.down_rank_num-p_num):
                        bar(text=f"正在下载<{data[t]['dir_name'].split(' ')[0]}>的图片")
                        t += 1
                        p_num = self.counter.down_rank_num
                if p_num == self.counter.ranknum:
                    break
