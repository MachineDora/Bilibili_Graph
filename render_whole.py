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
    # config the mongodb connection
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client.bilibili
    vv=db.ST

    node = list()
    for tag in vv.find():
        lis=tag['source']
        in_degree = len(lis)
        this_color = color_choose(in_degree)
        if in_degree==0:
            size=3
        else:
            size = int(math.sqrt(in_degree)*5)
        node.append({'name': tag['target'], 'symbolSize': size, 'itemStyle': {'color': this_color}})


    link = list()
    for relationship in vv.find():
        source = relationship['target']
        every_following = relationship['source']
        num_following = len(every_following)
        for i in range(num_following):
            link.append({'source': every_following[i], 'target': source})

    style = Style(
        title_color="#fff",
        title_pos="center",
        width=2760,
        height=1440,
        background_color='#404a59'

    )

    print(len(node))
    print(len(link))

    page = Page()
    chart = Graph("关系图", **style.init_style)
    chart.add("", node, link)
    page.add(chart)
    page.render()