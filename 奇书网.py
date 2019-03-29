#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-
from myproxy.get_proxy import getip
from bs4 import BeautifulSoup
import requests
import random
import time

def getproxy():
    """
    获得一个代理IP和端口
    :return:
    """
    # path = 'ip.txt'  # 存放爬取ip的文档path
    # targeturl = 'http://www.cnblogs.com/TurboWay/'  # 验证ip有效性的指定url
    # getip(targeturl, path)

    with open('ip.txt', 'r') as r:
        proxylist = r.readlines()

        pro = random.choice(proxylist)[:-1]

        ProList = pro.split(',')

        ProDict = {ProList[1]: ProList[0]}
    return ProDict


def choseagent():
    """
    获得一个UserAgent
    :return:
    """
    user_agent_list = [
        {"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"},
        {"user-agent": "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11"},
        {"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6"},
        {"user-agent": "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6"},
        {"user-agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1"},
        {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5"},
        {"user-agent": "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5"},
        {"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3"},
        {"user-agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3"},
        {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3"},
        {"user-agent": "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3"},
        {"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3"},
        {"user-agent": "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3"},
        {"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3"},
        {"user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3"},
        {"user-agent": "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3"},
        {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"},
        {"user-agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"}
    ]
    OneUserAgent = random.choice(user_agent_list)

    return OneUserAgent



def gethtm():

    header, ProDict = getproxy(), choseagent()

    responce = requests.get('http://www.xiangcunxiaoshuo.la/html/183480/', headers=header, proxies=ProDict)

    responce.encoding = 'gbk'

    with open('a.html', 'w') as f:
        f.write(responce.text)

def getURL():
    urllist = []
    namelist = []
    with open('a.html', 'r') as f:
        htmlpage = f.read()

    soup = BeautifulSoup(htmlpage, features="html.parser")

    allatag = soup.select("a[href^='/html/183480/']")

    for i in range(13,len(allatag)):
        aurl = 'http://www.xiangcunxiaoshuo.la{}'.format(allatag[i].attrs['href'])
        name = allatag[i].attrs['title']
        namelist.append(name)
        urllist.append(aurl)
    return urllist, namelist



def gettext(urllist, namelist):

    bodytext = ''

    textname, texturl = namelist, urllist

    header, ProDict = getproxy(), choseagent()

    for i in range(len(textname)):

        responce = requests.get(texturl[i], headers=header, proxies=ProDict)

        responce.encoding = 'gbk'

        soup = BeautifulSoup(responce.text,  features="html.parser")

        bodytexts = soup.select(".yd_text2")

        for j in bodytexts:
            bodytext = j.text.replace('    ', '\n')
            print(bodytext)

        with open('修真聊天群.txt', 'a') as f:
            print('开始下载{}'.format(textname[i]))
            f.write(textname[i])
            f.write('\n')
            f.write(bodytext)
            f.write('\n')
            print(' ')
            time.sleep(1)


if __name__=="__main__":
    gethtm()
    namelist, urllist = getURL()
    gettext(namelist, urllist)