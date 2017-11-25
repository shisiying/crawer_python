# coding: utf-8
import json
import logging
import sys
import time
import os
import requests
from sqlalchemy import create_engine
from dingding.common.config import dburl, corpsecret, corpid
from dingding.common.functions import duration,getName,getAccsory,getProjectName,getAmount,getLaneNumber,getPhoto,getRemark,getSpecificationModels,getStationName,getTotalPrice,getTradeMark,getUnitPrice,getUnits,getUseLocation,getPhoto
from sqlalchemy.orm import sessionmaker
from dingding.mappers.CostApplication import Costapplication
from dingding.mappers.CarCostHistory import Carcosthistory
from dingding.mappers.ComplainRecord import Complainrecord
from dingding.mappers.ImportantEvent import Importantevent
from dingding.mappers.ServerCheck import Servercheck
from dingding.mappers.DailyWorkReport import Dailyworkreport
from dingding.mappers.FaultHistory import Faulthistory
from dingding.mappers.InspectionRecord import Inspectionrecord

##初始化数据库
engine = create_engine(dburl,echo=True)
##初始化日志模块
logging.basicConfig(filename='error.log', filemode="w", level=logging.DEBUG)
##企业用户凭证以及应用凭证
corpid = corpid
corpsecret = corpsecret
##文件主目录
basepath = os.path.dirname(os.path.abspath(__file__))


##写入accesstoken文件到文件中
def writeAccessToken(corpid,corpsecret):
    accessUrl = "https://oapi.dingtalk.com/gettoken?corpid={}&corpsecret={}".format(corpid,corpsecret)
    response = requests.get(accessUrl).json()
    if response['errcode']==0:
        with open(os.path.join(basepath,'common')+'\\token.txt','wb') as file:
            file.write(response['access_token'].encode('utf-8'))

##获取accesstoken
def getAccessToken():
    with open(os.path.join(basepath,'common')+'\\token.txt','r') as file:
        token = file.read()
    return token

###获取每个process_code对应的数据
def getProcessinstanceList(AccessToken,process_code,start_time,end_time,cursor):

    processUrl = 'https://eco.taobao.com/router/rest?method=dingtalk.smartwork.bpms.processinstance.list&session={}&timestamp={}&format=json&v=2.0&process_code={}&start_time={}&end_time={}&size=10&cursor={}'.format(AccessToken,time.strftime("%Y-%m-%d %H:%M:%S"),process_code,start_time,end_time,cursor)
    headers = {
        'Content-Type':'application/json'
    }
    response = requests.get(processUrl,headers=headers)
    return json.loads(response.text)


##插入到费用申请表
##只插入审批状态成功的数据
def insertIntoCostapplication(start_time,end_time,AccessToken):
    mysession = sessionmaker(bind=engine)()
    process_codes ={
        'PROC-FF6YQLE1N2-KKBJDCMHQB3NGD5CUASW1-GHLC7J0J-D8':'计重类费用',
        'PROC-LY7L1NOV-IPYPQ63YR8YKK4BYIA6V1-J6G9QU9J-1':'设备维修费用',
        'PROC-FF6YRLE1N2-SOYP3ZCHPFAKXLF9S65T1-8QXEQU9J-3':'设备材料采购费用',
    }
    for process_code,type in process_codes.items():
        ##初始設置頁數為1
        cursor=0

        ##当返回结果没有该字段时表示没有更多数据了，没有该字段时设置为-1
        while cursor!=-1:
            response_data = getProcessinstanceList(AccessToken=AccessToken, process_code=process_code, start_time=start_time,end_time=end_time, cursor=cursor)
            if 'error_response' in response_data.keys():
                logging.info(response_data['error_response']['sub_msg'].encode('utf-8'))

                ##toeken後期設置，執行writetoken,再一次執行獲取數據
                writeAccessToken(corpid,corpsecret)
                AccessToken = getAccessToken()
                response_data = getProcessinstanceList(AccessToken=AccessToken, process_code=process_code,start_time=start_time, end_time=end_time, cursor=cursor)
            result_flag = response_data['dingtalk_smartwork_bpms_processinstance_list_response']['result']

            ##判断返回结果是否是成功的
            if result_flag['ding_open_errcode']==0:

                if 'next_cursor' not in result_flag['result'].keys():
                    ##设置cursor,如果不存在这个键值就设置为-1
                    cursor = -1
                else:
                    ##翻頁
                    cursor = int(result_flag['result']['next_cursor'])

                ##list有数据
                if result_flag['result']['list']:
                    ###獲取詳情數據
                   for data_list in result_flag['result']['list']['process_instance_top_vo']:

                       ##判断审批状态是否为成功
                        if data_list['status']=='COMPLETED':

                            project_data = json.loads(data_list['form_component_values']['form_component_value_vo'][-2]['value'])

                            ##循環費用明細
                            for project in enumerate(project_data):

                                # ##定義字段
                                projectName = None
                                tradeMark = None
                                specificationModels = None
                                units = None
                                amount = None
                                unitPrice =None
                                totalPrice = None
                                stationName = None
                                laneNumber = None
                                useLocation =None
                                remark =None
                                photo =None

                                ##處理字符串
                                for pr in project[1]:
                                    if pr['label']=='项目名称' or pr['label']=='设备名称' and 'value' in pr.keys():
                                        projectName = pr['value']
                                    if pr['label']=='品牌' and 'value' in pr.keys():
                                        tradeMark = pr['value']
                                    if pr['label']=='规格/型号' and 'value' in pr.keys():
                                        specificationModels = pr['value']
                                    if pr['label'] == '单位' and 'value' in pr.keys():
                                        units = pr['value']
                                    if pr['label'] == '数量' and 'value' in pr.keys():
                                        amount = pr['value']
                                    if pr['label'] == '单价（元）' and 'value' in pr.keys():
                                        unitPrice = pr['value']
                                    if pr['label'] == '合计金额' or  pr['label'] == '本项预算总金额'  and 'value' in pr.keys():
                                        totalPrice = pr['value']
                                    if pr['label'] == '站名' and 'value' in pr.keys():
                                        stationName = pr['value']
                                    if pr['label'] == '车道号' and 'value' in pr.keys():
                                        laneNumber = pr['value']
                                    if pr['label'] == '使用位置' and 'value' in pr.keys():
                                        useLocation = pr['value']
                                    if pr['label'] == '备注' and 'value' in pr.keys():
                                        remark = pr['value']
                                    if pr['label'] == '报送照片' or pr['label']=='照片' or pr['label']=='远景照片' and 'value' in pr.keys():
                                        photo = pr['value']

                                fileds = {
                                    'expensesStatement': project[0] + 1,
                                    'approvalNumber': data_list['process_instance_id'],
                                    'costType' : type,
                                    'headlin':data_list['title'],
                                    'approvalStatus' : 'COMPLETED',
                                    'approvalResult' :data_list['process_instance_result'],
                                    'approvalTime' : data_list['create_time'],
                                    'approvalFinshTime' : data_list['finish_time'],
                                    'initiatorsNumber' : None,
                                    'initiatorsUserID':data_list['originator_userid'],
                                    'initiatorsName' :getName(data_list['title']),
                                    'InitiatorsDepartment' : data_list['originator_dept_id'],
                                    'historicalApproverName' : str(data_list['approver_userid_list']['string']),
                                    'approvalHistory' : str(data_list['approver_userid_list']['string']),
                                    'currentProcessingName' : data_list['approver_userid_list']['string'][-1],
                                    'reviewsTake':duration(data_list['create_time'],data_list['finish_time']),##day
                                    'companyName' : data_list['form_component_values']['form_component_value_vo'][0]['value'],
                                    'highwaySection' :data_list['form_component_values']['form_component_value_vo'][1]['value'],
                                    'type' : data_list['form_component_values']['form_component_value_vo'][2]['value'],
                                    'projectName' :projectName,
                                    'tradeMark' : tradeMark,
                                    'specificationModels' :specificationModels,
                                    'units':units,
                                    'amount' :amount,
                                    'unitPrice': unitPrice,
                                    'totalPrice': totalPrice,
                                    'stationName' : stationName,
                                    'laneNumber': laneNumber,
                                    'useLocation': useLocation,
                                    'remark': remark,
                                    'photo':photo,
                                    'otherAccessory' : getAccsory(data_list['form_component_values']['form_component_value_vo'][-1])
                                }
                                costapplication = Costapplication(**fileds)
                                mysession.merge(costapplication)  # 主鍵有存在也新增
                                mysession.commit()
                                mysession.close()
            else:
                logging.info('{} the request of {} has error.the process code is {} '.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),sys._getframe().f_code.co_name,process_code))



