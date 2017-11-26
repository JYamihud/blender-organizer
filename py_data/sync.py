

b = ""

def cls():
    import os
    os.system("clear")

import time
import socket
import os
import commands
import random
import threading
import random

# Opening settings

settings = open(os.getcwd().replace("/py_data", "")+"/py_data/sync.data", "r")
settings = settings.read()

print "SETTINGS:"
print
print "JYExchange : "+settings.split("\n")[0]
print "Missing    : "+settings.split("\n")[1]
print "Larger     : "+settings.split("\n")[2]
print "Smaller    : "+settings.split("\n")[3]
print "Codename   : "+settings.split("\n")[4]
print "Save Log   : "+settings.split("\n")[5]
print "Close JYE  : "+settings.split("\n")[6]

time.sleep(1)

print 
print "SYNC STAGE 1: Looking up existing files / folders"

# broadcasting the computer

tosend = True
keeprecv = True
undone = True

walk = os.walk(os.getcwd().replace("/py_data", ""))
tmpwalk = []
for i in walk:
    tmpwalk.append(i)

walk = tmpwalk

ourdirlist = ""
ourfilelist = ""

for p in walk:
    ourdirlist = ourdirlist+"\n"+p[0]
    
    for f in p[-1]:
        ourfilelist = ourfilelist+"\n"+p[0]+"/"+f
    
ourdirlist = ourdirlist[1:]
ourfilelist = ourfilelist[1:]

# adding the filesizes in the end of the files list

tmpfiles = ourfilelist
ourfilelist = ""
for i in tmpfiles.split("\n"):
    
    ourfilelist = ourfilelist + "\n" + i + " " + str(os.path.getsize(i))




theirdirlist = ""
theirfilelist = ""

for p in ourdirlist.split("\n"):
    theirdirlist = theirdirlist +"\n"+ p[ourdirlist.split("\n")[0].rfind("/"):]

for p in ourfilelist.split("\n"):
    theirfilelist = theirfilelist +"\n"+ p[ourdirlist.split("\n")[0].rfind("/"):]



print "SYNC STAGE 2: Waiting for the other computer..."

def broadcasting():
    
    
    bc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    bc.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    
    while tosend:
        ourip = commands.getoutput("hostname -I")
        time.sleep(1)
        bc.sendto("ORG.PY SYNC: ["+settings.split("\n")[4]+"] ("+ourip+")", ("255.255.255.255", 45454))
    
    
def recvievingbcast():
    
    ip = "255.255.255.255"
    port = 45454
    
    rec = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #rec.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    rec.bind((ip, port))
    
    while keeprecv:
        
        data, addr = rec.recvfrom(1024)
        
        if commands.getoutput("hostname -I") not in data:
        
            #print  data
            
            client = socket.socket()
            
            global keeprecv
            keeprecv = False
            
            
            try:
                client.connect((addr[0], 45454))
                
                
                
                
                # THE FOLDER LIST SEND
                client.send(str(len(theirdirlist)))
                client.recv(1024)
                client.send(theirdirlist)
                # THE FILE LIST SEND
                client.recv(1024)
                client.send(str(len(theirfilelist)))
                client.recv(1024)
                client.send(theirfilelist)
                
                #THE NEED FILES LIST SEND
                
                while waitforneed:
                    pass
                
                print "SYNC STAGE 5: Creating JYExchange Script and starting synchronization"
                
                global need
                need = need[1:]
                
                
                r = client.recv(1024)
                if r == "need":
                    client.send(str(len(need)))
                    client.recv(1024)
                    client.send(need)
                
                # CREATING a script
                
                while waitfortheireneed:
                    pass
                
                
                r = client.recv(1024)
                if r == "name":
                    
                    client.send(ourname)
                    
                
                ##### WRITTING
                
                while waitforname:
                    pass
                
                script = open(os.getcwd().replace("/py_data", "")+"/py_data/sync.jyes", "w") 
                
                
                for i in theirneed.split("\n"):
                    script.write("ADD: "+os.getcwd().replace("/py_data", "")+i+"\n")
                
                script.write("BNAME: "+ourname+"\n")
                script.write("WAIT FOR: "+theirname+"\n")
                script.write("CONNECT TO: "+theirname+"\n")
                
                for x, i in enumerate(need.split("\n")):
                    script.write("DESTINATION: "+os.getcwd().replace("/py_data", "")+i[:i.rfind("/")]+"\n")
                    script.write("GET: "+str(x+1)+"\n")
                
                if settings.split("\n")[5] == "True":
                    try:
                        os.mkdir(os.getcwd().replace("/py_data", "")+"/py_data/jyelogs")
                    except:
                        pass
                    script.write("SAVE TO: "+os.getcwd().replace("/py_data", "")+"/py_data/jyelogs"+"\n")
                
                if settings.split("\n")[6] == "True":
                    script.write("EXIT")
                
                script.close()
                
                shfix = open(os.getcwd().replace("/py_data", "")+"/py_data/last_command.sh", "w")
                shfix.write("cd "+settings.split("\n")[0][:settings.split("\n")[0].rfind("/")]+"\n")
                shfix.write("python2 jyexchange.py "+os.getcwd().replace("/py_data", "")+"/py_data/sync.jyes")
                shfix.close()
                
                os.system("sh "+os.getcwd().replace("/py_data", "")+"/py_data/last_command.sh")
                
                
                ssave = open(os.getcwd().replace("/py_data", "")+"/py_data/sync.data", "w")
                ssave.write(settings)
                ssave.close()
                
            except:
                print "Failed to Connect"
                raise
                
