# -*-coding:utf-8 -*-
#!usr/bin/env python3
import os,datetime,time,subprocess,shlex
from aip import AipSpeech
import urllib.request ,sys
import re
""" 你的 APPID AK SK """
APP_ID = '10714616'
API_KEY = 'BDshdq4YRaUBQMU9QSgjvgIW'
SECRET_KEY = '3dcc26a065b7b6a915c78b692bb89f9d'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

def get_weather():
    #provice = input('输入省份名（请使用拼音）：')
    #city = input('输入城市名（请使用拼音）：')
    #获取天气的url
    #url = "http://qq.ip138.com/weather/"+provice+'/'+city+'_7tian.htm'
    url = "http://qq.ip138.com/weather/sichuan/FuShun.htm"
       
    
    #获取页面信息
    weatherhtml = urllib.request.urlopen(url)
    res = weatherhtml.read().decode('GB2312')

    #将获取信息写入
   # f=open('wea.txt','wb')
   # f.write(res.encode('GB2312'))
   # f.close()

    #正则表达式获取天气信息
    pattern = 'Title.+<b>(.+)</b>'
    Title = re.search(pattern,res).group(1)

    pattern = '>(\d*-\d*-\d*.+?)<'
    date = re.findall(pattern,res)

    #pattern = 'alt="(.+?)"'
    pattern = '.\d℃～...'
    weather = re.findall(pattern,res)
    
    pattern='img src="/image/b\d\.gif".*"*td'
    weather2=re.findall(pattern,res)
    weatx=weather2[0].split('br/>')[1].split('</td')[0]
    weatx2=weather2[1].split('br/>')[1].split('</td')[0]
    weatx3=weather2[2].split('br/>')[1].split('</td')[0] 
    cur=datetime.datetime.now()
    #time_now = ''+cur.month+'-'+cur.day+'-'+cur.hour+'点'
    mins=cur.minute
    hours=cur.hour
    tm="富顺今天天气:" +weather[0]+','+weatx+'天 .'
    if hours>=16:
        tm=tm+"富顺明天天气:" +weather[1]+','+weatx2+'天 .'
    if hours>=20:
        tm="富顺明天天气:" +weather[1]+','+weatx2+'天.'+"后天天气:" +weather[2]+','+weatx3+'天 .'
    if hours in (10,12,15,20):
        tm=tm+"﻿﻿孩子他妈,喂娃儿维生素AD了吗,喂娃儿维生素AD了吗   ."
    if mins==0:
        time_now="%s月%s日%s点整"%(cur.month,cur.day,cur.hour)
    else:
        time_now="%s月%s日%s点%s分"%(cur.month,cur.day,cur.hour,mins)
        
    if hours in (10,12,13,16,21):
       url="http://www.fsxzf.gov.cn/-17"
       fsgov1=getfsgov(url)
       url="http://www.fsxzf.gov.cn/web/fsx/gzgg"
       fsgov2=getfsgov(url)
       if (len(fsgov1)>0 and len(fsgov2)>0):
           tm=tm+" 富顺县政府今天动态： "+fsgov1+","+fsgov2
       
    if hours in (7,8,9):
        t=getmryj()
        tm=tm+" 天天学英语： "+t
    if hours==22:
        tm=tm+"i am raspberrypi, Good night!"
        
    voicx='现在是:'+time_now+','+tm
    result  = client.synthesis(voicx, 'zh', 1, {
        'vol': 5,
    })
    print (voicx)
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open('weat.mp3', 'wb') as f:
            f.write(result)
    log = open(os.path.join(os.getcwd(), 'output.log'),'w+')
    com_line = 'mpv /home/pi/weat.mp3'
    #com_line = 'mpv /home/pi/Desktop/voice/weat.mp3'
    subprocess.call(shlex.split(com_line), stdout=log, stderr=log)

    
def getmryj():
    urle="http://dict.cn"
    whtm = urllib.request.urlopen(urle)
    resx = whtm.read().decode('UTF-8')
    #print (resx)
    pattern = 'cleardot.gif.*\s.*'
    textc = re.findall(pattern,resx)
    pattern = '\s\w.*\t'
    text2=re.findall(pattern,textc[0])
    text3=text2[0].replace("&nbsp;",",")
    return text3
    #print (text2)

def getfsgov(url):
    #url="http://www.fsxzf.gov.cn/-17"
    weatherhtml = urllib.request.urlopen(url)
    res = weatherhtml.read().decode('utf-8')
    pattern = 'white-space:nowrap;">(.*)</span></li>'
    cont = re.findall(pattern,res)
    curday=datetime.datetime.now().strftime('%Y-%m-%d')
    #print (curday)
    #curday="2018-03-01"
    retext=""
    for keysc in cont:
        pattern="^(.*)</a><span style=\"float:right\">\["+curday+"\]$"
        cont2=re.findall(pattern,keysc)
       # print (keysc)
        for keysc2 in cont2:
            retext=retext+','+keysc2
    return retext
    #print (retext)


if __name__=="__main__":
    #getmryj()
    get_weather()
