# -*- coding:utf-8 -*-

if __name__ == "__main__":
    set=open("D:\PY\GraphX\Rel\word_set.txt",'r',errors='ignore',encoding='utf-8')
    st=open("D:\PY\GraphX\Rel\S_T.txt",'r',errors='ignore',encoding='utf-8')
    #ed=open("D:\PY\GraphX\Rel\Edge.txt",'a',errors='ignore',encoding='utf-8')
    ed = open("D:\PY\GraphX\Rel\Edge2.txt", 'a', errors='ignore', encoding='utf-8')
    ve = open("D:\PY\GraphX\Rel\Vertex.txt", 'a', errors='ignore', encoding='utf-8')
    list=set.read().split("\n")
    list_set=[]

    list2=st.read().split("\n")
    list2_set=[]

    count=0
    for i in list:
        count+=1
        if count==1:
            continue
        list_set.append(eval(i))

    #for v in list_set:
    #    ve.write(str(v[0])+" "+str(v[1]))
    #    ve.write("\n")

    count2 = 0
    for j in list2:
        num1=0
        num2=0
        count2 += 1
        if count2 == 1:
            continue
        e=eval(j)
        to=e['source']
        for ttt in list_set:
            if ttt[1]==to:
                num2=ttt[0]
        for tag in e['target']:
            for tt in list_set:
                if tt[1]==tag:
                    num1=tt[0]
                    list2_set.append(str(num2) + " " + str(num1))
    for r in list2_set:
        ed.write(str(r))
        ed.write("\n")


