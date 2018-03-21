#coding:utf-8

import time
from multiprocessing import Process,Queue
from multiprocessing.managers import BaseManager

from easy_distributed_crawler.MasterNode.DataOuput import DataOutput
from easy_distributed_crawler.MasterNode.URlManager import UrlManager

class NodeManager(object):
    ##创建分布式管理器，url_queue：url队列，result_queue结果队列
    def start_Manger(self,url_queue,result_queue):
        ##将创建的两个队列注册在网络上，利用register方法，callable则关联queue对象
        BaseManager.register('get_task_queue',callable=lambda:url_queue)
        BaseManager.register('get_result_queue',callable=lambda :result_queue)
        ##绑定端口8001，设置验证口令'seven'
        manager = BaseManager(address=('',8081),authkey='seven')
        return manager

    ##url管理进程
    def url_manager_proc(self,url_queue,conn_queue,root_url):
        url_manager = UrlManager()
        url_manager.add_new_url(root_url)
        while True:
            while(url_manager.has_new_url()):

                ##获取新的url
                new_url = url_manager.get_new_url()
                ##将新的url发给工作节点
                url_queue.put(new_url)
                ##显示已经爬取过的url链接
                print('orl_url_size=',url_manager.old_url_size())
                ##判断条件,当怕去到2000个链接之后就关闭，并且爆粗你进度
                if (url_manager.old_url_size()>2000):
                    ##通知爬虫接点工作借宿
                    url_queue.put('end')
                    print("控制接点发起结束通知")
                    ##关闭管理接点，同事存储set状态
                    url_manager.save_progress('new_urls.txt',url_manager.new_urls)
                    url_manager.save_progress('old_urls.txt',url_manager.old_urls)
                    return
            try:
                if not conn_queue.empty():
                    urls = conn_queue.get()
                    url_manager.add_new_urls(urls)
            except BaseException:
                time.sleep(0.1)

    def result_solve_proc(self,result_queue,conn_queue,store_queue):
        while True:
            try:
                if not result_queue.empty():
                    content = result_queue.get(True)
                    if content['new_urls'] =='end':
                        print("结果分析进程接受通知然后结束")
                        store_queue.put('end')
                        return
                    ##url为set类型
                    conn_queue.put(content['new_urls'])
                    ##解析出来的数据为dict类型
                    store_queue.put(content['data'])
                else:
                    time.sleep(0.1)
            except BaseException:
                time.sleep(0.1)

    def store_proc(self,store_queue):
        output = DataOutput()
        while True:
            if not store_queue.empty():
                data = store_queue.get()
                if data =='end':
                    print("存储进程接受通知然后结束")
                    output.output_end(output.filepath)
                    return
                output.store_data(data)
            else:
                time.sleep(0.1)

if __name__=='__main__':
    ##初始队列
    url_queue = Queue()
    result_queue = Queue()
    store_queue = Queue()
    conn_queue = Queue()

    ##创建分布式管理器
    node =NodeManager()
    manager = node.start_Manger(url_queue,result_queue)

    ##创建Url管理进程，数据提取进程和数据存储进程
    url_manager_proc = Process(target=node.url_manager_proc,args=(url_queue,conn_queue,'http://baike.baidu.com/view/284853.htm'))
    result_solve_proc = Process(target=node.result_solve_proc,args=(result_queue,conn_queue,store_queue))
    store_queue = Process(target=node.store_proc,args=(store_queue,))

    ##启动3个进程和分布式管理器
    url_manager_proc.start()
    result_solve_proc.start()
    store_queue.start()
    manager.get_server().serve_forever()
