from dingapi import writeAccessToken,getAccessToken,insertIntoCostapplication,insertCarCostHistory,insertComplainRocord,insertDailyWorkReport,insertFaultHistory,insertImportantEvent,insertServerCheck,inspectionRecord,insertReturnvisit
from common.config import corpid,corpsecret
from dingapi import sendMessage

import time
import threading
import datetime

if __name__ == '__main__':


    end_time = datetime.datetime.now()
    d1 = end_time
    end_time = time.mktime(end_time.timetuple())*1000
    start_time = d1 - datetime.timedelta(days=60)
    start_time = time.mktime(start_time.timetuple())*1000

    start_time = str(start_time).split('.')[0]
    end_time  = str(end_time).split('.')[0]
    # sendMessage('开始爬虫','爬取爬取两个月以来的数据')

    AccessToken = getAccessToken()

    #多綫程執行不同的入庫
    threads = []
    t1 = threading.Thread(target=insertIntoCostapplication, args=(start_time, end_time, AccessToken))
    threads.append(t1)
    # t2 = threading.Thread(target=insertCarCostHistory, args=(start_time, end_time, AccessToken))
    # threads.append(t2)
    # t3 = threading.Thread(target=insertComplainRocord, args=(start_time, end_time, AccessToken))
    # threads.append(t3)
    # t4 = threading.Thread(target=insertDailyWorkReport, args=(start_time, end_time, AccessToken))
    # threads.append(t4)
    # t5 = threading.Thread(target=insertFaultHistory, args=(start_time, end_time, AccessToken))
    # threads.append(t5)
    # t6 = threading.Thread(target=insertImportantEvent, args=(start_time, end_time, AccessToken))
    # threads.append(t6)
    # t7 = threading.Thread(target=insertServerCheck, args=(start_time, end_time, AccessToken))
    # threads.append(t7)
    # t8 = threading.Thread(target=inspectionRecord, args=(start_time, end_time, AccessToken))
    # threads.append(t8)
    # t9 = threading.Thread(target=insertReturnvisit, args=(start_time, end_time, AccessToken))
    # threads.append(t9)
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # sendMessage('爬虫结束', '两个月的数据已经更新完毕')

    print('Done!')