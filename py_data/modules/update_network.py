# -*- coding: utf-8 -*-

import os
import urllib2

print "Opening the link"


update_info = urllib2.urlopen("https://raw.githubusercontent.com/JYamihud/blender-organizer/master/update_info.data")
update_info = update_info.read()

stop = False

currentversion = open("update_info.data", "r")
currentversion =  currentversion.read().split("\n")[0]

getfiles = []

for i in update_info.split("\n"):
    
    if i == currentversion:
        break
        
    if i.startswith("MAIN_FILE"):
        if "MAIN_FILE" not in getfiles:
            getfiles.append("MAIN_FILE")
    if i.startswith("FILE"):
        if i[i.find(" ")+1:] not in getfiles:
            getfiles.append(i[i.find(" ")+1:])

savegetfiles = open("/tmp/blender-organizer-update-filesinfo.data", "w")
for i in getfiles:
    savegetfiles.write(i+"\n")
savegetfiles.close()





for i in update_info.split("\n"):
    if i.startswith("VERSION"):
        
        if stop:
            break
        else:
            stop = True
            
    print i
    
    if i.startswith("UPDATE PAGE "):
        
        print "PAGE"
        
        update_page = urllib2.urlopen(i[i.replace(" ", "_", 1).find(" ")+1:])
        update_page = update_page.read()
        
        mode = "normal"
        imgN = 0
        butN = 0
        but = ['" "', ""]
        for i in update_page.split("\n"):
            
            if mode == "normal":    
                
                if i not in ["<images>", "<button>"]:
                    print i
            
            elif mode == "images":
                
                if i.startswith("</images>"):
                    mode = "normal"
                    continue
                  
                imgN = imgN + 1
                
                image_file = urllib2.urlopen(i)
                image_name = "/tmp/ble_orga"+str(imgN)+i[i.rfind("."):]
                s = open(image_name, "w")
                s.write(image_file.read())
                s.close()
                
                print "<image> "+image_name
                
            elif mode == "button":
                
                if i.startswith("</button>"):
                    
                    print "<button> "+but[0], but[1]
                    
                    mode = "normal"
                    continue
                
                try:
                    but[butN] = i
                    butN = butN+1
                except:
                    pass
                    
                
            
            if i.startswith("<images>"):
                
                mode = "images"
            
            if i.startswith("<button>"):
                
                mode = "button"
                butN = 0
            
