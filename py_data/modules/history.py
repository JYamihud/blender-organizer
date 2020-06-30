# -*- coding: utf-8 -*-

# THIS FILE IS RESPONSIBLE FOR WRITTING AND READING HISTORY OF THE PROJECT


import os
import datetime


def write(pf, filename, action):
    
    
    if filename.startswith(pf):
        filename = filename[len(pf):]
    
    
    
    # GETTING THE DATE N TIME STRING CORRENTLY PUT TOGETHER
    
    y, m, d, h, n, s = int(datetime.datetime.now().year), int(datetime.datetime.now().month)-1, int(datetime.datetime.now().day), int(datetime.datetime.now().hour), int(datetime.datetime.now().minute), int(datetime.datetime.now().second)

    y, m, d, h, n, s = str(y), str(m+1), str(d), str(h), str(n) , str(s)
    if len(m) < 2:
        m = "0"+m
    if len(d) < 2:
        d = "0"+d
    if len(h) < 2:
        h = "0"+h
    if len(n) < 2:
        n = "0"+n
    if len(s) < 2:
        s = "0"+s
    
    
    newdate = y+"/"+m+"/"+d+" "+h+":"+n+":"+s


    print "HISTORY", newdate, filename, action
    
    
    #writting down the hystory
    
    # THIS IS GOING TO BE A LARGE F-ING FILE
    
    if not os.path.exists(pf+"/history.data"):
        f = open(pf+"/history.data", "w")
        f.write(newdate+" "+filename+" "+action)
        f.close()
    else:
        f = open(pf+"/history.data", "ab")
        f.write("\n"+newdate+" "+filename+" "+action)
        f.close()
    
    #cleaning unnesesary repetiotion
    
    f = open(pf+"/history.data", "r")
    f = f.read().split("\n")
    s = open(pf+"/history.data", "w")
    w = []
    for i in f:
        if i not in w and i != "":
            w.append(i)
            s.write(i+"\n")
    s.close()
