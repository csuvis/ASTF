from apps.BSSVA.viewToState import transView
import numpy as np
'''
description: 获取关键点相对位置差值
description zz: 顺带计算vp1
description zz: 顺带计算新方法
kind = 0 老方法（弃用）
kind = 1 新方法（一对一）
kind = 2 新方法（一对多）
param {时间段字典} seg
return {*}
'''
def getSim_CD(seg,kind,tTime,leftTime):
    # print(seg)
    # if seg['view'] >= 4:
    #     return 0
    view = transView(seg['view'])
    vp1 = 0
    L = seg['eTime'] - seg['sTime'] if kind == 0 else tTime
    ab = 0
    if view == 5:
        vp1 = 0
    elif view == 4:
        vp1 = 1
    elif view == 3:
        if kind == 0:
            ab = abs(L*0.25-seg['mAnglePos'][0])
        elif kind == 1: 
            ab = abs(leftTime+L*0.25 - (seg['mAnglePos'][0] + seg['sTime']))
        else:
            abc = np.mean(seg['mAnglePos'][::2])
            ab = abs(leftTime+L*0.25 - (abc + seg['sTime']))
        vp1 = 0.75
    elif view == 2:
        if kind == 0:
            ab = abs(L*0.75-seg['mAnglePos'][0])
        elif kind == 1:
            ab = abs(leftTime+L*0.75 - (seg['mAnglePos'][0] + seg['sTime']))
        else:
            abc = np.mean(seg['mAnglePos'][::2])
            ab = abs(leftTime+L*0.75 - (abc + seg['sTime']))
        vp1 = 0.75
    elif view == 1 or view == 6:
        if kind == 0:
            ab = abs(L*0.25-seg['mAnglePos'][0]) + abs(L*0.75-seg['mAnglePos'][-1])
        elif kind == 1:
            ab = abs(leftTime+L*0.25  - (seg['mAnglePos'][0] + seg['sTime'])) + abs(leftTime+L*0.75 - (seg['mAnglePos'][-1] + seg['sTime']))
        else:
            abc1 = np.mean(seg['mAnglePos'][::2])
            abc2 = np.mean(seg['mAnglePos'][1::2])
            ab = abs(leftTime+L*0.25 - (abc1 + seg['sTime'])) + abs(leftTime+L*0.75 - (abc2 + seg['sTime']))
        vp1 = 0.5
    res = 0
    if ab == 0 or L == 0:
        res = 0
    else:
        # print("ab:",ab,L)
        res = ab/L if kind == 0 else ab
        #if kind == 1:
        #    print("计算",index,allStime+index*L+L*0.25,allStime+index*L+L*0.75,seg['mAnglePos'][0] + seg['sTime'],res)
    return res,vp1