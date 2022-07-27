from readData import temp_data
from apps.api.BSSVAPro import BSSVAPro
def ASTFDataPro(startTime,endTime,flag=False):
    return BSSVAPro(temp_data.df,temp_data.angleDf,startTime,endTime,temp_data.Signal_webStartFre,temp_data.Signal_webEndFre,temp_data.Signal_avgDict,temp_data,flag)
    