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
from subprocess import *

# self made modules

import thumbnailer
import dialogs
import checklist

import itemselector
import linkconfig
import history



def config(pf, path, blend):
    window = gtk.Dialog("Autolink Items : ", None, 0, (gtk.STOCK_OK,  gtk.RESPONSE_APPLY, 
                                                                                gtk.STOCK_CANCEL, gtk.RESPONSE_CLOSE))
    

    box = window.get_child()
    
    namebox = gtk.HBox(False)
    box.pack_start(namebox, False)
    
    #namebox.pack_start(gtk.Label(" Search: "), False)
    
    nameentry = gtk.Entry()
    #nameentry.set_text(searchitem)
    
    #namebox.pack_start(nameentry)
    
    finalname = gtk.Entry()
    finalname.set_text("")
    #namebox.pack_end(finalname, False)
    
    
    
    class draw:
        
        def __init__(self, pf, box , win, path, blend):
            
            self.box = box
            self.win = win
            self.pf = pf
            self.path = path
            self.blend = blend
            
            self.allowed = True
            self.scroll = 0
            
            self.dW = 0
            self.DH = 0
            
            self.mpx = 0
            self.mpy = 0
            self.mpf = ""
            
            self.objicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/obj_asset_undone.png")
            self.chricon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/chr_asset_undone.png")
            self.vehicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/veh_asset_undone.png")
            self.locicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/loc_asset_undone.png")
            
            self.plus = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/plus.png")
            self.delete = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/delete.png")
            
            self.settingsicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/settings.png")
            
            
            
            # GETTING DATA FROM AUTOLINK.DATA
            
            df = open(self.path, "r")
            df = df.read()
            print df
            
            #cleaning
            
            self.linkdata = []
            for line in df.split("\n"):
                if line.startswith("Link : "):
                    self.linkdata.append(line[7:])
            
            print self.linkdata
            
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
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#2b2b2b")) ## CHOSE COLOR
                widget.window.draw_rectangle(xgc, True, 0, 0, w, h)  ## FILL FRAME 
                
                
                #ctx.set_font_size(15)
                #ctx.move_to( 20, 20)
                #ctx.show_text(self.path) 
                
                #ctx.set_font_size(15)
                #ctx.move_to( 20, 40)
                #ctx.show_text(self.blend) 
                
                
                
                # OUTPUTTING THE LIST OF THE ITEM TO LINK HERE
                n = -1
                
                for n, i in enumerate(self.linkdata):
                    
                    
                    
                    #every even darker
                    if (n % 2) == 0:    
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#262626")) ## CHOSE COLOR
                        widget.window.draw_rectangle(xgc, True, 0, self.scroll+n*20+2,  w, 20)
                    
                    
                    config = False
                    #checking that isn't finished
                    if not os.path.exists(self.pf+"/ast/"+i[5:]+".blend"):
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#af5d5d")) ## CHOSE COLOR
                        widget.window.draw_rectangle(xgc, True, 0, self.scroll+n*20+2,  w, 20)
                        
                        ctx.set_font_size(15)
                        ctx.move_to( 52, 15+self.scroll+n*20)
                        ctx.show_text(i[i.rfind("/")+1:] + " [NOT FINISHED]")
                        
                    
                    elif not os.path.exists(self.pf+i+"/autolink.data"):
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#af5d5d")) ## CHOSE COLOR
                        widget.window.draw_rectangle(xgc, True, 0, self.scroll+n*20+2,  w, 20)
                        
                        ctx.set_font_size(15)
                        ctx.move_to( 52, 15+self.scroll+n*20)
                        ctx.show_text(i[i.rfind("/")+1:] + " [NOT CONFIGURED]")
                        config = True
                    
                    else:
                    
                        ctx.set_font_size(15)
                        ctx.move_to( 52, 15+self.scroll+n*20)
                        ctx.show_text(i[i.rfind("/")+1:])
                        config = True
                        
                    
                    
                    
                    if config:
                        #SETUP LINKABLE
                        
                        
                        
                        #
                        
                        if my in range(self.scroll+n*20+2, self.scroll+n*20+22) and my in range(0, h) and mx in range(0, 20):
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#395384")) ## CHOSE COLOR
                            widget.window.draw_rectangle(xgc, True, 0, self.scroll+n*20+2,  20, 20)
                            
                            
                            if "GDK_BUTTON1" in str(fx) and self.allowed and "GDK_BUTTON1" not in str(self.mpf) and win.is_active(): #IF CLICKED
                                
                                self.clickedtheconfigurebuttonat = i[5:]
                                def ee():   
                                    
                                    linkconfig.config(self.pf, self.clickedtheconfigurebuttonat )
                                    
                                glib.timeout_add(10, ee)
                        
                        
                        widget.window.draw_pixbuf(None, self.settingsicon, 0, 0, 1, self.scroll+n*20, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                    
                    
                    
                    
                    
                    if "/chr/" in i:
                        widget.window.draw_pixbuf(None, self.chricon, 0, 0, 30, self.scroll+n*20, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                    elif "/veh/" in i:
                        widget.window.draw_pixbuf(None, self.vehicon, 0, 0, 30, self.scroll+n*20, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                    elif "/loc/" in i:
                        widget.window.draw_pixbuf(None, self.locicon, 0, 0, 30, self.scroll+n*20, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                    elif "/obj/" in i:
                        widget.window.draw_pixbuf(None, self.objicon, 0, 0, 30, self.scroll+n*20, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                    
                    #DELETE
                    
                    #mouse over
                    if my in range(self.scroll+n*20+2, self.scroll+n*20+22) and my in range(0, h) and mx in range(w-22, w):
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#af5d5d")) ## CHOSE COLOR
                        widget.window.draw_rectangle(xgc, True, w-22, self.scroll+n*20+2,  20, 20)
                        
                        
                        if "GDK_BUTTON1" in str(fx) and self.allowed and "GDK_BUTTON1" not in str(self.mpf) and win.is_active(): #IF CLICKED
                            
                            
                            del self.linkdata[n]
                            self.save()
                    
                    
                    
                    widget.window.draw_pixbuf(None, self.delete, 0, 0, w-20, self.scroll+n*20+5, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                    
                    
                    
                
                # ADD MORE
                
                if my in range(self.scroll+n*20+2+20, self.scroll+n*20+22+20) and my in range(0, h) and mx in range(0, w):
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#395384")) ## CHOSE COLOR
                    widget.window.draw_rectangle(xgc, True, 0, self.scroll+n*20+2+20,  w, 20)
                    
                    
                    if "GDK_BUTTON1" in str(fx) and self.allowed and "GDK_BUTTON1" not in str(self.mpf) and win.is_active(): #IF CLICKED
                        
                        
                        def ee():   
                            
                            tmp = itemselector.select(self.pf)
                            
                            if tmp and tmp not in self.linkdata:
                                self.linkdata.append( tmp)
                                self.save()
                            
                        glib.timeout_add(10, ee)
                
                
                widget.window.draw_pixbuf(None, self.plus, 0, 0, 1, self.scroll+n*20+20, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                ctx.set_font_size(15)
                ctx.move_to( 30, 15+self.scroll+n*20+20)
                ctx.show_text("Add...")
                    
                
                
                
                
                
                
                # SCROLLING IT SELF
                # the scroll is done with the middle mouse button
                if self.mpy > my and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf) and mx in range(0, w):
                    self.scroll = self.scroll + (my-self.mpy)
                    
                if self.mpy < my and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf) and mx in range(0, w):
                    self.scroll = self.scroll - (self.mpy-my)
                
                
                #if self.scroll < 0-((n+al)*20)+h-33:  #THOSE VALUES HAVE TO BE REDONE
                #    self.scroll = 0-((n+al)*20)+h-33
                    
                if self.scroll > 0:
                    self.scroll = 0
                
                
            
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
                        

                glib.timeout_add(10, callback)
                
                
                
                
            graph = gtk.DrawingArea()
            graph.set_size_request(350,300)

            self.box.pack_start(graph)
            graph.show()
            graph.connect("expose-event", framegraph)         
        
        
        def save(self):
            
            df =  df = open(self.path, "w")
            for i in self.linkdata:
                df.write("Link : "+i+"\n")
            
            df.close()
        
        
    drawer = draw(pf, box, window, path, blend)

    box.show_all()
    r = window.run()
    
    ret = False
    
    
    cblndr = ""
             
             
                                        
    try:
        bv = open(pf+"/py_data/blenderver.data", "r")
        bv = bv.read().split("\n")
        
        print "BLENDER VERSION YOU LOOOKING FOR IS : ", bv
        
        if int(bv[0]) > 0:
            cblndr = bv[int(bv[0])]+"/"
    except:
        print "COULNT LOAD THE RIGHT BLENDER"
    
    
    
    if r == gtk.RESPONSE_APPLY:
        
        
        print "STARTING LINKING"
        
        checkframes = Popen([cblndr+"blender", "-b", blend , "-P", pf+"/py_data/modules/autolink.py"],stdout=PIPE, universal_newlines=True)

        checkframes.wait()
        checkstring = checkframes.stdout.read()
        
        print checkstring, "DONE"
        
        
        
        
        #WRITTING TO HYSTORY
        history.write(pf ,blend, "[Linked]")
        
        ret = finalname.get_text()
        
    
    window.destroy()
    return ret
    
