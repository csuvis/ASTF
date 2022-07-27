import json
import math
from flask import Blueprint, make_response, request
from readData import temp_data
from apps.api.ASTFDataPro import ASTFDataPro
from settings import dataPath,baseParam 
api_bp = Blueprint("api", __name__)
@api_bp.route("/get_brushInit",methods=['GET'])
def get_brushInit():
    step = float(request.args.get("freqStep"))
    step_time = int(request.args.get("timeStep")) 
    if any(baseParam[temp_data.dataSetNum]) == False:
        minFre = math.floor(temp_data.Signal_MinFre-temp_data.Signal_MinFre_band)
        maxFre = math.ceil(temp_data.Signal_MaxFre+temp_data.Signal_MaxFre_band)
    else:
        minFre = baseParam[temp_data.dataSetNum]['startFre']
        maxFre = baseParam[temp_data.dataSetNum]['endFre']
    print(minFre,maxFre)
    freqBrush = []
    freqStart = minFre
    freqEnd = minFre
    while True:
        freqEnd = freqEnd+step
        if freqEnd>maxFre:
            break
        else:
            freqBrush.append({'freq':freqStart,'cnt':0})
            freqBrush.append({'freq':freqEnd,'cnt':0})
        freqStart+=step
    if freqBrush[-1]['freq'] != maxFre:
        freqBrush.append({'freq':freqStart,'cnt':0})
        freqBrush.append({'freq':maxFre,'cnt':0})
    maxCnt = 0
    for item in temp_data.Signal_avgDict.values():
        #计算位于哪个区
        freq = item['avgFre']
        pos = math.ceil((freq-minFre)/step)
        #1--0 1;   2-- 2 3;  3-- 4 5;
        pos = (pos*2)-1
        freqBrush[pos]['cnt']+=1
        freqBrush[pos-1]['cnt']+=1
        maxCnt = max(maxCnt,freqBrush[pos]['cnt'])
    #计算时域统计图
    minTime = temp_data.Signal_startTime
    maxTime = temp_data.Signal_endTime
    timeBrush = []
    if step_time!= 1:
        timeStart = minTime
        timeEnd = minTime
        while True:
            timeEnd = timeStart + step_time
            if timeEnd > maxTime:
                break
            else:
                timeBrush.append({'time':timeStart,'cnt':0})
                timeBrush.append({'time':timeEnd,'cnt':0})
            timeStart+=step_time
        if timeBrush[-1]['time'] != maxTime:
            timeBrush.append({'time':timeStart,'cnt':0})
            timeBrush.append({'time':maxTime,'cnt':0})
        for item in temp_data.Signal_timeNumber:
            time = item['time']
            value = item['cnt']
            #计算该时间所在区域位置
            # [1\6) = [0\1]  [6\11) = [2\3]
            pos = math.floor((time-minTime)/step_time)
            pos = pos*2
            try:
                maxValue = timeBrush[pos]['cnt']
                maxValue = max(maxValue,value)
                timeBrush[pos]['cnt'] = maxValue
                timeBrush[pos+1]['cnt'] = maxValue
            except:
                print("******************")
                print(pos,time,value)
    else:
        timeBrush = temp_data.Signal_timeNumber
    result_data = {'timeBrush':timeBrush,#'freqBrush':temp_data.Signal_freqCeil,
    'freqBrush':freqBrush,
    'freqNumberMaxCnt':maxCnt,
    'maxTime':maxTime,'minTime':minTime,
    'maxFre':maxFre,'minFre':minFre,
    'dataSet':temp_data.dataSetNum}
    response = make_response(json.dumps(result_data))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response

#一重初始化 后端记录一重时间与一重频率  提供前端平均频率与带宽
@api_bp.route("/init",methods=['GET'])
def init():
    startTime = float(request.args.get("startTime")) #秒的版本
    endTime = float(request.args.get("endTime")) 
    startFre = float(request.args.get("startFre"))
    endFre= float(request.args.get("endFre"))

    temp_data.Signal_webStartTime = startTime
    temp_data.Signal_webEndTime = endTime
    temp_data.Signal_webStartFre = startFre
    temp_data.Signal_webEndFre = endFre
    result_data = {}
    maxBand = 0
    minBand = float('inf')
    result_data['avg'] = []
    for item in temp_data.Signal_avgArray:
        if item['avgFre']>=startFre and item['avgFre']<=endFre:
            minBand = min(item['MinBand'],minBand)
            maxBand = max(item['MaxBand'],maxBand)
            result_data['avg'].append(item)
    result_data['extent'] = {'MaxFre':temp_data.Signal_MaxFre,'MinFre':temp_data.Signal_MinFre,
                            'startTime':temp_data.Signal_startTime,'endTime':temp_data.Signal_endTime,
                            'MinBand':minBand,'MaxBand':maxBand}
    response = make_response(json.dumps(result_data))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response
#二重时间选择
@api_bp.route("/getASTFData",methods=['GET','POST'])
def getASTFData():
    startTime = request.args.get("startTime")
    endTime = request.args.get("endTime")
    flag = request.args.get("flag")
    if flag == None:
        flag = False
    if startTime == None:
        startTime = temp_data.Signal_webStartTime
        endTime = temp_data.Signal_webEndTime
    else:
        startTime = float(startTime)
        endTime = float(endTime)
    result_data =ASTFDataPro(startTime,endTime,flag)
    response = make_response(json.dumps(result_data))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = "POST, GET, PUT, OPTIONS, DELETE"
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response



def judgeBei(data,init):
    if data == None:
        return init
    else:
        return float(data)