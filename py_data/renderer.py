import os
infodata = open(os.getcwd().replace("/py_data", "")+"/py_data/renderinfo.data", "r")

info = infodata.read().split("\n")



blendfile = info[0]
blenderpath = info[1]
destination = info[2]
extention = info[3]
startframe = info[4]
frames = info[5]






print blenderpath
print blendfile
print destination
print extention
print startframe
print frames
print "\n\n"



try:
    int(frames), int(startframe)
except:
    print "frames should be numbers"
    exit()

import os
import datetime
for i in range(int(startframe), int(frames)+1):
    
    startframetime = datetime.datetime.now()
    
    
    #### ACTUALL RENDER
    os.system(blenderpath+" -b "+blendfile+ " -o "+destination+"#### -F "+extention+" -f "+str(i))
    #### ENDS HERE
    
    
    
    endframetime = datetime.datetime.now()
    DELTA = endframetime - startframetime
    seconds = DELTA.seconds
    
    try:
        readfile = open(blendfile[:blendfile.rfind("/")]+"/renderspeed.data", "r")
        readfile = readfile.read()
    except:
        
        readfile = ""
    
    print blendfile[:blendfile.rfind("/")]+"/renderspeed.data"

    read = []
    for r in readfile[:-1].split("\n"):
        read.append(r)
    
    readfile = read
    
    
    foundframe = False
    for index, line in enumerate(readfile):
        if line.startswith(str(i)+" "):
            foundframe = True
            readfile[index] = str(i)+" "+str(seconds)
    if foundframe == False:
        readfile.append(str(i)+" "+str(seconds))
    
            
    
    
    writefile = open(blendfile[:blendfile.rfind("/")]+"/renderspeed.data", "w")
    for r in readfile:
        writefile.write(r+"\n")
    
    writefile.close()
    
    
    
    
    
    
    
