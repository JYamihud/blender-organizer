# -*- coding: utf-8 -*-

# system
import os


# THIS FILE HANDELS WRITTING AND READING OF PROJECT.DATA FILE.

# For sake of convinience of use. I will not use self.pf or pf in this file. 
# So be aware of it.


def  get(option):
    pf = os.getcwd()
    
    sf = open(pf+"/project.data", "r")
    for i in sf.read().split("\n"):
        
        if i.startswith(option):
            return i[i.find(':')+1:]
    
def save(option, value):
    
    
    
    if len(option) > 9:
        print "Value Too Long (longer then 9)"
        return
    
    pf = os.getcwd()
    
    value = str(value)
    
    sf = open(pf+"/project.data", "r")
    sf = sf.read().split("\n")
    
    wf = open(pf+"/project.data", "w")
    for i in sf:
        if ":" in i:
            
            if i.startswith(option):
                wf.write(option+" "*(9-len(option))+":"+value+"\n")
            else:
                wf.write(i+"\n")
    wf.close()
