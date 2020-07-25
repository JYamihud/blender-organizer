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
import datetime

import itemselector

# self made modules
import dialogs
import history


### READ FILE ####


def openckecklist(filepath, rang=[9,-1], minus=0):
    
    # open file
    
    File = open(filepath, "r")
    File = File.read()
    # black placeholder for the checklist LIST
    checklist = ["[ ]"]
    
    if rang[1] == -1:
        rang[1] = len(File.split("\n"))+1


    for index, line in enumerate(File.split("\n")):
        
        line = line[minus:]
        
        if line.startswith("[") and index in range(rang[0],rang[1]) and line[line.find("]")+2] != "#":
            #every indentation is a list
            part = [line]
            indent = minus/4
            #recurcive method... running the function with in itself.
            def checkindent(part, indexb, indent, minus):
                indentb = indent + 1
                for index, line in enumerate(File.split("\n")): 
                    if line.startswith("    "*indentb+"[") and index > indexb:# and index in range(rang[0],rang[1]):
                        
                        #line = line[minus:]
                        partb = [line[line.find("["):]]
                        partb = checkindent(partb, index, indentb, minus) #here
                        
                        if partb[0][partb[0].find("]")+2] != "#":
                            part.append(partb)
                    if line.startswith("    "*(indent)+"[") and index > indexb:
                        break
                
                return part

            part = checkindent(part, index, indent, minus) # and here
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
            
            # int() FUNCTION in python doesn't hold well enough
            # when dealing with 1.0 calcalted by the algorythm
            #it's something to do with how float numbers are stored
            #in memory i guess.
            #On some checklists it was returning 99% instead of 100%
            #so the quick fix 
            
            if fraction > 0.9999:
                fraction = 1.0
            
    
    
    
    return fraction
    




### CHECKLIST MANAGER WINDOW ###
# and finally we need a window editor for those graphs

