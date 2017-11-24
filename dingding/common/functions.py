from datetime import datetime
import re

def duration(start_time,end_time):
    a = datetime.strptime(str(start_time), "%Y-%m-%d %H:%M:%S")
    b = datetime.strptime(str(end_time), "%Y-%m-%d %H:%M:%S")
    return (b-a).days

def getName(title):
    try:
        name =  re.search('(\w+)的', title).group(1)
    except:
        name =None

def getAccsory(data):
    if 'value' in data:
        res = data['value']
    else:
        res = None
    return res

def getProjectName(data):
    if data['label'] == '项目名称':
        return data['value']
    elif data['label']=='设备名称':
        return data['value']
    else:
        return None

def getTradeMark(data):
    if data['label'] == '品牌':
        return data['value']
    else:
        return None

def getSpecificationModels(data):
    if data['label'] == '规格/型号':
        return data['value']
    else:
        return None

def getUnits(data):
    if data['label'] == '单位':
        return data['value']
    else:
        return None

def getAmount(data):
    if data['label'] == '数量':
        return data['value']
    else:
        return None

def getUnitPrice(data):
    if data['label'] == '单价（元）':
        return data['value']
    else:
        return None

def getTotalPrice(data):
    if data['label'] == '合计金额':
        return data['value']
    else:
        return None

def getStationName(data):
    if data['label'] == '站名':
        return data['value']
    else:
        return None

def getLaneNumber(data):
    if data['label'] == '车道号':
        return data['value']
    else:
        return None

def getUseLocation(data):
    if data['label'] == '使用位置':
        return data['value']
    else:
        return None

def getRemark(data):
    if data['label'] == '备注':
        return data['value']
    else:
        return None

def getPhoto(data):
    if data['label'] == '报送照片':
        return data['value']
    else:
        return None
