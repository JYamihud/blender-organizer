# -*- coding: utf-8 -*-

# system
import os
import socket

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
from subprocess import *

# self made modules

import thumbnailer
import dialogs
import checklist

class draw_blendver:
    
    def __init__(self, pf, box, win):
    
        self.pf = pf # pf stands for project folder. It's a string to know
                     # where the project's folders start with
        
        self.box = box # the gtk.Box() container to put this widget into
        
        self.win = win
        
        self.newfiles = os.walk(self.pf+"/py_data/new_file").next()[2]
        self.thumbs = []
        for i in self.newfiles:
            self.thumbs.append(False)
        
        print "GOT HERE 1"
        
        
        # drawing it's own box cutting in 2 for right and left halfs
        
        
        
        
        
        # reading persentages
        
        
        
        
        
        
        
        
        ####   DRAWING TO THE SCREEN ####
        
        self.allowed = True # a value for the redrawing of the drawable for the next frame
        
        self.dW = 0
        self.DH = 0
        self.banner = thumbnailer.thumbnail(pf+"/py_data/banner.png", 500, 500)
        self.pixbuf = gtk.gdk.pixbuf_new_from_file(self.banner)
        self.mpx = 0
        self.mpy = 0
        self.mpf = ""
        
        self.plusicon  = gtk.gdk.pixbuf_new_from_file(pf+"/py_data/icons/plus.png")
        self.blendOSicon  = gtk.gdk.pixbuf_new_from_file(pf+"/py_data/icons/OS_blendico.png")
        self.blendicon  = gtk.gdk.pixbuf_new_from_file(pf+"/py_data/icons/blender.png")
        
        self.okayicon  = gtk.gdk.pixbuf_new_from_file(pf+"/py_data/icons/ok.png")
        self.deleteicon  = gtk.gdk.pixbuf_new_from_file(pf+"/py_data/icons/delete.png")
        self.checkicon  = gtk.gdk.pixbuf_new_from_file(pf+"/py_data/icons/checklist.png")
        
        self.blendOS = ["Empty", "Empty", "Empty"]
        
        self.keys = []
        self.dell = -1
        
        self.blscroll = 0 
        self.chscroll = 0   
        self.bvscroll = 0        
        #making a filewith the setting storeage
        
        self.launchfolder = True # Makes sure just one folder choose dialogue is running
        
        if os.path.exists(pf+"/py_data/blenderver.data"):
            pass
        else:
            bldvf = open(pf+"/py_data/blenderver.data", "w")
            bldvf.write("0")
            bldvf.close()
        
        
        self.blendDATA = []
        self.choise = 0
        bldvf = open(pf+"/py_data/blenderver.data", "r")
        bldvf = bldvf.read().split("\n")
        
        try:
            self.choise = int(bldvf[0])
        except:
            self.choise = 0
        
        print bldvf
        for n, i in enumerate(bldvf):
            if n > 0 and n < len(bldvf)-1:
                self.blendDATA.append([i, ["Empty", "Empty", "Empty"]])
        
        def framegraph(widget, event):
                                                    
            w, h = widget.window.get_size()
            xgc = widget.window.new_gc()
            
            mx, my, fx  = widget.window.get_pointer()
            
            
            # GETTING WHETHER THE WINDOW IS ACTIVE
            
            self.winactive = win.is_active()
            

                
            
            
            
            ctx = widget.window.cairo_create()
            #ctx.select_font_face("Sawasdee", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            
            ctx2 = widget.window.cairo_create()
            ctx2.select_font_face("Monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            
            
            xgc.line_width = 2
            
            # BACKGROUND COLOR
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#868686")) ## CHOSE COLOR
            widget.window.draw_rectangle(xgc, True, 0, 0, w, h)  ## FILL FRAME            
            
            
            ######################################################################################
            #                                                                                    #
            #                            DRAW FROM HERE                                          #
            #                                                                                    #
            ######################################################################################
            
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
            ctx3.set_source_rgba(0.2,0.2,0.2,0.8)
            ctx3.rectangle(0, 0, w, h)
            ctx3.fill()
            
            
            
            
            # RAW 1
            
            # THIS RAW IS SHOWING ALL THE BLEND FILES IN /py_data/new_file
            
            
            ctx.set_source_rgb(1,1,1)
            ctx.set_font_size(15)
            ctx.move_to( 10,20)
            ctx.show_text("Starting / Recovery Blend Files") 
            
            
            ctx3.set_source_rgba(0,0,0,0.4)
            ctx3.rectangle(0, 30, w, 150)
            ctx3.fill()
            
            
            space = 0
            for n, i in enumerate(self.newfiles):
                
                if i.endswith(".blend"):
                    
                    
                    if not self.thumbs[n]:
                        try:
                            pic = thumbnailer.blenderthumb(self.pf+"/py_data/new_file/"+i, 130, 130)
                            pic = gtk.gdk.pixbuf_new_from_file(pic)
                            
                        except:
                            pic = self.pf+"/py_data/icons/blendfile_big.png"
                            pic = gtk.gdk.pixbuf_new_from_file(pic)
                        self.thumbs[n] = pic
                    else:
                        widget.window.draw_pixbuf(None, self.thumbs[n], 0, 0, 10+self.blscroll+space+5, 30+5+5, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                    
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#526969"))
                    widget.window.draw_rectangle(xgc, True,  10+self.blscroll+space, 30+5, 140, 20)
                    
                    
                    ctx3.set_source_rgba(0,0,0,0.4)
                    ctx3.rectangle(10+self.blscroll+space, 30+5, 140, 140)
                    ctx3.fill()
                    
                    ctx2.set_source_rgb(1,1,1)
                    ctx2.set_font_size(11)
                    ctx2.move_to( 10+30+self.blscroll+space,30+20)
                    ctx2.show_text(i[:i.find(".")])
                    
                    widget.window.draw_pixbuf(None, self.blendicon, 0, 0, 10+self.blscroll+space+5, 30+5, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
            
                    if my in range(30, 30+140) and mx in range(10+self.blscroll+space, 10+self.blscroll+space+140):
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#aaa"))
                        widget.window.draw_rectangle(xgc, False,  10+self.blscroll+space, 30+5, 140, 140)
                        
                        if  "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active():
                            
                            if self.choise == 0:
                                Popen(["blender", self.pf+"/py_data/new_file/"+i])
                            elif self.choise != -1:
                                Popen([self.blendDATA[self.choise-1][0]+"/blender", self.pf+"/py_data/new_file/"+i])
                    
                    
                    space = space + 150
            
            # RAW 2
            
            #THIS RAW IS FOR ALL THE CHECKLISTS BEING CREATED WHEN YOU ADD
            #ITEM OR SHOT CHECKLIST
            
            
            ctx.set_source_rgb(1,1,1)
            ctx.set_font_size(15)
            ctx.move_to( 10,20+180)
            ctx.show_text("Starting Checklists") 
            
            
            ctx3.set_source_rgba(0,0,0,0.4)
            ctx3.rectangle(0, 30+180, w, 150)
            ctx3.fill()
            
            space = 0
            for n, i in enumerate(sorted(self.newfiles)):
                
                if i.endswith(".progress"):
                    
                    
                    self.chscroll
                    ctx3.set_source_rgba(0,0,0,0.4)
                    ctx3.rectangle(10+self.chscroll+space, 30+180+5, 140, 140)
                    ctx3.fill()
                    
                    ctx2.set_source_rgb(1,1,1)
                    ctx2.set_font_size(11)
                    ctx2.move_to( 10+30+self.chscroll+space,30+180+20)
                    ctx2.show_text(i[:i.find(".")])
                    
                    widget.window.draw_pixbuf(None, self.checkicon, 0, 0, 10+self.chscroll+space+5, 30+180+5, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                    
                    ct = open(self.pf+"/py_data/new_file/"+i, "r")
                    ct = ct.read()
                    
                    for c, t in enumerate(ct.split("\n")[9:9+15]):
                        ctx2.set_source_rgb(1,1,1)
                        ctx2.set_font_size(7)
                        ctx2.move_to( 12+self.chscroll+space,30+180+40+c*7)
                        ctx2.show_text(t[:34])
                    
                    
                    if my in range(30+180, 30+180+140) and mx in range(10+self.chscroll+space, 10+self.chscroll+space+140):
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#aaa"))
                        widget.window.draw_rectangle(xgc, False,  10+self.chscroll+space, 30+180+5, 140, 140)
                        
                        if  "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active():
                            checklist.checkwindow(pf=self.pf, title="NEW FILE FOR "+i[:i.find(".")], FILE=self.pf+"/py_data/new_file/"+i)
                            
                        
                        
            
                    space = space + 150
            
            
            # RAW 3
            
            # THIS RAW IS RESPONSIBLE FOR CONFIGURATION OF DIFFERENT BLENDER VERSIONS.
            # USERS MIGH HAVE MORE THEN 1 BLENDER INSTALLED. AND THIS IS A WAY TO 
            # SELECT WHAT BLENDER TO USE FOR BLEND FILES, ASSET CONFIGURATION AND RENDERING.
            
            
            ctx.set_source_rgb(1,1,1)
            ctx.set_font_size(15)
            ctx.move_to( 10,20+180+180)
            ctx.show_text("Blender Version") 
            
            
            ctx3.set_source_rgba(0,0,0,0.4)
            ctx3.rectangle(0, 30+180+180, w, 150)
            ctx3.fill()
            
            
            
            # add one more blenderversion
            
            
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#4c4c4c")) ## CHOSE COLOR
            if my in range(30+180+180-25, 30+180+180-5) and mx in range(140, 165):
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#000")) ## CHOSE COLOR
                widget.window.draw_rectangle(xgc, True, 138, 30+180+180-27,200, 25)
                
                ctx.set_source_rgb(1,1,1)
                ctx.set_font_size(15)
                ctx.move_to( 165, 20+180+180)
                ctx.show_text("Add Another Blender") 
                
                if "GDK_BUTTON1" in str(fx) and self.win.is_active():
                    if self.launchfolder:
                        glib.timeout_add(10, selfolder)
                        self.launchfolder = False
            
            widget.window.draw_pixbuf(None, self.plusicon, 0, 0, 140, 30+180+180-25, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
            
            space = 0
            
            NS = space + self.bvscroll
            
            #SYSTEM BLEDNER IF THERE IS SUCK
            if self.blendOS[0] == "Empty":
                if os.system("blender -v") == 32512:
                    self.blendOS[0] = False
                    self.blendOS[1] = False
                    self.blendOS[2] = False
                    
                    
                else:
                    checkframes = Popen(["blender", "-v"],stdout=PIPE, universal_newlines=True)
                    checkframes.wait()
                    checkstring = checkframes.stdout.read()
                    
                    
                    self.blendOS[0] = checkstring[:12]
                    #blenderplayer
                    if self.blendOS[1] == "Empty":
                        if os.system("blenderplayer --help") == 32512:
                            self.blendOS[1] = False
                        else:
                            self.blendOS[1] = True
                    
                    #blender-thumbnailer.py
                    if self.blendOS[2] == "Empty":
                        if os.system("blender-thumbnailer.py --help") == 32512:
                            self.blendOS[2] = False
                        else:
                            self.blendOS[2] = True
               
            # outputtin the results
            
            
            if self.blendOS[0]:
                    
                ctx3.set_source_rgba(0,0,0,0.4)
                ctx3.rectangle(10+self.bvscroll, 30+180+180+5, 140, 140)
                ctx3.fill()
                
                ctx2.set_source_rgb(1,1,1)
                ctx2.set_font_size(11)
                ctx2.move_to( 10+30+self.bvscroll,30+180+180+20)
                ctx2.show_text(str(self.blendOS[0]))
                
                
                
                widget.window.draw_pixbuf(None, self.blendicon, 0, 0, 12+self.bvscroll, 30+180+180+5, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                
                # system blender                
                
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#000")) ## CHOSE COLOR
                widget.window.draw_rectangle(xgc, True, 15+self.bvscroll, 30+180+180+5+30,20, 20)
                widget.window.draw_pixbuf(None, self.okayicon, 0, 0, 12+self.bvscroll+5, 30+180+180+5+30-5, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                
                ctx2.set_source_rgb(1,1,1)
                ctx2.set_font_size(10)
                ctx2.move_to( 10+30+self.bvscroll,30+180+180+20+30)
                ctx2.show_text("System Installed")
                
                # Game engine
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#000")) ## CHOSE COLOR
                widget.window.draw_rectangle(xgc, True, 15+self.bvscroll, 30+180+180+5+30+25,20, 20)
                ctx2.set_source_rgb(1,0,0)
                if self.blendOS[1]:
                    ctx2.set_source_rgb(1,1,1)
                    widget.window.draw_pixbuf(None, self.okayicon, 0, 0, 12+self.bvscroll+5, 30+180+180+5+30+25-5, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                
                ctx2.set_font_size(10)
                ctx2.move_to( 10+30+self.bvscroll,30+180+180+20+30+25)
                ctx2.show_text("Game Engine")
                
                 # Thumbnail support
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#000")) ## CHOSE COLOR
                widget.window.draw_rectangle(xgc, True, 15+self.bvscroll, 30+180+180+5+30+25+25,20, 20)
                ctx2.set_source_rgb(1,0,0)
                if self.blendOS[2]:
                    ctx2.set_source_rgb(1,1,1)
                    widget.window.draw_pixbuf(None, self.okayicon, 0, 0, 12+self.bvscroll+5, 30+180+180+5+30+25+25-5, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                
                ctx2.set_font_size(10)
                ctx2.move_to( 10+30+self.bvscroll,30+180+180+20+30+25+25)
                ctx2.show_text("Preview Support")
                
                
                 # collections (aka if it's after 2.80)
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#000")) ## CHOSE COLOR
                widget.window.draw_rectangle(xgc, True, 15+self.bvscroll, 30+180+180+5+30+25+25+25,20, 20)
                ctx2.set_source_rgb(1,0,0)
                
                try:
                    if float(self.blendOS[0][8:8+3]) > 2.79:
                        ctx2.set_source_rgb(1,1,1)
                        widget.window.draw_pixbuf(None, self.okayicon, 0, 0, 12+self.bvscroll+5, 30+180+180+5+30+25+25+25-5, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                except:
                    raise
                ctx2.set_font_size(10)
                ctx2.move_to( 10+30+self.bvscroll,30+180+180+20+30+25+25+25)
                ctx2.show_text("Collections")
                
                space = space + 150
                NS = space + self.bvscroll
                
                if self.choise == 0 or my in range(30+180+180, 30+180+180+140) and mx in range(10+self.bvscroll, 10+self.bvscroll+140):
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#aaa"))
                    widget.window.draw_rectangle(xgc, False,  10+self.bvscroll, 30+180+180+5, 140, 140)
                
                if my in range(30+180+180, 30+180+180+140) and mx in range(10+self.bvscroll, 10+self.bvscroll+140) and "GDK_BUTTON1" in str(fx) and self.win.is_active():
            
                    self.choise = 0
                    save()
            
            for n, i in enumerate(self.blendDATA):
                
                
                if self.blendDATA[n][1][0] == "Empty":
                    if os.path.exists(i[0]+"/blender"):
                        checkframes = Popen([i[0]+"/blender", "-v"],stdout=PIPE, universal_newlines=True)
                        checkframes.wait()
                        checkstring = checkframes.stdout.read()
                        
                        
                        self.blendDATA[n][1][0] = checkstring[:12]
                    else:
                        self.blendDATA[n][1][0] = False
                
                #blenderplayer
                if self.blendDATA[n][1][1] == "Empty":
                    if os.path.exists(i[0]+"/blenderplayer"):
                        self.blendDATA[n][1][1] = True
                    else:
                        self.blendDATA[n][1][1] = False
                
                #blender-thumbnailer.py
                if self.blendDATA[n][1][2] == "Empty":
                    if os.path.exists(i[0]+"/blender-thumbnailer.py"):
                        self.blendDATA[n][1][2] = True
                    else:
                        self.blendDATA[n][1][2] = False
                   
                # outputtin the results
                
                
                if self.blendDATA[n][1][0]:
                        
                    ctx3.set_source_rgba(0,0,0,0.4)
                    ctx3.rectangle(10+self.bvscroll+space, 30+180+180+5, 140, 140)
                    ctx3.fill()
                    
                    ctx2.set_source_rgb(1,1,1)
                    ctx2.set_font_size(11)
                    ctx2.move_to( 10+30+self.bvscroll+space,30+180+180+20)
                    ctx2.show_text(str(self.blendDATA[n][1][0]))
                    
                    
                    
                    widget.window.draw_pixbuf(None, self.blendicon, 0, 0, 12+self.bvscroll+space, 30+180+180+5, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                    
                    # system blender                
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#000")) ## CHOSE COLOR
                    widget.window.draw_rectangle(xgc, True, 15+self.bvscroll+space, 30+180+180+5+30,20, 20)
                    #widget.window.draw_pixbuf(None, self.okayicon, 0, 0, 12+self.bvscroll+5+space, 30+180+180+5+30-5, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                    
                    ctx2.set_source_rgb(1,0,0)
                    ctx2.set_font_size(10)
                    ctx2.move_to( 10+30+self.bvscroll+space,30+180+180+20+30)
                    ctx2.show_text("System Installed")
                    
                    # Game engine
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#000")) ## CHOSE COLOR
                    widget.window.draw_rectangle(xgc, True, 15+self.bvscroll+space, 30+180+180+5+30+25,20, 20)
                    ctx2.set_source_rgb(1,0,0)
                    if self.blendDATA[n][1][1]:
                        ctx2.set_source_rgb(1,1,1)
                        widget.window.draw_pixbuf(None, self.okayicon, 0, 0, 12+self.bvscroll+5+space, 30+180+180+5+30+25-5, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                    
                    ctx2.set_font_size(10)
                    ctx2.move_to( 10+30+self.bvscroll+space,30+180+180+20+30+25)
                    ctx2.show_text("Game Engine")
                    
                     # Thumbnail support
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#000")) ## CHOSE COLOR
                    widget.window.draw_rectangle(xgc, True, 15+self.bvscroll+space, 30+180+180+5+30+25+25,20, 20)
                    ctx2.set_source_rgb(1,0,0)
                    if self.blendDATA[n][1][2]:
                        ctx2.set_source_rgb(1,1,1)
                        widget.window.draw_pixbuf(None, self.okayicon, 0, 0, 12+self.bvscroll+5+space, 30+180+180+5+30+25+25-5, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                    
                    ctx2.set_font_size(10)
                    ctx2.move_to( 10+30+self.bvscroll+space,30+180+180+20+30+25+25)
                    ctx2.show_text("Preview Support")
                    
                    
                     # collections (aka if it's after 2.80)
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#000")) ## CHOSE COLOR
                    widget.window.draw_rectangle(xgc, True, 15+self.bvscroll+space, 30+180+180+5+30+25+25+25,20, 20)
                    ctx2.set_source_rgb(1,0,0)
                    
                    try:
                        if float(self.blendDATA[n][1][0][8:8+3]) > 2.79:
                            ctx2.set_source_rgb(1,1,1)
                            widget.window.draw_pixbuf(None, self.okayicon, 0, 0, 12+self.bvscroll+5+space, 30+180+180+5+30+25+25+25-5, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                    except:
                        pass
                    ctx2.set_font_size(10)
                    ctx2.move_to( 10+30+self.bvscroll+space,30+180+180+20+30+25+25+25)
                    ctx2.show_text("Collections")
                    
                    if self.choise == n+1 or my in range(30+180+180, 30+180+180+140) and mx in range(10+self.bvscroll+space, 10+self.bvscroll+space+140):
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#aaa"))
                        widget.window.draw_rectangle(xgc, False,  10+self.bvscroll+space, 30+180+180+5, 140, 140)
                    
                    if my in range(30+180+180, 30+180+180+140) and mx in range(10+self.bvscroll+space, 10+self.bvscroll+space+140) and "GDK_BUTTON1" in str(fx) and self.win.is_active():
                
                        self.choise = n+1
                        save()
                    
                    
        
                    #delete button
                    if my in range(30+180+180+7, 30+180+180+7+20) and mx in range(self.bvscroll+10+space+120, self.bvscroll+10+space+120+20):
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
                        widget.window.draw_rectangle(xgc, True,  self.bvscroll+10+space+120-2, 30+180+180+5, 20, 20)
                        
                        if  "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active():
                            self.dell = n
                    
                    widget.window.draw_pixbuf(None, self.deleteicon, 0, 0, self.bvscroll+10+space+120, 30+180+180+7, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                    
                    
                    space = space + 150
                    NS = space + self.bvscroll
            ######################################################################################
            #                                                                                    #
            #                            DRAW TILL HERE                                          #
            #                                                                                    #
            ######################################################################################
            
            
            
            
            #### SCROLL
            
            #BLENDER FILES SCROOLL
            if my in range(30, 30+140):
                if self.mpx > mx and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf) and self.win.is_active():
                    
                    self.blscroll = self.blscroll + (mx-self.mpx)
                    
                    
                
                if self.mpx < mx and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf) and self.win.is_active():
                    
                    self.blscroll = self.blscroll - (self.mpx-mx)
                        
            
            
            # CHECKLISTS SCROLL
            if my in range(30+180, 30+180+140):
                if self.mpx > mx and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf) and self.win.is_active():
                    
                    self.chscroll = self.chscroll + (mx-self.mpx)
                    
                    
                
                if self.mpx < mx and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf) and self.win.is_active():
                    
                    self.chscroll = self.chscroll - (self.mpx-mx)
            
            #BLENDER VERSIONS SCROOLL
            if my in range(30+180+180, 30+180+180+140):
                if self.mpx > mx and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf) and self.win.is_active():
                    
                    self.bvscroll = self.bvscroll + (mx-self.mpx)
                    
                    
                
                if self.mpx < mx and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf) and self.win.is_active():
                    
                    self.bvscroll = self.bvscroll - (self.mpx-mx)
            
            
            # deletion
            
            if self.dell > -1:
                del self.blendDATA[self.dell]
                self.dell = -1
                self.choise = 0
                
                save()
            
            
            # TESTING SOMETHING
            ctx.set_font_size(20)
            ctx.move_to( mx, my)
            #ctx.show_text(str(mx)+":"+str(my)+" "+str(fx)+"  "+str(self.scroll))    
            
            
            self.dW = w
            self.DH = h
            
            self.mpx = mx
            self.mpy = my
            self.mpf = fx
            
            
            def callback():
                if self.allowed == True:
                    widget.queue_draw()

            glib.timeout_add(10, callback)
            
            
        graph = gtk.DrawingArea()
        graph.set_size_request(500,500)
        
        self.box.pack_start(graph)
        graph.connect("expose-event", framegraph) 
        
        
        def selfolder():
            
            
            chosefolder = gtk.FileChooserDialog("CHOOSE FOLDER CONTAINING BLENDER",
                                             None,
                                             gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                                            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                             gtk.STOCK_OPEN, gtk.RESPONSE_OK))
            chosefolder.set_default_response(gtk.RESPONSE_OK)
            
            
            
            response = chosefolder.run()
            if response == gtk.RESPONSE_OK:
                
                get = chosefolder.get_filename()
                
                self.blendDATA.append([get, ["Empty", "Empty", "Empty"]])
                save()
            
            chosefolder.destroy()
            self.launchfolder = True
            
        def save():
            
            f = open(pf+"/py_data/blenderver.data", "w")
            f.write(str(self.choise)+"\n")
            for i in self.blendDATA:
                f.write(i[0]+"\n")
                
            f.close()
        
        ## GETTING BUTTON PRESS EVENTS
        def bpe( w, event):
            
            
            if event.keyval not in self.keys:
                self.keys.append( event.keyval )
            print self.keys
            
        def bre (w, event):    
            
            try:
                self.keys.remove( event.keyval )
            except:
                pass
            
            print self.keys
            
        self.win.connect("key_press_event", bpe)
        self.win.connect("key_release_event", bre)
        
        
        self.box.show_all()
