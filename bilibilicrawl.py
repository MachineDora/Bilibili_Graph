# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import time

from  concurrent import futures

import pymongo
import threading

result=0
client=pymongo.MongoClient(host='127.0.0.1',port=27017)
db=client.bilibili
v=db.videosAhead
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}

lock=threading.Lock()

def run(url):
    global  result
    req2 = requests.get(url[1], headers=headers)
    #req = requests.get(url[0], headers=headers, timeout=6).json()
    req2.encoding = "utf-8"
    html = req2.text
    soup = BeautifulSoup(html, 'html.parser')
    find = soup.find_all('h1')
    find2 = soup.find_all('li', class_='tag')
    find3 = soup.find_all('div', class_='video-data')
    find22 = []
    for m in range(0, len(find2)):
        find22.append(find2[m].text)
    time.sleep(0.1)  # 延迟，避免太快 ip 被封
    try:
        #data = req["data"]
        if find != []:
            s = {
                #'aid': url[0],  # 视频编号
                'time': find3[0].find_all('span')[1].get_text(),  # 视频发布时间
                'title': find[0]['title'],  # 视频标题
                #'view': data["view"],  # 播放量
                #'danmaku': data["danmaku"],  # 弹幕数
                #'reply': data["reply"],  # 评论数
                #'favorite': data["favorite"],  # 收藏数
                #'coin': data["coin"],  # 硬币数
                #'share': data["share"],  # 分享数
                'key': find22,  # 标签
            }
            print(s)
            with lock:
                if result % 100 == 0:
                    print(result)
                result += 1
    except:
        pass


if __name__ == "__main__":
    print("启动爬虫，开始爬取数据")
    for i in range(1, 127):
        begin = 26740000+100000*(i-1)
        urls = [
            (j,"https://www.bilibili.com/video/av{}".format(j))
            for j in range(begin, begin + 100000,50)
        ]
        with futures.ThreadPoolExecutor(64) as executor:
            executor.map(run, urls)
    print("爬虫结束，共为您爬取到 {} 条数据".format(result))