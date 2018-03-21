## 项目介绍
简单分布式爬虫项目，该项目，分布式采用简单的主从模式，采用分布式进程和进程间的通信，同时，涵盖了普通爬虫应有的几个模块，URL管理模块，Html解析模块，Html下载模块，数据存储模块，爬虫调度模块

### 项目目录介绍
MasterNode--主节点
SlaveNode--从节点

### 爬虫结构

![](https://github.com/shisiying/crawer_python/blob/master/easy_distributed_crawler/爬虫结构.png)

### 爬虫执行力流程

![](https://github.com/shisiying/crawer_python/blob/master/easy_distributed_crawler/执行流程.png)

### 爬虫分布式进程通信的队列

![](https://github.com/shisiying/crawer_python/blob/master/easy_distributed_crawler/爬虫队列.png)


