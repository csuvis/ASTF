import math
import time as ktime
import datetime
import pandas as pd
from settings import baseParam,baseParam
from apps.BSSVA.main import BSSVA_Start,EquidDivSegs,BSSVA_Init
idx = pd.IndexSlice
#频率摘要函数
#共有多少个时间片 
MIN_SLICES_NUMBER = 8
MEDIUM_SLICES_NUMBER = 15
MAX_SLICES_NUMBER = 15
#缓冲 某些情况无需重新进行时间片划分 只需判断异常即可
save = {}
curDataNum = 0
freRatio = 0
#是否将打印信息输出到文件中
DEBUG = False
DEBUG_LOG = False
TEST_ID = ["19961"]  #准备打印测试信号
def writeFile(file,log):
    if DEBUG == True:
        file.write(log+'\n')
def printLog(*log):
    if DEBUG_LOG == True:
        print(*log)
def get_signal(row):
    id = row[3]
    time = ktime.mktime(row[2].timetuple())
    state = row[4]
    freq = row[5]
    band = row[6]
    dbm = row[7]
    snr = row[8]
    angle = row[9]
    abFreq = row[10]
    abBand = row[11]
    abDbm = row[12]
    abSnr = row[13]
    return {
        'id':id,
        'time':time,
        'state':state,
        'freq':freq,
        'band':band,
        'dbm':dbm,
        'snr':snr,
        'angle':angle,
        'abFreq':abFreq,
        'abBand':abBand,
        'abDbm':abDbm,
        'abSnr':abSnr,
    }
def initSegsParam(segs):
    for i in range(len(segs)):
        # 时间片是否存在四种异常,提前算好
        segs[i]['abFreq'] = False
        segs[i]['abBand'] = False
        segs[i]['abDbm'] = False
        segs[i]['abSnr'] = False
        segs[i]['maxDbm'] = 0
        segs[i]['minDbm'] = 0
        segs[i]['avgDbm'] = 0
        segs[i]['maxSnr'] = 0
        segs[i]['minSnr'] = 0
        segs[i]['avgSnr'] = 0
def findExtentDbmSnr(extentDbmSnr,signal):
    if signal['state']!=2 and signal['freq']!=0 and signal['band']!=0:
        if signal['abDbm'] == False:
            extentDbmSnr[1] = max(extentDbmSnr[1],signal['dbm'])
            extentDbmSnr[0] = min(extentDbmSnr[0],signal['dbm'])
        if signal['abSnr'] == False:
            extentDbmSnr[3] = max(extentDbmSnr[3],signal['snr'])
            extentDbmSnr[2] = min(extentDbmSnr[2],signal['snr'])