##故障处理记录
def insertFaultHistory(start_time,end_time,AccessToken):
    mysession = sessionmaker(bind=engine)()
    process_codes ={
        'PROC-WIYJNNZV-UX9N03U8Q08AF1478BSC3-OHV9136J-9',
        'PROC-QQXJ732V-XH9NOULZUXBW27PS2T2X1-2GOJ336J-Z',
        'PROC-PCDKZZAV-UZ9N7KSHRTGHPUVNSTZK1-AQIQ336J-G',
        'PROC-WIYJDNZV-Y2WLNDQ4UUJYB2E1ZVAS1-N23G354J-N'
    }
    for process_code in process_codes:
        ##初始化頁數為1
        cursor=0

        ##当返回结果没有该字段时表示没有更多数据了，没有该字段时设置为-1
        while cursor!=-1:
            response_data = getProcessinstanceList(AccessToken=AccessToken, process_code=process_code, start_time=start_time,end_time=end_time, cursor=cursor)
            if 'error_response' in response_data.keys():
                logging.info(response_data['error_response']['sub_msg'].encode('utf-8'))

                ##toeken後期設置，執行writetoken,再一次執行獲取數據
                writeAccessToken(corpid, corpsecret)
                AccessToken = getAccessToken()
                response_data = getProcessinstanceList(AccessToken=AccessToken, process_code=process_code, start_time=start_time, end_time=end_time, cursor=cursor)
            result_flag = response_data['dingtalk_smartwork_bpms_processinstance_list_response']['result']

            ##判断返回结果是否是成功的
            if result_flag['ding_open_errcode']==0:

                if 'next_cursor' not in result_flag['result'].keys():
                    ##设置cursor,如果不存在这个键值就设置为-1
                    cursor = -1
                else:
                    cursor = int(result_flag['result']['next_cursor'])

                ##list有数据
                if result_flag['result']['list']:

                   for data_list in result_flag['result']['list']['process_instance_top_vo']:
                       #判断审批状态是否为成功
                       if data_list['status']=='COMPLETED':

                           ##定義動態的字段
                           highwaySection = None
                           controalStation = None
                           Station = None
                           lane = None
                           faultType = None
                           faultPhenomenon = None
                           otherPhenomenon = None
                           result = None
                           presentTime = None
                           presentSite = None
                           photo = None
                           photo2 = None
                           photo3 = None
                           photo4 = None

                           for data_form_component in data_list['form_component_values']['form_component_value_vo']:

                               if data_form_component['name'] == '所属路段' and 'value' in data_form_component.keys():
                                   highwaySection = data_form_component['value']
                               if data_form_component['name'] == '管理所' and 'value' in data_form_component.keys():
                                   controalStation = data_form_component['value']
                               if data_form_component['name'] == '收费站' and 'value' in data_form_component.keys():
                                   Station = data_form_component['value']
                               if data_form_component['name'] == '地点' and 'value' in data_form_component.keys():
                                   lane = data_form_component['value']
                               if data_form_component['name'] == '故障类型' and 'value' in data_form_component.keys():
                                   faultType = data_form_component['value']
                               if data_form_component['name'] == '故障现象' and 'value' in data_form_component.keys():
                                   faultPhenomenon = data_form_component['value']
                               if data_form_component['name'] == '其他现象' and 'value' in data_form_component.keys():
                                   otherPhenomenon = data_form_component['value']
                               if data_form_component['name'] == '处理结果' and 'value' in data_form_component.keys():
                                   result = data_form_component['value']
                               if data_form_component['name'] == '["当前时间","当前地点"]' and 'value' in data_form_component.keys():
                                   presentTime = eval(data_form_component['value'])[0]
                                   presentSite = str(eval(data_form_component['value'])[1]) + ',' + str(eval(data_form_component['value'])[2]) + ',' + eval(data_form_component['value'])[3]
                               if data_form_component['name'] == '图片' and 'value' in data_form_component.keys():
                                   photo = data_form_component['value']
                               if data_form_component['name'] == '图片(2)' and 'value' in data_form_component.keys():
                                   photo2 = data_form_component['value']
                               if data_form_component['name'] == '图片(3)' and 'value' in data_form_component.keys():
                                   photo3 = data_form_component['value']
                               if data_form_component['name'] == '图片(4)' and 'value' in data_form_component.keys():
                                   photo4 = data_form_component['value']

                           fileds = {
                               'approvalNumber': data_list['process_instance_id'],
                               'headline': data_list['title'],
                               'approvalStatus': 'COMPLETED',
                               'approvalResult': data_list['process_instance_result'],
                               'approvalTime': data_list['create_time'],
                               'approvalFinshTime': data_list['finish_time'],
                               'initiatorsNumber': None,
                               'initiatorsUserID': data_list['originator_userid'],
                               'initiatorsName': getName(data_list['title']),
                               'initiatorsDepartment': data_list['originator_dept_id'],
                               'historicalApproverName': str(data_list['approver_userid_list']['string']),
                               'approvalHistory': str(data_list['approver_userid_list']['string']),
                               'currentProcessingName': data_list['approver_userid_list']['string'][-1],
                               'reviewTake': duration(data_list['create_time'], data_list['finish_time']),  ##day
                                'highwaySection': highwaySection,
                                'controalStation': controalStation,
                                'Station': Station,
                                'lane': lane,
                                'faultType': faultType,
                                'faultPhenomenon': faultPhenomenon,
                                'otherPhenomenon': otherPhenomenon,
                                'result': result,
                                'presentTime': presentTime,
                                'presentSite': presentSite,
                                'photo': photo,
                                'photo2': photo2,
                                'photo3': photo3,
                                'photo4': photo4
                           }
                           faulthistory = Faulthistory(**fileds)
                           mysession.merge(faulthistory)  # 主鍵有存在也新增
                           mysession.commit()
                           mysession.close()
            else:
                logging.info('{} the request of {} has error.the process code is {} '.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),sys._getframe().f_code.co_name,process_code))


