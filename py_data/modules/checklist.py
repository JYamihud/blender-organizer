# -*- coding: utf-8 -*-


### THIS IS THE FILE THAT DEALS WITH ASSET.PROGRESS FILES
# It's core idea is to be able to manage checklist of the
# project asset by asset

# in the previous version, the checklist was constructed
# with a limitation of one indentation of a sub-task
# in this one I want to make sure people can make as many
# layers of subtaks as they need.

# also I will remove the not-needed X button and change it
# to simple deletion

# Importing stuff to make everything work

# system
import os
import socket

# graphics interface
import gtk
import pango
import cairo


### READ FILE ####


def openckecklist(filepath):
    
    # open file
    
    File = open(filepath, "r")
    File = File.read()
    # black placeholder for the checklist LIST
    checklist = ["[ ]"]

    for index, line in enumerate(File.split("\n")):
        
        if line.startswith("["):
            #every indentation is a list
            part = [line]
            indent = 0
            #recurcive method... running the function with in itself.
            def checkindent(part, indexb, indent):
                indentb = indent + 1
                for index, line in enumerate(File.split("\n")): 
                    if line.startswith("    "*indentb+"[") and index > indexb:
                        
                        
                        partb = [line[line.find("["):]]
                        partb = checkindent(partb, index, indentb) #here
                        part.append(partb)
                    
                    if line.startswith("    "*(indent)+"[") and index > indexb:
                        break
                
                return part

            part = checkindent(part, index, indent) # and here
            checklist.append(part)        
    return checklist # returning checklist

    
### GET THE FINAL FRACTION ###    

def partcalculate(part):
    
    fraction = 0.0
    
    if part[0].startswith("[V]"):
        fraction = 1.0
    
    
    else:
        for i in part[1:]:
            fraction = fraction + (partcalculate(i) / len(part[1:]))
            print i
            print fraction
    
    
    
    return fraction
    
#print partcalculate(openckecklist("test.progress"))



### CHECKLIST MANAGER WINDOW ###
# and finally we need a window editor for those graphs

def checkwindow(w=False, title="Checklist"):
    mainwin = gtk.Window()
    