class checkwindow:
    def __init__(self, w=False, pf="/", title="Checklist", FILE=None, highlight=None):
        
        
        print "\033[1;31m ⬥ CHECKLIST EDITOR : \033[1;m"
        print "\033[1;32m     ⬦ File "+FILE+"  \033[1;m"
        print "\033[1;32m     ⬦ Title "+title+"  \033[1;m"
        print "\033[1;32m     ⬦ Highlight "+str(highlight)+"  \033[1;m"
        
        #saving all the input to SELF
        self.widget = w
        self.title = title
        self.FILE = FILE
        self.FILENAME = FILE
        
        self.highlight = highlight
        
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
        self.schedule = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/schedule.png")
        
        self.closed = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/closed.png")
        self.openicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/open.png")
        self.pasteicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/paste.png")
        
        
        # FOR GRAB FEATURE
        
        self.tool = "select"
        self.grab = [-1]
        self.grab_text = ""
        self.grabbed = False
        self.initframe = True
        
        graph = gtk.DrawingArea()
        graph.set_size_request(500,700)
        
        self.mainbox.pack_start(graph)
        graph.connect("expose-event", self.framegraph) 
        
        
        
        
            
        
        
        
        
        
        
        
        
        self.win.show_all()
    
    def open(self):
        self.FILE = open(self.FILENAME, "r")
        self.FILE = self.FILE.read().split("\n")
        
        print "\033[1;32m     ⬦ Content (only index tasks) :  \033[1;m"
        
        for i in self.FILE:
            if i.startswith("[ ]") or i.startswith("[V]"):
                print "\033[1;34m          "+str(i.replace("[ ]", "☐").replace("[V]", "☑"))+"  \033[1;m"
        
        
        
        self.colapsed = []
        for n, i in enumerate(self.FILE):
            self.colapsed.append(False)
        
        self.FILE.append("[ ] !!!LASTLINE!!!")
        
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
            
            
            if i != "[ ] !!!LASTLINE!!!":
                save.write(i+"\n")
        
        save.close()
    
    def get_line_path(self, ind, line):
        
        line = line.replace("].", "] ")
        
        sep = "=:>"
        
        p = ""
        if line.startswith("["):
            p = line[line.find("]")+1:]
        else:
            
            parts = []
            
            now = ind+9
            nowline = line
            curindent = len(nowline[:nowline.find("[")])
            for i in range(len(self.FILE)):
                
                try:
                    len(self.FILE[now-1][:self.FILE[now-1].find("[")])
                    
                except:
                    break    
                if len(self.FILE[now-1][:self.FILE[now-1].find("[")]) < curindent:
                    
                    
                    nowline = self.FILE[now-1][self.FILE[now-1].find("]")+1:]
                    parts.append(nowline)
                    curindent = curindent - 4
                now = now - 1
                
                
                
            for i in parts[::-1]:
                p = p+i+sep
            p = p + line[line.find("]")+1:]
        return p
    
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
        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#2b2b2b")) ## CHOSE COLOR
        widget.window.draw_rectangle(xgc, True, 0, 0, w, h)  ## FILL FRAME  
        
        
        # BANNER IMAGE FOR INSPIRATION
            
        # updating the image if let's say we changed it
        if self.dW == 0 and self.DH == 0:
            self.banner = self.pf+"/py_data/banner.png"
            self.pixbuf = gtk.gdk.pixbuf_new_from_file(self.banner)
        
        #lets get how much to scale H
        scaleimageH =  int( float(self.pixbuf.get_height()) / self.pixbuf.get_width() * w)
        #scaling image to the frame
        drawpix = self.pixbuf.scale_simple(w, scaleimageH, gtk.gdk.INTERP_NEAREST) 
        #drawing image
        widget.window.draw_pixbuf(None, drawpix, 0, 0, 0, (h - drawpix.get_height()) / 2, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
        
        #UI Backdrop
        ctx3 = widget.window.cairo_create()
        ctx3.set_source_rgba(0.1,0.1,0.1,0.95)
        ctx3.rectangle(0, 0, w, h)
        ctx3.fill()
        
        
        
        
        
        
        #############################################################################
        ############################# DRAW HERE #####################################
        #############################################################################
        
        removestring = []
        
        
        if self.tool == "select":
            widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.ARROW))
        elif self.tool == "grab":
            widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.FLEUR))
        if self.grabbed:
            self.tool = "select"
            self.grabbed = False
            
            #self.open()
            
            
        if "GDK_BUTTON3" in str(fx) and "GDK_BUTTON3" not in str(self.mpf) and self.win.is_active():
            self.tool = "select"
        
        
        
        
        prevline = "[ ]"
        sofar = [False, 0]
        foundhightlight = False
        
        yline = -40
        
        
        
        for ind, line in enumerate(self.FILE[9:]):
            
            notlastline = True
            #if it's the LASTLINE BUGFIXER THINGY
            if line == "[ ] !!!LASTLINE!!!":
                notlastline = False
            
            
            
            
            #reloadfile = False
            
            if "[ ]" in line or "[V]" in line or "[v]" in line:
                
                notcomment = True
                #COMMENTS
                if line[line.find("]")+2] == "#":
                    notcomment = False
                
                
                try:
                    if self.colapsed[ind+9] and not self.grabbed:                    
                        continue
                except:
                    pass
                
                if ind not in self.grab:
                    yline = yline + 40
                ymove = yline+self.offset
                
                #if ymove not in range(0-40,h):
                #    continue
                
                
                
                xmove = line.find("[")*20 + 50
                
                
                
                
                put = " "
                
                
                gpos = ((len(self.grab_text[:self.grab_text.find("\n")])*12)+35+35)-35
                
                
                checkedhigher = False #THIS WILL BE IF IT'S CHECKED HIGHER IN THE HIRACHY
                
                checked = False # ONLY FOR VISUAL CONFORMATION
                
                
                
                
                 
                #every even darker
                if (yline/40 % 2) == 0 and self.tool != "grab":
                    
                    
                    ctx3 = widget.window.cairo_create()
                    ctx3.set_source_rgba(0,0,0,0.4)
                    ctx3.rectangle(0, ymove,  w, 39)
                    ctx3.fill()
                    
                if not notcomment:    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#2c2c2c")) ## CHOSE COLOR
                    widget.window.draw_rectangle(xgc, True, xmove-50, ymove,  w, 40)
                    
                
                if my in range(ymove, ymove+35) and self.tool == "select" and notlastline and notcomment:
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#414141")) ## CHOSE COLOR
                    widget.window.draw_rectangle(xgc, True, xmove-50, ymove,  w, 39)
                
                
                
                ### LETS TRY TO FIND THE % OF EACH PART IN THE CHECKLIST
                if "[V]" in line:
                    checkpercent = 1.0
                    checkedhigher = True
                    checked = True
                else:
                    checkpercent = 0.0
                
                s_ind = ind
                
                try:
                    if  line.find("[") < self.FILE[9+ind+1].find("[") :#and ymove in range(0, h):
                    
                        nextline = ""
                        fn = -1
                        then = -1
                        
                        
                        for n, l in enumerate(self.FILE[ind+9:]):
                            if line.find("[") == l.find("["):
                                fn = fn + 1
                                if fn == 1:  
                                    then = n
                            if line.find("[") > l.find("["):
                                break
                        fn = fn + 1
                        if fn == 1:  
                            then = n
                        s_ind = then
                        if "[ ]" in line and "[V]" not in line:
                            checkpercent = partcalculate(openckecklist(self.FILENAME, [ind+9, then+ind+9], line.find("[")))
                except:
                    pass
                    
                
                
                
                
                
                
                    
                    
                   # CHECKING COLAPSED
                
                def checkcolapsed():
                    colapsed = False 
                    
                    try:
                        if self.FILE[ind+10].find("[") > line.find("["):
                            
                            if my in range(ymove, ymove+35) and mx in range(xmove-30, xmove-10) and self.tool == "select" :
                        
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#1c1c1c")) ## CHOSE COLOR
                                widget.window.draw_rectangle(xgc, True, xmove-30, ymove+5,  20, 20)
                            
                                # IF CLICKED
                                if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active():
                                    
                                    put = "."
                                    if line[line.find("]")+1:].startswith("."):
                                        put = " "
                                        
                                    
                                     
                                    self.FILE[ind+9] = line[:line.find("]")+1]+put+line[line.find("]")+2:]
                                    
                                    
                                    self.save()
                                    self.open()
                                
                         
                    
                    
                
                
                    
                            try:
                                if not line[line.find("]")+1:].startswith("."):
                                    
                                    if self.tool == "select":
                                        widget.window.draw_pixbuf(None, self.openicon, 0, 0, xmove-30, ymove+5 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                                else:
                                    if self.tool == "select":
                                        widget.window.draw_pixbuf(None, self.closed, 0, 0, xmove-30, ymove+5 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                                    colapsed = True
                            except:
                                pass 
                    
                    
                    except:
                        pass  
                    
                    
                    if colapsed:
                        
                        try:
                            
                            for i in range(ind+10, s_ind+ind+9):
                                self.colapsed[i] = True
                        
                        except:
                            pass
                    else:
                        for i in range(ind+10, s_ind+ind+9):
                            try:
                                self.colapsed[i] = False
                            except:
                                pass
                        
                checkcolapsed()      
                
                
                ## HIGLIGHT
                if self.highlight and self.tool == "select":
                    if self.highlight.endswith(self.get_line_path(ind, line)):
                        foundhightlight = True
                        
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#395384")) ## CHOSE COLOR
                        widget.window.draw_rectangle(xgc, True, xmove, ymove,  w, 39)
                        
                        if self.initframe:
                            self.offset = 0-ymove+100
                
                
                
                    
                
                
                
                
                # IF GRABBING IS ABOVE THIS TASK
                    
                if my in range(ymove, ymove+35) and self.tool == "grab" :
                    
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#1c1c1c")) ## CHOSE COLOR
                    widget.window.draw_rectangle(xgc, True, int(float(mx - gpos)/80)*80+50, ymove,  w, 40)
                    
                    gl = self.grab_text.split("\n")[0]
                    
                    ctx.set_source_rgb(1,1,1)
                    if checkedhigher or "[V]" in gl:
                        ctx.set_source_rgb(0.7,0.4,0.2) #395384
                    ctx.set_font_size(20)
                    ctx.move_to(  int(float(mx - gpos)/80)*80+50+40, ymove+25)
                    ctx.show_text(gl[gl.find("]")+2:])
                    
                    
                    
                    yline = yline + 40
                    ymove = yline+self.offset
                    
                    
                    
                    
                    widget.window.draw_line(xgc, int(float(mx - gpos)/80)*80+50, 0, int(float(mx - gpos)/80)*80+50, h )
                    
                    
                    # IF RELESED
                    if "GDK_BUTTON1" not in str(fx) and "GDK_BUTTON1" in str(self.mpf) and self.win.is_active() and not self.grabbed:
                        
                         
                        for i in self.grab:
                            
                            
                            self.FILE[i+9] = "!!!DELETE!!!"
                            
                        for n, i in enumerate(self.grab_text.split("\n")[::-1]):
                            
                            #if n == -1:
                            #i = i[:i.find("]")+1]+" "+i[i.find("]")+2:]
                            
                            
                            
                            self.FILE.insert(ind+9, " "*((int(float(mx - gpos)/80)*80)/20)+i)
                            
                            
                        
                        
                        
                        
                        
                        for i in self.grab:
                            self.FILE.remove("!!!DELETE!!!")
                        
                        
                        
                        
                        
                        # refrashing the file
                                    
                        self.grab_text = ""
                        self.grab = [-1]
                        
                        #reloadfile = True
                        self.save()
                        self.open()         
                        
                        
                        
                        self.grabbed = True
                        
                        self.colapsed = []
                        for n, i in enumerate(self.FILE):
                            self.colapsed.append(False)
                    
                        checkcolapsed()
                
                    
                
                
                # TEXT OF THE TASK
                
                if notlastline:
                
                    ctx.set_source_rgb(1,1,1)
                    if checkedhigher or "[V]" in line or checkpercent == 1.0:
                        ctx.set_source_rgb(0.7,0.4,0.2) #395384
                    if not notcomment:
                        ctx.set_source_rgb(0.4,0.5,0.5)
                    
                    ctx.set_font_size(20)
                    
                    
                    
                    ctx.move_to(  xmove+40, ymove+25)
                    
                    if ind not in self.grab and notcomment:
                        ctx.show_text(line[line.find("]")+2:])
                    if not notcomment:
                        ctx.show_text(line[line.find("]")+3:])
                        ctx.move_to(  xmove+10, ymove+25)
                        ctx.show_text("#")
                    
                    if "[ ]" in line and not "[V]" in line and checkpercent > 0.0 and checkpercent < 1.0:
                        ctx.set_source_rgb(0.7,0.7,0.7)
                        ctx.set_font_size(10)
                        ctx.move_to(  xmove+2+40, ymove+37)
                        ctx.show_text(str(int(checkpercent*100))+"%")
                        
                        #d0d0d0
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#d0d0d0")) ## CHOSE COLOR
                        widget.window.draw_rectangle(xgc, True, xmove+75, ymove+31, w-30-(xmove+75)-40, 5)
                        
                        #cb9165
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165")) ## CHOSE COLOR
                        widget.window.draw_rectangle(xgc, True, xmove+75, ymove+31, int(round((w-30-(xmove+75)-40)*checkpercent)), 5)
                        
                    
                # CHECK BUTTON
                
                
                
                
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#5c5c5c")) ## CHOSE COLOR
                # IF MOUSE OVER
                if my in range(ymove+5, ymove+5+20) and mx in range(xmove+5, xmove+5+20) and self.tool == "select" and notlastline and notcomment:
                    widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
                    
                    # IF CLICKED
                    if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active():
                        
                        put = "V"
                        if line[line.find("[")+1:].startswith("V") or line[line.find("[")+1:].startswith("v") or checkpercent == 1.0:
                            put = " "
                            
                        
                         
                        self.FILE[ind+9] = line[:line.find("[")+1]+put+line[line.find("]"):]
                        
                        if self.FILE[ind+10].find("[") > line.find("["):
                             allcomment = True
                             for n, i in enumerate(self.FILE):
                                if n in range(ind+10, ind+s_ind+9):
                                    self.FILE[n] = i[:i.find("[")+1]+put+i[i.find("]"):]
                                    if self.FILE[n][line.find("]")+2+4] != "#" and line.find("[")+4 == line.find("["):
                                        allcomment = False
                             if not allcomment:
                                self.FILE[ind+9] = line[:line.find("[")+1]+" "+line[line.find("]"):]
                        
                        #WRITTING TO HYSTORY
                        history.write(self.pf ,self.FILENAME, self.get_line_path(ind, line)+" ["+put+"]")
                        
                        
                        # refrashing the file
                        #reloadfile = True
                        self.save()
                        self.open()
                        
                if notlastline and notcomment:
                    widget.window.draw_rectangle(xgc, True, xmove+5, ymove+5, 20, 20)
                
                
                if line[line.find("[")+1:].startswith("V") or line[line.find("[")+1:].startswith("v") or checkpercent == 1.0 : # IF THE LINE IS CHECKED
                    
                    if notcomment:
                        widget.window.draw_pixbuf(None, self.ok, 0, 0, xmove+7, ymove , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                        
                        
                        #HERE I WANT TO ADD A SPECIAL THING THAT MAKES IT SO IF YOU CHECKED THE THING THERE IS NO ADD SCHEDULES
                        removestring.append(self.get_line_path(ind, line))
                        #foundhightlight = False
                        checked = True
                
                # ADD SUBTASK
                
                
                if my in range(ymove+5, ymove+5+20) and mx in range(xmove+(len(line[line.find("]")+1:])*12)+35, xmove+(len(line[line.find("]")+1:])*12)+35+20) and self.tool == "select" and notlastline:# and not checkedhigher:
                    widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
                    widget.window.draw_rectangle(xgc, True, xmove+(len(line[line.find("]")+1:])*12)+35, ymove+5-2, 22, 22)
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#1c1c1c"))
                    widget.window.draw_rectangle(xgc, True, xmove+(len(line[line.find("]")+1:])*12)+35+30+35+35, ymove+5-2, 160, 27)
                    
                    
                    ctx.set_source_rgb(1,1,1)
                    ctx.set_font_size(20)
                    ctx.move_to(  xmove+(len(line[line.find("]")+1:])*12)+35+35+35+35, ymove+5+20)
                    ctx.show_text("Add Subtask")
                    
                    
                    
                    # IF CLICKED
                    if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active():
                        
                        
                        
                        
                        def ee(theline, p_line, line):
                                
                            Pname = ""
                            comm = False
                            if line[line.find("]")+2] != "#":
                                Pname = dialogs.PickName("New Subtask")
                            else:
                                comm = True
                                Pname = dialogs.PickName("#New Sub-Comment")
                            
                            if comm and not Pname.startswith("#"):
                                Pname = "#"+Pname
                            
                            if Pname != "":
                                self.FILE[theline+9] = line[:line.find("[")+1]+" "+line[line.find("]"):]
                                
                                if self.FILE[theline+10].find("[") > line.find("["):
                                    self.FILE.insert(theline+p_line+9,  line[:line.find("[")]+"    [ ] "+Pname)
                                else:
                                    self.FILE.insert(theline+10,  line[:line.find("[")]+"    [ ] "+Pname)
                                
                                # refrashing the file
                                #reloadfile = True
                                self.save()
                                self.open()
                            
                            
                        
                        
                        glib.timeout_add(10, ee, ind, s_ind , line)
                
                
                
                
                if self.tool == "select" and notlastline and notcomment: 
                
                    widget.window.draw_pixbuf(None, self.plus, 0, 0, xmove+(len(line[line.find("]")+1:])*12)+35, ymove+5 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                if my in range(ymove, ymove+35) and not notcomment and notlastline:
                    widget.window.draw_pixbuf(None, self.plus, 0, 0, xmove+(len(line[line.find("]")+1:])*12)+35, ymove+5 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                    
                # ACTIVATE GRAB BUTTON
                
                if my in range(ymove+5, ymove+5+20) and mx in range(xmove+(len(line[line.find("]")+1:])*12)+35+35, xmove+(len(line[line.find("]")+1:])*12)+35+20+35) and self.tool == "select"  and notlastline:
                    widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.FLEUR))
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
                    widget.window.draw_rectangle(xgc, True, xmove+(len(line[line.find("]")+1:])*12)+35+35, ymove+5-2, 22, 22)
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#1c1c1c"))
                    widget.window.draw_rectangle(xgc, True, xmove+(len(line[line.find("]")+1:])*12)+35+30+35+35, ymove+5, 160, 27)
                    
                    
                    ctx.set_source_rgb(1,1,1)
                    ctx.set_font_size(20)
                    ctx.move_to(  xmove+(len(line[line.find("]")+1:])*12)+35+35+35+35, ymove+5+20)
                    ctx.show_text("Move Task")
                    
                    # IF CLICKED
                    if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active():
                        
                        self.tool = "grab"
                        self.grab = [ind]
                        self.grab_text = line[line.find("["):]
                        
                        if self.FILE[ind+10].find("[") > line.find("["):
                        
                            for n, i in enumerate(self.FILE):
                                if n in range(ind+10, ind+s_ind+9):
                                    self.grab_text = self.grab_text + "\n" + i[line.find("["):]
                                    self.grab.append(n-9)
                                
                        
                        
                if self.tool == "select"  and notlastline and notcomment:# and not checkedhigher:       
                    widget.window.draw_pixbuf(None, self.move, 0, 0, xmove+(len(line[line.find("]")+1:])*12)+35+35, ymove+5 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                if my in range(ymove, ymove+35) and not notcomment and notlastline:
                    widget.window.draw_pixbuf(None, self.move, 0, 0, xmove+(len(line[line.find("]")+1:])*12)+35+35, ymove+5 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                
                
                ## ADD TO SCHEDULE
                
                
                
                # EDIT TASK'S STRING
                
                # removestring
                if not checked:
                    #checking is task has a scheduling already
                    o = open(self.pf+"/schedule.data","r")
                    o = o.read().split("\n")
                    
                    alreadyexist = False
                    
                    for task in o:
                        
                        
                        
                        if task.endswith(self.get_line_path(ind, line)) and self.FILENAME.replace(self.pf, "") in task:
                            
                            
                            
                            
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#1c1c1c"))
                            widget.window.draw_rectangle(xgc, True, xmove+(len(line[line.find("]")+1:])*12)+35+30+35+35, ymove+5-2, 130, 27)
                            
                            ctx.set_source_rgb(1,1,1)
                            ctx.set_font_size(20)
                            ctx.move_to(  xmove+(len(line[line.find("]")+1:])*12)+35+35+35+35, ymove+5+20)
                            ctx.show_text(task[:task.find(" ")])
                            
                            alreadyexist = True
                            
                            
                            
                            if my in range(ymove+5, ymove+5+20) and mx in range(xmove+(len(line[line.find("]")+1:])*12)+35+35+35, xmove+(len(line[line.find("]")+1:])*12)+35+20+35+35) and self.tool == "select"  and notlastline and notcomment:
                                widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
                                widget.window.draw_rectangle(xgc, True, xmove+(len(line[line.find("]")+1:])*12)+35+35+35, ymove+5, 22, 22)
                                
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#1c1c1c"))
                                widget.window.draw_rectangle(xgc, True, xmove+(len(line[line.find("]")+1:])*12)+35+30+35+35, ymove+5, 200, 27)
                                
                                
                                ctx.set_source_rgb(1,1,1)
                                ctx.set_font_size(20)
                                ctx.move_to(  xmove+(len(line[line.find("]")+1:])*12)+35+35+35+35, ymove+5+20)
                                ctx.show_text("Remove Schedule")
                                
                                # IF CLICKED
                                if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active():
                                    
                                    removestring.append(self.get_line_path(ind, line))
                                    
                    
                    if my in range(ymove+5, ymove+5+20) and mx in range(xmove+(len(line[line.find("]")+1:])*12)+35+35+35, xmove+(len(line[line.find("]")+1:])*12)+35+20+35+35) and self.tool == "select" and not alreadyexist  and notlastline and notcomment:
                        widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
                        widget.window.draw_rectangle(xgc, True, xmove+(len(line[line.find("]")+1:])*12)+35+35+35, ymove+5, 22, 22)
                        
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#1c1c1c"))
                        widget.window.draw_rectangle(xgc, True, xmove+(len(line[line.find("]")+1:])*12)+35+30+35+35, ymove+5, 200, 27)
                        
                        
                        ctx.set_source_rgb(1,1,1)
                        ctx.set_font_size(20)
                        ctx.move_to(  xmove+(len(line[line.find("]")+1:])*12)+35+35+35+35, ymove+5+20)
                        ctx.show_text("Add To Schedule")
                        
                        # IF CLICKED
                        if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active():
                            
                            
                            def ee(ind, line):
                            
                                #MAKING A STRING TO WRITE TO THE SCHEDULE.DATA FILE
                                #IT CONTAINS 3 PARTS
                                # date
                                #spacebar
                                # path to the .progress (checklist) file
                                # spacebar
                                # path to the task with in the file
                                # EXAMPLE: 2018/12/31 /dev/chr/character/asset.progress Modeling=:>BaseModeling
                                
                                # GETTING DATE
                                y, m, d = int(datetime.datetime.now().year), int(datetime.datetime.now().month)-1, int(datetime.datetime.now().day)
                        
                        
                                y, m, d = dialogs.GetDate(y, m, d)
                                
                                
                                y, m, d = str(y), str(m+1), str(d)
                                if len(m) < 2:
                                    m = "0"+m
                                if len(d) < 2:
                                    d = "0"+d
                                
                                newdate = y+"/"+m+"/"+d
                                
                                
                                ### ADDING THE FILENAME TO THE STRING
                                
                                schstr = newdate+" "+self.FILENAME.replace(self.pf, "")
                                
                                #WRITTING TO HYSTORY
                                history.write(self.pf ,self.FILENAME, self.get_line_path(ind, line)+" [Scheduled] "+newdate)
                                
                                
                                
                                # GETTING THE PATH WITH IN 
                                
                                
                                
                                
                                
                                p = self.get_line_path(ind, line)
                                
                                schstr = schstr+" "+p
                                
                                
                                
                                
                                # OPENING EXISTANT FILE
                                o = open(self.pf+"/schedule.data","r")
                                o = o.read().split("\n")
                                if o [-1] == "":
                                    o = o[:-1]
                                
                                o.append(schstr)
                                
                                # SORTING WHEN ADDING
                                try:
                                    dl = []
                                    d = o[0][:o[0].find(" ")]
                                    tdl = []
                                    for i in o:
                                        if i[:i.find(" ")] == d:
                                            tdl.append(i)
                                            
                                        
                                        else:
                                            #if schstr[:schstr.find(" ")] == d:
                                            #    tdl.append(schstr)
                                            dl.append(tdl)
                                            tdl = []
                                            tdl.append(i)
                                            d = i[:i.find(" ")]
                                    
                                    
                                    dl.append(tdl)
                                    tdl = []
                                    tdl.append(i)
                                    d = i[:i.find(" ")]
                                    
                                            
                                    
                                    dl = sorted(dl)
                                    
                                    o = []
                                    for i in dl:
                                        for b in i:
                                            
                                            if b != "":
                                                o.append(b)
                                            
                                except Exception as c:
                                    
                                    
                                    o = sorted(o)
                                
                                
                                s = open(self.pf+"/schedule.data","w")
                                for i in o:
                                    s.write(i+"\n")
                                
                                s.close()
                                
                                
                                            
                            
                            glib.timeout_add(10, ee, ind, line)
                        
                        
                    if self.tool == "select"  and notlastline and notcomment:       
                        widget.window.draw_pixbuf(None, self.schedule, 0, 0, xmove+(len(line[line.find("]")+1:])*12)+35+35+35, ymove+5 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                
                
                
                # EIDTING TASK'S NAME    
                    
                if mx in range(xmove+25,  xmove+(len(line[line.find("]")+1:])*12)+35) and my in range(ymove+5, ymove+5+25) and notlastline:
                    #widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.display_get_default(), self.edit, 1,20))
                    
                    widget.window.draw_pixbuf(None, self.edit, 0, 0, mx+2, my-24 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                
                    
                    # IF CLICKED
                    if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active():
                        
                        def ee(ind, line):
                            newtext = dialogs.PickName(line[line.find("]")+2:])
                            
                            if newtext != "": # if returned something (if pressed ok and has text)
                                
                                
                                self.FILE[ind+9] = line[:line.find("]")+2]+newtext
                                
                                # refrashing the file
                                #reloadfile = True
                                self.save()
                                self.open()
                                
                                
                            
                        glib.timeout_add(10, ee, ind, line)
                
                
                # DELETE TASK
                
                
                
                # IF MOUSE OVER
                if my in range(ymove+5, ymove+5+20) and mx in range(w-40, w-40+20) and self.tool == "select"  and notlastline:
                    widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
                    widget.window.draw_rectangle(xgc, True, w-42, ymove+5-2, 22, 22)
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#1c1c1c"))
                    widget.window.draw_rectangle(xgc, True, w-210, ymove+5-2, 160, 27)
                    
                    
                    ctx.set_source_rgb(1,1,1)
                    ctx.set_font_size(20)
                    ctx.move_to(  w-200, ymove+20+5)
                    ctx.show_text("Delete Task")
                    
                    
                    
                    # IF CLICKED
                    if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active():
                        
                       
                    
                        if self.FILE[ind+10].find("[") > line.find("["):
                            for i in range(ind, ind+s_ind):
                                
                                removestring.append(self.get_line_path(i, self.FILE[i+9]))
                                self.FILE[i+9] = "!!!DELETE!!!"
                            for i in range(ind, ind+s_ind):     
                                self.FILE.remove("!!!DELETE!!!")
                        else:
                            
                            removestring.append(self.get_line_path(ind, line))
                            self.FILE[ind+9] = "!!!DELETE!!!"
                            self.FILE.remove("!!!DELETE!!!")
                        
                                    
                        
                            
                        # refrashing the file
                        #reloadfile = True
                        self.save()
                        self.open()
                        
                        
                        
                if self.tool == "select"  and notlastline and notcomment:
                    widget.window.draw_pixbuf(None, self.delete, 0, 0, w-40, ymove+5 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                if my in range(ymove, ymove+35) and not notcomment and notlastline:
                    widget.window.draw_pixbuf(None, self.delete, 0, 0, w-40, ymove+5 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                
                
            
                
                
            prevline = line
        
            
            
        yline = yline + 40    
        ymove = yline+self.offset
        
        
        # ADD TASK
                
                
        if my in range(ymove+5, ymove+5+20) and mx in range(50, 50+20) and self.tool == "select":
            widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
            widget.window.draw_rectangle(xgc, True, 50, ymove+5+self.offset-2, 22, 22)
            
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#1c1c1c"))
            widget.window.draw_rectangle(xgc, True, 50+30+32, ymove+5, 160, 30)
            
            
            ctx.set_source_rgb(1,1,1)
            ctx.set_font_size(20)
            ctx.move_to(  50+32+32, ymove+25)
            ctx.show_text("Add Task")
            
            
            
            # IF CLICKED
            if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active():
                
                def ee(theline, line):
                        
                    Pname = ""
                    Pname = dialogs.PickName("New Task")
                    
                    
                    
                    
                    if Pname != "":
                        self.FILE.append("[ ] "+Pname)
                        
                        
                        # refrashing the file
                        #reloadfile = True
                        self.save()
                        self.open()
                    
                    
                
                
                glib.timeout_add(10, ee, ind, line)
        
        
        
        
        
        widget.window.draw_pixbuf(None, self.plus, 0, 0, 50, ymove+5 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
        
        
        
        # IF ASSET COPY CHECKLIST FROM ASSET
        if self.FILENAME.replace(self.pf, "").startswith("/dev/"):
            
            if my in range(ymove+5, ymove+5+20) and mx in range(50+32, 50+32+20) and self.tool == "select":
                widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
                widget.window.draw_rectangle(xgc, True, 50+32, ymove+5+self.offset-2, 22, 22)
                
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#1c1c1c"))
                widget.window.draw_rectangle(xgc, True, 50+30+32, ymove+5, 160+50, 30)
                
                
                ctx.set_source_rgb(1,1,1)
                ctx.set_font_size(20)
                ctx.move_to(  50+32+32, ymove+25)
                ctx.show_text("Import Checklist")
                
                
                
                # IF CLICKED
                if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active():
            
                    def ee(ind, line):
                        
                        importing =  self.pf+itemselector.select(self.pf)+"/asset.progress"
                        if os.path.exists(importing):
                            importing = open(importing, "r")
                            importing = importing.read().split("\n")
                            for n, i in enumerate(importing[9:]):
                                if "[ ]" in i or "[V]" in i:
                                    self.FILE.append(i.replace("[V]", "[ ]"))
                                    
                            self.save()
                            self.open()
                                    
                        
                    glib.timeout_add(10, ee, ind, line)
                    
                    
            widget.window.draw_pixbuf(None, self.pasteicon, 0, 0, 50+32, ymove+5 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
        
        
        
        #if not foundhightlight and self.highlight:
        #    #
        #    removestring.append(self.highlight)
        if removestring:
            
            for removing in removestring:
                o = open(self.pf+"/schedule.data","r")
                o = o.read().split("\n")
                
                if o[-1] == "":
                    o = o[:-1]
                
                try:
                    
                    
                    for i in o:
                        if i.endswith(removing) and self.FILENAME.replace(self.pf, "") in i:
                            o.remove(i)
                    
                    
                    
                    s = open(self.pf+"/schedule.data","w")
                    for i in o:
                        
                        s.write(i+"\n")
                    s.close()
                    #self.highlight = None
                except Exception as e:
                    pass
                    
                
            
        
        #SCROLL
        
        if self.mpy > my and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf) and self.win.is_active():
                    
            self.offset = self.offset + (my-self.mpy)
        
        if self.mpy < my and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf) and self.win.is_active():
                    
            self.offset = self.offset - (self.mpy-my)
        
        
        if self.offset < 0-(yline+40-h):
            self.offset = 0-(yline+40-h)
            
        if self.offset > 0:
            self.offset = 0
        
        
        
        #if reloadfile:
        #   
        #    self.save()
        #    self.open()
        
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
        
        
        self.initframe = False
        def callback():
            if self.allowed == True:
                widget.queue_draw()

        glib.timeout_add(10, callback)
    