##巡检保养记录
def inspectionRecord(start_time,end_time,AccessToken):
    mysession = sessionmaker(bind=engine)()
    process_codes ={
        'PROC-424LSGUV-SZ9N89XXSLGDX14TZAWW3-IDY0A36J-H':'通信',
        'PROC-WIYJMNZV-O4BNVGVBSZTU92XCXE113-ZCB7H46J-3':'车道',
        'PROC-3KYJ13FV-HPNP8O27UPWJB1QMDNCV2-UTPREF9J-M':'收费服务器',
        'PROC-PC5LGMYU-YZANCYV9MT7IS1EOZBJ22-LR7ZD46J-6':'电源',
        'PROC-GTHKCO8W-H45QOQTVMG2YOPV1SBRS1-AQOIR3AJ-3':'监控室',
        'PROC-3KYJ23FV-2Z9N2J7QRHZ8I2XG952R3-5CA0B36J-R':'通信',
        'PROC-FF6YHQ9WQ2-W1BNI5ZHNXIK28HR3WAU1-7BKHE46J-8':'电源',
        'PROC-0SBKJ8AV-T4BN40I8QZUT304MNR0F2-0XMGH46J-3':'车道',
        'PROC-0SBKJ8AV-2RNPVGZYO0M5E438SZSN1-ZBW5EF9J-6':'收费服务器',
        'PROC-G5SKLVFV-TV4QHJ55OGQBSRQBYA0X1-32ZCQ3AJ-W':'监控室',
        'PROC-WIYJONZV-63ANQ7M8SW4PO2U1ZZ5X1-HKBWA36J-B':'通信',
        'PROC-3KYJW2FV-50BNT9W9VBS4R2V4OAP82-K9MEH46J-E':'车道',
        'PROC-3KYJ13FV-X5BNFQ6LVZ8F71YZ8PPX2-PA1RP46J-N':'隧道',
        'PROC-G5SKLVFV-BTNP2HURM1SEO24QGVS62-LS9CFF9J-1':'收费服务器',
        'PROC-FF6YRLE1N2-F0BN9AM5M2QTGSTOE6TY1-TP0CE46J-6':'电源',
        'PROC-MOEKBM6V-715Q0R1AUG8LWA1C2XUU1-IO8DR3AJ-9':'监控室',
        'PROC-FF6YHQ9WQ2-53ANDJZCQ7RRB04YTHYJ3-5S9HA36J-H':'通信',
        'PROC-A2FKOLYV-XHANS4J3OYH9Y00K8E943-XWR7E46J-M':'电源',
        'PROC-FF6YR2IQO2-K6BN7S3ASH7781BVSWQP3-5RGPP46J-D':	'隧道',
        'PROC-4W5K1S1W-G3NO5FPZNEPQIBSLLEBQ1-U8PKUZ7J-1':'车道',
        'PROC-WIYJONZV-PKHP7HCQPYIYY0XFD3JU1-IOXTO69J-5':'收费服务器',
        'PROC-X3IK793W-H45QKMYHVRUV98E7SKIV1-5759R3AJ-2':'监控室',
        'PROC-QQXJ732V-QW5NJLAJSLBYD5T2SCEO1-2W0NN16J-41':'通信',
        'PROC-EF6YFCYSO2-V0BNSQQFR2TL6JDA7QSQ1-WZ9OD46J-5':	'电源',
        'PROC-WIYJDNZV-D1BNYX36PRWJ712543D52-TVW4H46J-E':'车道',
        'PROC-WIYJNNZV-LRNP8THKT8FSL3QFK76K3-9WB0FF9J-7':'收费服务器',
        'PROC-WIYJDNZV-V35QXMJNNJ2YUXKR4ZZW1-SXS2R3AJ-5':'监控室'
    }
    for process_code, type in process_codes.items():
        cursor=0
        ##当返回结果没有该字段时表示没有更多数据了，没有该字段时设置为-1
        while cursor!=-1:
            response_data = getProcessinstanceList(AccessToken=AccessToken, process_code=process_code, start_time=start_time,end_time=end_time, cursor=cursor)
            if 'error_response' in response_data.keys():
                logging.info(response_data['error_response']['sub_msg'].encode('utf-8'))
                ##toeken後期設置，執行writetoken,再一次執行獲取數據
                writeAccessToken(corpid, corpsecret)
                AccessToken = getAccessToken()
                response_data = getProcessinstanceList(AccessToken=AccessToken, process_code=process_code,start_time=start_time, end_time=end_time, cursor=cursor)
            result_flag = response_data['dingtalk_smartwork_bpms_processinstance_list_response']['result']
            ##判断返回结果是否是成功的
            if result_flag['ding_open_errcode']==0:
                if 'next_cursor' not in result_flag['result'].keys():
                    ##设置cursor,如果不存在这个键值就设置为-1
                    cursor = -1
                else:
                    cursor = int(result_flag['result']['next_cursor'])
                ##list有数据
                if result_flag['result']['list']:
                   for data_list in result_flag['result']['list']['process_instance_top_vo']:
                       ##判断审批状态是否为成功
                        if data_list['status']=='COMPLETED':

                            ##定義字段
                            highwaySection = None
                            recordType = None
                            site = None
                            otherSite = None
                            temperature = None
                            humidness = None
                            jobContent = None
                            foundFault = None
                            presentTime = None
                            presentSite = None
                            photo = None
                            photo2 = None
                            photo3 = None
                            photo4 = None

                            for data_form_component in data_list['form_component_values']['form_component_value_vo']:

                                if data_form_component['name'] == '路段' and 'value' in data_form_component.keys():
                                    highwaySection = data_form_component['value']
                                if data_form_component['name'] == '记录类型' and 'value' in data_form_component.keys():
                                    recordType = data_form_component['value']
                                if data_form_component['name'] == '巡检（保养）地点' and 'value' in data_form_component.keys():
                                    site = data_form_component['value']
                                if data_form_component['name'] == '地点补充' and 'value' in data_form_component.keys():
                                    otherSite = data_form_component['value']
                                if data_form_component['name'] == '机房温度' and 'value' in data_form_component.keys():
                                    temperature = data_form_component['value']
                                if data_form_component['name'] == '机房湿度' and 'value' in data_form_component.keys():
                                    humidness = data_form_component['value']
                                if data_form_component['name'] == '工作内容' and 'value' in data_form_component.keys():
                                    jobContent = data_form_component['value']
                                if data_form_component['name'] == '发现故障' and 'value' in data_form_component.keys():
                                    foundFault = data_form_component['value']
                                if data_form_component[ 'name'] == '["当前时间","当前地点"]' and 'value' in data_form_component.keys():
                                    presentTime = eval(data_form_component['value'])[0]
                                    presentSite = str(eval(data_form_component['value'])[1]) + ',' + str(eval(data_form_component['value'])[2]) + ',' + eval(data_form_component['value'])[3]
                                if data_form_component['name'] == '图片' and 'value' in data_form_component.keys():
                                    photo = data_form_component['value']
                                if data_form_component['name'] == '图片(2)' and 'value' in data_form_component.keys():
                                    photo2 = data_form_component['value']
                                if data_form_component['name'] == '图片(3)' and 'value' in data_form_component.keys():
                                    photo3 = data_form_component['value']
                                if data_form_component['name'] == '图片(4)' and 'value' in data_form_component.keys():
                                    photo4 = data_form_component['value']

                            fileds = {
                                'type': type,
                                'approvalNumber': data_list['process_instance_id'],
                                'headline': data_list['title'],
                                'approvalStatus': 'COMPLETED',
                                'approvalResult': data_list['process_instance_result'],
                                'approvalTime': data_list['create_time'],
                                'approvalFinshTime': data_list['finish_time'],
                                'initiatorsNumber': None,
                                'initiatorsUserID': data_list['originator_userid'],
                                'initiatorsName': getName(data_list['title']),
                                'initiatorsDepartment': data_list['originator_dept_id'],
                                'historicalApproverName': str(data_list['approver_userid_list']['string']),
                                'approvalHistory': str(data_list['approver_userid_list']['string']),
                                'currentProcessingName': data_list['approver_userid_list']['string'][-1],
                                'reviewTake': duration(data_list['create_time'], data_list['finish_time']),  ##day
                                'highwaySection': highwaySection,
                                'recordType': recordType,
                                'site' :site,
                                'otherSite' : otherSite,
                                'temperature' : temperature,
                                'humidness' : humidness,
                                'jobContent' : jobContent,
                                'foundFault':foundFault,
                                'presentTime': presentTime,
                                'presentSite': presentSite,
                                'photo': photo,
                                'photo2': photo2,
                                'photo3': photo3,
                                'photo4': photo4
                            }
                            inspectionrecord = Inspectionrecord(**fileds)
                            mysession.merge(inspectionrecord)  # 主鍵有存在也新增
                            mysession.commit()
                            mysession.close()

            else:
                logging.info('{} the request of {} has error.the process code is {} '.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),sys._getframe().f_code.co_name,process_code))

