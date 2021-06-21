from django.shortcuts import HttpResponse
import json
from datetime import datetime

def success(code, message, data):
    response_data = {}
    response_data["code"] = code
    response_data["message"] = message
    if data is not None:
        response_data["data"] = data
    response = HttpResponse(content=json.dumps(response_data, ensure_ascii=False),
                            content_type='application/json;charset = utf-8',
                            status='200',
                            reason='success',
                            charset='utf-8')
    return response


# 用户鉴权失败的返回
def tokenOutTime():
    response_data = {}
    response_data["code"] = 10000
    response_data["message"] = "鉴权信息过期，请重新登录"
    response_data["data"] = -101
    response = HttpResponse(content=json.dumps(response_data, ensure_ascii=False),
                            content_type='application/json;charset = utf-8',
                            status='200',
                            reason='success',
                            charset='utf-8')
    return response

#时间比较失败的返回
def timeJudge(time):
    request_time = datetime.strptime(time,'%Y-%m-%d %H:%M:%S')
    local_time = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
    difference=(local_time-request_time)
    if difference.days*24*60*60+difference.seconds<20:
        return True
    return False

def timeError():
    return success(0,"请设置正确的系统时间",None)


