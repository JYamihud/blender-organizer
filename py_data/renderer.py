import os
infodata = open(os.getcwd()+"/py_data/renderinfo.data", "r")

info = infodata.read().split("\n")

blenderpath = info[1]
blendfile = info[0]
startframe = info[2]
frames = info[3]

print blenderpath
print blendfile
print startframe
print frames
print "\n\n"



try:
    int(frames), int(startframe)
except:
    print "frames should be numbers"
    exit()

import os
for i in range(int(startframe), int(frames)+1):

    os.system(blenderpath+" -b "+blendfile+" -f "+str(i))