##车辆加油记录
def insertCarCostHistory(start_time,end_time,AccessToken):
    mysession = sessionmaker(bind=engine)()
    process_codes ={
       'PROC-FF6Y696SO2-1IQIDPV9RV9EPI9N9Y0W1-BY95APZI-Z'
    }
    for process_code in process_codes:
        cursor=0
        ##当返回结果没有该字段时表示没有更多数据了，没有该字段时设置为-1
        while cursor!=-1:
            response_data = getProcessinstanceList(AccessToken=AccessToken, process_code=process_code, start_time=start_time,end_time=end_time, cursor=cursor)
            if 'error_response' in response_data.keys():
                logging.info(response_data['error_response']['sub_msg'].encode('utf-8'))

                ##toeken後期設置，執行writetoken,再一次執行獲取數據
                writeAccessToken(corpid, corpsecret)
                AccessToken = getAccessToken()
                response_data = getProcessinstanceList(AccessToken=AccessToken, process_code=process_code,start_time=start_time, end_time=end_time, cursor=cursor)
            result_flag = response_data['dingtalk_smartwork_bpms_processinstance_list_response']['result']

            ##判断返回结果是否是成功的
            if result_flag['ding_open_errcode']==0:

                if 'next_cursor' not in result_flag['result'].keys():
                    ##设置cursor,如果不存在这个键值就设置为-1
                    cursor = -1
                else:
                    cursor = int(result_flag['result']['next_cursor'])
                ##list有数据
                if result_flag['result']['list']:
                   for data_list in result_flag['result']['list']['process_instance_top_vo']:
                       ##判断审批状态是否为成功
                        if data_list['status']=='COMPLETED':
                            carNumber = None
                            highwaySection =None
                            mileage = None
                            oilPrice = None
                            cost =None
                            instrumenBoardPhoto = None
                            receiptPhoto =None

                            for form_component in data_list['form_component_values']['form_component_value_vo']:

                                if form_component['name']=='车号' and 'value' in form_component.keys():
                                    carNumber = form_component['value']
                                if form_component['name'] == '路段' and 'value' in form_component.keys():
                                    highwaySection = form_component['value']
                                if form_component['name'] == '仪表盘里程数' and 'value' in form_component.keys():
                                    mileage = form_component['value']
                                if form_component['name'] == '油价' and 'value' in form_component.keys():
                                    oilPrice = form_component['value']
                                if form_component['name'] == '金额（元）' and 'value' in form_component.keys():
                                    cost = form_component['value']
                                if form_component['name'] == '仪表盘照片' and 'value' in form_component.keys():
                                    instrumenBoardPhoto = form_component['value']
                                if form_component['name'] == '加油小票照片' and 'value' in form_component.keys():
                                    receiptPhoto = form_component['value']

                            fileds = {
                                   'approvalNumber': data_list['process_instance_id'],
                                    'headlin' : data_list['title'],
                                    'approvalStatus' : 'COMPLETED',
                                    'approvalResult' : data_list['process_instance_result'],
                                    'approvalTime' : data_list['create_time'],
                                    'approvalFinshTime' : data_list['finish_time'],
                                    'initiatorsNumber' : None,
                                    'initiatorsUserID' :data_list['originator_userid'],
                                    'initiatorsName' : getName(data_list['title']),
                                    'initiatorsDepartment' : data_list['originator_dept_id'],
                                    'historicalApproverName' :str(data_list['approver_userid_list']['string']),
                                    'approvalHistory' : str(data_list['approver_userid_list']['string']),
                                    'currentProcessingName' : data_list['approver_userid_list']['string'][-1],
                                    'reviewsTake' : duration(data_list['create_time'], data_list['finish_time']),  ##day
                                    'carNumber' :carNumber,
                                    'highwaySection' :highwaySection,
                                    'mileage' :mileage,
                                    'oilPrice' :oilPrice,
                                    'cost' :cost,
                                    'instrumenBoardPhoto' :str(instrumenBoardPhoto),
                                    'receiptPhoto' :str(receiptPhoto)
                            }
                            carcosthistory = Carcosthistory(**fileds)
                            mysession.merge(carcosthistory)  # 主鍵有存在也新增
                            mysession.commit()
                            mysession.close()

            else:
                logging.info('{} the request of {} has error.the process code is {} '.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),sys._getframe().f_code.co_name,process_code))

