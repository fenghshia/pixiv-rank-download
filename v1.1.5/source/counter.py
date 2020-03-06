

class counter:

    def __init__(self):
        self.start_time = int  # 爬虫开始时间
        self.pagenum = 1  # 爬取页数
        self.blacknum = 0  # 遇到的黑名单数
        self.ranknum = 0  # 总排行数
        self.down_p_num = 0  # 下载的排行数
        self.down_rank_num = 0  # 获取到的下载排行数
        self.create_dir_num = 0  # 创建文件夹数
        self.repeat_p_num = 0  # 遭遇重复图片数
        self.bar_breaker = False  # 进度条线程中断
        self.pdown_breaker = False  # 下载进程终止
        self.end_time = int  # 爬虫结束时间
