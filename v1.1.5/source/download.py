import signal
from threading import Thread
from rate import rate
from counter import counter
from pixiv import pixiv
from time import sleep


class download:

    def __init__(self, config):
        self.counter = counter()
        self.counter.bar_breaker = False
        self.counter.pdown_breaker = False
        self.pixiv = pixiv(self.counter, config)
        self.rate = rate(self.counter)
        self.__start()

    def __start(self):
        signal.signal(signal.SIGINT, self.__stop)
        rankpage = Thread(target=self.rate.rank_page)
        rankpage.setDaemon(True)
        rankpage.start()
        self.pixiv.get_native_data()
        sleep(1)
        p_down = Thread(target=self.rate.p_down, args=(self.pixiv.native_data,))
        p_down.setDaemon(True)
        p_down.start()
        # self.down_pool = []
        for data in self.pixiv.native_data:  # 遍历原始数据
            if self.counter.pdown_breaker:
                break
            self.pixiv.down_p0(data)
        self.counter.bar_breaker = True
        # print(len(self.down_pool))
        # if self.counter.pdown_breaker:
        #     break
        # if len(self.down_pool) < 5:
        #     self.down_pool.append(Thread(target=self.pixiv.down_p0, args=(data,)))
        #     self.down_pool[-1].setDaemon(True)
        #     self.down_pool[-1].start()
        # else:
        #     for i in range(5):
        #         if not self.down_pool[i].is_alive():
        #             self.down_pool[i] = Thread(target=self.pixiv.down_p0, args=(data,))
        #             self.down_pool[i].setDaemon(True)
        #             self.down_pool[i].start()

    def __stop(self, signum, frame):
        self.counter.pdown_breaker = True
        self.counter.bar_breaker = True
