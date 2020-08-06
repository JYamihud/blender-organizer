# -*- coding: utf-8 -*-

# system
import os
import sys
import socket

# graphics interface
import gtk
import pango
import cairo
import glib
import datetime
try: 
    import Image
except:
    from PIL import Image

# calculational help
import datetime


# self made modules

import thumbnailer
import checklist
from subprocess import *
import quick

def destroyevent(w=False):
    drawer.process_kill()
    gtk.main_quit()
    
    

window = gtk.Window()
window.connect("destroy", destroyevent)
window.set_title("Rendering...")


##### GETTING THE FILE

FILE = sys.argv[-1]
print FILE

pf = ""

if "py_data/rnd_seq/" in FILE:
    
    try:
        rlist = open(FILE, "r")
        rlist = rlist.read().split("\n")
    except:
        rlist = []
    
    pf = FILE[:FILE.find("py_data/rnd_seq/")-1]
    
else:
    rlist = [FILE[FILE.find("rnd"):]]
    pf = FILE[:FILE.find("rnd")-1]

for i in rlist:
    print i

print "PF", pf

THEFILE = FILE

gtk.window_set_default_icon_from_file(pf+"/py_data/icons/render_big.png")
####### DRAWING ####
class draw:
    
    def __init__(self, pf, win):
        
        self.win = win
        self.pf = pf
        self.allowed = True
        
        self.nowfile = 0
        self.nowframe = 0
        
        self.START = 0
        self.END = 250
        self.FOLDER = ""
        self.FORMAT = ""
        
        self.starttime = datetime.datetime.now()
        
        self.process = self.process_get()
        
        
        self.preview = [None, 0]
        self.no_frame = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/no_frame.png")
        
        
        def framegraph(widget, event):
                                                            
            w, h = widget.window.get_size()
            xgc = widget.window.new_gc()
            
            mx, my, fx  = widget.window.get_pointer()
            
            
            # GETTING WHETHER THE WINDOW IS ACTIVE
            
            self.winactive = self.win.is_active()
            
            ctx = widget.window.cairo_create()
            #ctx.select_font_face("Sawasdee", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            ctx.set_source_rgb(1,1,1)
            
            xgc.line_width = 2
            
            # BACKGROUND COLOR
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#2c2c2c")) ## CHOSE COLOR
            widget.window.draw_rectangle(xgc, True, 0, 0, w, h)  ## FILL FRAME   
            
            #Top Line
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#424242")) ## CHOSE COLOR
            widget.window.draw_rectangle(xgc, True, 0, 0, w, 30)  ## FILL FRAME   
            
            
            
            
             
            
            # MAIN TRY BECAUSE SOMETIMES UNEXPECTED STUFF HAPPENS
            
            try:
                
                try:
                    # BASIC READING
                    line = self.process.stdout.readline()[:-1]
                except:
                    line = ""
                
                
                ctx.set_font_size(12)
                ctx.move_to( 20,20)
                
                ctx.show_text( line )
                
                ctx.move_to( 20,40)
                
                
                PS = 0.0
                SS = 0.0
                DN = 0.0
                
                donetile, tiles, intile = 0,1,1
                denoised = 0
                
                ### PARSING THE STRING
                
                if "Path Tracing Tile" in line:
                    
                    donetile, tiles =  line[line.find("Path Tracing Tile")+18:][:line[line.find("Path Tracing Tile")+18:].find(",")].split("/")
                    
                    PS = (float(donetile)+1)/float(tiles)
                
                if "Sample" in line:
                    
                    donesample, intile =  line[line.find("Sample")+7:][:line[line.find("Sample")+7:].find(",")].split("/")
                    
                    SS = float(donesample)/float(intile)
                
                if "Denoised" in line:
                    
                    denoised = line[line.find("Denoised")+9:][:line[line.find("Denoised")+9:].find("tiles")]
                    DN = float(denoised)/float(tiles)
                
                if "Compositing" in line:
                    
                    try:
                        donetile, tiles =  line[line.find("Compositing | Tile")+19:].split("-")
                    
                        PS = float(donetile)/float(tiles)
                    except:
                        pass
                    
                
                #xgc.set_rgb_fg_color(gtk.gdk.color_parse("#1d1d1d")) ## CHOSE COLOR
                #widget.window.draw_rectangle(xgc, True, 0, 30, int(w*PS), 20)  ## FILL FRAME  
                
                #xgc.set_rgb_fg_color(gtk.gdk.color_parse("#547ab5")) ## CHOSE COLOR
                #widget.window.draw_rectangle(xgc, True, 0, 30, int(float(intile)*SS)+int(w*PS)-int(float(w)/float(tiles)), 20)  ## FILL FRAME  
                
                #xgc.set_rgb_fg_color(gtk.gdk.color_parse("#5c5c5c")) ## CHOSE COLOR
                #widget.window.draw_rectangle(xgc, True, 0, 30, int(w*DN), 20)  ## FILL FRAME
                
                
                if self.process.poll() != None:
                
                    endframetime = datetime.datetime.now()
                    DELTA = endframetime - self.starttime
                    seconds = DELTA.seconds   
                    
                    # OUTPUTTING RENDER SPEED INTO IT'S FILE
                    
                    FILE = rlist[self.nowfile]
                    
                    readfirst = open(self.pf+"/"+FILE[:FILE.rfind("/")+1]+"extra/"+FILE[FILE.rfind("/")+1:]+".rnd", "r")
                    readfirst = readfirst.read()
                    
                    read = []
                    for i in readfirst.split("\n"):
                        read.append(i)
                    
                    found = False
                    for n, i in enumerate(read):
                        if i.startswith(str(self.nowframe)+" "):
                            
                            found = True
                            read[n] = str(self.nowframe)+" "+str(seconds)
                    if found == False:
                        
                        read.append(str(self.nowframe)+" "+str(seconds))
                    
                    writeback = open(self.pf+"/"+FILE[:FILE.rfind("/")+1]+"extra/"+FILE[FILE.rfind("/")+1:]+".rnd", "w")
                    for i in read:
                        writeback.write(i+"\n")
                    writeback.close()
                    
                    
                    
                    print seconds, "SECONDS WAS RENDERING"
                    
                    self.process = self.process_get()
                
                
                    
                    
                # PREVIEW IMAGE SPACE #
                
                PWX = 220
                
                #xgc.set_rgb_fg_color(gtk.gdk.color_parse("#5c5c5c")) ## CHOSE COLOR
                #widget.window.draw_rectangle(xgc, True, 20-5, 60, PWX-20, 110)  ## FILL FRAME    
                
                widget.window.draw_pixbuf(None, self.no_frame, 0, 0, 15, 60 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                
                
                #widget.window.draw_pixbuf(None, self.no_frame, 0, 0, 220, 60, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                
                
                
                ### GETTING ALL THE FRAMES IN THE FOLDER DRAWN
                
                FILE = rlist[self.nowfile]
                readfirst = open(self.pf+"/"+FILE[:FILE.rfind("/")+1]+"extra/"+FILE[FILE.rfind("/")+1:]+".rnd", "r")
                readfirst = readfirst.read()
                
                read = []
                for i in readfirst.split("\n"):
                    read.append(i)
                
                
                LARGEST = 1
                AVARAGE = 0
                
                for i in read:
                    
                    try:
                        if  os.path.exists(pf+"/"+self.FOLDER+"/"+quick.getfileoutput(i.split(" ")[0], self.FORMAT) ):
                            if int(i.split(" ")[1]) > LARGEST:
                                
                                LARGEST = int(i.split(" ")[1])
                        
                            if AVARAGE == 0:    
                                AVARAGE = int(i.split(" ")[1])
                            else:
                                
                                AVARAGE = (AVARAGE + int(i.split(" ")[1])) / 2
                            
                            
                            
                    except:
                        pass
                
                
                DONEFRAMS = 0
                endframetime = datetime.datetime.now()
                DELTA = endframetime - self.starttime
                seconds = DELTA.seconds
                
                frameselectstill = True
                
                
                if LARGEST < seconds:
                    LARGEST = seconds
                    
                divided = float(w-20-PWX-20)/int(self.END-self.START+1)
                
                print divided, "divided"
                
                
                for frame in range(self.START, self.END+1):   
                    
                    
                    
                    
                    if divided > 5: 
                        
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#1c1c1c")) ## CHOSE COLOR
                        widget.window.draw_rectangle(xgc, True, int(divided*(frame-self.START))+PWX, 60, int(divided)+1, 100)
                        #widget.window.draw_pixbuf(None, self.no_frame, 0, 0, int(divided*(frame-self.START))+PWX, 60 , int(round(divided)), 100, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                        
                    THIS = LARGEST
                    
                    for i in read:
                        
                        try:
                            if i.startswith(str(frame)+" "):
                                
                                THIS = int(i.split(" ")[1])
                            
                                # compare old frames
                                TY = int(100* (float(THIS) / float(LARGEST)) )
                                #print TY, THIS
                                
                            
                                
                                #DONEFRAMS = DONEFRAMS + 1
                                
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#2b2b2b")) ## CHOSE COLOR
                                widget.window.draw_rectangle(xgc, True, int(divided*(frame-self.START))+PWX, 60+100-TY, int(divided)+1, TY)
                                
                                
                                
                        except:
                            pass
                    
                    
                    
                    
                    
                    
                    if frame == self.nowframe:
                        
                        
                        
                        
                        
                        TY = int(100* (float(seconds) / float(LARGEST)) )
                        
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#363636")) ## CHOSE COLOR
                        widget.window.draw_rectangle(xgc, True, int(divided*(frame-self.START))+PWX+1, 60+100-TY-1, int(divided)-1, TY)
                        
                        
                        #blender style crosses during rendering
                                
                        #ff8500
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#ff8500"))
                        xgc.line_width = 1
                                
                        
                        widget.window.draw_line(xgc, int(divided*(frame-self.START))+PWX, 60, int(divided*(frame-self.START))+PWX+5, 60)
                        widget.window.draw_line(xgc, int(divided*(frame-self.START))+PWX, 60, int(divided*(frame-self.START))+PWX, 60+5)
                    
                        widget.window.draw_line(xgc, int(divided*(frame-self.START))+PWX+int(divided)-1, 60, int(divided*(frame-self.START))+PWX+int(divided)-6, 60)
                        widget.window.draw_line(xgc, int(divided*(frame-self.START))+PWX+int(divided)-1, 60, int(divided*(frame-self.START))+PWX+int(divided)-1, 60+5)
                        
                        widget.window.draw_line(xgc, int(divided*(frame-self.START))+PWX, 160, int(divided*(frame-self.START))+PWX+5, 160)
                        widget.window.draw_line(xgc, int(divided*(frame-self.START))+PWX, 160, int(divided*(frame-self.START))+PWX, 160-5)
                        
                        widget.window.draw_line(xgc, int(divided*(frame-self.START))+PWX+int(divided)-1, 160, int(divided*(frame-self.START))+PWX+int(divided)-6, 160)
                        widget.window.draw_line(xgc, int(divided*(frame-self.START))+PWX+int(divided)-1, 160, int(divided*(frame-self.START))+PWX+int(divided)-1, 160-5)
                        
                    
                    
                    TY = int(100* (float(THIS) / float(LARGEST)) )
                    #print TY, THIS
                    
                    if quick.getfileoutput(frame, self.FORMAT) in os.listdir(pf+"/"+self.FOLDER):
                        
                        DONEFRAMS = DONEFRAMS + 1
                        
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#3f3f3f")) ## CHOSE COLOR
                        widget.window.draw_rectangle(xgc, True, int(divided*(frame-self.START))+PWX, 60+100-TY, int(divided)+1, TY)
                        
                        
                        
                        if mx in range(int(divided*(frame-self.START)+PWX), int(divided*(frame-self.START)+PWX) + int(divided)+1 ) and my in range(60, 160) and frameselectstill:  
                            frameselectstill = False
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#395384")) ## CHOSE COLOR
                            widget.window.draw_rectangle(xgc, True, int(divided*(frame-self.START)+PWX), 60+100-TY, int(divided)+1, TY)
                            
                            
                            # FRAME TIME OUTPUT
                            thistime = quick.timestring(THIS)
                            
                            
                            ctx.set_font_size(12)
                            ctx.move_to( 20,h-50)
                            
                            ctx.show_text( "Frame: [ "+ quick.getfileoutput(frame, self.FORMAT)+" ] Took time: "+thistime)
                            
                            
                            if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active(): # IF CLICKED
                                
                                
                                os.system("xdg-open "+pf+"/"+self.FOLDER+"/"+quick.getfileoutput(frame, self.FORMAT))
                            
                            
                            
                            
                            try:
                                
                                if self.preview[1] != frame:
                                
                                    self.preview = [gtk.gdk.pixbuf_new_from_file(thumbnailer.thumbnail(pf+"/"+self.FOLDER+"/"+quick.getfileoutput(frame, self.FORMAT), pf=pf)), frame]
                                
                                widget.window.draw_pixbuf(None, self.preview[0], 0, 0, 20-5, 60 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
                            except:
                                pass
                
                    
                
                
                print seconds
                REMSECS = ((self.END - DONEFRAMS) * AVARAGE) - seconds
                REMAINING = quick.timestring(REMSECS)
                ctx.set_font_size(12)
                ctx.move_to( 20,h-20)
                
                starttime = datetime.datetime.now()
                DELTA = starttime + datetime.timedelta(seconds= REMSECS )
                
                
                
                
                DONEAT = DELTA.strftime("%Y/%m/%d %H:%M:%S")
                print DONEAT
                
                ctx.show_text("Time Remaining (For Whole Shot) : "+REMAINING+" With Avarage Time Per Frame : "+quick.timestring(AVARAGE)+"  ESTIMATED END TIME : "+DONEAT)
                
                
                
                
                
                
            except:
                pass # MAIN EXCEPTION
            
            
            # TESTING SOMETHING
            ctx.set_font_size(20)
            ctx.move_to( mx, my)
            #ctx.show_text(str(mx)+":"+str(my)+"  "+str(self.winactive)+"   "+str(fx)) 
            
            self.dW = w
            self.DH = h
            
            self.mpx = mx
            self.mpy = my
            self.mpf = fx
            
            
            def callback():
                if self.allowed == True:
                    widget.queue_draw()

            glib.timeout_add(1, callback)
            
            
            
            
        graph = gtk.DrawingArea()
        graph.set_size_request(1300,250)

        window.add(graph)
        graph.connect("expose-event", framegraph)
    
    
    def process_get(self):
        
        self.starttime = datetime.datetime.now()
        
        for ind, FILE in enumerate(rlist):
            
            self.nowfile = ind
            
                    
                
            print "NOW FILE ", FILE
            print
            
            if FILE != "":
                
                
                
                fromsaved = open(self.pf+"/"+FILE[:FILE.rfind("/")+1]+"extra/"+FILE[FILE.rfind("/")+1:]+".rnd", "r")
                fromsaved = fromsaved.read()
        
                START = 1
                END = 250
                FORMAT = "JPEG"
                FOLDER = "/"+FILE[:FILE.rfind("/")+1]+"storyboard"
                
                if fromsaved:
                    
                    for line in fromsaved.split("\n"): 
                        if line.startswith("START = "):
                            
                            START = int(line[line.find("= ")+1:])
                        
                        if line.startswith("END = "):
                            
                            END = int(line[line.find("= ")+1:])
                    
                        if line.startswith("FORMAT = "):
                            
                            FORMAT = str(line[line.find("= ")+1:]).strip()
                        
                        if line.startswith("FOLDER = "):
                            
                            FOLDER = str(line[line.find("= ")+1:]).strip()
                
                self.START = START
                self.END = END
                self.FORMAT = FORMAT
                self.FOLDER = FOLDER
                
                 
                ## DOING MAGIC
                if self.nowframe < START:
                    self.nowframe = START                        
                
                print pf+FOLDER
                
                for i in range(START, END+1):
                    
                    
                    
                
                    if quick.getfileoutput(i, FORMAT) not in os.listdir(pf+"/"+FOLDER):
                        
                        self.nowframe = i
                        
                        
                        print self.nowframe
                        
                        if "py_data/rnd_seq/" in THEFILE:
                            
                            self.win.set_title("RENDER LIST : "+THEFILE[THEFILE.rfind("/")+1:]+" FILE: "+FILE+" FRAME: "+str(i))
                            
                        else:
                            self.win.set_title("FILE : "+FILE+" FRAME: "+str(i))
                        
                        cblndr = ""
                                        
                        try:
                            bv = open(self.pf+"/py_data/blenderver.data", "r")
                            bv = bv.read().split("\n")
                            
                            print "bv", bv
                            
                            if int(bv[0]) > 0:
                                cblndr = bv[int(bv[0])]+"/"
                        except:
                            pass
                        
                        return Popen(['stdbuf', '-o0', cblndr+"blender", "-b", pf+"/"+FILE, "-o",pf+FOLDER+"/####", "-F", FORMAT ,"-f", str(self.nowframe)], stdout=PIPE, universal_newlines=True)
        
        os.system("notify-send Blender-Organizer Finished\ Rendering")
        gtk.main_quit()
        
    def process_kill(self):
    
        self.process.kill()
        



drawer = draw(pf, window)



window.show_all()






gtk.main()


