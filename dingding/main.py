from dingding.dingapi import writeAccessToken,getAccessToken,insertIntoCostapplication,insertCarCostHistory,insertComplainRocord,insertDailyWorkReport,insertFaultHistory,insertImportantEvent,insertServerCheck,inspectionRecord
from dingding.common.config import corpid,corpsecret
import time
import threading

if __name__ == '__main__':


    dt = "2017-09-01 00:00:00"
    # 转换成时间数组
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    # 转换成时间戳
    timestamp = int(time.mktime(timeArray) * 1000)
    # start_time = int(time.time()*1000)
    start_time = timestamp
    # end_time = start_time + 46400
    end_time = int(time.time() * 1000)
    AccessToken = getAccessToken()

    ##多綫程執行不同的入庫
    threads = []
    t1 = threading.Thread(target=insertIntoCostapplication, args=(start_time, end_time, AccessToken))
    threads.append(t1)
    t2 = threading.Thread(target=insertCarCostHistory, args=(start_time, end_time, AccessToken))
    threads.append(t2)
    t3 = threading.Thread(target=insertComplainRocord, args=(start_time, end_time, AccessToken))
    # threads.append(t3)
    t4 = threading.Thread(target=insertDailyWorkReport, args=(start_time, end_time, AccessToken))
    threads.append(t4)
    t5 = threading.Thread(target=insertFaultHistory, args=(start_time, end_time, AccessToken))
    threads.append(t5)
    t6 = threading.Thread(target=insertImportantEvent, args=(start_time, end_time, AccessToken))
    threads.append(t6)
    t7 = threading.Thread(target=insertServerCheck, args=(start_time, end_time, AccessToken))
    threads.append(t7)
    t8 = threading.Thread(target=inspectionRecord, args=(start_time, end_time, AccessToken))
    threads.append(t8)
    for t in threads:
        t.start()
    for t in threads:
        t.join()



    print('Done!')