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
import dialogs
import checklist
import fileformats
def select(pf, searchitem=""):
    window = gtk.Dialog("Choose Image", None, 0, (gtk.STOCK_OK,  gtk.RESPONSE_APPLY, "Outside...", 666, 
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
            
            
            for r, d, f in os.walk(self.pf):
                for item in f:
                    for i in fileformats.images:
                        if item.endswith("."+i): 
                            self.listofitems.append([os.path.join(r, item).replace(self.pf, ""),"NO PIXBUF"])
            
            
            self.IsNowProcessing = False
            
            self.objicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/obj_asset_undone.png")
            self.chricon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/chr_asset_undone.png")
            self.vehicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/veh_asset_undone.png")
            self.locicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/loc_asset_undone.png")
            self.foldericon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/folder.png")
            self.scnicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/scn_asset_undone.png")
            self.picicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/pic.png")
            
            self.plus = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/plus.png")
            
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
                
                
                rx = 0
                ry = 20
                
                prevf = ""
                foundcount = 0
                
                for n, i in enumerate(self.listofitems):
                    
                    docont = False
                    if nameentry.get_text():
                        for name in nameentry.get_text().upper().split(" "):
                            if name not in i[0].upper():
                                docont = True
                    
                    if docont:
                        continue
                    
                    foundcount = foundcount + 1
                    
                    fol = i[0][:i[0].rfind("/")] #FOLDER NAME
                    fin = i[0][i[0].rfind("/")+1:] #FILENAME
                    
                    if prevf != fol:
                        
                        if rx != 0:
                            ry = ry + 150
                        
                        if "/dev/" in fol:
                            
                            if self.scroll+ry in range(-150, h):
                                needicon = self.chricon
                                if "/obj/" in fol:
                                    needicon = self.objicon
                                elif "/loc/" in fol:
                                    needicon = self.locicon
                                elif "/veh/" in fol:
                                    needicon = self.vehicon
                                
                                widget.window.draw_pixbuf(None, needicon, 0, 0, 1, self.scroll+ry-17, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                                
                                
                                ctx.set_font_size(15)
                                ctx.move_to( 30, self.scroll+ry)
                                
                                na = fol[:fol.rfind("/")]
                                na = na[na.rfind("/")+1:]
                                
                                ctx.show_text(na)
                            ry = ry + 20
                            if self.scroll+ry in range(-150, h):
                                widget.window.draw_pixbuf(None, self.foldericon, 0, 0, 20, self.scroll+ry-17, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                                
                                ctx.move_to( 50, self.scroll+ry)
                                ctx.show_text(fol[fol.rfind("/")+1:])
                            ry = ry + 20
                            
                        else:
                            if self.scroll+ry in range(-150, h):
                                needicon = self.foldericon
                                
                                if fol.startswith("/rnd/"):
                                    needicon = self.scnicon
                                
                                widget.window.draw_pixbuf(None, needicon, 0, 0, 1, self.scroll+ry-17, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                                
                                ctx.set_font_size(15)
                                ctx.move_to( 30, self.scroll+ry)
                                ctx.show_text(fol)
                            ry = ry + 20
                    
                        rx = 0
                        
                    if self.scroll+ry in range(-150, h):  # WITHOUT THIS IT HIT AN OVERFLOW AND BROKE GTK LOL
                        ctx3 = widget.window.cairo_create()
                        ctx3.set_source_rgba(0,0,0,0.4)
                        ctx3.rectangle(rx, self.scroll+ry+10,100, 100)
                        ctx3.fill()
                        
                        if i[1] == "NO PIXBUF": 
                            if not self.IsNowProcessing:
                                self.IsNowProcessing = True
                                
                                def ee(n, i):
                                    self.listofitems[n][1] = gtk.gdk.pixbuf_new_from_file(thumbnailer.thumbnail(self.pf+i[0], 100,100))
                                    self.IsNowProcessing = False
                                glib.timeout_add(10, ee, n, i)
                            
                            
                            
                        else:
                            
                            center_X = (100-i[1].get_width())/2
                            center_Y = (100-i[1].get_height())/2 
                            
                            
                            mox = rx
                            moy = self.scroll+ry+10
                            
                            
                            imx = mox   + center_X
                            imy = moy   + center_Y
                            
                            
                            widget.window.draw_pixbuf(None, i[1], 0, 0, imx, imy, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                        
                        
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#8a7d2c"))
                        widget.window.draw_rectangle(xgc, True, rx, self.scroll+ry-5, 100, 20)
                        
                        widget.window.draw_pixbuf(None, self.picicon, 0, 0, rx, self.scroll+ry-5, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                        
                        
                        
                        ctx.set_font_size(10)
                        ctx.move_to( rx+20, self.scroll+ry+7)
                        ctx.show_text(fin[:12])
                        
                        if mx in range(rx, rx+100) and my in range(self.scroll+ry-5, self.scroll+ry-5+150) and mx in range(0,w) and my in range(0, h):
                            
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#fff"))
                            widget.window.draw_rectangle(xgc, False, rx, self.scroll+ry-5, 100, 115)
                            
                            if "GDK_BUTTON1" in str(fx) and self.allowed and "GDK_BUTTON1" not in str(self.mpf) and win.is_active():
                            
                                finalname.set_text(self.pf+i[0])
                            
                        if finalname.get_text() == self.pf+i[0]:
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#fff"))
                            widget.window.draw_rectangle(xgc, False, rx, self.scroll+ry-5, 100, 115)
                        
                    rx = rx + 120
                    
                    if rx > w-120:
                        
                        rx = 0
                        ry = ry + 150
                
                    prevf = fol
                
                
                infoy = 0
                if my in range(0, 30):
                    infoy = h - 30
                
                ctx3 = widget.window.cairo_create()
                ctx3.set_source_rgba(0,0,0,0.7)
                ctx3.rectangle(w-202, 3+infoy,w, 24)
                ctx3.fill()
                
                
                ctx.set_font_size(15)
                ctx.move_to( w-200, 20+infoy)
                ctx.show_text("Found "+str(foundcount)+" images")
                
                
                # SCROLLING IT SELF
                # the scroll is done with the middle mouse button
                if self.mpy > my and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf):
                    self.scroll = self.scroll + (my-self.mpy)
                    
                if self.mpy < my and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf):
                    self.scroll = self.scroll - (self.mpy-my)
                
                
                if self.scroll < 0-ry-150+h-33:
                    self.scroll = 0-ry-150+h-33
                    
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
                        

                glib.timeout_add(1, callback)
                
                
                
                
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
    elif r == 666:
        # FILE CHOOSER
        window.destroy()
        addbuttondialog = gtk.FileChooserDialog("CHOOSE IMAGE",
                                         None,
                                         gtk.FILE_CHOOSER_ACTION_OPEN,
                                        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                         gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        addbuttondialog.set_default_response(gtk.RESPONSE_OK)
        addbuttondialog.set_current_folder(os.getcwd())
        
        
        
        response = addbuttondialog.run()
        if response == gtk.RESPONSE_OK:
            
            ret = addbuttondialog.get_filename()
        addbuttondialog.destroy()
    window.destroy()
    return ret
    
