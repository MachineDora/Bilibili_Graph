# -*- coding:utf-8 -*-

if __name__ == "__main__":

    count=open("D:\PY\GraphX\Rel\Rel_count.txt",'r',errors='ignore',encoding='utf-8')
    st = open("D:\PY\GraphX\Rel\S_T.txt", 'a', errors='ignore', encoding='utf-8')
    list=count.read().split('\n')
    list_new=[]
    count=0
    for j in list:
        count+=1
        if count==1:
            continue
        e=eval(j)
        n=e['all_count']
        if n>=10000:#当标签大于10000
            fl=n/125
        else:#小数量的标签
            fl=80
        rel=e['rel_count']
        key_list=[]
        for d in rel:
            if d['count']>=fl:
                key_list.append(d['tag'])
        s={
            'source':e['tag'],#将新的数据存入mongodb
            'target':key_list
        }
        list_new.append(s)
    leng=0

    for i in list_new:
        print(i)
        st.write(str(i))
        st.write('\n')
        print(len(i['target']))
        leng=leng+len(i['target'])
    print(leng)