###业主投诉受理
def insertComplainRocord(start_time,end_time,AccessToken):
    mysession = sessionmaker(bind=engine)()
    process_codes ={
      'PROC-FF6YBV6WQ2-3IQI4JI0N8O9P2VPPRBN1-QHMU9PZI-F'
    }
    for process_code in process_codes:
        cursor=0
        ##当返回结果没有该字段时表示没有更多数据了，没有该字段时设置为-1
        while cursor!=-1:
            response_data = getProcessinstanceList(AccessToken=AccessToken, process_code=process_code, start_time=start_time,end_time=end_time, cursor=cursor)
            if 'error_response' in response_data.keys():
                logging.info(response_data['error_response']['sub_msg'].encode('utf-8'))
                ##toeken後期設置，執行writetoken,再一次執行獲取數據
                writeAccessToken(corpid, corpsecret)
                AccessToken = getAccessToken()
                response_data = getProcessinstanceList(AccessToken=AccessToken, process_code=process_code,start_time=start_time, end_time=end_time, cursor=cursor)

            result_flag = response_data['dingtalk_smartwork_bpms_processinstance_list_response']['result']
            ##判断返回结果是否是成功的
            if result_flag['ding_open_errcode']==0:

                if 'next_cursor' not in result_flag['result'].keys():
                    ##设置cursor,如果不存在这个键值就设置为-1
                    cursor = -1
                else:
                    cursor = int(result_flag['result']['next_cursor'])
                ##list有数据
                if result_flag['result']['list']:
                   for data_list in result_flag['result']['list']['process_instance_top_vo']:
                       ##判断审批状态是否为成功
                        if data_list['status']=='COMPLETED':

                            ##定義字段
                            customerName = None
                            highwaySection = None
                            list = None
                            complain = None
                            photo = None
                            accessory = None

                            for form_component in data_list['form_component_values']['form_component_value_vo']:
                                if form_component['name'] == '反映问题业主姓名' and 'value' in form_component.keys():
                                    customerName = form_component['value']
                                if form_component['name'] == '投诉路段' and 'value' in form_component.keys():
                                    highwaySection = form_component['value']
                                if form_component['name'] == '问题清单' and 'value' in form_component.keys():
                                    list = form_component['value']
                                if form_component['name'] == '图片' and 'value' in form_component.keys():
                                    photo = form_component['value']
                                if form_component['name'] == '附件' and 'value' in form_component.keys():
                                    accessory = form_component['value']

                            fileds = {
                                'approvalNumber': data_list['process_instance_id'],
                                'headline': data_list['title'],
                                'approvalStatus': 'COMPLETED',
                                'approvalResult': data_list['process_instance_result'],
                                'approvalTime': data_list['create_time'],
                                'approvalFinishTime': data_list['finish_time'],
                                'initiatorsNumber': None,
                                'initiatorsUserID': data_list['originator_userid'],
                                'initiatorsName': getName(data_list['title']),
                                'initiatorsDepartment': data_list['originator_dept_id'],
                                'historicalApproverName': str(data_list['approver_userid_list']['string']),
                                'approverHistory': str(data_list['approver_userid_list']['string']),
                                'currentProcessingName': data_list['approver_userid_list']['string'][-1],
                                'reviewTake': duration(data_list['create_time'], data_list['finish_time']),  ##day
                                'customerName' : customerName,
                                'highwaySection' : highwaySection,
                                'list' : list,
                                'complain' : complain,
                                'photo' : photo,
                                'accessory' : accessory
                            }
                            complain = Complainrecord(**fileds)
                            mysession.merge(complain)  # 主鍵有存在也新增
                            mysession.commit()
                            mysession.close()

            else:
                logging.info('{} the request of {} has error.the process code is {} '.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),sys._getframe().f_code.co_name,process_code))

