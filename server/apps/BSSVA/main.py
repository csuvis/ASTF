from apps.BSSVA.baseConfig import UP,DOWN
import copy
from apps.BSSVA.lossMeasure import lossMeasure
from apps.BSSVA.viewToState import transWebViews
events = None
def BSSVA_Init(tEvents):
    global events
    events = tEvents
def BSSVA_Start(events,MINNUM,MAXNUM):
    segs,target_list = BEETER_EquidDiv(events,MINNUM,MAXNUM)
    timeInters = getTimeInters(len(segs),events)
    #step2 进行合并
    error,segs = ObtainOptimalDivPoint(segs,timeInters)
    #step3 计算误差
    error,list_target = lossMeasure(events,segs,timeInters)
    baseTimeLines = []
    #equidSegs = []
    sTime = events[0]['time']
    eTime = events[0]['time']
    for i in range(len(timeInters)):
        eTime+=timeInters[i]
        baseTimeLines.append(sTime)
        sTime = eTime
    baseTimeLines.append(sTime)
    transWebViews(segs,error)
    return segs,baseTimeLines

'''
description: 等距分段
param {*} k  段数
return {*} segs
'''  
def EquidDivSegs(k,leftTime=0,rightTime=0):
    segs = []
    if leftTime == 0 and rightTime == 0:
        leftTime = events[0]['time']
        rightTime = events[-1]['time']
    timeInter = round((rightTime - leftTime)/k)
    timeInters = [timeInter for i in range(k)]
    newSum = timeInter*k - int(rightTime - leftTime)
    if newSum > 0:
        for i in range(newSum):
            timeInters[i] = timeInters[i]-1
    else:
        for i in range(abs(newSum)):
            timeInters[i] = timeInters[i]+1
    sTime = leftTime
    eTime = leftTime
    for i in range(k):
        eTime+=timeInters[i]
        segs.append({'sTime':sTime,'eTime':eTime})
        sTime = eTime
    return segs,timeInters
'''
description: 判断段内first和last是否有意义，即是否位于起始点和结束点
param {*} 
return {*}
'''
def makeSense(seg,index,length):
    isSense = [True,True]
    if index == 0:
        isSense[0] = False
    if index == length-1:
        isSense[1] = False
    if len(seg['angles']) == 1:
        if seg['angles'][0]['time'] == seg['sTime']:
            isSense[1] = False
        elif seg['angles'][0]['time'] == seg['eTime']:
            isSense[0] = False
    return isSense

def moveDiv(tsegs,index,pos):
    if pos == 0:
        if tsegs[index]['angles'][0]['angle'] == DOWN:
            tsegs[index-1]['eTime'] = tsegs[index]['angles'][0]['time']
            tsegs[index]['sTime'] = tsegs[index]['angles'][0]['time']
        elif tsegs[index]['angles'][0]['angle'] == UP:
            if tsegs[index]['angles'][0]['time']+1 == tsegs[index]['eTime']:
                return
            tsegs[index-1]['eTime'] = tsegs[index]['angles'][0]['time']+1
            tsegs[index]['sTime'] = tsegs[index]['angles'][0]['time']+1
    else:
        if tsegs[index]['angles'][-1]['angle'] == UP:
            tsegs[index+1]['sTime'] = tsegs[index]['angles'][-1]['time']
            tsegs[index]['eTime'] = tsegs[index]['angles'][-1]['time']
        elif tsegs[index]['angles'][-1]['angle'] == DOWN:
            if tsegs[index]['angles'][-1]['time']-1 == tsegs[index]['sTime']:
                return
            tsegs[index+1]['sTime'] = tsegs[index]['angles'][-1]['time']-1
            tsegs[index]['eTime'] = tsegs[index]['angles'][-1]['time']-1
'''
description: 偏移并计算误差
param {segs} 时间段
param {index} 哪个时间片
param {pos} 时间片的first 0 还是last 1 
return {误差}
'''
def computeMergeError(tsegs,index,pos,timeInters):
    #记录 用于后续复原
    my = copy.deepcopy(tsegs[index])
    pianIndex = index-1 if pos == 0 else index+1
    pianSeg = copy.deepcopy(tsegs[pianIndex])
    moveDiv(tsegs,index,pos)
    error,list_target = lossMeasure(events,tsegs,timeInters)
    # 恢复
    tsegs[pianIndex] = pianSeg
    tsegs[index] = my
    return error
'''
description: better中用于合并
param {*} 
return {*}
'''
def ObtainOptimalDivPoint(segs,timeInters):
    initError,list_target = lossMeasure(events,segs,timeInters)
    tsegs = segs
    while True:
        recordIndex = -1
        recordPos = -1
        curMinError = float('inf')
        length = len(tsegs)
        for index in range(length):
            if tsegs[index]['view'][0] == 5 and tsegs[index]['view'][1] == 5:
                continue
            if tsegs[index]['view'][0] == 4 and tsegs[index]['view'][1] == 4:
                continue
            isSense = makeSense(tsegs[index],index,length)
            if isSense[0] == True: #若左边状态变化点可以偏移
                curError = computeMergeError(tsegs,index,0,timeInters)
                if curError < curMinError:
                    curMinError = curError
                    recordIndex = index
                    recordPos = 0
            if isSense[1] == True: #若右边状态变化点可以偏移
                curError = computeMergeError(tsegs,index,1,timeInters)
                if curError < curMinError:
                    curMinError = curError
                    recordIndex = index
                    recordPos = 1
        if curMinError < initError:
            moveDiv(tsegs,recordIndex,recordPos)
            error,list_target = lossMeasure(events,tsegs,timeInters)
            initError = error
        else:
            break
    return initError,tsegs
    
def getTimeInters(segL,events):
    timeInter = round((events[-1]['time'] - events[0]['time'])/segL)
    timeInters = [timeInter for i in range(segL)]
    newSum = timeInter*segL - int(events[-1]['time'] - events[0]['time'])
    if newSum > 0:
        for i in range(newSum):
            timeInters[i] = timeInters[i]-1
    else:
        for i in range(abs(newSum)):
            timeInters[i] = timeInters[i]+1
    return timeInters
def EquidDivTarget(par):
    k = int(par[0])
    segs,timeInters = EquidDivSegs(k)
    error,list_target = lossMeasure(events,segs,timeInters)
    #print(error)
    return error
def BEETER_EquidDiv(events,MINNUM,MAXNUM,sliceNum=-1):
    #BSSVA_Init(events)
    minError = float('inf')
    n = sliceNum
    if MINNUM != None and MAXNUM != None:
        for curn in range(MINNUM,MAXNUM+1):
            error = EquidDivTarget([curn])
            if error < minError:
                n = curn
                minError = error

    segs,timeInters = EquidDivSegs(n)
    error,list_target = lossMeasure(events,segs,timeInters)
    return segs,list_target


