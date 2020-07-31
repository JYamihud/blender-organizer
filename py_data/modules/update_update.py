# -*- coding: utf-8 -*-

import os
import urllib2
import sys

# THIS PATH IS TO THE UPDATE RESPOSITORY 
path = "https://raw.githubusercontent.com/JYamihud/blender-organizer/master/"


l = open("/tmp/blender-organizer-update-filesinfo.data", "r")
l = l.read().split("\n")

amount = len(l)-1

for n, i in enumerate(l):
    
    try:
        if i == "MAIN_FILE":
            
            MAIN_FILE = open("MAIN_FILE")
            MAIN_FILE = MAIN_FILE.read()
            
            f = urllib2.urlopen(path+"blender-organizer.py")
            
            
            curfile = open(MAIN_FILE, "w")
            
            curfile.write( f.read() )
            curfile.close()
        
        
        if i != "MAIN_FILE":
            #print "UPDATE STRTING:  " + i
            
            f = urllib2.urlopen(path+i)
            
            
            curfile = open(i, "w")
            
            curfile.write( f.read() )
            curfile.close()
            
        print float(n) / amount
    except:
        pass



print "DONE" ### FORCING THE UPDATE WINDOW OT RESTAR ORGANIZER
