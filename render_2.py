# -*- coding:utf-8 -*-
import pymongo
from pyecharts.custom.page import Page
from pyecharts import Graph
from pyecharts import Style
import math

def color_choose(number):
    if number > 30:
        color = 'rgba(255,102,102,0.8)'
    elif number > 25:
        color = 'rgba(255,204,0,0.8)'
    elif number > 20:
        color = 'rgba(102,153,51,0.8)'
    elif number > 15:
        color = 'rgba(51,153,204,0.8)'
    elif number > 10:
        color = 'rgba(153,50,204,0.8)'
    elif number > 5:
        color = 'rgba(205,133,63,0.8)'
    else:
        color = 'rgba(204,204,204,0.8)'
    return color


if __name__ == "__main__":

    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client.bilibili
    vv = db.ST

    vpoint=open('D:\PY\GraphX\Rel\Vertex.txt','r',encoding='utf-8')
    l=vpoint.read().split("\n")

    list_v=[]

    count=0
    for i in l:
        count+=1
        if count==1:
            continue
        list_v.append(i.split(" "))

    rel2=open('D:\PY\GraphX\Rel\Rel2.txt','r',encoding='utf-8')
    list_r=rel2.read().split("\n")

    target_tag="英雄联盟"

    node = list()
    link = list()

    t_s=vv.find_one({'target': target_tag})
    indegree=len(t_s['source'])
    this_color = color_choose(indegree)
    tsize = int(math.sqrt(indegree) * 5)

    node.append({'name': target_tag, 'symbolSize': int(tsize),
                 'itemStyle': {'color': this_color}})

    flag=0
    following_list=[]
    for i in list_v:
        if i[1]==target_tag:
            flag=i[0]
    for j in list_r:
        j=eval(j)
        if j[0]==flag:
            following_list=j[1]
            break

    for sour in following_list:
        for ii in list_v:
            if ii[0]==sour:
                str=ii[1]
                if str==target_tag:
                    continue
                if str=='Fate/Grand':
                    str='Fate/Grand Order'
                foll_as_tar=vv.find_one({'target': str})
                indegree = len(foll_as_tar['source'])
                s_this_color = color_choose(indegree)
                if indegree == 0:
                    size = 3
                else:
                    size = int(math.sqrt(indegree) * 5)
                node.append({'name': str, 'symbolSize': int(size),
                 'itemStyle': {'color': s_this_color}})
                link.append({'source': target_tag, 'target': str})

    style = Style(
        title_color="#fff",
        title_pos="center",
        width=2760,
        height=1440,
        background_color='#404a59'

    )

    print(len(node))
    print(node)
    print(link)
    print(len(link))

    page = Page()
    chart = Graph("二度关系图", **style.init_style)
    chart.add("", node, link)
    page.add(chart)
    page.render()