##重大事件
def insertImportantEvent(start_time,end_time,AccessToken):
    mysession = sessionmaker(bind=engine)()
    process_codes ={
      'PROC-FF6YNLE1N2-97QITADQN31AE8BL4EQN1-MERLAPZI-D7'
    }
    for process_code in process_codes:
        cursor=0
        ##当返回结果没有该字段时表示没有更多数据了，没有该字段时设置为-1
        while cursor!=-1:
            response_data = getProcessinstanceList(AccessToken=AccessToken, process_code=process_code, start_time=start_time,end_time=end_time, cursor=cursor)
            if 'error_response' in response_data.keys():
                logging.info(response_data['error_response']['sub_msg'].encode('utf-8'))
                ##toeken後期設置，執行writetoken,再一次執行獲取數據
                writeAccessToken(corpid, corpsecret)
                AccessToken = getAccessToken()
                response_data = getProcessinstanceList(AccessToken=AccessToken, process_code=process_code,start_time=start_time, end_time=end_time, cursor=cursor)
            result_flag = response_data['dingtalk_smartwork_bpms_processinstance_list_response']['result']
            ##判断返回结果是否是成功的
            if result_flag['ding_open_errcode']==0:

                if 'next_cursor' not in result_flag['result'].keys():
                    ##设置cursor,如果不存在这个键值就设置为-1
                    cursor = -1
                else:
                    cursor = int(result_flag['result']['next_cursor'])
                ##list有数据
                if result_flag['result']['list']:
                   for data_list in result_flag['result']['list']['process_instance_top_vo']:
                       ##判断审批状态是否为成功
                        if data_list['status']=='COMPLETED':


                            
                            ##定義字段
                            department = None
                            highwaySection = None
                            eventTime = None
                            FinshTime = None
                            influenceTime = None
                            eventSite = None
                            eventType = None
                            eventDescription = None
                            influence = None
                            method = None
                            loss = None
                            lossCapital = None
                            photo = None
                            accessory = None

                            for form_component in data_list['form_component_values']['form_component_value_vo']:

                                if form_component['name'] == '所属分中心' and 'value' in form_component.keys():
                                    department = form_component['value']
                                if form_component['name'] == '所属路段' and 'value' in form_component.keys():
                                    highwaySection = form_component['value']
                                if form_component['name'] == '所属路段' and 'value' in form_component.keys():
                                    highwaySection = form_component['value']
                                if form_component['name'] == '["事件发生时间","预计恢复时间"]' and 'value' in form_component.keys():
                                    eventTime = eval(form_component['value'])[0]
                                    FinshTime = eval(form_component['value'])[1]
                                    influenceTime = eval(form_component['value'])[2]
                                if form_component['name'] == '事件地点' and 'value' in form_component.keys():
                                    eventSite = form_component['value']
                                if form_component['name'] == '事件类型' and 'value' in form_component.keys():
                                    eventType = form_component['value']
                                if form_component['name'] == '事件描述' and 'value' in form_component.keys():
                                    eventDescription = form_component['value']
                                if form_component['name'] == '造成影响' and 'value' in form_component.keys():
                                    influence = form_component['value']
                                if form_component['name'] == '采取手段' and 'value' in form_component.keys():
                                    method = form_component['value']
                                if form_component['name'] == '预计损失（元）' and 'value' in form_component.keys():
                                    loss = form_component['value']
                                    lossCapital = form_component['value']
                                if form_component['name'] == '图片' and 'value' in form_component.keys():
                                    photo = form_component['value']
                                if form_component['name'] == '附件' and 'value' in form_component.keys():
                                    accessory = form_component['value']

                            fileds = {
                                'approvalNumber': data_list['process_instance_id'],
                                'headline': data_list['title'],
                                'approvalStatus': 'COMPLETED',
                                'approvalResult': data_list['process_instance_result'],
                                'approvalTime': data_list['create_time'],
                                'approvalFinishTime': data_list['finish_time'],
                                'initiatorsNumber': None,
                                'initiatorsUserID': data_list['originator_userid'],
                                'initiatorsName': getName(data_list['title']),
                                'InitiatorsDepartment': data_list['originator_dept_id'],
                                'historicalApproverName': str(data_list['approver_userid_list']['string']),
                                'approvalHistory': str(data_list['approver_userid_list']['string']),
                                'currentProcessingName': data_list['approver_userid_list']['string'][-1],
                                'reviewTake': duration(data_list['create_time'], data_list['finish_time']),  ##day
                                'department' :department,
                                'highwaySection' : highwaySection,
                                'eventTime' :eventTime,
                                'FinshTime' : FinshTime,
                                'influenceTime' : influenceTime,
                                'eventSite' : eventSite,
                                'eventType' : eventType,
                                'eventDescription' : eventDescription,
                                'influence' : influence,
                                'method' : method,
                                'loss' : loss,
                                'lossCapital' : lossCapital,
                                'photo' : photo,
                                'accessory' :accessory,
                            }
                            importantevent = Importantevent(**fileds)
                            mysession.merge(importantevent)  # 主鍵有存在也新增
                            mysession.commit()
                            mysession.close()


            else:
                logging.info('{} the request of {} has error.the process code is {} '.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),sys._getframe().f_code.co_name,process_code))

