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
def select(pf, searchitem=""):
    window = gtk.Dialog("Choose Item", None, 0, (gtk.STOCK_OK,  gtk.RESPONSE_APPLY, 
                                                   gtk.STOCK_CANCEL, gtk.RESPONSE_CLOSE))
    

    box = window.get_child()
    
    namebox = gtk.HBox(False)
    box.pack_start(namebox, False)
    
    namebox.pack_start(gtk.Label(" Search: "), False)
    
    nameentry = gtk.Entry()
    nameentry.set_text(searchitem)
    
    namebox.pack_start(nameentry)
    
    finalname = gtk.Entry()
    finalname.set_text("")
    #namebox.pack_end(finalname, False)
    
    
    
    class draw:
        
        def __init__(self, pf, box , win, search, finalname):
            
            self.box = box
            self.win = win
            self.pf = pf
            self.search = search
            self.finalname = finalname
            
            self.allowed = True
            self.scroll = 0
            
            self.dW = 0
            self.DH = 0
            
            self.mpx = 0
            self.mpy = 0
            self.mpf = ""
            
            
            # LET'S PREPARE ALL THE ITEMS
            
            self.listofitems = []
            
            for CUR in ["chr", "veh", "loc", "obj"]:
                
                print self.pf+"/dev/"+CUR
                
                for i in os.walk(self.pf+"/dev/"+CUR).next()[1]:
                    self.listofitems.append([CUR,i])
            
            
            
            self.objicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/obj_asset_undone.png")
            self.chricon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/chr_asset_undone.png")
            self.vehicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/veh_asset_undone.png")
            self.locicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/loc_asset_undone.png")
            
            
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
                
                
                
                
                #IF WE SEARCH
                
                showlist = self.listofitems
                if self.search.get_text() > 0:
                    
                    showlist = []
                    for i in self.listofitems:
                        if self.search.get_text().lower() in i[0].lower() or self.search.get_text().lower() in i[1].lower():
                            showlist.append(i)
                
                
                
                
                
                # SCROLL SO I COULD DO THAT
                
                
                S = self.scroll # the scroll value
                
                # OUTPUTTING THEM TO THE SCREEN
                n = 0
                i = ["", ""]
                sett = True
                for n, i in enumerate(sorted(showlist)):
                    
                    
                    hoti = (20*n)+S # HEIGHT OF THIS ITEM
                    
                    
                    #every even darker
                    if (n % 2) == 0:    
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#262626")) ## CHOSE COLOR
                        widget.window.draw_rectangle(xgc, True, 0, hoti+2,  w, 20)
                    
                    
                    
                    
                    #mouse over
                    if my in range(hoti+2, hoti+22) and my in range(0, h) and mx in range(0,w):
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#3f3f3f")) ## CHOSE COLOR
                        widget.window.draw_rectangle(xgc, True, 0, hoti+2,  w, 20)
                        
                        
                        if "GDK_BUTTON1" in str(fx) and self.allowed and "GDK_BUTTON1" not in str(self.mpf) and win.is_active() and sett: #IF CLICKED
                            self.finalname.set_text("/dev/"+i[0]+"/"+i[1])
                            sett = False
                    
                    # if selected   395384
                    if "/dev/"+i[0]+"/"+i[1] == self.finalname.get_text():
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#395384")) ## CHOSE COLOR
                        widget.window.draw_rectangle(xgc, True, 0, hoti+2,  w, 20)
                    
                    ctx.set_font_size(15)
                    ctx.move_to( 30, hoti+17)
                    ctx.show_text(i[1])
                
                    #drawing icons
                    if i[0] == "chr":
                        widget.window.draw_pixbuf(None, self.chricon, 0, 0, 1, hoti+2, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                    elif i[0] == "veh":
                        widget.window.draw_pixbuf(None, self.vehicon, 0, 0, 1, hoti+2, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                    elif i[0] == "loc":
                        widget.window.draw_pixbuf(None, self.locicon, 0, 0, 1, hoti+2, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                    elif i[0] == "obj":
                        widget.window.draw_pixbuf(None, self.objicon, 0, 0, 1, hoti+2, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                
                    
                    
                    
                    
                    
                
                
                
                
                # SCROLLING IT SELF
                # the scroll is done with the middle mouse button
                if self.mpy > my and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf):
                    self.scroll = self.scroll + (my-self.mpy)
                    
                if self.mpy < my and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf):
                    self.scroll = self.scroll - (self.mpy-my)
                
                
                if self.scroll < 0-(n*20)+h-33:
                    self.scroll = 0-(n*20)+h-33
                    
                if self.scroll > 0:
                    self.scroll = 0
                
                
            
                # TESTING SOMETHING
                ctx.set_font_size(20)
                ctx.move_to( mx, my)
                #ctx.show_text(str(mx)+":"+str(my)+"  "+str(self.winactive)+"   "+str(fx)+"   "+self.search.get_text()+"  "+self.finalname.get_text()) 
                
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
            graph.set_size_request(400,400)

            self.box.pack_start(graph)
            graph.show()
            graph.connect("expose-event", framegraph)         



    drawer = draw(pf, box, window, nameentry, finalname)

    box.show_all()
    r = window.run()
    
    ret = False
    
    if r == gtk.RESPONSE_APPLY:
        ret = finalname.get_text()
        
    
    window.destroy()
    return ret
    
