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
import checklist
import quick
from subprocess import *

class main:
    
    def __init__(self, pf):
        
        print "RENDER LISTS WINDOW"
        
        self.pf = pf
        
        self.win = gtk.Window()
        self.win.set_title("RENDER LISTS EDITOR")
        self.win.set_default_size(800,800)
        self.win.set_position(gtk.WIN_POS_CENTER)

        self.mainbox = gtk.VBox(False)
        self.win.add(self.mainbox)
        
        
        
        self.allowed = True
        
        
        self.RLISTS = []
        
        # LOAD THE FILES
        self.load()
        
        
        
        self.mainscroll = 0
        
        
        
        
        ## ICONS LOAD
        
        self.plus = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/plus.png")
        self.render = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/render.png")
        self.render_big = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/render_big.png")
        
        self.delete = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/delete.png")
        
        
        
        
        
        
        
        # HELPERS
        
        self.dW = 0
        self.DH = 0
        
        self.mpx = 0
        self.mpy = 0
        self.mpf = 0
        
        
        
        # GRAB TOOL
        
        self.tool = "select" # JUST A TOOL WITH NO PARTICULAR THING
        self.grab = [0,0] # IND of FILE, IND of BLEND
        self.grabbed = False
        
            
        graph = gtk.DrawingArea()
        graph.set_size_request(500,700)
        
        self.mainbox.pack_start(graph)
        graph.connect("expose-event", self.framegraph) 
        
        
        
        self.FRAMES = 0
        
        
        self.win.show_all()
    
    
    
    #### THIS FUNCTION IS HERE TO LOAD DATA ###
    def load(self):
        self.FRAMES = 0
        self.RLISTS = []
        
        for FILE in sorted(os.listdir(self.pf+"/py_data/rnd_seq")):
            
            #print FILE
            
            infile = []
            
            readfile = open(self.pf+"/py_data/rnd_seq/"+FILE, "r")
            readfile = readfile.read().split("\n")
            
            for blend in readfile:
                
                if blend.endswith(".blend") and os.path.exists(self.pf+"/"+blend):
                    #print blend
                    infile.append([False, blend])
    
            self.RLISTS.append([FILE, 0, infile]) #NAME OF THE LIST > SCROLL > LIST OF BLENDS IN THIS FILE
    
    #### THIS FUNCTION DRAWS THE PIXELS IN THE WINDOW ####
    def framegraph(self, widget, event):
             
        self.FRAMES = self.FRAMES + 1
        if self.FRAMES > 9999:
            self.FRAMES = 0
                                               
        w, h = widget.window.get_size()
        xgc = widget.window.new_gc()
        
        mx, my, fx  = widget.window.get_pointer()
        
        
        # GETTING WHETHER THE WINDOW IS ACTIVE
        
        self.winactive = self.win.is_active()
        
        ctx = widget.window.cairo_create()
        ctx.select_font_face("Sawasdee", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        
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
        ctx3.set_source_rgba(0.2,0.2,0.2,0.8)
        ctx3.rectangle(0, 0, w, h)
        ctx3.fill()
        
        
        
        
        widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.ARROW))
        #############################################################################
        ############################# DRAW HERE #####################################
        #############################################################################
        if self.tool == "select":
            widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.ARROW))
        elif self.tool == "grab":
            widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.FLEUR))
        if self.grabbed:
            self.tool = "select"
            self.grabbed = False
        if "GDK_BUTTON3" in str(fx) and "GDK_BUTTON3" not in str(self.mpf) and self.win.is_active():
            self.tool = "select"
        
        
        
        listY = 200
        
        
        
        #SCROLL
        
        if self.mpy > my and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf) and self.win.is_active():
                    
            self.mainscroll = self.mainscroll + (my-self.mpy)
        
        if self.mpy < my and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf) and self.win.is_active():
                    
            self.mainscroll = self.mainscroll - (self.mpy-my)
        
        
        if self.mainscroll < 0-(len(self.RLISTS)*listY-h):
            self.mainscroll = 0-(len(self.RLISTS)*listY-h)
            
        if self.mainscroll > 0:
            self.mainscroll = 0
        
        
        
        for ind,  LIST in enumerate(self.RLISTS):
            
            blendX = 100
            
            
            ### SCROLL ###
            
            if my in range((listY*ind)+self.mainscroll+20, (listY*ind)+self.mainscroll+20+listY):
            
                if self.mpx > mx and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf) and self.win.is_active():
                        
                    self.RLISTS[ind][1] = self.RLISTS[ind][1] + (mx-self.mpx)
                
                if self.mpx < mx and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf) and self.win.is_active():
                            
                    self.RLISTS[ind][1] = self.RLISTS[ind][1] - (self.mpx-mx)
                
                if self.RLISTS[ind][1] < 0-(len(LIST[2])*(blendX+40)-w):
                    self.RLISTS[ind][1] = 0-(len(LIST[2])*(blendX+40)-w)
                
                if self.RLISTS[ind][1] > 0:
                    self.RLISTS[ind][1] = 0
            
            
            # RLIST FRAME
            
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#3f3f3f")) ## CHOSE COLOR
            #widget.window.draw_rectangle(xgc, True, 0, (listY*ind)+self.mainscroll+20, w, listY-20)
            
            ctx3 = widget.window.cairo_create()
            ctx3.set_source_rgba(0,0,0,0.4)
            ctx3.rectangle(0, (listY*ind)+self.mainscroll+20, w, listY-20)
            ctx3.fill()
            
            
            
            
            
            
            
            ### DELETE LIST ICON ####
            
            # MOUSE OVER
            if mx in range(w-22, w) and my in range((listY*ind)+self.mainscroll+15, (listY*ind)+self.mainscroll+15+22):
                
                
                
                
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#e47649")) ## CHOSE COLOR
                widget.window.draw_rectangle(xgc, True, w-23, (listY*ind)+self.mainscroll+14, 18, 18)
            
                if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active():
                    
                    widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
                    
                    try:
                        os.remove(self.pf+"/py_data/rnd_seq/"+LIST[0])
                    except:
                        pass
                    self.load()
                
            
            widget.window.draw_pixbuf(None, self.delete, 0, 0, w-22, (listY*ind)+self.mainscroll+15 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
            
            
            
            ## TITLE ##
            ctx.set_source_rgb(1,1,1)
            ctx.set_font_size(15)
            ctx.move_to( 40, (listY*ind)+self.mainscroll+37)
            ctx.show_text(LIST[0])
        
        
            ##### THE INSIDE FILES ##
            
            
            list_scroll = LIST[1]
            
            
            rendrnow = True
            checkedfirstrendnow = False
            
            
            if len(LIST[2]) == 0 and self.tool == "grab":
                
                if my in range((listY*ind)+self.mainscroll+15, (listY*ind)+self.mainscroll+15 + listY):
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#4c4c4c")) ## CHOSE COLOR
                    widget.window.draw_rectangle(xgc, True, 5 , (listY*ind)+self.mainscroll+50-2, blendX+4, blendX+4) 
                
                    # IF RELESED
                    if "GDK_BUTTON1" not in str(fx) and "GDK_BUTTON1" in str(self.mpf) and self.win.is_active():
                        
                        
                        # moving line is like copying it first
                        # and then deleting the previous one
                        
                        ### MARK ###
                        
                        # marking to delete the line
                        
                        print self.RLISTS[self.grab[0]][2][self.grab[1]][1]
                        
                        delete_filename = self.RLISTS[self.grab[0]][0]
                        delete_file = open(self.pf+"/py_data/rnd_seq/"+delete_filename, "r")
                        delete_file = delete_file.read().split("\n")
                        
                        print "\n----- DELETE FILE ------ (before)\n"
                        for dn,  i in enumerate(delete_file):
                            print i
                            if i == self.RLISTS[self.grab[0]][2][self.grab[1]][1]:
                                delete_file[dn] = "!!!DELETE!!!"
                        print "\n----- DELETE FILE ------ (after)\n"
                        for dn,  i in enumerate(delete_file):
                            print i
                            
                        if delete_file[-1] == "":
                            delete_file = delete_file[:-1]
                        
                        
                        
                        
                        save = open(self.pf+"/py_data/rnd_seq/"+delete_filename, "w")
                        
                        for i in delete_file:   
                            save.write(i+"\n")
                        
                        save.close()
                        
                        
                        
                        ### INSERT ####
                        
                        insert_filename = self.RLISTS[ind][0]
                        save = open(self.pf+"/py_data/rnd_seq/"+insert_filename, "w")
                        
                        save.write(self.RLISTS[self.grab[0]][2][self.grab[1]][1]+"\n")
                        save.close()
                        
                        ### REMOVE ####
                        
                        delete_filename = self.RLISTS[self.grab[0]][0]
                        delete_file = open(self.pf+"/py_data/rnd_seq/"+delete_filename, "r")
                        delete_file = delete_file.read().split("\n")
                        delete_file.remove("!!!DELETE!!!")
                        if delete_file[-1] == "":
                            delete_file = delete_file[:-1]
                        
                        
                        
                        
                        save = open(self.pf+"/py_data/rnd_seq/"+delete_filename, "w")
                        
                        for i in delete_file:   
                            save.write(i+"\n")
                        save.close()
                        
                        
                        self.load()
                        self.grabbed =True
            
            
            ## IF THERE ARE BLENDS
            for n, BLEND in enumerate(LIST[2]):
                
                
                
                if self.tool == "grab" and self.grab[0] == ind and self.grab[1] == n:
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#4c4c4c")) ## CHOSE COLOR
                    widget.window.draw_rectangle(xgc, True, ((blendX+40)*n)+list_scroll-2 , (listY*ind)+self.mainscroll+50-2, blendX+4, blendX+4)
                    
                    
                      
                    
                else:
                        
                    
                    # GETTING FILE PERCENTAGE #
                    
                    
                    START = 1
                    END = 1
                    FOLDER = "storyboard"
                    FORMAT = "PNG"
                    
                    try:
                        rndfile = open(self.pf+"/"+BLEND[1][:BLEND[1].rfind("/")]+"/extra/"+BLEND[1][BLEND[1].rfind("/")+1:]+".rnd", "r")
                        for line in rndfile.read().split("\n"):
                            
                            if line.startswith("START = "):
                        
                                START = int(line[line.find("= ")+1:])
                            
                            if line.startswith("END = "):
                                
                                END = int(line[line.find("= ")+1:])
                        
                            if line.startswith("FORMAT = "):
                                
                                FORMAT = str(line[line.find("= ")+1:]).strip()
                            
                            if line.startswith("FOLDER = "):
                                
                                FOLDER = str(line[line.find("= ")+1:]).strip()
                        
                        framnames = []
                        
                        for frame in range(START, END+1):
                            framnames.append(quick.getfileoutput(frame, FORMAT))
                        
                        count = 0
                        
                        for i in os.listdir(self.pf+FOLDER):
                            if i in framnames:
                                
                                count = count + 1
                        
                        BLEND_COMP  = float(count)/float(END+1-START)
                    except:
                        pass
                        
                    #print BLEND_COMP
                        
                    
                        
                    ctx.set_source_rgb(1,1,1)
                    ctx.set_font_size(10)
                    ctx.move_to( ((blendX+40)*n)+list_scroll+10, (listY*ind)+self.mainscroll+listY-25)
                    ctx.show_text(str(int(BLEND_COMP*100))+" %")
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#4c4c4c")) ## CHOSE COLOR
                    widget.window.draw_rectangle(xgc, True, ((blendX+40)*n)+list_scroll, (listY*ind)+self.mainscroll+listY-10,  blendX, 2)
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#e47649")) ## CHOSE COLOR
                    widget.window.draw_rectangle(xgc, True, ((blendX+40)*n)+list_scroll, (listY*ind)+self.mainscroll+listY-10,  int(blendX*BLEND_COMP), 2)
                    
                    
                    
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#4c4c4c")) ## CHOSE COLOR
                    widget.window.draw_rectangle(xgc, True, ((blendX+40)*n)+list_scroll , (listY*ind)+self.mainscroll+50, blendX, blendX)
                    
                    
                    ## TITLE ##
                    ctx.set_source_rgb(1,1,1)
                    ctx.set_font_size(10)
                    ctx.move_to( ((blendX+40)*n)+list_scroll+10, (listY*ind)+self.mainscroll+listY-40)
                    ctx.show_text(BLEND[1][BLEND[1].rfind("/")+1:])
            
                    
                    ### REMOVE BUTTON ####
                    
                    # MOUSE OVER
                    if mx in range(((blendX+40)*n)+list_scroll+blendX, ((blendX+40)*n)+list_scroll+blendX+16) and my in range((listY*ind)+self.mainscroll+40, (listY*ind)+self.mainscroll+40+16):
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#e47649")) ## CHOSE COLOR
                        widget.window.draw_rectangle(xgc, True, ((blendX+40)*n)+list_scroll+blendX-1, (listY*ind)+self.mainscroll+39, 18, 18)
                        
                        if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active():
                        
                            widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
                            
                            try:
                                DF = open(self.pf+"/py_data/rnd_seq/"+LIST[0], "r")
                                DF = DF.read().split("\n")
                                
                                NF = ""
                                
                                for d in DF:
                                    
                                    if BLEND[1] not in d:
                                        NF = NF + d+"\n"
                                        
                                
                                SF = open(self.pf+"/py_data/rnd_seq/"+LIST[0], "w")
                                SF.write(NF)
                                SF.close()
                                         
                                
                                
                                
                            except:
                                pass
                            self.load()
                        
                    
                    
                    widget.window.draw_pixbuf(None, self.delete, 0, 0, ((blendX+40)*n)+list_scroll+blendX, (listY*ind)+self.mainscroll+40 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
                    
                    # IF IT'S RENDERING CURRENTLY
                    
                    if int(BLEND_COMP) == 1:
                        
                        rendrnow = False
                    
                    if rendrnow:
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#e47649")) ## CHOSE COLOR
                        widget.window.draw_rectangle(xgc, True, ((blendX+40)*n)+list_scroll-2 , (listY*ind)+self.mainscroll+50-2, blendX+4, blendX+4)
                        rendrnow= False
                        checkedfirstrendnow = True
                    
                    if int(BLEND_COMP) == 1 and checkedfirstrendnow == False:
                        
                        rendrnow = True
                    
                    
                    
                            
                    ### IMAGE ###
                    
                    if BLEND[0] and BLEND[0] != "None":
                        
                        widget.window.draw_pixbuf(None, BLEND[0], 0, 0, ((blendX+40)*n)+list_scroll, (listY*ind)+self.mainscroll+50 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
                    
                    elif BLEND[0] != "None" and self.FRAMES > n and ((blendX+40)*n)+list_scroll in range(0, w):
                        
                        try:
                            
                            print self.pf+BLEND[1]
                            BPic = gtk.gdk.pixbuf_new_from_file(thumbnailer.blenderthumb(self.pf+"/"+BLEND[1], 100,100))
                        except:
                            
                             
                            raise
                            BPic = "None"
                        
                        
                        self.RLISTS[ind][2][n][0] = BPic
            
            
            
            ## MOUSE OVER let's say fot the grab tool ###
                    
                    
                if mx in range( ((blendX+40)*n)+list_scroll-2,  ((blendX+40)*n)+list_scroll-2+blendX+4):
                    
                    if my in range((listY*ind)+self.mainscroll+50-2, (listY*ind)+self.mainscroll+50-2+blendX+4):
                        
                        widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.FLEUR))
                        
                        
                        
                        if self.tool == "grab":
                            
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#2c2c2c")) ## CHOSE COLOR
                            widget.window.draw_rectangle(xgc, True, ((blendX+40)*n)+list_scroll-15, (listY*ind)+self.mainscroll+40,  2, blendX+80)
                            
                            
                            # IF RELESED
                            if "GDK_BUTTON1" not in str(fx) and "GDK_BUTTON1" in str(self.mpf) and self.win.is_active():
                                
                                
                                # moving line is like copying it first
                                # and then deleting the previous one
                                
                                ### MARK ###
                                
                                # marking to delete the line
                                
                                print self.RLISTS[self.grab[0]][2][self.grab[1]][1]
                                
                                delete_filename = self.RLISTS[self.grab[0]][0]
                                delete_file = open(self.pf+"/py_data/rnd_seq/"+delete_filename, "r")
                                delete_file = delete_file.read().split("\n")
                                
                                print "\n----- DELETE FILE ------ (before)\n"
                                for dn,  i in enumerate(delete_file):
                                    print i
                                    if i == self.RLISTS[self.grab[0]][2][self.grab[1]][1]:
                                        delete_file[dn] = "!!!DELETE!!!"
                                print "\n----- DELETE FILE ------ (after)\n"
                                for dn,  i in enumerate(delete_file):
                                    print i
                                    
                                if delete_file[-1] == "":
                                    delete_file = delete_file[:-1]
                                
                                
                                
                                
                                save = open(self.pf+"/py_data/rnd_seq/"+delete_filename, "w")
                                
                                for i in delete_file:   
                                    save.write(i+"\n")
                                
                                save.close()
                                
                                
                                
                                ### INSERT ####
                                
                                # opening the file
                                insert_filename = self.RLISTS[ind][0]
                                insert_file = open(self.pf+"/py_data/rnd_seq/"+insert_filename, "r")
                                insert_file = insert_file.read().split("\n")
                                
                                print "\n----- INSERT FILE ------(before)\n"
                                for i in insert_file:
                                    print i
                                
                                insert_file.insert(n, self.RLISTS[self.grab[0]][2][self.grab[1]][1])
                                
                                print "\n----- INSERT FILE ------(after)\n"
                                for i in insert_file:
                                    print i
                                
                                if insert_file[-1] == "":
                                    insert_file = insert_file[:-1]
                                
                                
                                
                                
                                save = open(self.pf+"/py_data/rnd_seq/"+insert_filename, "w")
                                
                                for i in insert_file:   
                                    save.write(i+"\n")
                                save.close()
                                
                                ### REMOVE ####
                                
                                delete_filename = self.RLISTS[self.grab[0]][0]
                                delete_file = open(self.pf+"/py_data/rnd_seq/"+delete_filename, "r")
                                delete_file = delete_file.read().split("\n")
                                delete_file.remove("!!!DELETE!!!")
                                if delete_file[-1] == "":
                                    delete_file = delete_file[:-1]
                                
                                
                                
                                
                                save = open(self.pf+"/py_data/rnd_seq/"+delete_filename, "w")
                                
                                for i in delete_file:   
                                    save.write(i+"\n")
                                save.close()
                                
                                
                                self.load()
                                self.grabbed =True
                            
                        elif "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active():
                        
                            self.tool = "grab"
                            self.grab = [ind, n]
        
        
                            
                            
                            
        
        
        
        
        
            
            #RENDER ICON#
            widget.window.draw_pixbuf(None, self.render, 0, 0, 10, (listY*ind)+self.mainscroll+20 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
            
            
            
            ### ACTIVATE THE RENDER ####
            
            
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#4c4c4c")) ## CHOSE COLOR
            
            #MOUSE OVER
            if mx in range(w-210, w) and my in range((listY*ind)+self.mainscroll+20+listY-50, (listY*ind)+self.mainscroll+20+listY-50+44):
                # get mouse to show the hand
                widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#e47649"))
                
                if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active():
                
                    
                    ## POPEN MOTHERFUCKER # subprocess
                    Popen(["python", self.pf+"/py_data/modules/render.py", self.pf+"/py_data/rnd_seq/"+LIST[0]], universal_newlines=True)    
                
                
                
            
            widget.window.draw_rectangle(xgc, True, w-210, (listY*ind)+self.mainscroll+20+listY-50, w, 44)
            
            
            ctx.set_source_rgb(1,1,1)
            ctx.set_font_size(25)
            ctx.move_to( w-150, (listY*ind)+self.mainscroll+20+listY-15)
            ctx.show_text("RENDER")
            
            
           
            widget.window.draw_pixbuf(None, self.render_big, 0, 0, w-200, (listY*ind)+self.mainscroll+20+listY-48 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
        
        if self.tool == "grab": #WRITTING IT HERE SO IT WILL OVERWTITE ONTO PREVIOUSLY WRITTEN THINGS
            
            
            ind = self.grab[0]
            n = self.grab[1]
            try:
                BLEND = self.RLISTS[ind][2][n]
            
                
                if BLEND[0] and BLEND[0] != "None":
                    
                    widget.window.draw_pixbuf(None, BLEND[0], 0, 0, mx, my , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
                else:
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#4c4c4c")) ## CHOSE COLOR
                    widget.window.draw_rectangle(xgc, True, mx , my, blendX+4, blendX+4)
                
                ## TITLE ##
                ctx.set_source_rgb(1,1,1)
                ctx.set_font_size(10)
                ctx.move_to( mx+10, my+listY-80)
                ctx.show_text(BLEND[1][BLEND[1].rfind("/")+1:])
            except:
                pass
        
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
        
        
        
        def callback():
            if self.allowed == True:
                widget.queue_draw()

        glib.timeout_add(10, callback)
        
        
        
        