def BSSVAPro(df,angleDf,startTime,endTime,startFre,endFre,avgDict,temp_data,flag=False):
    global curDataNum
    curDataNum = temp_data.dataSetNum #当前数据集
    global freRatio
    freRatio = baseParam[curDataNum]['freRatio']
    start = ktime.perf_counter()
    global save
    #时间片数量设置
    global MAX_SLICES_NUMBER,MIN_SLICES_NUMBER,MEDIUM_SLICES_NUMBER
    MAX_SLICES_NUMBER = baseParam[curDataNum]['maxNum']
    MIN_SLICES_NUMBER = baseParam[curDataNum]['minNum']
    MEDIUM_SLICES_NUMBER = baseParam[curDataNum]['mediumNum']
    print("时间片数量",MIN_SLICES_NUMBER,MAX_SLICES_NUMBER)
    abList = []
    if flag == 'true': #无需重新计算时间片划分
        period_result = save
    else: #重新计算时间片划分
        period_result = timeSliceDivision(angleDf,startTime,endTime,startFre,endFre,avgDict)
        save = period_result

    #return period_result['signal_dict']
    # 判断每个时间片内为何种信号
    signal_dict = period_result['signal_dict']
    idArray = period_result['idArray']
    pdStartTime = period_result['pdStartTime']
    pdEndTime = period_result['pdEndTime']
    resTrueStartTime = period_result['resTrueStartTime']
    extentDbmSnr = [
        float('inf'),float('-inf'),float('inf'),float('-inf')
    ]
    for key in signal_dict:
        signal = signal_dict[key]  #key为信号id 获取某一id的全部信号
        initSegsParam(signal['segs'])
    params = {}
    bases = {}
    # 1. 初始化计算参数
    for key in idArray:
        params[key] = init_param()
        bases[key] = init_base()
    tempDf = df.loc[resTrueStartTime,:]
    for row in tempDf.itertuples():
        id = row[3]
        if id not in idArray:
            continue
        signal = signal_dict[id] 
        temp = signal['segs'][0]
        if 'baseKind' not in temp:
            # other 全1或全0状态的信号
            temp_signal = get_signal(row)
            baseKind = 1
            if temp_signal['state']!=2:
                baseKind = 2
            else:
                baseKind = 1
            for i in range(len(signal['segs'])):
                signal['segs'][i]['baseKind'] = baseKind
    if True:
        # 2. 遍历数据
        # 3. 计算异常
        tempDf = df.loc[pdStartTime:pdEndTime,:]
        for row in tempDf.itertuples():
            id = row[3]
            if id not in idArray:
                continue
            if bases[id]['curSlice']+1 > len(signal_dict[id]['segs']):
                continue
            temp_signal = get_signal(row)
            time = temp_signal['time'] 
            state= temp_signal['state']
            # 全局 极大极小载噪比与电平 计算
            findExtentDbmSnr(extentDbmSnr,temp_signal)
            signal = signal_dict[id] 
            if state == 1:
                bases[id]['DutyHigh']+=1
            bases[id]['DutyAll']+=1
            if time>=signal['segs'][bases[id]['curSlice']]['sTime'] and time < signal['segs'][bases[id]['curSlice']]['eTime']:
                judgeThing(signal['segs'][bases[id]['curSlice']],temp_signal,params[id])
                #若是最后的数据： 直接结算
                if time == signal['trueEndTime']:
                    over(signal['segs'][bases[id]['curSlice']],params[id],bases[id],id)
            else:
                over(signal['segs'][bases[id]['curSlice']],params[id],bases[id],id)

                params[id] = init_param()
                bases[id]['curSlice']+=1
                if bases[id]['curSlice']+1 > len(signal['segs']):
                    continue
                #下一时间片的起始时间点
                if time>=signal['segs'][bases[id]['curSlice']]['sTime'] and time < signal['segs'][bases[id]['curSlice']]['eTime']:
                    judgeThing(signal['segs'][bases[id]['curSlice']],temp_signal,params[id])

    result = []
    
    for key in signal_dict:
        result.append({
            'id': key,
            'segs': signal_dict[key]['segs'],
            'baseTimeLines': signal_dict[key]['baseTimeLines'],
            'avgFre': signal_dict[key]['avgFre'],
            'avgBand': signal_dict[key]['avgBand'],
            'MaxBand': signal_dict[key]['MaxBand'],
            'avgDbm': avgDict[key]['avgDbm'],
            'avgSnr': avgDict[key]['avgSnr'],
        })
    result.sort(key=lambda x: x['avgFre']) 
    end = ktime.perf_counter()
    print("全部所需时间",(end-start),"min")
    if math.isinf(extentDbmSnr[1]) == True:
        extentDbmSnr[1] = temp_data.Signal_MaxDbm
    if math.isinf(extentDbmSnr[0]) == True:
        extentDbmSnr[0] = temp_data.Signal_MinDbm
    if math.isinf(extentDbmSnr[3]) == True:
        extentDbmSnr[3] = temp_data.Signal_MaxSnr
    if math.isinf(extentDbmSnr[2]) == True:
        extentDbmSnr[2] = temp_data.Signal_MinSnr  
    return {'data':result,'extentDbmSnr':extentDbmSnr}
    
