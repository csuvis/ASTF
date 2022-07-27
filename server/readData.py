import json
import time
import pandas as pd
#后端缓冲的数据 全部在此存放
class temp_data:
    df = {}
    angleDf = {}
    #当前数据集 
    dataSetNum = 0

    #需初始化 记录信号平均 与 信号mean std等
    Signal_avgDict = {}    #平均频率与带宽,key是信号id,value是{'avgFre':xxx,'avgBand':xxx}
    Signal_avgArray = []   #平均频率与带宽 以数组存储 给前端用


    #暂时可以不管 刷子没有指定最大最小频率时使用
    Signal_MaxFre = 0      #最大频率
    Signal_MinFre = float('inf') #最小频率
    Signal_MaxFre_band = 0
    Signal_MinFre_band = 0
    
    Signal_timeNumber = [] #时间刷子绘制所需

    #需初始化 后台全部数据的最小与最大 
    Signal_startTime = float('inf') 
    Signal_endTime = 0

    #无需初始化 记录前端所选定的时间和频率
    Signal_webStartTime = 0 
    Signal_webEndTime = 0
    Signal_webStartFre = 0 
    Signal_webEndFre = 0

    # 需初始化 用于刷选时间频率信号 无法求出最大最小dbm时使用
    Signal_MaxDbm = float('-inf')
    Signal_MinDbm = float('inf')
    Signal_MaxSnr = float('-inf')
    Signal_MinSnr = float('inf')

    #需初始化 时间-位置对应信息 方便快速查找
    Signal_time_cnt = {}  
    Signal_Max_pos = 0
    

class single_signal:
    def __init__(self):
        self.frameId = 0
        self.id = 0
        self.state = 0
        self.freq = 0.0
        self.band = 0.0
        self.snr=0
        self.dbm=0
        self.time=0
        self.angle = 0
        self.abFreq = False
        self.abBand = False
        self.abDbm = False
        self.abSnr = False
def initClass(): 
    #清空数据
    temp_data.Signal_avgDict = {}    #平均频率与带宽,key是信号id,value是{'avgFre':xxx,'avgBand':xxx}
    temp_data.Signal_avgArray = []   #平均频率与带宽 以数组存储 给前端用
    temp_data.Signal_MaxFre = 0      #最大频率
    temp_data.Signal_MinFre = float('inf') #最小频率

    # 用于刷选时间频率信号 无法求出最大最小dbm时使用
    temp_data.Signal_MaxDbm = float('-inf')
    temp_data.Signal_MinDbm = float('inf')
    temp_data.Signal_MaxSnr = float('-inf')
    temp_data.Signal_MinSnr = float('inf')

    #时间刷子绘制所需
    temp_data.Signal_timeNumber = [] 

    #后台全部数据的最小与最大
    temp_data.Signal_startTime = float('inf') 
    temp_data.Signal_endTime = 0

    #记录前端所选定的时间和频率
    temp_data.Signal_webStartTime = 0 
    temp_data.Signal_webEndTime = 0
    temp_data.Signal_webStartFre = 0 #前端一重频率所选定的时间
    temp_data.Signal_webEndFre = 0

    #需初始化 用于快速定位第几行
    temp_data.Signal_time_cnt = {}  #时间-位置对应信息 方便快速查找
    temp_data.Signal_Max_pos = 0



def readData(path):
    #单个信号的基本信息获取
    start = time.perf_counter()
    dataPath = path+'new_table.csv'
    jsonPath = path+'new_allInformation.json'
    informationPath = path+'new_information.csv'
    brushPath = path+'brushTime.csv'
    anglePath = path+'angleTime.csv'
    initClass()
    fim = pd.read_csv(informationPath)
    fim["id"] = fim["id"].astype("str")
    for data in fim.itertuples():
        temp_data.Signal_avgDict[data[1]] = {}
        temp_data.Signal_avgDict[data[1]]['id'] = data[1]

        temp_data.Signal_avgDict[data[1]]['MinBand'] = data[10]
        temp_data.Signal_avgDict[data[1]]['MaxBand'] = data[11]

        temp_data.Signal_avgDict[data[1]]['avgFre'] = data[12]
        temp_data.Signal_avgDict[data[1]]['avgBand'] = data[13]
        temp_data.Signal_avgDict[data[1]]['avgDbm'] = data[14]
        temp_data.Signal_avgDict[data[1]]['avgSnr'] = data[15]

        temp_data.Signal_avgDict[data[1]]['minTime'] = data[16]
        temp_data.Signal_avgDict[data[1]]['maxTime'] = data[17]
        temp_data.Signal_avgArray.append(temp_data.Signal_avgDict[data[1]]) 
    #angle分段信息
    temp_data.angleDf = pd.read_csv(anglePath)
    temp_data.angleDf["id"] = temp_data.angleDf["id"].astype("str")
    temp_data.angleDf['time'] = pd.to_datetime(temp_data.angleDf['time'])
    temp_data.angleDf.set_index("time",drop=False,inplace=True)
    temp_data.angleDf.sort_index(inplace=True)
    #整个信号的基本信息获取
    with open(jsonPath,'r',encoding='utf8') as fp:
        json_data = json.load(fp)
        temp_data.Signal_MaxFre = json_data['Signal_MaxFre']
        temp_data.Signal_MaxFre_band = json_data['Signal_MaxFre_band']
        temp_data.Signal_MinFre = json_data['Signal_MinFre']
        temp_data.Signal_MinFre_band = json_data['Signal_MinFre_band']
        temp_data.Signal_endTime = json_data['Signal_endTime']
        temp_data.Signal_startTime = json_data['Signal_startTime'] 
        temp_data.Signal_MaxDbm = json_data['Signal_MaxDbm'] 
        temp_data.Signal_MinDbm = json_data['Signal_MinDbm'] 
        temp_data.Signal_MaxSnr = json_data['Signal_MaxSnr'] 
        temp_data.Signal_MinSnr = json_data['Signal_MinSnr'] 
    #时间刷子获取
    brushF = pd.read_csv(brushPath)
    for row in brushF.itertuples():
        temp_data.Signal_timeNumber.append({'time':row[1],'cnt':row[2]})
    #全部信号获取
    temp_data.df = pd.read_csv(dataPath)
    temp_data.df['time'] = pd.to_datetime(temp_data.df['time'])
    temp_data.df["id"] = temp_data.df["id"].astype("str")
    temp_data.df.set_index("time",drop=False,inplace=True)
    temp_data.df.sort_index(inplace=True)

    end = time.perf_counter()
    print("初始化所需时间",(end-start)/60,"min")
