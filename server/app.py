import json 
from flask import request,make_response
from readData import readData,temp_data
from apps import create_app
from settings import dataPath
app = create_app()
@app.route("/upDataSet",methods=['GET'])
def upDataSet():
    dataSetNum = int(request.args.get("dataSetNum")) #数据集编号
    temp_data.dataSetNum = dataSetNum
    readData(dataPath[dataSetNum]['path'])
    response = make_response(json.dumps("success"))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response

if __name__ == '__main__':
    readData(dataPath[temp_data.dataSetNum]['path'])  #此函数会将数据全部读取缓存下来,缓存到一个类当中
    app.run(threaded=True,port=4900)