'''
description: 时间片划分算法
param{angleDf}: angle数据集
param{startTime}：startTime: 刷选起始时间
param{endTime}：endTime: 刷选结束时间
param{startFre-endFre}: 刷选频率
param{}：avgDict: 信号基本内容
return {*}
'''
def timeSliceDivision(angleDf,startTime,endTime,startFre,endFre,avgDict):
    #print("时间片划分")
    #化简详细过程测试专用
    if DEBUG == True:
        ftest = open('./data/text.txt','w+',encoding='utf8')#指定写入编码为utf8，否则写入中文会乱码
    else:
        ftest = None

    result = {}   #最终结果存放
    start = ktime.perf_counter()
    #查询规定时间和频率范围的数据
    idArray = []
    startTime = int(startTime)
    endTime = int(endTime)
    pdStartTime = datetime.datetime.fromtimestamp(startTime)
    pdStartTime = pd.Timestamp(pdStartTime)
    pdEndTime = datetime.datetime.fromtimestamp(endTime)
    pdEndTime = pd.Timestamp(pdEndTime)
    resTrueStartTime = None
    resTrueEndTime = None
    print("效果内:",pdStartTime,pdEndTime)
    # 1. 刷选时间范围可能超出真实数据时间范围 因此需要更新测试
    # 2. 更新处于刷选频率范围内的信号
    for key in avgDict:
        if avgDict[key]['avgFre']>=startFre and avgDict[key]['avgFre']<=endFre:
            idArray.append(key)
            trueStartTime = startTime
            trueEndTime = endTime
            if startTime <= avgDict[key]['minTime']:
                trueStartTime = avgDict[key]['minTime']
            if endTime >= avgDict[key]['maxTime']:
                trueEndTime = avgDict[key]['maxTime']
            result[key] = {'avgFre':avgDict[key]['avgFre'],
                            'avgBand': avgDict[key]['avgBand'],
                            'MaxBand': avgDict[key]['MaxBand'],
                            'events':[],
                            'trueStartTime': trueStartTime,
                            'trueEndTime': trueEndTime,
            }
            resTrueStartTime = trueStartTime
            resTrueEndTime = trueEndTime
    resTrueStartTime = datetime.datetime.fromtimestamp(resTrueStartTime)
    resTrueStartTime = pd.Timestamp(resTrueStartTime)
    resTrueEndTime = datetime.datetime.fromtimestamp(resTrueEndTime)
    resTrueEndTime = pd.Timestamp(resTrueEndTime)
    # events创造
    queryAngleDf = angleDf.loc[pdStartTime:pdEndTime,:]
    #print(queryAngleDf.head())
    for row in queryAngleDf.itertuples():
        xtime = int(ktime.mktime(row[1].timetuple()))
        id = row[2]
        if id not in idArray:
            continue
        angle = row[3]
        if len(result[id]['events']) == 0:
            if xtime != result[id]['trueStartTime']:
                result[id]['events'].append({'time':result[id]['trueStartTime'],'angle':0})
        result[id]['events'].append({'time':xtime,'angle':angle})
    # 时间片划分方法
    for key in result:
        if len(result[key]['events']) != 0:
            BSSVA_Init(result[key]['events'])
            if result[key]['events'][-1]['time'] != result[key]['trueEndTime']:
                result[key]['events'].append({'time':result[key]['trueEndTime'],'angle':0})
            result[key]['segs'],result[key]['baseTimeLines'] = BSSVA_Start(result[key]['events'],MIN_SLICES_NUMBER,MAX_SLICES_NUMBER)
        else:
            result[key]['segs'],_ = EquidDivSegs(MEDIUM_SLICES_NUMBER,result[key]['trueStartTime'],result[key]['trueEndTime'])
            result[key]['baseTimeLines'] = []
            for i in range(len(result[key]['segs'])):
                result[key]['segs'][i]['error'] = 0

                result[key]['baseTimeLines'].append(result[key]['segs'][i]['sTime'])
            result[key]['baseTimeLines'].append(result[key]['segs'][-1]['eTime'])
    end = ktime.perf_counter()
    print("查询以及时间段分割所需要时间",(end-start),"s") 


    if DEBUG == True:
        ftest.close()
    return  {
            'signal_dict':result,
            'pdStartTime':pdStartTime,
            'pdEndTime':pdEndTime,
            'idArray':idArray,
            'resTrueStartTime':resTrueStartTime,
            'resTrueEndTime':resTrueEndTime,
            }  


