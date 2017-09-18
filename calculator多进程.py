#!/usr/bin/env python3

import argparse
from multiprocessing import Process,Queue

def jc1():
    args_file = argparse.ArgumentParser()
    args_file.add_argument("-c")
    args_file.add_argument("-d")
    args_file.add_argument("-o")
    
    args = args_file.parse_args()
    cfg = args.c
    user = args.d
    filegz = args.o
    user1 = open(user, 'r')
    User = user1.read()
    listuser = User.split('\n')
    listuser.remove('')
    splitlistuser = ','.join(listuser).split(',')
    listid = splitlistuser[::2]
    listshuiq = splitlistuser[1::2]
    t = []
    for i in listshuiq:
        t.append(int(i))
    listshuiq = t
    user1.close()
    
    cfg1  = open(cfg, 'r')
    diccfg = {}
    
    for line in cfg1:
        v = line.strip().split(' = ')
        diccfg[v[0]] = float(v[1])
    cfg1.close()
    quequeid.put(listid)
    quequeshuiq.put(listshuiq)
    quequecfg.put(diccfg)
    quequefile.put(filegz)

def jc2():
    listid = quequeid.get()
    listshuiq = quequeshuiq.get()
    diccfg = quequecfg.get()
    jieguo = []
    shebao = []
    geshui = []
    shuihou = []
    he = diccfg['YangLao'] + diccfg['YiLiao'] + diccfg['ShiYe'] + diccfg['GongShang'] + diccfg['ShengYu'] + diccfg['GongJiJin']
    for i in range(len(listshuiq)):
        if listshuiq[i] < diccfg['JiShuL']:
            shebao.append(diccfg['JiShuL'] * he)
        elif listshuiq[i] > diccfg['JiShuH']:
            shebao.append(diccfg['JiShuH'] * he)
        else:
            shebao.append(listshuiq[i] * he)
        b = listshuiq[i] - 3500
        d = listshuiq[i] - shebao[i] - 3500
        if b <= 0:
            c = 0
        elif b <= 1500:
            c = d * 0.03
        elif b <= 4500 and b > 1500:
            c = (d * 0.1) - 105
        elif b <= 9000 and b > 4500:
            c = (d * 0.2) - 555
        elif b <= 35000 and b > 9000:
            c = (d * 0.25) - 1005
        elif b <= 55000 and b > 35000:
            c = (d * 0.3) - 2755
        elif b <= 80000 and b > 55000:
            c = (d * 0.35) - 5505
        elif b > 80000:
            c = (d * 0.45) - 13505
        geshui.append(c)
        shuihou.append(listshuiq[i] - shebao[i] - geshui[i])
        jieguo.append('{},{},{:.2f},{:.2f},{:.2f}'.format((listid[i]),(listshuiq[i]),(shebao[i]),(geshui[i]),(shuihou[i])))
    quequejg.put(jieguo)
def jc3():
    file1 = quequefile.get()
    jg = quequejg.get()
    with open(file1, 'w') as file:
        for i in range(len(jg)):
            file.write(jg[i] + '\n')
def main():
    Process(target=jc1).start()
    Process(target=jc2).start()
    Process(target=jc3).start()
if  __name__ == '__main__':
    quequeid = Queue()
    quequeshuiq =Queue()
    quequecfg = Queue()
    quequefile = Queue()
    quequejg = Queue()
    main()
