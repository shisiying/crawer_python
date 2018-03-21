from multiprocessing.managers import BaseManager

from easy_distributed_crawler.SlaveNode.HtmlDownloader import HtmlDownloader
from easy_distributed_crawler.SlaveNode.HtmlParser import HtmlParse

class SlaveWork(object):

    def __init__(self):

        #初始化分布式进程中的工作节点的链接工作
        #实现第一步，使用basemanager注册获取queue的方法名称
        BaseManager.register('get_task_queue')
        BaseManager.register('get_result_queue')

        ##实现第二步，连接到服务器
        server_addr = '127.0.0.1'
        # 端口和验证口令注意保持与服务进程设置的完全一致:
        self.m = BaseManager(address=(server_addr, 8081), authkey='seven')
        # 从网络连接:
        self.m.connect()

        ##实现第三步
        self.task = self.m.get_task_queue()
        self.result = self.m.get_result_queue()

        ##初始化网页下载器和解析器
        self.downloader = HtmlDownloader()
        self.parser = HtmlParse()

    def crawl(self):
        while(True):
            try:
                if not self.task.empty():
                    url = self.task.get()
                    if url =='end':
                        print("控制节点通知爬虫节点停止工作")
                        self.result.put({'new_urls':'end','data':'end'})
                        return
                    print('爬虫节点正在解析:%s' % url.encode('utf-8'))
                    content = self.downloader.download(url)
                    new_urls, data = self.parser.parser(url, content)
                    self.result.put({"new_urls": new_urls, "data": data})
            except EOFError:
                print("连接工作节点失败")
                return
            except Exception:
                print('Crawl  fali ')

if __name__=="__main__":
    spider = SlaveWork()
    spider.crawl()