#!usr/bin/python3
# coding=utf-8
import requests
from lxml import etree
import Queue
import time

# Python的协程库
import gevent
from gevent import monkey
# 猴子补丁
monkey.patch_all()
# gevent 让我们可以用同步的逻辑，来写异步的程序。
# monkey.patch_all() 在Python程序执行的时候，会动态的将底层的网络库（socket，select）打个补丁，变成异步的库。
# 让程序在执行网络操作的时候，按异步的方式去执行。

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
        job_list = [gevent.spawn(self.load_page, url) for url in url_list]
        gevent.joinall(job_list)

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