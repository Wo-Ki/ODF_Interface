"""
Created on Wed Jun 19 15:07:48 2019

@author: maoyingxue
"""
from flask import Flask, request
import json
from Interface import calType, calPoints, calGridInfo, predictPorts
import cv2
from ftplib import FTP
import numpy as np
app = Flask(__name__)


@app.route('/addr', methods=['POST'])
def getTypebyAddr():
    try:
        data = request.get_data().decode("utf-8")
        data = json.loads(data)
    except:
        return json.dumps({"error": "json format error!"})
    else:
        img = cv2.imread(data["addr"])
        #print(type(img))
        result = calType(img)
        sendData = json.dumps(result).encode("utf-8")
        return sendData


@app.route('/remoteaddr', methods=['POST'])
def getTypebyRemoteAddr():
    # try:
        data = request.get_data().decode("utf-8")
        data = json.loads(data)
        print(data)
        ftp = FTP()
        ftp.connect(data["ip"], data["port"])  # 连接的ftp sever和端口
        ftp.login(data["user"], data["password"])
        path = "image/1.jpg"
        file = open(data["addr"], "wb").write
        ftp.retrbinary(path, file)
        # img=cv2.imread(path)
    # except:
    #     return json.dumps({"error": "json format error!"})
    # else:
        result = calType(file)
        result["addr"] = path
        sendData = json.dumps(result).encode("utf-8")
        return sendData


@app.route('/filestream', methods=['POST'])
def getTypebyFileStream():
    try:
        # read image file string data
        filestr = request.files['file'].read()
        # convert string data to numpy array
        npimg = np.fromstring(filestr, np.uint8)
        # convert numpy array to image
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    except:
        return json.dumps({"error": "json format error!"})
    else:
        result = calType(img)
        # result["addr"] = path
        sendData = json.dumps(result).encode("utf-8")
        return sendData


@app.route('/points', methods=['POST'])
def getpoints():
    try:
        data = request.get_data().decode("utf-8")
        data = json.loads(data)
    except:
        return json.dumps({"error": "json format error!"})
    else:
        result = calPoints(data)
        sendData = json.dumps(result).encode("utf-8")
        return sendData


@app.route('/gridnums', methods=['POST'])
def getgridnums():
    try:
        data = request.get_data().decode("utf-8")
        data = json.loads(data)
    except:
        return json.dumps({"error": "json format error!"})
    else:
        result = calGridInfo(data)
        sendData = json.dumps(result).encode("utf-8")
        return sendData


@app.route('/ports', methods=['POST'])
def getports():
    try:
        data = request.get_data().decode("utf-8")
        data = json.loads(data)
    except:
        return json.dumps({"error": "json format error!"})
    else:
        result = predictPorts(data)
        sendData = json.dumps(result).encode("utf-8")
        return sendData


if __name__ == '__main__':
    app.run(debug=True)
