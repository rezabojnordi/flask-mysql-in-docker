#!flask/bin/python
from flask import Flask
#import mysql.connector
import os
from flask import jsonify,json,request
import socket
from time import time
import random

app = Flask(__name__)


#-------------------------------
def error_result(status,message):
    results={}
    results["error"]={}
    results["error"]["status"]=status
    results["error"]['message']=message
    return jsonify(results)


def success_result(status,message):
    results={}
    results["data"]={}
    results["data"]["status"]=status
    results["data"]['message']=message
    return jsonify(results)

def get_result(status,message):
    results={}
    results={}
    results["status"]=status
    results["data"]=message
    return jsonify(results)

#-------------------------------# return error_result("fail","insert error%s"%e) 

@app.route('/v1/change',methods=['GET'])
def change():

    b = {
        "a":32
    }
    return get_result("ok",b)


# def get_url():
#     #aya ghablan didam ya na
#     return {
#         time: "int",
#         pre_url: "",
#     }

# def get_token():
#     params = mac
#     if(mac_address):


#     return {
#         token:""
#     }
    




if __name__ == '__main__':
	app.run(host= '0.0.0.0',debug=True,port=80)