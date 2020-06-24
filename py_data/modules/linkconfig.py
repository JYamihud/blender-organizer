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






def config(pf, path):
    window = gtk.Dialog("Congure item as linkable asset", None, 0, ())#(gtk.STOCK_OK,  gtk.RESPONSE_APPLY, 
   #                                                gtk.STOCK_CANCEL, gtk.RESPONSE_CLOSE))
    

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
        
        def __init__(self, pf, box , win, path):
            
            self.box = box
            self.win = win
            self.pf = pf
            self.path = path
            
            self.allowed = True
            self.scroll = 0
            
            self.dW = 0
            self.DH = 0
            
            self.mpx = 0
            self.mpy = 0
            self.mpf = ""
            
            
            cblndr = ""
             
             
                                        
            try:
                bv = open(self.pf+"/py_data/blenderver.data", "r")
                bv = bv.read().split("\n")
                
                print "BLENDER VERSION YOU LOOOKING FOR IS : ", bv
                
                if int(bv[0]) > 0:
                    cblndr = bv[int(bv[0])]+"/"
            except:
                print "COULNT LOAD THE RIGHT BLENDER"
            
            
            
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
            
            self.collectionicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/collection.png")
            self.meshicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/mesh.png")
            
            
            self.plus = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/plus.png")
            
            self.blenddata = []
            
            
            
            
            
            
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
                
                # the asset blendfile to read from
                assetblend = self.pf+"/ast/"+self.path+".blend"
                
                
                
                # IF THE AST FILE IS ASSINGED
                
                
                if os.path.exists(assetblend): 
                    
                
                
                    #FILENAME
                    ctx.set_font_size(15)
                    ctx.move_to( 22,20+self.scroll)
                    ctx.show_text("/ast/"+self.path+".blend") 
                
                
                
                    if len(self.blenddata) == 0:
                        
                        # READING DATA
                        
                        checkframes = Popen([cblndr+"blender", "-b", assetblend , "-P", self.pf+"/py_data/modules/get_linkdata.py"],stdout=PIPE, universal_newlines=True)

                        checkframes.wait()
                        checkstring = checkframes.stdout.read()
                    
                        #print checkstring
                        
                        #self.blenddata.append(checkstring)
                        
                        
                        if "VERSION = SUCCESS" in checkstring:
                            
                            currentcollection = []
                            colname = ""
                            
                            for collection in checkstring.split("\n"):
                                if collection.startswith(">>>"):
                                    #print collection, "TESTING HERE"
                                    
                                    coln = collection[4:collection.find(" <== ")]
                                    if coln != colname:
                                        print coln, "COLLECTION"
                                        
                                        
                                        self.blenddata.append([[False, colname], currentcollection])
                                        currentcollection = []
                                    print "    |", collection[collection.find(" <== ")+5:], "OBJECT"
                                    
                                    currentcollection.append([False, collection[collection.find(" <== ")+5:]])
                                    
                                        
                                    colname = coln
                              
                            self.blenddata = self.blenddata[1:]
                            self.load()
                            #print self.blenddata
                                    
                        else:      
                            ctx.set_font_size(15)
                            ctx.move_to( 22,40)
                            ctx.show_text("Please update to Blender 2.80 or later") 
                            self.allowed = False
                
                
                
                    # WHEN DATA ALREADY LOADED
                    coly = 50
                    objy = 50
                    
                    ctx.set_font_size(14)
                    ctx.move_to( 22, 45+self.scroll)
                    ctx.show_text("Collections To Link") 
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#222222")) ## CHOSE COLOR
                    widget.window.draw_rectangle(xgc, True, 0, 55+self.scroll,  w/2-5, h-self.scroll)
                    
                    
                    
                    ctx.set_font_size(14)
                    ctx.move_to( w/2 + 22, 45+self.scroll)
                    ctx.show_text("Make Proxies") 
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#222222")) ## CHOSE COLOR
                    widget.window.draw_rectangle(xgc, True, w/2, 55+self.scroll,  w/2, h-self.scroll)
                    
                    
                    
                    for coln, collection in enumerate(self.blenddata): #FOR ALL THE COLLECTIONS
                        
                        
                        
                        colactive = collection[0][0] #WHETHER IS SELECTED
                        colname = collection[0][1] #NAME OF THE COLLECTION
                        colobjs = collection[1] #OBJECTS IN THIS COLLECTION
                        
                        
                        coly = coly + 22
                        
                        
                        #mouse over
                        if my in range(coly-18+self.scroll, coly+self.scroll) and my in range(0, h) and mx in range(0,w/2-5):
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#3f3f3f")) ## CHOSE COLOR
                            widget.window.draw_rectangle(xgc, True, 0, coly-18+self.scroll,  w/2-5, 22)
                            
                            
                            if "GDK_BUTTON1" in str(fx) and self.allowed and "GDK_BUTTON1" not in str(self.mpf) and win.is_active(): #IF CLICKED
                                
                                self.blenddata[coln][0][0] = not colactive
                                self.save()
                                
                        
                        if colactive:
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#395384")) ## CHOSE COLOR
                            widget.window.draw_rectangle(xgc, True, 0, coly-18+self.scroll,  w/2-5, 22)
                        
                        
                        
                        ctx.set_font_size(15)
                        ctx.move_to( 22, coly+self.scroll)
                        ctx.show_text(colname) 
                        
                        widget.window.draw_pixbuf(None, self.collectionicon, 0, 0, 1, coly+self.scroll-18, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                        
                        
                        
                        
                        if colactive:  #IF THIS COLLECTION IS ACTIVE
                            for objn, obj in enumerate(colobjs):
                                
                                
                                
                                objactive = obj[0]
                                objname = obj[1]
                                
                                
                                objy = objy + 22
                                
                                
                                #mouse over
                                if my in range(objy-18+self.scroll, objy+self.scroll) and my in range(0, h) and mx in range(w/2,w):
                                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#3f3f3f")) ## CHOSE COLOR
                                    widget.window.draw_rectangle(xgc, True, w/2, objy-18+self.scroll,  w, 22)
                                    
                                    
                                    if "GDK_BUTTON1" in str(fx) and self.allowed and "GDK_BUTTON1" not in str(self.mpf) and win.is_active(): #IF CLICKED
                                        
                                        self.blenddata[coln][1][objn][0] = not objactive
                                        self.save()
                                
                                if objactive:
                                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#395384")) ## CHOSE COLOR
                                    widget.window.draw_rectangle(xgc, True, w/2, objy-18+self.scroll,  w, 22)
                                    
                                
                                
                                
                                ctx.set_font_size(15)
                                ctx.move_to( w/2+22, objy+self.scroll)
                                ctx.show_text(objname) 
                        
                                widget.window.draw_pixbuf(None, self.meshicon, 0, 0, w/2, objy+self.scroll-18, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                
                                
                
                
                
                # IF ASSET FILE IS STILL NOT ASSINGED
                
                else:
                    
                    #test
                    ctx.set_font_size(15)
                    ctx.move_to( 20,20)
                    ctx.show_text("Finish the item first") 
                
                
                
                
                
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
            graph.set_size_request(400,400)

            self.box.pack_start(graph)
            graph.show()
            graph.connect("expose-event", framegraph)         
        
        
        def save(self):
            
            
            
            st = open(self.pf+"/dev/"+self.path+"/autolink.data", "w")
            for col in self.blenddata:
                
                if col[0][0]:
                    st.write("Link : "+col[0][1]+"\n")
                    
                    for obj in col[1]:
                        
                        if obj[0]:
                            st.write("Proxy : "+obj[1]+"\n")
            st.close()
            
        
        def load(self):
            
            try:
                st = open(self.pf+"/dev/"+self.path+"/autolink.data", "r")
                st = st.read()
                for cn, col in enumerate(self.blenddata):
                    
                    for line in st.split("\n"):
                        
                        if line.startswith("Link : ") and col[0][1] in line:
                            
                            self.blenddata[cn][0][0] = True
                            
                            
                            for on, obj in enumerate(col[1]):
                                
                                for line in st.split("\n"):
                                    
                                    if line.startswith("Proxy : ") and obj[1] in line:
                                        
                                        self.blenddata[cn][1][on][0] = True
                
            except:
                pass
        
        
    drawer = draw(pf, box, window, path)

    box.show_all()
    r = window.run()
    
    ret = False
    
    
    
    
    
    
    if r == gtk.RESPONSE_APPLY:
        ret = finalname.get_text()
        
    
    window.destroy()
    return ret
    