def div(a,b):
    if b == 0:
        return 0
    else:
        return a/b
'''
description: 某个时间点异常判断
param{allAb}: 该信号是否为全局频率或带宽异常
param{timeCeilData}：该时间点对应的时间段字典
param{data}：该时间点的数据
param{param}: 该信号对应时间段的基本配置
param{information}：3std异常计算的相关参数
param{base}：3std异常计算的基本参数
return {*}
'''
def judgeThing(timeCeilData,data,param):
    # other 全1或全0状态的信号
    """     
    if 'baseKind' not in timeCeilData:
        if data['state']!=2:
            timeCeilData['baseKind'] = 2
            timeCeilData['error'] = 0
        else:
            timeCeilData['baseKind'] = 1
            timeCeilData['error'] = 0
    """
    #2. 记录当前时间段内的最大最小载噪比和电平
    if data['state']!=2 and data['freq']!=0:
        param['maxDbm'] = max(param['maxDbm'],data['dbm'])
        param['minDbm'] = min(param['minDbm'],data['dbm'])
        param['maxSnr'] = max(param['maxSnr'],data['snr'])
        param['minSnr'] = min(param['minSnr'],data['snr'])
        param['sumDbm']+= data['dbm']
        param['sumSnr']+= data['snr']
        param['dbmCnt']+= 1
        param['snrCnt']+= 1
    #3. 计算瞬时中断=状态出联但无频率/状态出联
    if data['state']!=2:
        #4. 判断干扰异常: 离群中心频率
        if timeCeilData['abFreq'] == False:
            timeCeilData['abFreq'] = data['abFreq']

        if timeCeilData['abBand'] == False:
            timeCeilData['abBand'] = data['abBand']

        if timeCeilData['abDbm'] == False:
            timeCeilData['abDbm'] = data['abDbm']

        if timeCeilData['abSnr'] == False:
            timeCeilData['abSnr'] = data['abSnr']
'''
description: 当前时间段遍历完毕 进行结算
param{timeCeilData}：该时间点对应的时间段字典
param{param}: 该信号对应时间段的基本配置
param{base}：3std异常计算的基本参数
return {*}
'''
def over(timeCeilData,param,base,id=None):

    #极值载噪比赋值
    timeCeilData['maxDbm'] = 'none' if math.isinf(param['maxDbm']) else param['maxDbm']
    timeCeilData['maxSnr'] = 'none' if math.isinf(param['maxSnr']) else param['maxSnr']
    timeCeilData['minDbm'] = 'none' if math.isinf(param['minDbm']) else param['minDbm']
    timeCeilData['minSnr'] = 'none' if math.isinf(param['minSnr']) else param['minSnr']
    #平均载噪比赋值 
    avgDbm = div(param['sumDbm'],param['dbmCnt'])
    avgSnr = div(param['sumSnr'],param['snrCnt'])
    timeCeilData['avgDbm'] = avgDbm
    timeCeilData['avgSnr'] = avgSnr
    
def init_param():
    param = {
            #'sumDbm': 0,'sumSnr':0,'dbmCnt':0,'snrCnt':0,
            'maxDbm':float('-inf'),'maxSnr':float('-inf'),'minDbm':float('inf'),'minSnr':float('inf'),
            'sumDbm':0,'sumSnr':0,'dbmCnt':0,'snrCnt':0
    }
    return param
def init_base():
    return {
        'curSlice':0,
        'DutyHigh':0,
        'DutyAll':0,
    }
# stdNum*std
# ratioNum*ratio
def judgeIsAb(kind,val,initAb,mean,nstd,nratio,stdNum,ratioNum=0):
    #先判断std
    absVal = abs(val-mean)
    stdAb = absVal>nstd
    if stdAb == False:
        return False
    ratioAb = True if nratio == 0 else absVal>nratio
    return ratioAb