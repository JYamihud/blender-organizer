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


# self made modules

import thumbnailer
import dialogs

class draw_blendver:
    
    def __init__(self, pf, box, win):
    
        self.pf = pf # pf stands for project folder. It's a string to know
                     # where the project's folders start with
        
        self.box = box # the gtk.Box() container to put this widget into
        
        self.win = win
        
        
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
        self.blendicon  = gtk.gdk.pixbuf_new_from_file(pf+"/py_data/icons/big_blendico.png")
        
        self.blendOS = ["Empty", "Empty", "Empty"]
        
        self.keys = []
        self.dell = -1
        
        
        self.scroll = 0        
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
            ctx.select_font_face("Sawasdee", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            
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
            
            
            
            space = 10
            
            NS = space + self.scroll
            
            
            # OS BASED VERSION
            
            xgc.line_width = 5
           
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#4c4c4c")) ## CHOSE COLOR
            widget.window.draw_rectangle(xgc, True, 10, NS, w-20, 120)
            if self.choise == 0 or my in range(NS, NS+140):
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#db3c16"))
                widget.window.draw_rectangle(xgc, False, 10, NS, w-20, 120)
            
            if my in range(NS, NS+140) and "GDK_BUTTON1" in str(fx) and self.win.is_active():
                
                self.choise = 0
                save()
            
            widget.window.draw_pixbuf(None, self.blendOSicon, 0, 0, 20, NS+10, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
            
            
            ctx.set_source_rgb(1,1,1)
            ctx.set_font_size(20)
            ctx.move_to( 150, NS+20)
            ctx.show_text("SYSTEM INSTALLED BLENDER") 
            
            ctx.set_font_size(20)
            ctx.move_to( 150, NS+45)
            ctx.show_text("Command: ") 
            
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#000")) ## CHOSE COLOR
            widget.window.draw_rectangle(xgc, True, 295, NS+24, w-320, 26)
            
            ctx2.set_source_rgb(1,1,1)
            ctx2.set_font_size(20)
            ctx2.move_to( 300, NS+45)
            ctx2.show_text("blender") 
            
            ctx.set_font_size(20)
            ctx.move_to( 150, NS+70)
            ctx.show_text("Blender Elements:") 
            
            # quickly checking the software
            
            #blender
            if self.blendOS[0] == "Empty":
                if os.system("blender --help") == 32512:
                    self.blendOS[0] = False
                else:
                    self.blendOS[0] = True
            
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
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#080")) ## CHOSE COLOR
            else:
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#800")) ## CHOSE COLOR
            widget.window.draw_rectangle(xgc, True, 145, NS+75, 300, 26)
            
            ctx2.set_source_rgb(1,1,1)
            ctx2.set_font_size(20)
            ctx2.move_to( 150, NS+95)
            ctx2.show_text("blender")
            
            if self.blendOS[1]:
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#080")) ## CHOSE COLOR
            else:
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#800")) ## CHOSE COLOR
            widget.window.draw_rectangle(xgc, True, 450, NS+75, 300, 26)
            
            ctx2.set_source_rgb(1,1,1)
            ctx2.set_font_size(20)
            ctx2.move_to( 455, NS+95)
            ctx2.show_text("blenderplayer")
            
            if self.blendOS[2]:
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#080")) ## CHOSE COLOR
            else:
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#800")) ## CHOSE COLOR
            widget.window.draw_rectangle(xgc, True, 755, NS+75, 300, 26)
            
            ctx2.set_source_rgb(1,1,1)
            ctx2.set_font_size(20)
            ctx2.move_to( 760, NS+95)
            ctx2.show_text("blender-thumbnailer.py")
            
            
            
            space = space + 140
            NS = space + self.scroll
            
            
            
            
            ######## OUTPUT THE LIST ####
            
            print self.blendDATA
            for n, i in enumerate(self.blendDATA):
                
                
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#4c4c4c")) ## CHOSE COLOR
                widget.window.draw_rectangle(xgc, True, 10, NS, w-20, 120)
                if self.choise == n+1 or my in range(NS, NS+140):
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#db3c16"))
                    widget.window.draw_rectangle(xgc, False, 10, NS, w-20, 120)
                    
                    if 65535 in self.keys and n+1 == self.choise:
                        self.dell = n
                        self.keys.remove(65535)
                        
                
                if my in range(NS, NS+140) and "GDK_BUTTON1" in str(fx) and self.win.is_active():
                
                    self.choise = n+1
                    save()
                    
                widget.window.draw_pixbuf(None, self.blendicon, 0, 0, 20, NS+10, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
                
                
                ctx.set_source_rgb(1,1,1)
                ctx.set_font_size(20)
                ctx.move_to( 150, NS+20)
                ctx.show_text("CUSTOM BLENDER") 
                
                ctx.set_font_size(20)
                ctx.move_to( 150, NS+45)
                ctx.show_text("Command: ") 
                
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#000")) ## CHOSE COLOR
                widget.window.draw_rectangle(xgc, True, 295, NS+24, w-320, 26)
                
                ctx2.set_source_rgb(1,1,1)
                ctx2.set_font_size(20)
                ctx2.move_to( 300, NS+45)
                ctx2.show_text(i[0]+"/blender") 
                
                
                ctx.set_font_size(20)
                ctx.move_to( 150, NS+70)
                ctx.show_text("Blender Elements:") 
                
                
                #blender
                if self.blendDATA[n][1][0] == "Empty":
                    if os.path.exists(i[0]+"/blender"):
                        self.blendDATA[n][1][0] = True
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
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#080")) ## CHOSE COLOR
                else:
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#800")) ## CHOSE COLOR
                widget.window.draw_rectangle(xgc, True, 145, NS+75, 300, 26)
                
                ctx2.set_source_rgb(1,1,1)
                ctx2.set_font_size(20)
                ctx2.move_to( 150, NS+95)
                ctx2.show_text("blender")
                
                if self.blendDATA[n][1][1]:
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#080")) ## CHOSE COLOR
                else:
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#800")) ## CHOSE COLOR
                widget.window.draw_rectangle(xgc, True, 450, NS+75, 300, 26)
                
                ctx2.set_source_rgb(1,1,1)
                ctx2.set_font_size(20)
                ctx2.move_to( 455, NS+95)
                ctx2.show_text("blenderplayer")
                
                if self.blendDATA[n][1][2]:
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#080")) ## CHOSE COLOR
                else:
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#800")) ## CHOSE COLOR
                widget.window.draw_rectangle(xgc, True, 755, NS+75, 300, 26)
                
                ctx2.set_source_rgb(1,1,1)
                ctx2.set_font_size(20)
                ctx2.move_to( 760, NS+95)
                ctx2.show_text("blender-thumbnailer.py")
                
                
                
                
                space = space + 140
                NS = space + self.scroll
            
            
            
            
            # add one more
            
            
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#4c4c4c")) ## CHOSE COLOR
            if my in range(NS, NS+32):
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#db3c16"))
                
                if "GDK_BUTTON1" in str(fx) and self.win.is_active():
                    if self.launchfolder:
                        glib.timeout_add(10, selfolder)
                        self.launchfolder = False
                    
            
            widget.window.draw_rectangle(xgc, True, 10, NS, w-20, 32)
            
            widget.window.draw_pixbuf(None, self.plusicon, 0, 0, 20, NS+5, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
            
            ctx.set_font_size(20)
            ctx.move_to( 50, NS+20)
            ctx.show_text("Add New Blender") 
            
            
            space = space + 40
            NS = space + self.scroll
            
            
            
            
            
            
            # deletion
            
            if self.dell > -1:
                del self.blendDATA[self.dell]
                self.dell = -1
                self.choise = 0
                
                save()
            ######################################################################################
            #                                                                                    #
            #                            DRAW TILL HERE                                          #
            #                                                                                    #
            ######################################################################################
            
            
            
            
            #### SCROLL
            
            if self.mpy > my and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf) and self.win.is_active():
                
                self.scroll = self.scroll + (my-self.mpy)
                
                
            
            if self.mpy < my and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf) and self.win.is_active():
                
                self.scroll = self.scroll - (self.mpy-my)
            
            
            
            
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
