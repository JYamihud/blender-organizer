# -*- coding: utf-8 -*-

# system
import os
import socket
import sys

# graphics interface
import gtk
import pango
import cairo
import glib
try: 
    import Image
except:
    from PIL import Image

# calculational help
import datetime


# self made modules

import thumbnailer
import checklist
import dialogs
import fileformats
from subprocess import *

class main: 
    def __init__(self,w, pf): 
    
        
        self.pf = pf
        
        self.win = gtk.Window()
        self.win.set_title("Updates")
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
        self.end = 0
        
        ##### MAIN LIST FOR PREVIEW #####
        
        
        self.MAINLIST = [] # [type, data]
        # TYPES:
        # text, image, button
        # string, pixbuf, [string, command]
        
        
        self.VER = "0.0"
        self.FILES = []
        
        self.writepagemode = False
        
        
        self.process = Popen(['stdbuf', '-o0', "python2", self.pf+"/py_data/modules/update_network.py"], stdout=PIPE, universal_newlines=True)
        
        self.update_update = False
        self.update_progress = 1.0
        
        
        def destroyevent(w=False):
             self.process.process_kill()
        self.win.connect("destroy", destroyevent)
        
        graph = gtk.DrawingArea()
        graph.set_size_request(500,700)
        
        self.mainbox.pack_start(graph)
        graph.connect("expose-event", self.framegraph) 
        
        
        self.win.show_all()
        
        
    #### THIS FUNCTION DRAWS THE PIXELS IN THE WINDOW ####
    def framegraph(self, widget, event):
             
        self.end = 0
                                               
        w, h = widget.window.get_size()
        xgc = widget.window.new_gc()
        
        mx, my, fx  = widget.window.get_pointer()
        
        
        # GETTING WHETHER THE WINDOW IS ACTIVE
        
        self.winactive = self.win.is_active()
        
        ctx = widget.window.cairo_create()
        ctx.select_font_face("Monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        
        xgc.line_width = 2
        
        # BACKGROUND COLOR
        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#363636")) ## CHOSE COLOR
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
        #############################   POPEN   #####################################
        #############################################################################
        
        
        
        
        
        
        
        try:
            # BASIC READING
            line = self.process.stdout.readline()[:-1]
        except:
            line = ""
        if line:
            print line
        
            ctx.set_source_rgb(1,1,1)
            ctx.set_font_size(15)
            ctx.move_to(  2, h-2)
            ctx.show_text(line)
            
            if line.startswith("MAIN_FILE"):
                
                self.FILES.append("MAIN_FILE")
            if line.startswith("FILE "):
                
                self.FILES.append(line[line.find(" ")+1:])
            
            if line.startswith("VERSION "):
                
                self.VER = line[line.find(" "):]
            
            
            
            if self.writepagemode:  
                
                if line.startswith("<image>"):
                    self.MAINLIST.append(["image", gtk.gdk.pixbuf_new_from_file(line[line.find(" ")+1:])])
                
                elif line.startswith("<button>"):
                    self.MAINLIST.append(["button", [line[line.find('"')+1:line.replace('"', " ", 1).find('"')], line[line.replace('"', " ", 1).find('"')+1:]]])
                    
                
                else:
                    self.MAINLIST.append(["text", line])
        
        
        
            if line.startswith("PAGE"): 
                self.writepagemode = True
        
        
        #############################################################################
        ############################# DRAW HERE #####################################
        #############################################################################
        
        
        
        self.end = self.end + 60
        
        
        
        
        
        
        
        if len(self.MAINLIST) == 0 and len(self.FILES) == 0: 
            
            ctx.set_source_rgb(1,1,1)
            ctx.set_font_size(30)
            ctx.move_to(  50, 50)
            ctx.show_text("LOADING...")
        
        else:
            ctx.set_source_rgb(1,1,1)
            ctx.set_font_size(25)
            ctx.move_to(  50, 50+self.offset+self.end)
            ctx.show_text("UPDATE TO : "+self.VER)
            
            self.end = self.end + 30
            
            ### FILES LIST
            
            for i in self.FILES:
                
                ctx.set_source_rgb(1,1,1)
                ctx.set_font_size(10)
                ctx.move_to(  50, 50+self.end+self.offset)
                ctx.show_text(i)
                
                self.end = self.end + 11
                
                
                
            self.end = self.end + 30
            
            
            #ctx.select_font_face("Sawasdee", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            
            
            for i in self.MAINLIST:
                
                if i[0] == "text":
                
                    ctx.set_source_rgb(1,1,1)
                    ctx.set_font_size(20)
                    ctx.move_to(  50, 50+self.end+self.offset)
                    ctx.show_text(i[1])
                    
                    self.end = self.end + 22
                
                if i[0] == "image":
                    
                    pixbuf = i[1]
                    
                    widget.window.draw_pixbuf(None, pixbuf, 0, 0, 10, 50+self.end+self.offset , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
                        
                    self.end = self.end + pixbuf.get_height() + 50
                
                if i[0] == "button":
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#5c5c5c")) ## CHOSE COLOR
                    widget.window.draw_rectangle(xgc, True, 0, 50+self.end+self.offset, w, 50)
                    
                    if mx in range(0, w) and my in range(50+self.end+self.offset, 50+self.end+self.offset+50) and my > 50:
                        
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#7c7c7c")) ## CHOSE COLOR
                        widget.window.draw_rectangle(xgc, True, 0, 50+self.end+self.offset, w, 50)
                        
                        # IF CLICKED
                        if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active():
                        
                            try:
                                os.system(i[1][1])
                            except:
                                pass
                    
                    
                    
                    ctx.set_source_rgb(1,1,1)
                    ctx.set_font_size(20)
                    ctx.move_to(  70, 50+self.end+self.offset+22)
                    ctx.show_text(i[1][0])
                    
                    ctx.set_source_rgb(1,1,1)
                    ctx.set_font_size(10)
                    ctx.move_to(  70, 50+self.end+self.offset+40)
                    ctx.show_text(i[1][1])
                    
                    
                    self.end = self.end + 120
                    
        
        
        #### UPDATE LOUNCH BUTTON #####
        
        ctx.select_font_face("Ubuntu Mono", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        
        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#5c5c5c"))
        widget.window.draw_rectangle(xgc, True, 0, 0, w, 50)
        
        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#db3c16"))
        if mx in range(0,w) and my in range(50):
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#e47649")) ## CHOSE COLOR
            
            # IF CLICKED AND NOT LAUNCHED
            if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active() and not self.update_update:
                
                print __file__, "<<<<<<<<<<<<<<<< THE FILE NAME"
                
                self.update_update = Popen(['stdbuf', '-o0', "python", self.pf+"/py_data/modules/update_update.py"], stdout=PIPE, universal_newlines=True)
                
                
                
                
            
        
        if self.update_update:
            try:
                # BASIC READING
                line = self.update_update.stdout.readline()[:-1]
            except:
                line = ""
            if line:
                print line
            
            try:
                
                self.update_progress = float(line)
               
            except:
                self.update_progress = 1.0
        
            if self.update_update.poll() or line.startswith("DONE"):
                self.update_progress = 1.1
                self.update_update = False
                
        
        widget.window.draw_rectangle(xgc, True, 0, 0, int(w*self.update_progress), 50)
        
        
        ctx.set_source_rgb(1,1,1)
        ctx.set_font_size(40)
        ctx.move_to(  80, 40)
        
        if self.update_update and self.update_progress < 1.1:
            ctx.show_text(str(int(self.update_progress*100))+"% Updating ...")
        
        elif self.update_progress == 1.1:
        
            ctx.show_text("DONE! Restarting...")
            
            def restart():
                os.execl(sys.executable, sys.executable, *sys.argv)
            
            glib.timeout_add(500, restart)
                
        
        else:
            ctx.show_text("Launch Update")
        
        #############################################################################
        ############################# UNTIL HERE ####################################
        #############################################################################
        
        
        
        #SCROLL
        
        if self.mpy > my and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf) and self.win.is_active()  and my > 50:
                    
            self.offset = self.offset + (my-self.mpy)
        
        if self.mpy < my and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf) and self.win.is_active() and my > 50:
                    
            self.offset = self.offset - (self.mpy-my)
        
        
        if self.offset < 0-(self.end-h)-60:
            self.offset = 0-(self.end-h)-60
            
        if self.offset > 0:
            self.offset = 0
        
        
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

        glib.timeout_add(1, callback)
