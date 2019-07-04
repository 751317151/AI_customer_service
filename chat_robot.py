#!/usr/bin/env python3
#-*- coding: utf-8 -*-


import urllib.request
import urllib.parse
import flask
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import parse_message
from wechatpy.replies import TextReply,ImageReply
import urllib     
from bs4 import BeautifulSoup
import random 

app = flask.Flask(__name__)

def get_robot_reply(msg):
    if "你叫什么"or"名字"or"你是谁" in msg.content:
        answer = "洋葱骑士"
    elif "小组编号" in msg.content:
        answer = "02"
    elif "小组成员" in msg.content:
        answer = "杨涵越（组长），华豪，邹鹏程，许金仓，张诚，王清洋，李书宽"
    elif "军事新闻" in msg.content:
        answer = NEWS() 
    else:    
        try:
            # 调用NLP接口实现智能回复
            params = urllib.parse.urlencode({'msg':msg.content}).encode()  # 接口参数需要进行URL编码
            req = urllib.request.Request("http://api.itmojun.com/chat_robot",params,method="POST")  # 创建请求
            answer = urllib.request.urlopen(req).read().decode()  # 调用接口(即向目标服务器发出HTTP请求，并获取服务器的响应数据)
            if answer == "":
                answer = "人家听不懂你在说什么"
        except Exception as e:
            answer = "AI机器人出现故障!(原因：%s)" % e    
    reply = TextReply(content='%s'% answer, message=msg)
    return reply.render()

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
    
    msg = parse_message(flask.request.data)
    if msg.type == "text":
        xml = get_robot_reply(msg)
    elif msg.type == "image":
        xml = image_reply(msg)

    if flask.request.method == "GET":
        return echostr
    elif flask.request.method == "POST":
        return xml

def NEWS():   
    page = urllib.request.urlopen('http://news.baidu.com/mil')   
    contents = page.read()     
    soup = BeautifulSoup(contents,"html.parser")  
    sc = soup.find_all('a', class_='title')
    
    i = ""
    j = 1
    for tag in sc:     
        m_name = tag.get_text() 
        m_url=tag.get("href")
        i += "%d"%j + "." + "<a href=" + "\"" + m_url + "\">" + m_name + "</a>" + "\n"
        j += 1
    return i 

def image_reply(msg):
    reply = ImageReply(message=msg)
    id = random.randint(0,7)

    if id == 0:
        reply.media_id = "3nZjDfLSZGG6pM1moOgVpiIxl77Ii501riZPHS7NdOY"
    elif id == 1:
        reply.media_id = "3nZjDfLSZGG6pM1moOgVpm4_XftO2zaJxsCO9KHOpZE"
    elif id == 2:
        reply.media_id = "3nZjDfLSZGG6pM1moOgVphls0UeRqcAHael9a_KTrM4"
    elif id == 3:
        reply.media_id = "3nZjDfLSZGG6pM1moOgVpteYUBCK3Evkc3YYnQcDf3E"
    elif id == 4:
        reply.media_id = "3nZjDfLSZGG6pM1moOgVppGMwQTVoaNRb5nQMIPYMmE"
    elif id == 5:
        reply.media_id = "3nZjDfLSZGG6pM1moOgVpp21QXwC-r14DremI0PdZjQ"
    elif id == 6:
        reply.media_id = "3nZjDfLSZGG6pM1moOgVpgWdPB8IBUo57Avk3Med_4k"
    else:
        k = msg.media_id
        reply.media_id = "%s"%k
    
    return reply.render()


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="80")
        