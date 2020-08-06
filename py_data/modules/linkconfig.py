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
import history





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
            
            
            
            
            self.objicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/obj_asset_undone.png")
            self.chricon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/chr_asset_undone.png")
            self.vehicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/veh_asset_undone.png")
            self.locicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/loc_asset_undone.png")
            self.settingsicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/settings.png")
            self.collectionicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/collection.png")
            self.meshicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/mesh.png")
            
            self.blendericon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/blender.png")
            self.plus = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/plus.png")
            
            self.blenddata = []
            
            
            # FOR THE CREATOR OF THE AST
            self.itemblends = []
            self.itemblendsselect = 0
            
            l = 0
            for FILE in os.walk(self.pf+"/dev/"+self.path).next()[2]:
            
                if FILE.endswith(".blend"):
                
                    self.itemblends.append(FILE)
                    
                    print FILE, "BLENDFILE "
                    
                    
                    if FILE == self.path[4:]+".blend":
                        
                        
                        self.itemblendsselect = l
                        print FILE, "THIS IS THE ONE", self.itemblendsselect
                    
                    l = l + 1
            
            
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
                        
                        print "########## ALL THE DATA FROM BLENDER ##########\n\n", checkstring, "\n\n############## DONE ##############"
                        
                        
                        if "VERSION = SUCCESS" in checkstring:
                            
                            currentcollection = []
                            colname = ""
                            
                            for collection in checkstring.split("\n"):
                                if collection.startswith(">>>"):
                                    #print collection, "TESTING HERE"
                                    
                                    if " <== " in collection:
                                        coln = collection[4:collection.find(" <== ")]
                                        if coln != colname:
                                            print coln, "COLLECTION"
                                            
                                            
                                            self.blenddata.append([[False, colname], currentcollection])
                                            currentcollection = []
                                        print "    |", collection[collection.find(" <== ")+5:], "OBJECT"
                                        
                                        currentcollection.append([False, collection[collection.find(" <== ")+5:]])
                                        colname = coln
                                    else:
                                          coln = collection[4:]
                                          self.blenddata.append([[False, coln], []])
                                          
                                          #colname = coln
                                    
                                if collection.startswith("VERSION"): # GETTING THE LAST THING IN THE LIST
                                    self.blenddata.append([[False, colname], currentcollection])
                                
                                
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
                    
                    
                    percent = checklist.partcalculate(checklist.openckecklist(self.pf+"/dev/"+self.path+"/asset.progress"))
                    
                    
                    # IF CHECKLIST IF NOT YET FULLY DONE
                    if percent < 0.99:
                        
                        #test
                        ctx.set_font_size(15)
                        ctx.move_to( 20,20)
                        ctx.show_text("Checklist is at "+str(percent*100)+"%") 
                    
                        ctx.set_font_size(15)
                        ctx.move_to( 20,40)
                        ctx.show_text("Please return when this asset is fully created.") 
                    
                    if percent > 0.98:
                        
                        ctx.set_font_size(15)
                        ctx.move_to( 20,20+self.scroll)
                        ctx.show_text("You are ready to create the /AST/ BLEND FILE") 
                        
                        ctx.set_font_size(15)
                        ctx.move_to( 20,40+self.scroll)
                        ctx.show_text("If changes will be nessesary you will need")
                        
                        ctx.set_font_size(15)
                        ctx.move_to( 20,60+self.scroll)
                        ctx.show_text("to edit /ast/"+self.path+".blend manually.")
                        
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#222222")) ## CHOSE COLOR
                        widget.window.draw_rectangle(xgc, True, 0, 80+self.scroll,  w/3*2, h-self.scroll)
                        #self.itemblends
                        #self.itemblendsselect
                        
                        for n, i in enumerate(self.itemblends):
                            
                            # IF THIS BLENDFILE SELECTED
                            if n == self.itemblendsselect:
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#395384")) ## CHOSE COLOR
                                widget.window.draw_rectangle(xgc, True, 0, 100+self.scroll+n*20-18,  w/3*2, 20)
                                
                                #mouse over blendfile
                                if my in range(100+self.scroll+n*20-18, 100+self.scroll+n*20-18+20) and my in range(0, h) and mx in range(w/3*2, w):
                                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#3f3f3f")) ## CHOSE COLOR
                                    widget.window.draw_rectangle(xgc, True, w/3*2, 100+self.scroll+n*20-18,  w/3*2, 20)
                                    
                                    
                                    if "GDK_BUTTON1" in str(fx) and self.allowed and "GDK_BUTTON1" not in str(self.mpf) and win.is_active(): #IF CLICKED
                                        
                                        print "BEFORECHECK"
                                        checkframes = Popen([cblndr+"blender", "-b", self.pf+"/dev/"+self.path+"/"+i , "-P", self.pf+"/py_data/modules/makeast.py"],stdout=PIPE, universal_newlines=True)

                                        checkframes.wait()
                                        checkstring = checkframes.stdout.read()
                                        print checkstring, "CHECKSTRING"
                                
                                
                                
                                widget.window.draw_pixbuf(None, self.settingsicon, 0, 0, w/3*2+2, 100+self.scroll+n*20-18, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                                ctx.set_font_size(15)
                                ctx.move_to( w/3*2+30,100+self.scroll+n*20)
                                ctx.show_text("Make /AST/")
                                
                            #mouse over blendfile
                            if my in range(100+self.scroll+n*20-18, 100+self.scroll+n*20-18+20) and my in range(0, h) and mx in range(0,w/3*2):
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#3f3f3f")) ## CHOSE COLOR
                                widget.window.draw_rectangle(xgc, True, 0, 100+self.scroll+n*20-18,  w/3*2, 20)
                                
                                
                                if "GDK_BUTTON1" in str(fx) and self.allowed and "GDK_BUTTON1" not in str(self.mpf) and win.is_active(): #IF CLICKED
                                    self.itemblendsselect = n
                                        
                            
                            ctx.set_font_size(15)
                            ctx.move_to( 30,100+self.scroll+n*20)
                            ctx.show_text(i)
                            
                            widget.window.draw_pixbuf(None, self.blendericon, 0, 0, 2, 100+self.scroll+n*20-18, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                            
                            
                        
                
                
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
                        

                glib.timeout_add(1, callback)
                
                
                
                
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
            
            #WRITTING TO HYSTORY
            history.write(self.pf ,"/dev/"+self.path+"/autolink.data", "[Updated]")
        
        def load(self):
            
            try:
                st = open(self.pf+"/dev/"+self.path+"/autolink.data", "r")
                st = st.read()
                for cn, col in enumerate(self.blenddata):
                    
                    for line in st.split("\n"):
                        
                        if line.startswith("Link : ") and col[0][1] == line[7:]:
                            
                            self.blenddata[cn][0][0] = True
                            
                            
                            for on, obj in enumerate(col[1]):
                                
                                for line in st.split("\n"):
                                    
                                    if line.startswith("Proxy : ") and obj[1] == line[8:]:
                                        
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
    
