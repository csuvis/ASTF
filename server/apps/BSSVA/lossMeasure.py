'''
Author: your name
Date: 2021-11-04 10:18:41
LastEditTime: 2021-11-11 13:52:42
LastEditors: Please set LastEditors
Description: 目标函数
FilePath: \CSU_RAD\lossMeasure.py
'''
import numpy as np
from apps.BSSVA.baseConfig import UP,DOWN
from apps.BSSVA.getAbstractView import getAbstractView
from apps.BSSVA.getSim_CD import getSim_CD
'''
description: 获取整体的出联时间比值（dp1）
param {全部的关键点数组} events
return {出联时间总长度} dp1
'''
def getDp1(events):
    dp1 = 0
    for index in range(len(events)-1):
        if index == 0:
            state = 1 if events[index+1]['angle'] == DOWN else 2
        else:
            state = 1 if events[index]['angle'] == UP else 2    
        if state == 1:
            dp1 += (events[index+1]['time'] - events[index]['time'])
    # print("outd",outd)
    # print("dp1",dp1)
    return dp1/(events[-1]['time'] - events[0]['time'])
'''
description: 误差度量
param {全部的关键点数组} events
param {时间段字典数组} segs
param {若默认值,则直接计算当前时间分段误差;若为元组,则先合并后计算误差} mergeIndex
return {返回多目标度量值} 
'''
def lossMeasure(events,segs,timeInters):
    tsegs = segs
    segs_l = []
    # 结果
    result_list = [0 for i in range(6)]
    sumOverAllRelaPos = 0
    sumVp1 = 0
    leftTime = events[0]['time']
    #1. 计算全局相对位置
    for i in range(len(tsegs)):
        getAbstractView(events,tsegs[i])
        tTime = timeInters[i]
        overAllRelaPos,singleVp1 = getSim_CD(tsegs[i],2,tTime,leftTime) #全局相对
        leftTime+=tTime
        sumOverAllRelaPos += overAllRelaPos
        sumVp1 += singleVp1
        segs_l.append(tsegs[i]['eTime']-tsegs[i]['sTime']) # 计算每一段的时间长度
    sumOverAllRelaPos = sumOverAllRelaPos/(events[-1]['time'] - events[0]['time'])
    result_list[5] = sumOverAllRelaPos
    #2 计算变异系统数
    std = np.std(segs_l)/np.mean(segs_l)
    result_list[0] = std
    #3 整体出联时间长度与视觉出联时间长度比值的差值
    dp1 = getDp1(events)
    vp1 = sumVp1 / len(tsegs)
    result_list[2] = abs(dp1-vp1)

    result = 0
    result = sum(result_list)
    return result,result_list
