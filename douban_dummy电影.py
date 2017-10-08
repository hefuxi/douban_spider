#!usr/bin/python3
# coding=utf-8
import requests
from lxml import etree
import Queue
import time
#导入多线程的线程池
from multiprocessing.dummy import Pool

class douban_spider(object):
    def __init__(self):
        #创建队列,先进先出
        self.queue = Queue.Queue()
        #基本url
        self.base_url = "http://movie.douban.com/top250?start="
        #第一页
        self.num = 0
        #请求头的代理服务器
        self.headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
    def load_page(self,url):
        html = requests.get(url,headers = self.headers).content
        # print "正在抓取第%d页"%self.num
        self.parse_page(html)
        # return html
    def parse_page(self,html):
        #etree处理
        res = etree.HTML(html)
        #截取所有class=info的节点,返回一个列表
        obj_list = res.xpath('//div[@class="info"]')
        for obj in obj_list:
            title = obj.xpath('.//a/span[@class="title"]/text()')[0]
            # print title
            score = obj.xpath(".//span[@class='rating_num']/text()")[0]
            # print score
            #存入队列
            self.queue.put(score + "\t" + title)
            self.num += 1

    def set_spider(self):
        #利用列表tuidaoshi
        url_list = [self.base_url+ str(num) for num in range(0,250+1,25)]
        # 创建10个线程的线程池
        pool = Pool(len(url_list))
        # map()高阶函数，用来批量处理函数传参
        pool.map(self.load_page, url_list)
        # 关闭线程池
        pool.close()
        # 阻塞主线程，等待子线程结束
        pool.join()

        #取队列数据,取当前链接页的数据
        while not self.queue.empty():
            print self.queue.get()
        #打印所有的数量
        print self.num
if __name__ == "__main__":
    douban_spider = douban_spider()
    start = time.time()
    douban_spider.set_spider()
    print "[INFO]: Useing time %f seconds." % (time.time() - start)