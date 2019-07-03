#!/usr/bin/env python3
#-*- coding: utf-8 -*-


import urllib.request
import urllib.parse
import flask
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException


app = flask.Flask(__name__)

def get_robot_reply(question):
    '''
    函数功能：对于特定问题进行特定回复，对于非特定问题进行智能回复

    参数描述：
    question：聊天内容或问题

    返回值：str，回复内容
    '''
    '''
        if  "你叫什么名字" in question:
            answer = "我叫华豪"
        elif "你多少岁" in question:
            answer = "18"
        elif "你是GG还是MM" in question:
            answer = "你猜呢"
        else:
    '''
    try:
        # 调用NLP接口实现智能回复
        params = urllib.parse.urlencode({'msg':question}).encode()  # 接口参数需要进行URL编码
        req = urllib.request.Request("http://api.itmojun.com/chat_robot",params,method="POST")  # 创建请求
        answer = urllib.request.urlopen(req).read().decode()  # 调用接口(即向目标服务器发出HTTP请求，并获取服务器的响应数据)
    except Exception as e:
        answer = "AI机器人出现故障!(原因：%s)" % e    

    return answer

@app.route("/wx",methods=["GET","POST"])
def weixin_handler():
    token = "huahao"
    signature = flask.request.args.get("signature")
    timestamp = flask.request.args.get("timestamp")
    nonce = flask.request.args.get("nonce")
    echostr = flask.request.args.get("echostr")

    try:
        # 校验token
        check_signature(token, signature, timestamp, nonce)
    except InvalidSignatureException:
        # 处理异常情况或忽略
        flask.abort(403)  # 校验token失败，证明这条消息不是微信服务器发送过来的
    
    if flask.request.method == "GET":
        return echostr
    elif flask.request.method == "POST":
        print(flask.request.data)


if __name__ == '__main__':
    # # 测试get_robot_reply函数
    # while True:
    #     question = input("(输入(退出)即可退出聊天)我说： ")       
    #     if question == "退出":
    #         break
    #     answer = get_robot_reply(question)
    #     print("小魔仙说：%s"%answer)
    app.run(debug=True,host="0.0.0.0",port="80")
        