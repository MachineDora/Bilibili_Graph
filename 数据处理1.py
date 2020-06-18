# -*- coding:utf-8 -*-
import pymongo


def get_main(main):
    main_tags = []

    mainl = main.read().split('\n')
    count = 0
    for m in mainl:
        count += 1
        if count == 1:
            continue
        main_tags.append(m.strip('(').strip(')').split(",")[0].strip('\''))

    return main_tags

def get_all(all):
    all_tags=[]

    alll = all.read().split('\n')
    coun = 0
    for a in alll:
        coun += 1
        if coun == 1:
            continue
        all_tags.append(a.strip('(').strip(')').split(",")[0].strip('\''))

    return all_tags

if __name__ == "__main__":

    main=open("D:\PY\GraphX\Rel\main_tags.txt",'r',errors='ignore',encoding='utf-8')
    all = open("D:\PY\GraphX\Rel\All_tags.txt", 'r', errors='ignore', encoding='utf-8')
    rel = open("D:\PY\GraphX\Rel\Rel_count.txt", 'a', errors='ignore', encoding='utf-8')
    main_tags=get_main(main)
    all_tags=get_all(all)

    list=[]

    for i in main_tags:
        dic={
            'tag':i,
            'all_count':0,
            'rel_count':[]
        }
        lll=dic['rel_count']
        for j in all_tags:
            if j==i:
                continue
            else:
                d={
                    'tag':j,
                    'count':0
                }
                lll.append(d)
        list.append(dic)

    client = pymongo.MongoClient(host='127.0.0.1', port=27017)
    db = client.bilibili
    v = db.videosAhead
    vv=db.tags

    c=0

    for tag in main_tags:#主要105标签
        c+=1
        print(c)
        for user in v.find().limit(100000):#100000条视频信息
            tags = user['key']
            for t in tags:#0-12每个视频的标签数
                if t==tag:
                    for l in list:#105如果标签里包含主要标签
                        if l['tag']==t:
                            list_count=l['rel_count']
                            for all in tags:#105
                                for dict in list_count:#备选的1000多个标签
                                    if dict['tag']==all:
                                        dict['count']+=1
                                        l['all_count']+=1


    for item in list:
        rel.write(str(item))
        rel.write('\n')



    #for item in list:
    #    s={
    #        'tag':item['tag'],
    #        'around':item['around']
    #    }
    #    vv.insert(s)