##收费服务器巡检
def insertServerCheck(start_time,end_time,AccessToken):
    mysession = sessionmaker(bind=engine)()
    process_codes ={
        'PROC-WIYJNNZV-LRNP8THKT8FSL3QFK76K3-9WB0FF9J-7',
        'PROC-WIYJONZV-PKHP7HCQPYIYY0XFD3JU1-IOXTO69J-5',
        'PROC-G5SKLVFV-BTNP2HURM1SEO24QGVS62-LS9CFF9J-1',
        'PROC-0SBKJ8AV-2RNPVGZYO0M5E438SZSN1-ZBW5EF9J-6',
        'PROC-3KYJ13FV-HPNP8O27UPWJB1QMDNCV2-UTPREF9J-M'
    }
    for process_code in process_codes:
        cursor=0
        ##当返回结果没有该字段时表示没有更多数据了，没有该字段时设置为-1
        while cursor!=-1:
            response_data = getProcessinstanceList(AccessToken=AccessToken, process_code=process_code, start_time=start_time,end_time=end_time, cursor=cursor)
            if 'error_response' in response_data.keys():
                logging.info(response_data['error_response']['sub_msg'].encode('utf-8'))
                ##toeken後期設置，執行writetoken,再一次執行獲取數據
                writeAccessToken(corpid, corpsecret)
                AccessToken = getAccessToken()
                response_data = getProcessinstanceList(AccessToken=AccessToken, process_code=process_code,start_time=start_time, end_time=end_time, cursor=cursor)
            result_flag = response_data['dingtalk_smartwork_bpms_processinstance_list_response']['result']

            ##判断返回结果是否是成功的
            if result_flag['ding_open_errcode']==0:
                if 'next_cursor' not in result_flag['result'].keys():
                    ##设置cursor,如果不存在这个键值就设置为-1
                    cursor = -1
                else:
                    cursor = int(result_flag['result']['next_cursor'])
                ##list有数据
                if result_flag['result']['list']:
                   for data_list in result_flag['result']['list']['process_instance_top_vo']:
                       ##判断审批状态是否为成功
                        if data_list['status']=='COMPLETED':
                            
                            ##定義字段
                            highwaySection = None
                            serverName = None
                            CPU = None
                            RAM = None
                            virusDB = None
                            virusDBphoto = None
                            CPUphoto = None
                            presentTime = None
                            presentSite = None
                            for form_component in data_list['form_component_values']['form_component_value_vo']:

                                if form_component['name'] == '路段' and 'value' in form_component.keys():
                                    highwaySection = form_component['value']
                                if form_component['name'] == '服务器名称' and 'value' in form_component.keys():
                                    serverName = form_component['value']
                                if form_component['name'] == 'CPU使用率' and 'value' in form_component.keys():
                                    CPU = form_component['value']
                                if form_component['name'] == '内存使用率' and 'value' in form_component.keys():
                                    RAM = form_component['value']
                                if form_component['name'] == '病毒库特征码版本号' and 'value' in form_component.keys():
                                    virusDB = form_component['value']
                                if form_component['name'] == '病毒库特征码照片' and 'value' in form_component.keys():
                                    virusDBphoto = form_component['value']
                                if form_component['name'] == 'CPU内存使用率照片' and 'value' in form_component.keys():
                                    CPUphoto = form_component['value']
                                if form_component['name'] == '["当前时间","当前地点"]' and 'value' in form_component.keys():
                                    presentTime = eval(form_component['value'])[0]
                                    presentSite = str(eval(form_component['value'])[1])+','+str(eval(form_component['value'])[2])+','+eval(form_component['value'])[3]

                            fileds = {
                                'approvalNumber': data_list['process_instance_id'],
                                'headline': data_list['title'],
                                'approvalStatus': 'COMPLETED',
                                'approvalResult': data_list['process_instance_result'],
                                'approvalTime': data_list['create_time'],
                                'approvalFinshTime': data_list['finish_time'],
                                'initiatorsNumber': None,
                                'initiatorsUserID': data_list['originator_userid'],
                                'initiatorsName': getName(data_list['title']),
                                'initiatorsDepartment': data_list['originator_dept_id'],
                                'historicalApproverName': str(data_list['approver_userid_list']['string']),
                                'approvalHistory': str(data_list['approver_userid_list']['string']),
                                'currentProcessingName': data_list['approver_userid_list']['string'][-1],
                                'reviewTake': duration(data_list['create_time'], data_list['finish_time']),  ##day
                                'highwaySection' : highwaySection,
                                'serverName' :serverName,
                                'CPU' : CPU,
                                'RAM' : RAM,
                                'virusDB' : virusDB,
                                'virusDBphoto':  virusDBphoto,
                                'CPUphoto' : CPUphoto,
                                'presentTime' : presentTime,
                                'presentSite' : presentSite
                            }

                            servercheck = Servercheck(**fileds)
                            mysession.merge(servercheck)  # 主鍵有存在也新增
                            mysession.commit()
                            mysession.close()
            else:
                logging.info('{} the request of {} has error.the process code is {} '.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),sys._getframe().f_code.co_name,process_code))

