'''
Author: your name
Date: 2021-11-11 10:32:12
LastEditTime: 2021-11-11 10:37:50
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: \csu_-rad\时间序列分割实验\getAbstractView.py
'''
'''
Author: your name
Date: 2021-11-11 10:11:54
LastEditTime: 2021-11-11 10:31:30
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: \csu_-rad\时间序列分割实验\getAbstractView.py
'''
from apps.BSSVA.baseConfig import UP,DOWN
'''
description: 获取时间段对应视图 三角形版本
param {全部的关键点数组} events
param {时间段字典 {sTime,eTime,view}} seg
return {添加view: 矩形4 空5 左三角3 右三角2} 
'''
def getAbstractView(events,seg):
    sTime = seg['sTime']
    eTime = seg['eTime']
    #记录有效angle
    angles = []
    #记录若为空或矩形时的状态
    state = -1
    for i in range(len(events)):
        if events[i]['angle'] == 0:
            continue
        if events[i]['time'] > eTime:
            if state == -1:
                state = 1 if events[i]['angle'] == DOWN else 0
            break
        elif events[i]['time'] == eTime:
            if events[i]['angle'] == DOWN:
                angles.append(events[i])
            if state == -1:
                state = 1 if events[i]['angle'] == DOWN else 0
            break
        elif events[i]['time'] <= sTime:
            #if events[i]['angle']!=0:
            state = 1 if events[i]['angle'] == UP else 0
            if events[i]['time'] == sTime and events[i]['angle'] == UP:
                angles.append(events[i])
        elif events[i]['time'] > sTime:
            angles.append(events[i])

    view = []
    #矩形4 空5 左三角3 右三角2
    #若是矩形或空
    if len(angles) == 0:
         view = [5,5] if state == 0 else [4,4]
    elif len(angles) == 1: #若是三角形+矩形的组合
        if angles[0]['angle'] == DOWN:
            view = [4,2]  #先矩形后右三角形
        else:
            view = [3,4] #先左三角形后矩形
    elif angles[0]['angle'] == angles[-1]['angle']: #若第一个和最后一个相同
        if angles[0]['angle'] == DOWN:
            view = [4,2,1]
        else:
            view = [3,4,1]
    elif angles[0]['angle'] == DOWN and angles[-1]['angle'] == UP:
        if len(angles) > 2:
            view = [2,3,1]
        else:
            view = [2,3]
    elif angles[0]['angle'] == UP and angles[-1]['angle'] == DOWN:
        if len(angles) > 2:
            view = [3,2,1]
        else:
            view = [3,2]
    seg['view'] = view
    seg['angles'] = angles
    mAnglePos = []
    for val in angles:
        mAnglePos.append(val['time'] - sTime)
    if len(mAnglePos)!=0:
        seg['mAnglePos'] = mAnglePos
