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
import glib

# self made modules
import dialogs



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
            #print i
            #print fraction
    
    
    
    return fraction
    
#print partcalculate(openckecklist("test.progress"))



### CHECKLIST MANAGER WINDOW ###
# and finally we need a window editor for those graphs

class checkwindow:
    def __init__(self, w=False, pf="/", title="Checklist", FILE=None):
        
        #saving all the input to SELF
        self.widget = w
        self.title = title
        self.FILE = FILE
        self.FILENAME = FILE
        
        self.LIST = openckecklist(self.FILE)
        self.mainpercent = partcalculate(self.LIST)
        
        self.open()
        
        
        self.pf = pf
        
        self.win = gtk.Window()
        self.win.set_title(self.title+"   "+FILE.replace(self.pf, ""))
        self.win.set_default_size(800,800)
        self.win.set_position(gtk.WIN_POS_CENTER)

        self.mainbox = gtk.VBox(False)
        self.win.add(self.mainbox)
        
        self.allowed = True #allowed to refresh frame
        
        # HELPERS
        
        self.dW = 0
        self.DH = 0
        
        self.mpx = 0
        self.mpy = 0
        self.mpf = 0
          
        self.offset = 0       
        
        ## ICONS
        
        self.ok = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/ok.png")
        self.plus = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/plus.png")
        self.delete = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/delete.png")
        self.move = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/move.png")
        self.edit = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/edit.png")
        
        # FOR GRAB FEATURE
        
        self.tool = "select"
        self.grab = 0
        self.grab_text = ""
        self.grabbed = False
        
        
        graph = gtk.DrawingArea()
        graph.set_size_request(500,700)
        
        self.mainbox.pack_start(graph)
        graph.connect("expose-event", self.framegraph) 
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        self.win.show_all()
    
    def open(self):
        self.FILE = open(self.FILENAME, "r")
        self.FILE = self.FILE.read().split("\n")
        
    def save(self):
        
        n = []
        
        for i in self.FILE:
            
            if i != "":  
                
                n.append(i)
        self.FILE = n
        
        
        save = open(self.FILENAME, "w")
        
        if self.FILE[-1] == "":
            self.FILE = self.FILE[:-1]
        
        for i in self.FILE:
        
            save.write(i+"\n")
        
        save.close()
    
    
    #### THIS FUNCTION DRAWS THE PIXELS IN THE WINDOW ####
    def framegraph(self, widget, event):
             
        
                                               
        w, h = widget.window.get_size()
        xgc = widget.window.new_gc()
        
        mx, my, fx  = widget.window.get_pointer()
        
        
        # GETTING WHETHER THE WINDOW IS ACTIVE
        
        self.winactive = self.win.is_active()
        
        ctx = widget.window.cairo_create()
        ctx.select_font_face("Monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        
        xgc.line_width = 2
        
        # BACKGROUND COLOR
        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#868686")) ## CHOSE COLOR
        widget.window.draw_rectangle(xgc, True, 0, 0, w, h)  ## FILL FRAME  
        
        
        
        #############################################################################
        ############################# DRAW HERE #####################################
        #############################################################################
        if self.tool == "select":
            widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.ARROW))
        elif self.tool == "grab":
            widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.FLEUR))
        if self.grabbed:
            self.tool = "select"
            self.grabbed = False
        if "GDK_BUTTON3" in str(fx) and "GDK_BUTTON3" not in str(self.mpf) and self.win.is_active():
            self.tool = "select"
        
        
        
        
        prevline = "[ ]"
        sofar = [False, 0]
        for ind, line in enumerate(self.FILE[9:]):
            
            
                
                
                
            
            if "[ ]" in line or "[V]" in line or "[v]" in line:
                
                
                # IF THIS TASK GRABBED
                xmove = line.find("[")*20
                ymove = ind*40+self.offset
                
                gpos = ((len(self.grab_text)*12)+35+35)
                
                if self.tool == "grab" and self.grab == ind:
                    
                    xmove = mx - gpos
                    ymove = my
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#7c7c7c")) ## CHOSE COLOR
                    widget.window.draw_rectangle(xgc, True, line.find("[")*20, ind*40+self.offset,  w, 39)
                    
                    widget.window.draw_rectangle(xgc, True, xmove, ymove,  w, 39)
                    
                
                
                # IF GRABBING IS ABOVE THIS TASK
                    
                if my in range(ind*40+self.offset, ind*40+self.offset+35) and self.tool == "grab":
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#5c5c5c")) ## CHOSE COLOR
                    widget.window.draw_rectangle(xgc, True, int(float(mx - gpos)/80)*80, ind*40+self.offset-7,  w, 5)
                    widget.window.draw_line(xgc, int(float(mx - gpos)/80)*80, 0, int(float(mx - gpos)/80)*80, h )
                    
                    
                    # IF RELESED
                    if "GDK_BUTTON1" not in str(fx) and "GDK_BUTTON1" in str(self.mpf) and self.win.is_active():
                        
                        self.FILE[self.grab+9] = "!!!DELETE!!!"
                        self.FILE.insert(ind+9, " "*((int(float(mx - gpos)/80)*80)/20)+self.grab_text)
                        self.FILE.remove("!!!DELETE!!!")
                        
                        # refrashing the file
                        self.save()
                        self.open()
                        
                        self.grabbed = True
                        
                    
                    
                if my in range(ind*40+self.offset, ind*40+self.offset+35) and self.tool == "select":
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#7c7c7c")) ## CHOSE COLOR
                    widget.window.draw_rectangle(xgc, True, xmove, ymove,  w, 39)
                    
                
                
                # IF IT ALREADY WAS CHECK OFF AT EARLIER STAGE
                
                if prevline.find("[") < line.find("["):
                    
                    if prevline[prevline.find("[")+1:].startswith("V") or prevline[prevline.find("[")+1:].startswith("v"): 
                        sofar = [True, line.find("[")]
                        
                if sofar[1] > line.find("["):
                    sofar = [False, line.find("[")]
                
                
                ctx.set_source_rgb(1,1,1)
                if sofar[0]:
                    ctx.set_source_rgb(0.6,1,0.6)
                ctx.set_font_size(20)
                
                
                
                ctx.move_to(  xmove+30, ymove+25)
                ctx.show_text(line[line.find("]")+1:])
                
                
                
                # CHECK BUTTON
                
                
                
                
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#5c5c5c")) ## CHOSE COLOR
                # IF MOUSE OVER
                if my in range(ind*40+5+self.offset, ind*40+5+self.offset+20) and mx in range(line.find("[")*20+5, line.find("[")*20+5+20) and self.tool == "select":
                    widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#e47649"))
                    
                    # IF CLICKED
                    if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active():
                        
                        put = "V"
                        if line[line.find("[")+1:].startswith("V") or line[line.find("[")+1:].startswith("v"):
                            put = " "
                            
                        
                         
                        self.FILE[ind+9] = line[:line.find("[")+1]+put+line[line.find("]"):]
                        
                        # refrashing the file
                        self.save()
                        self.open()
                    
                    
                    
                widget.window.draw_rectangle(xgc, True, xmove+5, ymove+5, 20, 20)
                
                
                if line[line.find("[")+1:].startswith("V") or line[line.find("[")+1:].startswith("v"):
                    
                    widget.window.draw_pixbuf(None, self.ok, 0, 0, xmove+7, ymove , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                
                
                # ADD SUBTASK
                
                
                if my in range(ind*40+5+self.offset, ind*40+5+self.offset+20) and mx in range(line.find("[")*20+(len(line[line.find("]")+1:])*12)+35, line.find("[")*20+(len(line[line.find("]")+1:])*12)+35+20) and self.tool == "select":
                    widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#e47649"))
                    widget.window.draw_rectangle(xgc, True, line.find("[")*20+(len(line[line.find("]")+1:])*12)+35, ind*40+5+self.offset-2, 22, 22)
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#5c5c5c"))
                    widget.window.draw_rectangle(xgc, True, line.find("[")*20+(len(line[line.find("]")+1:])*12)+35+30+35, ind*40+5+self.offset-2, 160, 30)
                    
                    
                    ctx.set_source_rgb(1,1,1)
                    ctx.set_font_size(20)
                    ctx.move_to(  line.find("[")*20+(len(line[line.find("]")+1:])*12)+35+35+35, ind*40+25+self.offset)
                    ctx.show_text("Add Subtask")
                    
                    
                    
                    # IF CLICKED
                    if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active():
                        
                        def ee(theline, line):
                                
                            Pname = ""
                            Pname = dialogs.PickName("New Subtask")
                            
                            
                            
                            
                            if Pname != "":
                                self.FILE.insert(theline+10,  line[:line.find("[")]+"    [ ] "+Pname)
                                
                                
                                # refrashing the file
                                self.save()
                                self.open()
                            
                            
                        
                        
                        glib.timeout_add(10, ee, ind, line)
                
                
                
                
                if self.tool == "select":
                    widget.window.draw_pixbuf(None, self.plus, 0, 0, line.find("[")*20+(len(line[line.find("]")+1:])*12)+35, ind*40+self.offset+5 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                    
                    
                # ACTIVATE GRAB BUTTON
                
                if my in range(ind*40+5+self.offset, ind*40+5+self.offset+20) and mx in range(line.find("[")*20+(len(line[line.find("]")+1:])*12)+35+35, line.find("[")*20+(len(line[line.find("]")+1:])*12)+35+20+35) and self.tool == "select":
                    widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.FLEUR))
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#e47649"))
                    widget.window.draw_rectangle(xgc, True, line.find("[")*20+(len(line[line.find("]")+1:])*12)+35+35, ind*40+5+self.offset-2, 22, 22)
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#5c5c5c"))
                    widget.window.draw_rectangle(xgc, True, line.find("[")*20+(len(line[line.find("]")+1:])*12)+35+30+35, ind*40+5+self.offset-2, 160, 30)
                    
                    
                    ctx.set_source_rgb(1,1,1)
                    ctx.set_font_size(20)
                    ctx.move_to(  line.find("[")*20+(len(line[line.find("]")+1:])*12)+35+35+35, ind*40+25+self.offset)
                    ctx.show_text("Move Task")
                    
                    # IF CLICKED
                    if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active():
                        
                        self.tool = "grab"
                        self.grab = ind
                        self.grab_text = line[line.find("["):]
                        
                        
                        
                if self.tool == "select":       
                    widget.window.draw_pixbuf(None, self.move, 0, 0, line.find("[")*20+(len(line[line.find("]")+1:])*12)+35+35, ind*40+self.offset+5 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                
                # EDIT TASK'S STRING
                
                
                if mx in range(line.find("[")*20+25,  line.find("[")*20+(len(line[line.find("]")+1:])*12)+35) and my in range(ind*40+self.offset+5, ind*40+self.offset+5+25):
                    widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.display_get_default(), self.edit, 1,20))
                    
                    #widget.window.draw_pixbuf(None, self.edit, 0, 0, mx-1, my-20 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                
                    
                    # IF CLICKED
                    if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active():
                        
                        def ee(ind, line):
                            newtext = dialogs.PickName(line[line.find("]")+1:])
                            
                            if newtext != "": # if returned something (if pressed ok and has text)
                                
                                
                                self.FILE[ind+9] = line[:line.find("]")+1]+newtext
                                
                                # refrashing the file
                                self.save()
                                self.open()
                                
                                
                            
                        glib.timeout_add(10, ee, ind, line)
                
                
                # DELETE TASK
                
                
                
                # IF MOUSE OVER
                if my in range(ind*40+5+self.offset, ind*40+5+self.offset+20) and mx in range(w-40, w-40+20) and self.tool == "select":
                    widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#e47649"))
                    widget.window.draw_rectangle(xgc, True, w-42, ind*40+5+self.offset-2, 22, 22)
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#5c5c5c"))
                    widget.window.draw_rectangle(xgc, True, w-210, ind*40+5+self.offset-2, 160, 30)
                    
                    
                    ctx.set_source_rgb(1,1,1)
                    ctx.set_font_size(20)
                    ctx.move_to(  w-200, ind*40+25+self.offset)
                    ctx.show_text("Delete Task")
                    
                    
                    
                    # IF CLICKED
                    if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active():
                        
                        del self.FILE[ind+9]
                
                        # refrashing the file
                        self.save()
                        self.open()
                        
                if self.tool == "select":
                    widget.window.draw_pixbuf(None, self.delete, 0, 0, w-40, ind*40+self.offset+5 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                
                
                
            
                
                
            prevline = line
        
            
            
            
            
            
        # ADD SUBTASK
                
                
        if my in range(ind*40+5+self.offset, ind*40+5+self.offset+20) and mx in range(line.find("[")*20+(len(line[line.find("]")+1:])*12)+35, line.find("[")*20+(len(line[line.find("]")+1:])*12)+35+20) and self.tool == "select":
            widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#e47649"))
            widget.window.draw_rectangle(xgc, True, line.find("[")*20+(len(line[line.find("]")+1:])*12)+35, ind*40+5+self.offset-2, 22, 22)
            
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#5c5c5c"))
            widget.window.draw_rectangle(xgc, True, line.find("[")*20+(len(line[line.find("]")+1:])*12)+35+30, ind*40+5+self.offset-2, 160, 30)
            
            
            ctx.set_source_rgb(1,1,1)
            ctx.set_font_size(20)
            ctx.move_to(  line.find("[")*20+(len(line[line.find("]")+1:])*12)+35+35, ind*40+25+self.offset)
            ctx.show_text("Add Task")
            
            
            
            # IF CLICKED
            if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active():
                
                def ee(theline, line):
                        
                    Pname = ""
                    Pname = dialogs.PickName("New Task")
                    
                    
                    
                    
                    if Pname != "":
                        self.FILE.append("[ ] "+Pname)
                        
                        
                        # refrashing the file
                        self.save()
                        self.open()
                    
                    
                
                
                glib.timeout_add(10, ee, ind, line)
        
        
        
        
        
        widget.window.draw_pixbuf(None, self.plus, 0, 0, line.find("[")*20+(len(line[line.find("]")+1:])*12)+35, ind*40+self.offset+5 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
        
        
        
    
        
        
        #SCROLL
        
        if self.mpy > my and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf) and self.win.is_active():
                    
            self.offset = self.offset + (my-self.mpy)
        
        if self.mpy < my and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf) and self.win.is_active():
                    
            self.offset = self.offset - (self.mpy-my)
        
        
        if self.offset < 0-(ind*40+40-h):
            self.offset = 0-(ind*40+40-h)
            
        if self.offset > 0:
            self.offset = 0
        
        
        
        
        
        #############################################################################
        ############################# UNTIL HERE ####################################
        #############################################################################
        
        
        
        # TESTING SOMETHING
        ctx.set_font_size(20)
        ctx.move_to( mx, my)
        #ctx.show_text(str(mx)+":"+str(my)+"  "+str(self.mainscroll)) 
        
        self.dW = w
        self.DH = h
        
        self.mpx = mx
        self.mpy = my
        self.mpf = fx
        
        
        
        def callback():
            if self.allowed == True:
                widget.queue_draw()

        glib.timeout_add(10, callback)
    