##路段工作日报
def insertDailyWorkReport(start_time,end_time,AccessToken):
    mysession = sessionmaker(bind=engine)()
    process_codes ={
      'PROC-FF6YLZF1N2-0RPIAV13T49FSPF50JJY1-430NSOZI-61'
    }
    for process_code in process_codes:
        cursor=0
        ##当返回结果没有该字段时表示没有更多数据了，没有该字段时设置为-1
        while cursor!=-1:
            response_data = getProcessinstanceList(AccessToken=AccessToken, process_code=process_code, start_time=start_time,end_time=end_time, cursor=cursor)
            if 'error_response' in response_data.keys():
                logging.info(response_data['error_response']['sub_msg'].encode('utf-8'))
                ##toeken後期設置，執行writetoken,再一次執行獲取數據
                writeAccessToken(corpid, corpsecret)
                AccessToken = getAccessToken()
                response_data = getProcessinstanceList(AccessToken=AccessToken, process_code=process_code,start_time=start_time, end_time=end_time, cursor=cursor)
            result_flag = response_data['dingtalk_smartwork_bpms_processinstance_list_response']['result']

            ##判断返回结果是否是成功的
            if result_flag['ding_open_errcode']==0:
                if 'next_cursor' not in result_flag['result'].keys():
                    ##设置cursor,如果不存在这个键值就设置为-1
                    cursor = -1
                else:
                    cursor = int(result_flag['result']['next_cursor'])

                ##list有数据
                if result_flag['result']['list']:
                   for data_list in result_flag['result']['list']['process_instance_top_vo']:

                       ##判断审批状态是否为成功
                        if data_list['status']=='COMPLETED':

                            ##定義字段

                            highwaySection = None
                            date = None
                            weather = None
                            temperature = None
                            rate = None
                            ratePhoto = None
                            workGoing = None
                            unfinshedWork = None
                            importantEvent = None
                            photo = None
                            accessory = None

                            for form_component in data_list['form_component_values']['form_component_value_vo']:

                                if 'name' in form_component.keys():
                                    if form_component['name'] == '路段' and 'value' in form_component.keys():
                                        highwaySection = form_component['value']
                                    if form_component['name'] == '日期' and 'value' in form_component.keys():
                                        date = form_component['value']
                                    if form_component['name'] == '天气' and 'value' in form_component.keys():
                                        weather = form_component['value']
                                    if form_component['name'] == '气温' and 'value' in form_component.keys():
                                        temperature = form_component['value']
                                    if form_component['name'] == '监控完好率' and 'value' in form_component.keys():
                                        rate = form_component['value']
                                    if form_component['name'] == '外场完好率图片' and 'value' in form_component.keys():
                                        ratePhoto = form_component['value']
                                    if form_component['name'] == '工作情况' and 'value' in form_component.keys():
                                        workGoing = form_component['value']
                                    if form_component['name'] == '未处理完成故障情况' and 'value' in form_component.keys():
                                        unfinshedWork = form_component['value']
                                    if form_component['name'] == '是否有重大事件发生' and 'value' in form_component.keys():
                                        importantEvent = form_component['value']
                                    if form_component['name'] == '图片' and 'value' in form_component.keys():
                                        photo = form_component['value']
                                    if form_component['name'] == '附件' and 'value' in form_component.keys():
                                        accessory = form_component['value']

                                fileds = {
                                    'approvalNumber': data_list['process_instance_id'],
                                    'headline': data_list['title'],
                                    'approvalStatus': 'COMPLETED',
                                    'approvalResult': data_list['process_instance_result'],
                                    'approvalTime': data_list['create_time'],
                                    'approvalFinishTime': data_list['finish_time'],
                                    'initiatorsNumber': None,
                                    'initiatorsUserID': data_list['originator_userid'],
                                    'initiatorsName': getName(data_list['title']),
                                    'initiatorsDepartment': data_list['originator_dept_id'],
                                    'historicalApproverName': str(data_list['approver_userid_list']['string']),
                                    'approverHistory': str(data_list['approver_userid_list']['string']),
                                    'currentProcessingName': data_list['approver_userid_list']['string'][-1],
                                    'reviewTake': duration(data_list['create_time'], data_list['finish_time']),  ##day
                                    'highwaySection' : highwaySection,
                                    'date' : date,
                                    'weather':weather,
                                    'temperature': temperature,
                                    'rate' :rate,
                                    'ratePhoto':ratePhoto,
                                    'workGoing' : workGoing,
                                    'unfinshedWork' : unfinshedWork,
                                    'importantEvent': importantEvent,
                                    'photo': photo,
                                    'accessory': accessory,
                                }

                                dailyworkreport = Dailyworkreport(**fileds)
                                mysession.merge(dailyworkreport)  # 主鍵有存在也新增
                                mysession.commit()
                                mysession.close()

                ##批量插入
            else:
                logging.info('{} the request of {} has error.the process code is {} '.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),sys._getframe().f_code.co_name,process_code))