waitforneed = True
need = ""    
waitfortheireneed = True
theirneed = ""
rndstr = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"

waitforname = True
ourname = ""
for i in range(10):
    ourname = ourname + random.choice(rndstr)
#print "OURNAME ", ourname
theirname = ""

            
def server():
    
    ser = socket.socket()
    
    ser.bind(("", 45454))
    ser.listen(1)
    
    c, addr = ser.accept()
    
    global tosend
    tosend = False
    
    print "SYNC STAGE 3: Creating missing folders"
        
    r = c.recv(1024)
    
    
    
    c.send("OK")
    
    theirdir = ""
    
    while len(theirdir) < int(r):
    
        theirdir = theirdir + c.recv(1024)
    
    leng = len(theirdir.split("\n"))
    
    for x, i in enumerate(theirdir.split("\n")):
        
        
        
        if i not in theirdirlist.split("\n"):
            print "           "+i[i[1:].find("/")+1:]
            
            try:
                os.mkdir(os.getcwd().replace("/py_data", "")+i[i[1:].find("/")+1:])
            except:
                print "FOLDER CANNOT BE MADE"
                raise
    
    c.send("OK")
    
    r = c.recv(1024)
    
    
    
    c.send("OK")
    
    theirfile = ""
    
    print "SYNC STAGE 4: Creating a list of needed files"
    print "MIGT TAKE COULPE MINUTES DEPENDING ON THE SPEED OF THE MACHINE"
    
    while len(theirfile) < int(r):
        
        theirfile = theirfile + c.recv(1024)       
    
    
    emptyflist = ""
    for b in theirfilelist.split("\n"):
        emptyflist = emptyflist + "\n" + b[:b.rfind(" ")]
    
    
    
    global need
    global b
    
    #b = ""
    mis = 0
    lar = 0
    sma = 0
    
    leng = len(theirfile.split("\n"))
    for x, i in enumerate(theirfile.split("\n")):
        
        #cls()
        #print "SEARCHING FILE: "+ str(x) + " OF " + str(leng) + "  " + str(int((float(x)/leng)*100))+"%" + "\nMissing - "+str(mis)\
        #+ "   |    Larger - "+str(lar)+ "   |    Smaller - " + str(sma)
        #print b
        
        
        if i[:i.rfind(" ")] not in emptyflist.split("\n") and settings.split("\n")[1] == "True":
            
            need = need + "\n" + i[:i.rfind(" ")][i[1:].find("/")+1:]
            print "           Missing "+ i[:i.rfind(" ")][i[1:].find("/")+1:]
            mis = mis +1
            
        else:
        
            for b in theirfilelist.split("\n"):
                
                
                
                if i[:i.rfind(" ")] == b[:b.rfind(" ")] and i is not "":
                    
                    
                    
                    
                    # LARGER
                    if settings.split("\n")[2] == "True" and int(i.split(" ")[-1]) > int(b.split(" ")[-1]):
                        
                        need = need + "\n" + i[:i.rfind(" ")][i[1:].find("/")+1:]
                        print "           Larger "+ i[:i.rfind(" ")][i[1:].find("/")+1:]
                        lar = lar +1
                        
                    # smaller
                    elif settings.split("\n")[3] == "True" and int(i.split(" ")[-1]) < int(b.split(" ")[-1]):
                        
                        need = need + "\n" + i[:i.rfind(" ")][i[1:].find("/")+1:]
                        print "           Smaller "+ i[:i.rfind(" ")][i[1:].find("/")+1:]
                        
                        sma = sma + 1
    global waitforneed
    waitforneed = False
    
    c.send("need")
    
    r = c.recv(1024)
    
    
    
    c.send("OK")
    
    global theirneed
    
    
    
    while len(theirneed) < int(r):
        
        theirneed = theirneed + c.recv(1024)
        
    global waitfortheireneed
    waitfortheireneed = False
    
    c.send("name")
    global theirname   
    theirname = c.recv(1024)
    
    global waitforname
    waitforname = False
    

bct = threading.Thread(target=broadcasting, args=())
bct.start()

reb = threading.Thread(target=recvievingbcast, args=())
reb.start()


se = threading.Thread(target=server, args=())
se.start()

#while undone:
#    pass









