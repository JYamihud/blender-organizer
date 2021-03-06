# -*- coding: utf-8 -*-

# system
import os
import socket

# graphics interface
import gtk
import pango
import cairo
import glib
import random

try: 
    import Image
except:
    from PIL import Image

# calculational help
import datetime


# self made modules

import thumbnailer
import history
import itemselector
import imageselector
import checklist
import dialogs
import fileformats
import render_lists
import assets # SO I COULD LINK TO ITEMS
import linkconfirm #AUTOMATIC LINKING WTF
import oscalls
import quick

import copy # OMG OPTIMIZATION HACKS OMG I HOPE IT'S GOING TO WORK

from subprocess import *

# FIRST LET'S BREAK APPRAT THE DATA STRUCTURE


#   name        color         comment

#   EVENT       #4c4c4c       THE HAPPENING OF SOMETHING REGARDLESS OF IF IT'S SHOWN IN THE MOVIE
#   SCENE       #db3c16       THE ACTUALL SHOWN STUFF ( ON TOP OF THE HAPPENING )
#   CUT         #e47649       THE CONNECTIONS BETWEEN THE SCENES TO KEEP TRACK OF THE MOVIE EDITING



# FILES .bos  #blender organizer story




#### MAIN STORY CLASS TO CALL ALL THE FUNCTIONS FROM

class story:
    
    
    def __init__(self, pf, box, win, mainbox=None, scene="", shot=""):
        
        
        
        
        
        self.pf = pf
        self.box = box
        self.win = win
        self.mainbox = mainbox
        
        
        # For linking scenes from other places
        self.searchscene = scene
        self.searchshot  = shot
        
        
        self.allowed = True
        
        self.nothing = True
        
        
        self.keys = []
        
        
        # THIS WILL REFRASH ALL THE THUMBNAILS SO YOU COULD EDIT PRVIEWS FOR EXAMPLE
        # AND CHANGES WILL BE PRESENTED
        # BASICALLY DELETING A FOLDER WITH THE THUMBNAILS
        os.system("rm -r "+self.pf+"/pln/thumbs")
        
        
        
        ## UNDO DATA
        
        self.undoDATA = []    # A PLACE WHERE I GONNA SAVE PREVIOUS COPIES
        self.undoINDEX = -1   # A PLACE WHERE YOU MOVE IN UNDO HISTORY
        self.doundo = False   # IT'S WHETHER SOMETHING CHANGED AND WHEHTER TO SAVE AFTER THE SAVE
        # PROBABLY WE WILL NEED A FUNCTION THAT WE PUT FOR IT. BECUSE UNDO IS RECORDED AT EVERY
        # CHANGE. AND SO WE NEED TO HAVE A FUNCTION TO PLUG INTO THOSE VARIOUS PLACES.
        # THEY A LITTLE BIT LATER def undo(), def redo(), def undo_record()
        
        # make a .bos file if no files exits in /pln/
        
        notfound = True
        for FILE in os.walk(self.pf+"/pln").next()[2]:
            if FILE.endswith(".bos"):
                
                notfound = False
        
        
        if notfound:
        
            self.FILE = bos(self.pf+"/pln/main.bos")
        else:
            
            if os.path.exists(self.pf+"/pln/main.bos"):
                self.FILE = bos(self.pf+"/pln/main.bos")
            else:
                self.FILE = bos(self.pf+"/pln/"+FILE)
            
        self.FILE.load()
        
        
        
        self.editor()
    
    def events_overlap(self, my, mx, ex, ey, esx, esy, this_frame_events):
        
        overlap = False
        
        for ind, event in enumerate(this_frame_events):
        
            if my in range(event[1], event[1]+event[3]):
            
                for p in range(event[0], event[0]+event[2]):
                    
                    if p in range(ex, ex+esx):
                    
                        
                        overlap = True
                        return event, overlap
        
        
        return None, overlap
    
    
    def undo(self):
        
        if self.undoINDEX < 1:
            self.undoINDEX = 1
        
        self.undoINDEX = self.undoINDEX - 1 # MOVE ONE WAY BACK
        
        try:
            wr = self.undoDATA[self.undoINDEX]
            wf = open(self.pf+"/pln/main.bos", "w")
            wf.write(wr)
            wf.close()
            
            self.FILE.load()
            
            
        
        except:
            self.undoINDEX = len(self.undoDATA)  
        
        
    
    def redo(self):
        
        self.undoINDEX = self.undoINDEX + 1 # MOVE ONE WAY FORWARD
        
        try:
            wr = self.undoDATA[self.undoINDEX]
            wf = open(self.pf+"/pln/main.bos", "w")
            wf.write(wr)
            wf.close()
            
            self.FILE.load()
            
            
        
        except:
            self.undoINDEX = len(self.undoDATA)  
        
        
    
    def undo_record(self):
        
        # MAKE SURE YOU RECORD BEFORE CHANGES TO THE FILE
        
        self.undoDATA = self.undoDATA[:self.undoINDEX+1]
        
        f = open(self.pf+"/pln/main.bos", "r")
        
        self.undoDATA.append(f.read())
        self.undoINDEX = len(self.undoDATA)  
        
        if len(self.undoDATA) > 32:
            self.undoDATA = self.undoDATA[32:] # RECORD ONLY LAST 32 INSTANCES
    
    def animate(self, thex, they):
        
        lx = [self.px, thex]
        lx = [lx[0], sum(lx)/len(lx), lx[1]]
        lx = [lx[0], sum([lx[0],lx[1]])/len([lx[0],lx[1]]), lx[1], sum([lx[1],lx[2]])/len([lx[1],lx[2]]), lx[2] ]
        
        ly = [self.py, they]
        ly = [ly[0], sum(ly)/len(ly), ly[1]]
        ly = [ly[0], sum([ly[0],ly[1]])/len([ly[0],ly[1]]), ly[1], sum([ly[1],ly[2]])/len([ly[1],ly[2]]), ly[2] ]
        
        
        
        
        self.animation = {}
        
        
        for n, i in enumerate(lx):
            
            self.animation[str(self.frame+n)] = [i, ly[n]]
            
        
        
    def editor(self):
    
        # TRANSFORMATION
        self.sx = 0.6
        self.sy = 61.5
        self.px = 0.0
        self.py = 0.0
        
        
        self.select = "bos"
        
        
        self.animation = {}
        
        
        
        
        self.FILE = bos("pln/main.bos")
        self.px, self.py, self.sx, self.sy = self.FILE.load()
        
        self.frame = 0
        
        self.previousactive = False
        
        self.dW = 0
        self.DH = 0
        
        self.mpx = 0
        self.mpy = 0
        self.mpf = None
        
        self.bosscroll = 0    
        
        self.event_text_scroll = 0.0
        self.showcross = True
        
        #editor features
        
        # tools:
        # grab, event, scene, cut
        
        
        self.tool = "select"
        # events
        self.toolactive = False
        
        self.toolXY = [0,0]
        
        self.event_resize = False
        self.event_move = False
        self.event_select = False
        self.image_select = False
        
        
        #scenes
        self.scene_select = -1
        self.scenes_in_event = []
        
        
        
        #arrows
        self.arrow_to = False
        self.arrow_selection = [False, False]
        self.arrow_delete_overwrite = [[False], [0,0]] ### FOR THE OVERWRITE AUTOMATIC DELETION 
                                                       # [ [ IND OF THE DELETABLE ARROW ],
                                                       # [ COORDINATES FOR THE RENDERER ] ]
        
        self.marker_select = -1
        self.deletelastframe = False 
        self.renamelastframe = False
        self.move_marker = False
        
        
        self.imageselected = -1
        self.arrowimage = False
        
        
        ### SHOTS HANDELLIGN OMG ####
        
        self.shotsDATA = [] # INSIDE THERE IS A FOLLOWING LIST OF LISTS
                            # [ "SHOT NAME" FALSE if not a shot, 
                            #"SHOT TEXT", 
                            #shotpreview pixbuf FALSE if not loaded; "NONE" if not found ] 
        
        self.shotsSCROLL = 0
        
        
        self.imagesearch = ""
        
        self.IsNowProcessing = False
        
        # LOADING ALL THE ICONS
        self.bosicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/bos_big.png")
        
        self.eventicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/event.png")
        self.scenceicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/scene_editor.png")
        self.markericon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/marker.png")
        self.saveicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/big_save.png")
        self.cuticon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/new_cut.png")
        self.split_event = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/split_event.png")
        self.split_action = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/split_action.png")
        self.item_big = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/item_big.png")
        self.blendericon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/blender.png")
        self.node_link = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/node_link.png")
        self.image_add = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/image_add.png")
        
        #start end
        
        self.start_grey = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/start_grey.png")
        self.start_mo = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/start_mo.png")
        self.start_active = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/start_active.png")
        
        
        
        self.end_grey = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/end_grey.png")
        self.end_mo = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/end_mo.png")
        self.end_active = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/end_active.png")
        
        self.gen_script = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/gen_script.png")
        self.gen_script_active = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/gen_script_active.png")
        
        self.sequence = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/sequence.png")
        
        
        self.render_big = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/render_big.png")
        
        self.big_right = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/big_right.png")
        self.big_left = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/big_left.png")
        
        
        
        #shots editor
        self.empty_frame = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/empty_frame.png")
        self.foldericon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/folder.png")
        self.imgAT = []
        
        
        self.BLboard = ""
        self.copy = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/copy.png")
        self.paste = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/paste.png")
        self.plus = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/plus.png")
        self.render = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/render.png")
        self.checklist = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/checklist.png")
        self.ok = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/ok.png")
        self.big_edit = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/big_edit.png")
        
        
        self.fade_01 = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/INT/fade_01.png")
        self.fade_02 = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/INT/fade_02.png")
        self.fade_03 = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/INT/fade_03.png")
        self.fade_04 = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/INT/fade_04.png")
        
        #getting icons into place OMG WHY????
        self.objicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/obj_asset_undone.png")
        self.chricon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/chr_asset_undone.png")
        self.vehicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/veh_asset_undone.png")
        self.locicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/loc_asset_undone.png")
        self.scnicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/scn_asset_undone.png")
        self.picicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/pic.png")
        self.linkicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/link.png")
        
        #BIG PREVIEWS
        self.objiconbig = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/obj_prev.png")
        self.chriconbig = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/chr_prev.png")
        self.vehiconbig = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/veh_prev.png")
        self.lociconbig = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/loc_prev.png")
        
        self.scnPERCENT = get_scenes_percentage(self.FILE)
        
        
        
        self.insertedimgs = []
        
        self.ImageArrowsDict = {} # THIS ONE IS TO SPEED UP THAT ONE
        self.itempercent = {}
        
        def framegraph(widget, event):
                                                    
            w, h = widget.window.get_size()
            xgc = widget.window.new_gc()
            
            mx, my, fx  = widget.window.get_pointer()
            tx, ty = self.toolXY
            
            focusevent = False
            
            # GETTING WHETHER THE WINDOW IS ACTIVE
            
            self.winactive = self.win.is_active()
            
            self.frame = self.frame + 1
            
            #fif = datetime.datetime.now()
            #mil  = fif - stf
            #print "HISTORY - ", mil.microseconds, "microseconds"
            
            stf = datetime.datetime.now()
            perfStat = []
            
            
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
            ctx3.set_source_rgba(0.2,0.2,0.2,0.9)
            ctx3.rectangle(0, 0, w, h)
            ctx3.fill()
            
            
            fif = datetime.datetime.now()
            mil  = fif - stf
            perfStat.append([ "BACKGROUND IMAGE", mil.microseconds ])
            
            stf = datetime.datetime.now()
            
            #######   LINKCHAINED   ######
            
            
            #trying to get whether the start actually connects to end
            linkchained = False
            
            linkchainpath = []
            
            startlink = False
            
            for i in self.FILE.arrows:
                
                if i[0][0] == -1:
                    
                    linkchainpath.append(i)
                    startlink = True
                    
                    
            while startlink: # dangerous motherfucker
                
                found = False
                
                for i in self.FILE.arrows:
                    
                    
                    
                    if linkchainpath[-1][1] == i[0]:
                        
                        
                        
                        found = True
                        linkchainpath.append(i)
                        
                        if i[1][0] == -1:
                            linkchained = True
                            break
                    
                if found == False:
                    break
            
            self.FILE.tree = linkchainpath
            
            ctx = widget.window.cairo_create()
            #ctx.select_font_face("Sawasdee", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            
            xgc.line_width = 2
            
            # BACKGROUND COLOR
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#222222")) ## CHOSE COLOR
            #widget.window.draw_rectangle(xgc, True, 0, 0, w, h)  ## FILL FRAME    
            
            
            ctx2 = widget.window.cairo_create()
            ctx2.select_font_face("Monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            
            
            
            ## tooltips
            
            tooltip = False
            
            
            
            #####################################
            
            
            
            
            # MOUSE CURSOR MAIN
            if mx > 0 and mx < w-(w)/3 and my > 50 and self.showcross:
                widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.CROSS))
                
            if self.showcross:  # IF MOUSE NOT IN EDITOR
                widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.ARROW)) 
            
            
            self.showcross = True   
            
            
            
            
            #### EDITOR #######################################################
            
           
            
            
            
            
            
            
            self.arrows_output_dots = []
            
            for i in self.FILE.arrows:
                
                self.arrows_output_dots.append(  [[0,0],[0,0], False]  )
            
            self.ImageArrows = [] # this is gonna be merged with self.arrows_output_dots right before drawing them.
            # it's used to see connections of images to items / assets
            
            
            
            # TRANSFORMATION
            sx = self.sx
            sy = self.sy
            px = self.px 
            py = self.py
            
            
            
            #ANIMATION 
            
            if str(self.frame) in self.animation:
                self.px, self.py = self.animation[str(self.frame)]
            
            
            
            nw = (w-(w)/3)/2
                
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#181818")) ## CHOSE COLOR
            
            xgc.line_width = 1
            #widget.window.draw_line(xgc, nw, 0, nw, h) 
            #widget.window.draw_line(xgc, 0, h/2, w, h/2)
            
            #mouse lines
            #widget.window.draw_line(xgc, mx, 0, mx, h) 
            #widget.window.draw_line(xgc, 0, my, w, my)
            
            #ctx2.set_source_rgb(1,1,1)
            #ctx2.set_font_size(20)
            #ctx2.move_to( mx, 65)
            #tmpx = str(float(mx - self.px) / self.sx )
            #ctx2.show_text(tmpx[:tmpx.find(".")+3])
            
            #ctx2.set_source_rgb(1,1,1)
            #ctx2.set_font_size(10)
            #ctx2.move_to( 5, my)
            #tmpy = str(int(float(my - self.py) / self.sy ))
            #ctx2.show_text(tmpy[:tmpy.find(".")+3])
            
            
            # grid
            #xgc.set_rgb_fg_color(gtk.gdk.color_parse("#181818"))
            #for y,  i in enumerate(range(int(float(0 - self.py) / self.sy ), int(float(h - self.py) / self.sy ))):
                
            #    widget.window.draw_line(xgc, 0, int(i*self.sy+self.py), w, int(i*self.sy+self.py))
            #p = 0
            #for x,  i in enumerate(range(int(float(0 - self.px) / self.sx ), int(float(w - self.px) / self.sx )/100)):
            #    if int(i*100*self.sx+self.px) > p+20:
            #        p = int(i*100*self.sx+self.px)
            #        widget.window.draw_line(xgc, p,0, p, h)
                    
            
            
            xgc.line_width = 2
            
            
            
            # scroll
            
            if mx > 0 and mx < w-(w)/3 and my > 50:
                # the scroll is done with the middle mouse button
                
                
                ### Y
                if self.mpy > my and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf) and 65507 not in self.keys and self.win.is_active():
                    
                    self.py = self.py + (my-self.mpy) 
                
                if self.mpy < my and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf) and 65507 not in self.keys and self.win.is_active():
                    
                    self.py = self.py - (self.mpy-my)
                
                
                
                
                
                ### X
                if self.mpx > mx and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf) and 65507 not in self.keys and self.win.is_active():
                    
                    self.px = self.px + (mx-self.mpx) 
                
                if self.mpx < mx and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf) and 65507 not in self.keys and self.win.is_active():
                    
                    self.px = self.px - (self.mpx-mx)
            
                
                
                
                
                
                
                #### RESIZE
                
                if 65451 in self.keys: # + key
                    
                    self.sy = self.sy + 0.3
                    self.sx = self.sx + 0.01
                    
                    
                    
                if 65453 in self.keys: # - key
                    
                    self.sy = self.sy - 0.3
                    self.sx = self.sx - 0.01
                self.arrow_delete_overwrite
                
                
                
                ### Y
                if self.mpy > my and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf) and 65507 in self.keys and self.win.is_active():
                    
                    self.sy = self.sy - 0.5
                
                if self.mpy < my and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf) and 65507 in self.keys and self.win.is_active():
                    
                    self.sy = self.sy + 0.5
                
                if self.sy < 5:
                    self.sy = 5
                
                
                
                  
                xsize = 0.03*sx
                
                
                ### X
                if self.mpx > mx and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf) and 65507 in self.keys and self.win.is_active():
                    
                    
                    
                    
                    self.sx = self.sx - xsize
                    
                    
                    
                if self.mpx < mx and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf) and 65507 in self.keys and self.win.is_active():
                    
                    self.sx = self.sx + xsize
                    
                
                
                
                
                if self.sx < 0.01:
                    self.sx = 0.01
                
                
                if self.sx != sx or self.sy != sy:
                
                    self.py = (self.py-h/2) / sy * self.sy   + h/2    
                    self.px = (self.px-nw) / sx * self.sx   + nw
                
                
                
            fif = datetime.datetime.now()
            mil  = fif - stf
            perfStat.append([ "INITIALIZAION OF THE EDITOR", mil.microseconds])
            
            stf = datetime.datetime.now()    
                
            
            
            
            
                
                
                
            ## SHOWING MARKERS
            
            allowdelete = False
            if not self.deletelastframe:
                allowdelete = True
                
            allowrename = False
            if not self.renamelastframe:
                allowrename = True
                
            for ind, i in enumerate(self.FILE.markers):
                
                markX = int(i[0]*sx+px)
                textPX = len(i[1])*6  + 2
                
                xgc.line_width = 1
                xgc.set_line_attributes(1, gtk.gdk.LINE_ON_OFF_DASH, gtk.gdk.CAP_NOT_LAST, gtk.gdk.JOIN_MITER)
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#9b9b9b"))
                
                if self.marker_select == ind:  ## IF MARKER SELECTED
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#9b9b9b"))
                    
                    
                    if 65535 in self.keys: # DELETE BUTTON
                        
                        
                        if allowdelete:
                            del self.FILE.markers[ind]
                            self.marker_select = len(self.FILE.markers)+2
                        allowdelete = False
                        self.deletelastframe = True
                    
                    else:
                        self.deletelastframe = False 
                    
                    
                    
                    if 65289 in self.keys:
                        if allowrename:
                            def ee(e=None):
                                dialogs.marker(self.marker_select, self.FILE)
                        
                    
                            glib.timeout_add(10, ee)
                        allowrename = False
                        self.renamelastframe = True
                    else:
                        
                        self.renamelastframe = False
                         
                        
                
                if mx in range(markX-textPX/2, markX+textPX/2) and my in range(h-10, h):    # IF MOUSE OVER
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#fff"))
                    
                        
                    if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active() and self.tool == "select":
                        
                        # IF CLICKED
                        self.marker_select = ind
                        self.event_select = len(self.FILE.events)+2
                        self.image_select = False
                        
                       
                
                
                widget.window.draw_line(xgc, markX, 0, markX, h)
                xgc.line_width = 2
                
                xgc.set_line_attributes(1, gtk.gdk.LINE_SOLID, gtk.gdk.CAP_NOT_LAST, gtk.gdk.JOIN_MITER) 
                
                
                widget.window.draw_rectangle(xgc, True, markX-textPX/2, h-10, textPX,10)
                
                
                
                
                ctx2.set_source_rgb(1,1,1)
                ctx2.set_font_size(10)
                ctx2.move_to( markX-textPX/2+1, h-1)
                ctx2.show_text(i[1])
            
            
            if self.tool == "split":
                if "GDK_BUTTON3" not in str(fx) and "GDK_BUTTON3" in str(self.mpf):
                    
                    self.tool = "select"
                
            
            # MOVING MARKERES    
            
            if self.tool == "select":
            
                for ind, i in enumerate(self.FILE.markers):
                    
                    
                    markX = int(i[0]*sx+px)
                    textPX = len(i[1])*6  + 2
                    
                    if self.marker_select == ind:
                        
                        # ACTIVATE MOVE
                        
                        if mx in range(markX-textPX/2, markX+textPX/2) and my in range(h-10, h):    # IF MOUSE OVER
                            if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active():
                                self.move_marker = True
                                self.tool = "select"
                        
                        # MOVING 
                        
                        if self.move_marker and "GDK_BUTTON1" in str(fx):
                
                            self.FILE.markers[self.marker_select][0] = (mx - px)/sx     
                        
                        
                        # STOP THE MOVE
                        
                        
                        if "GDK_BUTTON1" not in str(fx) and "GDK_BUTTON1" in str(self.mpf):
                            
                            
                            self.move_marker = False
                
                
                
            fif = datetime.datetime.now()
            mil  = fif - stf
            perfStat.append([  "MARKERS", mil.microseconds])
            
            stf = datetime.datetime.now()
            
            
            
            ######## SHOWING DRAGGED IMAGES ######
            self.arrow_to = False
            imagesonscreen = []
            for count, image in enumerate(self.FILE.images):
                
               
                
                imX, imY, mode, url, thumb, pixthumb = image
                
                
                
                
                imX = int(imX*sx+px) #DAMN IT WAS SO SIMPLE I WAS READING THE VALUES FROM THE PREVIOUS FRAME
                imY = int(imY*sy+py) #BY REMOVING THE SELF I NOW READ THE UPDATED VALUES HELL YEAH!!!!!!!!
                piX = 150
                piY = 150
                
                if imX in range(-piX, w/3*2) and imY in range(-piY, h):
                    
                    imagesonscreen.append(url)
                    
                    if pixthumb == "NO PIXBUF" and imX in range(-200, w/3*2) and imY in range(0, h):
                        
                        if not self.IsNowProcessing:
                            
                            self.IsNowProcessing = True
                            
                            def ee(count, url):
                                try:
                                    self.FILE.images[count][-1] = gtk.gdk.pixbuf_new_from_file(self.pf+"/pln/thumbs/"+thumb+".png")
                                except:
                                    
                                    # If the thumbnail isn't there try to recover it
                                    try:
                                        if mode == "ABSOLUTE":
                                            u = url
                                        if mode == "RELATIVE":
                                            u = self.pf+url
                                        
                                        
                                        if not os.path.exists(self.pf+"/pln/thumbs/"):
                                            os.makedirs(self.pf+"/pln/thumbs/")
                                    
                                    
                                        #chosing a random name for the thumb
                                        rndname = ""
                                        rndchar = "QWERTYUIOPASDFGHJKLZXCVBNM1234567890"
                                        while os.path.exists(self.pf+"/pln/thumbs/"+rndname+".png") or rndname == "":
                                            rndname = ""
                                            for l in range(20):
                                                rndname = rndname + random.choice(rndchar)
                                            
                                        
                                        #thumbnailer.thumbnail
                                        
                                        fromr  = open(thumbnailer.thumbnail(u, x=150, y=150), "r")
                                        saveto = open(self.pf+"/pln/thumbs/"+rndname+".png", "w")
                                        saveto.write(fromr.read())
                                        saveto.close()
                                        
                                        self.FILE.images[count][-2] = rndname
                                        thumb = rndname
                                        self.FILE.images[count][-1] = gtk.gdk.pixbuf_new_from_file(self.pf+"/pln/thumbs/"+thumb+".png")
                                    
                                    except:
                                        pass
                                    
                                self.IsNowProcessing = False
                            glib.timeout_add(10, ee, count, url)
                    #try:
                    #    piX = int(pixthumb.get_width()*self.sx*(self.sy/20))
                    #    piY = int(pixthumb.get_height()*self.sx*(self.sy/20))
                    #except:
                    #    pass    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#3f3f3f"))
                    
                    
                    tinyicon = self.picicon
                    
                    
                    previewurl = url
                    
                    checkurl = url[:url.rfind("/")]
                    checkurl = checkurl[:checkurl.rfind("/")]
                    
                    launchitem = False
                    
                    if mode != "ABSOLUTE":
                    
                         #IF THE IMAGE IS FROM THE PROJECT
                        
                        if url.startswith("/dev/chr"):
                            tinyicon = self.chricon
                        elif url.startswith("/dev/veh"):
                            tinyicon = self.vehicon
                        elif url.startswith("/dev/loc"):
                            tinyicon = self.locicon
                        elif url.startswith("/dev/obj"):
                            tinyicon = self.objicon
                        
                        
                        
                        
                        #Making a connetiong start
                        if url.startswith("/dev/") and "Preview." not in url: # IF IMAGE FROM ASSET BUT NOT THE ASSET HIM SELF
                        
                            
                            if url not in self.ImageArrowsDict:
                                self.ImageArrowsDict[url] = [[imX+piX, imY+10], [0,0], ""]
                            else:
                                #if self.ImageArrowsDict[url][0] == [0,0]:
                                self.ImageArrowsDict[url][0] = [imX+piX, imY+10]
                        # IF IMAGE IS ASSET ( OR A REFERENCE TO IT'S Preview file )
                            
                        elif url.startswith("/dev/") and "Preview." in url: # IF IMAGE IS ASSET HIM SELF
                    
                    
                    
                            # OPTIMIZATION NEEDED
                    
                            # I DON'T FEEL GOOD ABOUT THIS. BUT I CAN'T FASTER WAS TO DO IT YET.
                            for raw, part in enumerate(["reference", "tex", "renders"]):
                                curl = os.walk(self.pf+checkurl+"/"+part).next()[2]
                                for FILE in curl:
                                    thisurl = checkurl+"/"+part+"/"+FILE
                                    if thisurl not in self.ImageArrowsDict:
                                        self.ImageArrowsDict[thisurl] = [[0,0], [imX, imY+piY+20+(11*raw)], url]
                                    
                                    self.ImageArrowsDict[thisurl][2] = url
                                    self.ImageArrowsDict[thisurl][1] = [imX, imY+piY+20+(11*raw)]
                                    
                                    #imagesonscreen.append(checkurl+"/"+part+"/"+FILE)
                                
                            CUR = url[5:8]
                                
                                
                            name = url[9:9+url[9:].find("/")]
                            url = name
                        
                            launchitem = True
                        
                    
                    
                    ctx3 = widget.window.cairo_create()
                    ctx3.set_source_rgba(0,0,0,0.4)
                    ctx3.rectangle(imX-2, imY, piX+4, piY)
                    ctx3.fill()
                    
                    
                    
                    if not launchitem:
                        if self.toolXY[0] in range(imX, imX+piX) and self.toolXY[1] in range(imY, imY+piY) and mx in range(0, w-w/3) and my in range(50, h) and self.tool == "arrow":
                            self.toolXY = [imX+piX, imY+10]
                            self.arrowimage = [imX, imY, url[url.rfind("/")+1:], mode, url, self.FILE.images[count][0], self.FILE.images[count][1], count]
                    
                    
                    
                            
                    if mx in range(imX, imX+piX) and my in range(imY, imY+piY) and mx in range(0, w-w/3) and my in range(50, h):
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#395384"))
                        widget.window.draw_rectangle(xgc, True, imX-2, imY, piX+4, piY)
                        
                        
                        widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
                        self.showcross = False
                        
                        
                        
                        
                        if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active() and self.tool == "select":
                            if self.image_select and self.image_select[0] == count:
                                if launchitem:
                                    
                                    def ee(CUR, url):
                                        self.box.destroy()
                                        
                                        
                                        self.box = gtk.VBox(False)
                                        self.mainbox.pack_start(self.box, True)
                                        
                                        assets.draw_assets(os.getcwd(), self.box, self.win, CUR, url, mainbox=self.mainbox)
                                    
                                    glib.timeout_add(10, ee, CUR, url)
                                    
                                    launchitem = False
                                    
                                    
                                    
                                else:   
                                    if mode == "ABSOLUTE":
                                        oscalls.Open(url)
                                    elif mode == "RELATIVE":
                                        oscalls.Open(self.pf+url)
                            else:
                                if launchitem:
                                    self.image_select = [count, "[item]/dev/"+CUR+"/"+url]
                                else:
                                    self.image_select = [count, "[image]"+url]
                                
                                self.itemscenedata = []
                                self.event_select = False        
                                self.shotsDATA = False
                                self.shotsSCROLL = 0
                                
                                    
                                    
                    elif mx in range(imX, imX+piX) and my in range(imY-22, imY) and mx in range(0, w-w/3) and my in range(50, h):
                         widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.FLEUR))
                         self.showcross = False
                         xgc.set_rgb_fg_color(gtk.gdk.color_parse("#fff"))
                         widget.window.draw_rectangle(xgc, True, imX-3, imY-23, piX+6, 22)
                         xgc.set_rgb_fg_color(gtk.gdk.color_parse("#3f3f3f"))
                         if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active():
                            self.imageselected = count
                    
                    if self.image_select and self.image_select[0] == count:  #HIGHLIGHTING SELECTED IMAGE
                        if launchitem:
                            
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#fff"))
                            widget.window.draw_rectangle(xgc, False, imX-3, imY-23, piX+6, piX+26+51)
                        else:
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#fff"))
                            widget.window.draw_rectangle(xgc, False, imX-3, imY-23, piX+6, piX+26)
                                        
                                
                    if "GDK_BUTTON1" in str(fx) and self.win.is_active() and self.imageselected == count and self.tool == "select":
                        
                        self.FILE.images[count][0] = self.FILE.images[count][0] + ((mx-self.mpx ) / sx)
                        self.FILE.images[count][1] = self.FILE.images[count][1] + ((my-self.mpy ) / sy)
                        
                    if "GDK_BUTTON1" not in str(fx) and "GDK_BUTTON1" in str(self.mpf):
                        self.imageselected = -1
                        
                    
                    
                    
                    
                    
                    if self.image_select and self.image_select[0] == count:
                         
                        # DELETE EVENT SHOR KEY #
                        
                        allowdelete = False
                        if not self.deletelastframe:
                            allowdelete = True
                        
                        
                        if 65535 in self.keys: #and allowdelete
                            
                            
                            
                            if allowdelete  and self.tool == "select":
                                
                                self.undo_record()
                                
                                del self.FILE.images[count]
                                try:
                                    os.remove(self.pf+"/pln/thumbs/"+thumb+".png")
                                except:
                                    pass
                                
                                self.event_select = False
                                self.image_select = False
                                self.deletelastframe = True
                                
                                self.doundo = True
                                
                        else:
                            self.deletelastframe = False      
                    
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#2c2c2c"))
                    #widget.window.draw_rectangle(xgc, True, imX, imY, piX, piY)
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    percenttext = ""
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#8a7d2c"))
                    if launchitem:
                        
                        if True:    # POTENTIAL 10 MICROSECONDS IF THIS WILL BE SPEAD UP
                            try:
                                itempercent = self.itempercent[url]
                            except:
                                try:
                                    self.itempercent[url] = checklist.partcalculate(checklist.openckecklist(self.pf+"/dev/"+CUR+"/"+name+"/"+"/asset.progress")) #GETTING ITEMS %
                                except:
                                    self.itempercent[url] = 0
                                    
                                itempercent = self.itempercent[url]
                            # THIS IS PERCENT        THIS IS ITEMS PART LENGHT           
                            lenofsecondcube = int(round(float(piX+4) * itempercent))
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#d0d0d0"))
                            widget.window.draw_rectangle(xgc, True, imX-2, imY+piY, piX+4, 10)
                            
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
                            widget.window.draw_rectangle(xgc, True, imX-2, imY+piY, lenofsecondcube, 10)
                            
                            
                            percenttext = str(int(round(itempercent*100)))+"%"
                            
                        
                        
                        
                        # LET'S MAKE A LINKED NODE INPUTS FOR 
                        # References
                        # Textures
                        # Renders
                        # Infodocument
                        
                        ctx3 = widget.window.cairo_create()
                        ctx3.set_source_rgba(0,0,0,0.4)
                        ctx3.rectangle(imX-2, imY+piY+10, piX+4, 11*4)
                        ctx3.fill()
                        
                        #widget.window.draw_pixbuf(None, self.node_link, 0, 0, imX-5, imY+piY+10+5 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                        #widget.window.draw_pixbuf(None, self.node_link, 0, 0, imX-5, imY+piY+10+5+11 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                        #widget.window.draw_pixbuf(None, self.node_link, 0, 0, imX-5, imY+piY+10+5+22 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                        #widget.window.draw_pixbuf(None, self.node_link, 0, 0, imX-5, imY+piY+10+5+33 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                        
                        ctx.set_source_rgb(1,1,1)
                        ctx.set_font_size(10)
                        ctx.move_to( imX+10, imY+piY+10+15)               
                        ctx.show_text("References")
                        
                        ctx.move_to( imX+10, imY+piY+10+15+11)               
                        ctx.show_text("Textures")
                        
                        ctx.move_to( imX+10, imY+piY+10+15+22)               
                        ctx.show_text("Renders")
                        
                        #ctx.move_to( imX+10, imY+piY+10+15+33)               
                        #ctx.show_text("Information")
                        
                        putx, puty, puturl, putmode, frurl , wasx, wasy, co = 0,0,"","ABSOLUTE", "", 0,0, 0
                        
                        
                        if self.arrowimage:
                            putx, puty, puturl, putmode, frurl, wasx, wasy, co = self.arrowimage
                        
                        if putmode == "RELATIVE":
                            frurl = self.pf+"/"+frurl
                        
                        
                        
                        
                        
                            
                        
                        
                        docopy = False
                        
                        
                    
                        
                        #REF
                        if my in range(imY+piY+14, imY+piY+14+11) and mx in range(imX, imX+piX):
                            self.arrow_to = [imX, imY+piY+10+10]
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#fff"))
                            widget.window.draw_rectangle(xgc, False, imX+10, imY+piY+15, piX-10, 11)
                            
                            puturl = checkurl+"/reference/"+puturl
                            docopy = True
                            
                        #TEX
                        elif my in range(imY+piY+14+11, imY+piY+14+11+11) and mx in range(imX, imX+piX):
                            self.arrow_to = [imX, imY+piY+10+10+11]
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#fff"))
                            widget.window.draw_rectangle(xgc, False, imX+10, imY+piY+15+11, piX-10, 11)
                            
                            puturl = checkurl+"/tex/"+puturl
                            docopy = True
                            
                        #RND
                        elif my in range(imY+piY+14+22, imY+piY+14+11+22) and mx in range(imX, imX+piX):
                            self.arrow_to = [imX, imY+piY+10+10+22]
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#fff"))
                            widget.window.draw_rectangle(xgc, False, imX+10, imY+piY+15+22, piX-10, 11)
                            
                            puturl = checkurl+"/renders/"+puturl
                            
                            docopy = True
                        else:
                            checkurl = ""
                            
                        # OUTPUTTING THE IMAGE OUT
                        
                        if "GDK_BUTTON1" not in str(fx) and "GDK_BUTTON1" in str(self.mpf) and checkurl and self.tool != "arrow" and self.win.is_active():
                            
                            
                            if not self.imagesearch and my > 50 and mx < (w/3)*2:
                                self.imagesearch = puturl
                                if puturl.count("/") > 3:
                                    self.imagesearch = puturl[:puturl.rfind("/")]
                                self.tool = "linkimage"
                        
                        # MAKING A COPY OF THE IMAGE AND CONNECTING IT
                        if docopy and "GDK_BUTTON1" not in str(fx) and "GDK_BUTTON1" in str(self.mpf) and self.tool == "arrow" and self.arrowimage:
                            
                            #print self.arrowimage, "self.arrowimage"
                            
                            self.imagesearch = ""
                            
                            while os.path.exists(self.pf+puturl):
                                puturl = puturl[:puturl.rfind(".")]+"_copy"+puturl[puturl.rfind("."):]
                            
                            fr = open(frurl, "r")
                            tr = open(self.pf+puturl, "w")
                            tr.write(fr.read())
                            tr.close()
                            
                            putx = wasx +((20 ) / sx)
                            puty = wasy -((20 ) / sy)
                            
                            
                            rndname = ""
                            rndchar = "QWERTYUIOPASDFGHJKLZXCVBNM1234567890"
                            while os.path.exists(self.pf+"/pln/thumbs/"+rndname+".png") or rndname == "":
                                rndname = ""
                                for l in range(20):
                                    rndname = rndname + random.choice(rndchar)
                            
                            
                            if putmode == "RELATIVE":
                                self.FILE.images.append([putx, puty, "RELATIVE", puturl, rndname, "NO PIXBUF"])                 
                            else:
                                self.FILE.images[co] = [putx, puty, "RELATIVE", puturl, rndname, "NO PIXBUF"]
                            
                            self.arrowimage = False
                            
                        
                        
                        if not os.path.exists(self.pf+"/"+previewurl):
                            
                            
                            
                            if CUR == "chr":
                                pixthumb = self.chriconbig
                            elif CUR == "veh":
                                pixthumb = self.vehiconbig
                            elif CUR == "loc":
                                pixthumb = self.lociconbig
                            elif CUR == "obj":
                                pixthumb = self.objiconbig
                                
                            
                        
                        
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#6e5daf"))
                        
                    elif mode == "ABSOLUTE":
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#af5d5d"))
                    widget.window.draw_rectangle(xgc, True, imX-2, imY-22, piX+4, 22)
                    
                    
                    widget.window.draw_pixbuf(None, tinyicon, 0, 0, imX, imY-22 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                    
                    
                    
                    
                    ctx.set_source_rgb(1,1,1)
                    ctx.set_font_size(15)
                    ctx.move_to( imX+ 24, imY-6)
                    
                    text = url[url.rfind("/")+1:]
                    
                    if len(text) > 14:
                        text = text[:6]+"..."+text[-6:]
                    ctx.show_text(text)
                    
                    
                    
                    
                
                    try:
                        
                        #pixthumb = pixthumb.scale_simple(piX, piY, gtk.gdk.INTERP_NEAREST)
                        
                        
                        widget.window.draw_pixbuf(None, pixthumb, 0, 0, imX + ((piX-pixthumb.get_width())/2), imY + ((piY-pixthumb.get_height())/2), -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
                    except:
                        pass
                    
                    #IN CASE IMAGE IS WHITE MAKE % READABLE
                    
                    if len(percenttext) > 0:
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#464646"))
                        widget.window.draw_rectangle(xgc, True, imX, imY+piY-5-13, len(percenttext)*6+8, 13)
                    
                    
                    ctx.set_source_rgb(1,1,1)
                    ctx.set_font_size(10)
                    ctx.move_to( imX+2, imY+piY-8)
                    ctx.show_text(percenttext)
                
            
            
            
                    
                    
            
            
            fif = datetime.datetime.now()
            mil  = fif - stf
            perfStat.append([  "IMAGES, ITEMS", mil.microseconds])
            
            stf = datetime.datetime.now()
            
            
            
            
            
            
            
            
            
            
            ################# EVENT TOOL ##################
            
            
            ### SHOWING EVENTS
            
            this_frame_events = []
            
            
            
            start_active = False
            end_active = False
            
            if self.nothing:
                ex = 0
                ey = 0
                esx = 0
                esy = 0
                self.nothing = False
            
            for ind, event in enumerate(self.FILE.events):
                
                
                ex = int(event[0] * sx + px)
                ey = int(float(event[2]) * sy + py)
                esx = int(event[1] * sx )
                esy = int(sy)
                
                this_frame_events.append([ex, ey, esx, esy, event[3]])
                
                
                if ex not in range(0-w/2, w+w/2) and ex+esx not in range(0-w/2, w+w/2) and ex+esx/2 not in range(0-w/2, w+w/2):
                
                    continue
                elif ey not in range(0, h):
                    continue
                
                
                
                name = event[3]
                story = event[4]
                
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#3d3d3d"))
                #widget.window.draw_rectangle(xgc, True, ex, ey, esx+5, int(esy))
                ctx3 = widget.window.cairo_create()
                ctx3.set_source_rgba(0,0,0,0.4)
                ctx3.rectangle(ex-2, ey, esx+4, int(esy))
                ctx3.fill()
                #526969
                
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#526969"))
                #widget.window.draw_rectangle(xgc, True, ex, ey, esx, int(esy)/3)
                
                
                ############## SHOWING THE SCENES IN THE EVENT #############
                if self.event_select == ind and type(self.event_select) != bool:
                    self.scenes_in_event = []
                
                
                
                if "<scene>" in story and "</scene>" in story:
                    
                    sa = story.count("<scene>") # COUNT AMOUNT OF SCENES
                    
                    ts = story
                    
                    dot = 0
                    dots = []
                    
                    # getting the values of the dots
                    for n in range(sa):
                        
                        dot = dot + ts.find("<scene>")
                        d = [dot]
                        
                        ts = ts[ts.find("<scene>"):]
                        dot = dot + ts.find("</scene>")+8
                        
                        
                        # Adding scenes to a list to process later
                        
                        scene_text = ts[7:ts.find("</scene>")]
                        if self.event_select == ind and type(self.event_select) != bool:
                            self.scenes_in_event.append(scene_text)
                        
                        ts = ts[ts.find("</scene>")+8:]
                        
                        d.append(dot)
                        dots.append(d)
                        
                        
                            
                        
                        
                        
                        
                        
                    
                    
                    # printing them onto the screen
                    
                    for n, i in enumerate(dots):
                        
                        d1, d2 = i
                        
                        
                        
                        ds = int(  ex + ( float(esx) / len(story) *  d1 )  )
                        dw = int(   (float(esx) / len(story) *  d2)-( float(esx) / len(story) *  d1 ))
                        
    
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#526969"))
                        widget.window.draw_rectangle(xgc, True, ds+1, ey, dw-2, int(esy)/3)
                        
                        
                        
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#4c4c4c"))
                        #widget.window.draw_rectangle(xgc, False, ds, ey+3, dw, int(esy)-5)
                        
                        
                        
                        # MAKING SURE WE DRAW THE FUCKING ARROWS TO THE SCREEN LOL
                        
                        scnDATA = self.FILE.get_scenes_data()
                        
                        for arrowN, arrow in enumerate(self.FILE.arrows):
                            
                            
                            # start end arrows
                            if arrow[0][0] == -1:
                                self.arrows_output_dots[arrowN][0] = [60,80]
                                
                                start_active = True
                                
                            if arrow[1][0] == -1:
                                self.arrows_output_dots[arrowN][1] = [w-(w)/3-60,h-100]
                                
                                end_active = True
                            
                            
                            if arrow in linkchainpath:
                                self.arrows_output_dots[arrowN][2] = True
                                
                            
                            
                            try:
                                if arrow[0][0] == ind:
                                    
                                    if scnDATA[ind][n][1] == arrow[0][1]:
                                    
                                        
                                        self.arrows_output_dots[arrowN][0] = [dw+ds, (ey+(ey+esy))/2]
                                if arrow[1][0] == ind:
                                    
                                    if scnDATA[ind][n][1] == arrow[1][1]:
                                    
                                        
                                        self.arrows_output_dots[arrowN][1] = [ds, (ey+(ey+esy))/2]            
                                        
                                        
                            except:
                                pass        
                            
                            
                           
                        
                        
                        
                        
                        
                        if mx in range(ds, dw+ds) and my in range(ey, int(esy)+ey) and mx in range(0, w-w/3):
                            
                            
                            tooltip = "Event ID : "+name+"\nScene ID : "+scnDATA[ind][n][1]+"\n"+str(int(event[0]))+":"+str(int(event[2]))
                            
                            
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#fff"))
                            
                            if self.tool == "arrow":
                                
                                scnDATA = self.FILE.get_scenes_data()
                                
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#e13d3d"))
                                
                                self.arrow_to = [ds, (ey+(ey+esy))/2]
                                
                                self.arrow_selection[1] = [ind, scnDATA[ind][n][1]]
                                
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#4987af")) 
                            widget.window.draw_rectangle(xgc, True, ds+1, ey, dw-2, int(esy)/3)
                            
                            
                            if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active() and self.tool == "select": # IF CLICKED
                            
                                self.imgAT = []
                            
                                self.scene_select = n
                                
                                
                                try:
                                    scnDATA = self.FILE.get_scenes_data()
                                    scenestory = scnDATA[ind][n][3]
                                    self.shotsDATA = get_shots(scenestory, scnDATA[ind][n][1])
                                except:
                                    pass
                                self.shotsSCROLL = 0
                        
                        
                        
                        
                            ## IF TOOL IS SPLIT
                            
                            if self.tool == "split":
                                
                                
                                xgc.line_width = 4
                                
                                
                                END = False # Determents whether we looking at the end of the scene strip or the begining
                                
                                
                                if mx > ds+dw/2:
                                    
                                    END = True
                                    PIXEL = ((ds+dw) -   px)/sx -1
                                    
                                    
                                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#000"))
                                    widget.window.draw_line(xgc, ds+dw, int(esy/2)+ey-50, ds+dw, int(esy/2)+ey+50)
                                    widget.window.draw_pixbuf(None, self.split_action, 0, 0, ds+dw-20-1, int(esy/2)+ey-20 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
                                else:
                                    
                                    PIXEL = ((ds) -   px)/sx -1
                                    
                                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#000"))
                                    widget.window.draw_line(xgc, ds, int(esy/2)+ey-50, ds, int(esy/2)+ey+50)
                                    widget.window.draw_pixbuf(None, self.split_action, 0, 0, ds-20-1, int(esy/2)+ey-20 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
                        
                                if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active(): # IF CLICKED
                                
                                    self.undo_record()
                            
                            
                                    
                                    
                                    
                                    self.FILE.split(ind, i, END, PIXEL, n)
                                    self.tool = "select"
                                    
                                    scnDATA = self.FILE.get_scenes_data()
                                    
                                    self.doundo = True
                                    
                                xgc.line_width = 2
                                
                        ## IF ARROWS DRAWING
                            
                        if self.toolXY[0] in range(ds, dw+ds) and self.toolXY[1] in range(ey, int(esy)+ey) and self.tool == "arrow":    
                            
                            if self.tool == "arrow":
                                
                                scnDATA = self.FILE.get_scenes_data()
                                
                                self.toolXY = [dw+ds, (ey+(ey+esy))/2]
                                self.arrow_selection[0] = [ind, scnDATA[ind][n][1]]
                                
                                
                                
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#aaa"))
                                widget.window.draw_rectangle(xgc, False, ds+1, ey, dw-2, int(esy)/3)        
                                
                                
                        if n == self.scene_select and self.event_select == ind and type(self.event_select) != bool and self.tool != "arrow":
                            
                            #xgc.set_rgb_fg_color(gtk.gdk.color_parse("#fff"))
                            
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#4987af"))
                            widget.window.draw_rectangle(xgc, True, ds+1, ey, dw-2, int(esy)/3)
                        
                        # SCENE NAME
                        
                        try:                              # IDK WTF IS WITH THIS PEACE BUT IT WAS LAGGING WHEN SLIPT
                            ctx.set_source_rgb(1,1,1)     # IS ACTIVATED SO YEAH... I NEED TO LOOK INTO IT FURTHER
                            ctx.set_font_size(11)
                            ctx.move_to( ds+2, ey+12)
                            ctx.show_text(scnDATA[ind][n][1][:dw/7]) 
                        except:
                            pass
                
                
                
                
                # IF THIS EVEN IS CURRENTLY SELECTED
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#868686"))
                if self.event_select == ind and type(self.event_select) != bool:
                    
                    
                    # TAB
                    
                    
                    
                    if 65289 in self.keys and self.win.is_active():
                        if 65289 in self.keys:
                            self.keys.remove(65289)
                        
                        def ee(e=None):
                            
                            self.undo_record()
                            
                            editevent = dialogs.event(name, story, self.FILE, self.event_select)
                            editevent.edit()
                            
                            
                            try:
                                scnDATA = self.FILE.get_scenes_data()
                                scenestory = scnDATA[self.event_select][self.scene_select][3]
                                self.shotsDATA = get_shots(scenestory, scnDATA[self.event_select][self.scene_select][1])
                            except:
                                pass
                            
                            
                            
                            
                            self.doundo = True
                            
                        glib.timeout_add(10, ee)
                    
                    
                    
                    
                    # GUIDING LINES
                    xgc.line_width = 1
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#fff"))
                    widget.window.draw_rectangle(xgc, False, ex-2, ey, esx+4, int(esy))
                    #widget.window.draw_rectangle(xgc, False, 0, ey, w, esy)
                    #widget.window.draw_rectangle(xgc, False, ex, -2 , esx, h+2)
                    
                    # select color
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#e47649"))
                    
                #widget.window.draw_rectangle(xgc, False, ex, ey, esx, int(esy))
                
                # EVENT NAME
                ctx.set_source_rgb(1,1,1)
                ctx.set_font_size(11)
                ctx.move_to( ex+2, ey+esy/3+12)
                ctx.show_text(event[3][:esx/7])
                
                
                #this_frame_events.append([ex, ey, esx, esy, event[3]])
            
            
            # MERGING WITH THE ARROWS FROM IMAGES
            
            for i in self.ImageArrowsDict:
               
                if i in imagesonscreen and self.ImageArrowsDict[i][2] in imagesonscreen:
                    self.arrows_output_dots.append(self.ImageArrowsDict[i])
            
            #self.arrows_output_dots = self.arrows_output_dots +  self.ImageArrows
            
            ###### OUTPUTTING ARROWS TO THE SCREEEEENNNNNN
            
            for dot in self.arrows_output_dots:
                    
                
                
                arx, ary = dot[0]
                tox, toy = dot[1]
                shine    = dot[2]   
                
                #if arx not in range(1, w) or ary not in range(1, h) or tox not in range(1, w) or toy not in range(1, h):
                if ary not in range(1, h) or toy not in range(1, h):
                    continue
                
                
                
                if shine:
                    
                    
                    if linkchained:
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#959595"))        
                    else:
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#e47649"))    
                else:
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#e13d3d"))
                xgc.line_width = 3
                widget.window.draw_line(xgc, arx, ary, tox, toy)
                xgc.line_width = 1
                
                #TRIANGLES LOL
                #dots = (arx-10, ary+10), (arx, ary), (arx-10, ary-10)
                #widget.window.draw_polygon(xgc, True, dots)
                widget.window.draw_pixbuf(None, self.node_link, 0, 0, arx-5, ary-5 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                
                
                #dots = (tox, toy+10), (tox+10, toy), (tox, toy-10)
                #widget.window.draw_polygon(xgc, True, dots)
                widget.window.draw_pixbuf(None, self.node_link, 0, 0, tox-5, toy-5 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                
                
                
                
            fif = datetime.datetime.now()
            mil  = fif - stf
            perfStat.append([  "EVENT TOOL", mil.microseconds])
            
            stf = datetime.datetime.now()
            
            
            
            
            #ITEM ADDER
            
            
            if self.tool == "linkitem" or self.tool == "linkimage":
                
                
                if "GDK_BUTTON3" in str(fx): ## CANCEL with right mouse button
                    
                    self.tool = "select"
                    self.toolactive = False 
            
            
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#3f3f3f"))
                widget.window.draw_rectangle(xgc, False, mx, my, 150, 150+22)
                
                if "GDK_BUTTON1" in str(fx) and self.allowed and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active(): #IF CLICKED
                    
                    
                    
                    def ee(e=None):
                        
                        if e == "linkitem":
                             
                            try:
                                u = itemselector.select(self.pf)+"/renders/"
                                if u == "/renders/":
                                    self.tool = "select"
                                    self.toolactive = False 
                                    self.imagesearch = ""
                                    return
                                
                            except:
                                
                            
                                self.tool = "select"
                                self.toolactive = False 
                                
                                return
                                
                            if os.path.exists(self.pf+"/"+u+"Preview.png"):
                                u = u+"Preview.png"
                            elif os.path.exists(self.pf+"/"+u+"Preview.jpg"):
                                u = u+"Preview.jpg"
                            else:
                                u = u+"Preview.png"
                            
                            
                            u = self.pf+""+u
                        
                        elif e == "linkimage":
                            
                            u = imageselector.select(self.pf, self.imagesearch)
                                
                            if not u:
                                
                            
                                self.tool = "select"
                                self.toolactive = False 
                                self.imagesearch = ""
                                return
                            
                            self.imagesearch = ""
                            #u = "/home/vc3/launch_grub_texture.png"
                        
                        x,y = self.toolXY
                        
                        #pureX = (x  -  px)/sx  - 1   # NOT GOOD
                        #pureY = (y+22  -  py)/sy 
                        
                        pureX = x / sx - px           # GOOD
                        pureY = (y + 22) / sx - px
                        
                        ################## COPIED FROM THE BOTTOM ######################
                        
                        imageNOT = True
                        for i in fileformats.images:
                            
                            if u.lower().endswith(i):
                                imageNOT = False
                                
                                # FOUND THE IMAGE
                                
                                #making athumb and saving it using a random name
                                
                                #making sure that thumb directory exists
                                if not os.path.exists(self.pf+"/pln/thumbs/"):
                                    os.makedirs(self.pf+"/pln/thumbs/")
                                
                                
                                #chosing a random name for the thumb
                                rndname = ""
                                rndchar = "QWERTYUIOPASDFGHJKLZXCVBNM1234567890"
                                while os.path.exists(self.pf+"/pln/thumbs/"+rndname+".png") or rndname == "":
                                    rndname = ""
                                    for l in range(20):
                                        rndname = rndname + random.choice(rndchar)
                                    
                                
                                #thumbnailer.thumbnail
                                
                                fromr  = open(thumbnailer.thumbnail(u, x=150, y=150), "r")
                                saveto = open(self.pf+"/pln/thumbs/"+rndname+".png", "w")
                                saveto.write(fromr.read())
                                saveto.close()
                                pureX = (x -   self.px)/self.sx  - 1
                                pureY = int((y    - self.py   )/self.sy)
                                
                                if u.startswith(self.pf):
                                    self.FILE.images.append([pureX, pureY, "RELATIVE", u.replace(self.pf, ""), rndname, gtk.gdk.pixbuf_new_from_file(self.pf+"/pln/thumbs/"+rndname+".png")])
                                else:
                                    self.FILE.images.append([pureX, pureY, "ABSOLUTE", u, rndname, gtk.gdk.pixbuf_new_from_file(self.pf+"/pln/thumbs/"+rndname+".png")])
                                
                                
                                
                                
                        if imageNOT:
                            try:
                                MT = open(urllib.unquote(data.get_text().split("\n")[0])[7:], "r")
                                lets = "    qwertyuiop[]asdfghjkl;'\\zxcvbnm,./`1234567890-=\nQWERTYUIOP{}ASDFGHJKL:\"|ZXCVBNM<>?~!@#$%^&*()_+"
                                MT = MT.read()
                                for i in MT:
                                    if i not in lets:
                                        return
                                
                                #pureX = (x -   self.px)/self.sx  - 1
                                pureS = 100.0
                                #pureY = (y    - self.py   )/self.sy
                                
                                
                                self.FILE.events.append([pureX, pureS, pureY, urllib.unquote(data.get_text().split("\n")[0])[urllib.unquote(data.get_text().split("\n")[0]).rfind("/")+1:], MT])
                            
                            except:
                                raise
                        
                        
                        ##################### TILL HERE ####################
                        
                        
                        self.tool = "select"
                        self.toolactive = False 
                        
                    
                    
                    glib.timeout_add(10, ee, self.tool)
                    
                    self.tool = "linkingnow"
                    self.toolactive = False
                    self.toolXY = [mx, my]
            
            
            if self.tool == "linkingnow":
                
                x,y = self.toolXY
                
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#3f3f3f"))
                widget.window.draw_rectangle(xgc, False, x, y, 150, 150+22)
                
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#3f3f3f"))
                widget.window.draw_rectangle(xgc, False, x, y, 150, 22)
            
            fif = datetime.datetime.now()
            mil  = fif - stf
            perfStat.append([ "ITEM ADDER", mil.microseconds])
            
            stf = datetime.datetime.now()
            
            
            ### EDITING EVENTS
            
            if self.tool == "select":
                
                for ind, event in enumerate(this_frame_events):
                    
                    ex = event[0]
                    ey = event[1]
                    esx = int(event[2])
                    esy = int(sy)
                    name = event[4]
                    
                    if ex not in range(0-w/2, w+w/2) and ex+esx not in range(0-w/2, w+w/2) and ex+esx/2 not in range(0-w/2, w+w/2):
                
                        continue
                    elif ey not in range(0, h):
                        continue
                    
                    
                    if mx > 0 and mx < w-(w)/3 and my > 50:
                        # if on the right side TO RESIZE
                        if mx in range(ex-2, ex+2) and my in range(ey, ey+esy):
                            widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.SB_H_DOUBLE_ARROW))
                            self.showcross = False
                            if "GDK_BUTTON1" in str(fx) and self.allowed and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active():
                                self.event_resize = [0, ind]  
                                self.event_select = ind
                                self.image_select = False
                                self.marker_select = len(self.FILE.markers)+2
                                
                                if "<scene>" not in self.FILE.events[ind][4]: #REMOVING BUGGY SCENE PREVIEWS
                                    self.shotsDATA = []
                                
                                
                        # if on the left side TO RESIZE
                        elif mx in range(ex+esx-2, ex+esx+2) and my in range(ey, ey+esy):
                            widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.SB_H_DOUBLE_ARROW))
                            self.showcross = False
                            if "GDK_BUTTON1" in str(fx) and self.allowed and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active():
                                self.event_resize = [1, ind]  
                                self.event_select = ind
                                self.image_select = False
                                self.marker_select = len(self.FILE.markers)+2
                                
                                if "<scene>" not in self.FILE.events[ind][4]:  #REMOVING BUGGY SCENE PREVIEWS
                                    self.shotsDATA = []
                                
                        # selecting or moving the thingy
                        elif mx in range(ex, ex+esx) and my in range(ey, ey+esy):
                            
                           # get mouse to show the grabber
                            widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.FLEUR))
                            self.showcross = False
                            # show the selection color around
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#e47649"))
                            widget.window.draw_rectangle(xgc, False, ex-2, ey, esx+4, esy)
                            
                            
                            if "GDK_BUTTON1" in str(fx) and self.allowed and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active():
                                
                                self.event_move = [True, ind]
                                self.event_select = ind
                                self.image_select = False
                                self.marker_select = len(self.FILE.markers)+2
                                
                                if "<scene>" not in self.FILE.events[ind][4]:  #REMOVING BUGGY SCENE PREVIEWS
                                    self.shotsDATA = []
                    
                            
                        
                                
            ###### MOVING EVENTS    #####
            
            
            if self.event_move:
                
                ind = self.event_move[1]
                
                
                
                #### X
                if self.mpx > mx and "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" in str(self.mpf):
                        
                    self.FILE.events[ind][0] = self.FILE.events[ind][0] + (mx-self.mpx ) / sx
                    
                    
                if self.mpx < mx and "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" in str(self.mpf):
                    
                    self.FILE.events[ind][0] = self.FILE.events[ind][0] - (self.mpx-mx  ) / sx
                
                
                ### Y
                
                if self.mpy > my and "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" in str(self.mpf):
                        
                    self.FILE.events[ind][2] = self.FILE.events[ind][2] + float(my-self.mpy ) / sy 
                    
                    
                if self.mpy < my and "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" in str(self.mpf):
                    
                    self.FILE.events[ind][2] = self.FILE.events[ind][2] - float(self.mpy-my  ) / sy 
                
                
                    
                if "GDK_BUTTON1" not in str(fx) and "GDK_BUTTON1" not in str(self.mpf):
                    
                    # SO FAR THE BUG IS MADE BY THE DELETING OF EVENT WTF
                    try:
                        self.FILE.events[ind][2] = float(self.FILE.events[ind][2])
                        self.event_move = False
                    except:
                        pass
                
                
            
            #### RESIZING EVENTS #######
            
            if self.event_resize:
                
                direction = self.event_resize[0]
                ind = self.event_resize[1]
                
                if direction == 0:
                    if self.mpx > mx and "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" in str(self.mpf):
                        
                        self.FILE.events[ind][0] = self.FILE.events[ind][0] + (mx-self.mpx ) / sx
                        self.FILE.events[ind][1] = self.FILE.events[ind][1] - (mx-self.mpx ) / sx
                    
                    if self.mpx < mx and "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" in str(self.mpf):
                        
                        self.FILE.events[ind][0] = self.FILE.events[ind][0] - (self.mpx-mx  ) / sx
                        self.FILE.events[ind][1] = self.FILE.events[ind][1] + (self.mpx-mx  ) / sx
                    
                    if self.FILE.events[ind][1] < 2:
                        
                        self.event_resize = [1, ind]
                    
                if direction == 1:
                    if self.mpx > mx and "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" in str(self.mpf):
                        
                        self.FILE.events[ind][1] = self.FILE.events[ind][1] + (mx-self.mpx ) / sx
                        
                    
                    if self.mpx < mx and "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" in str(self.mpf):
                        
                        self.FILE.events[ind][1] = self.FILE.events[ind][1] - (self.mpx-mx  ) / sx
                        
                    
                    if self.FILE.events[ind][1] < 2:
                        
                        self.event_resize = [0, ind]
                
                
                
                
                
                
                
                
                if "GDK_BUTTON1" not in str(fx) and "GDK_BUTTON1" not in str(self.mpf):
                    
                    self.event_resize = False
                
                
            
            
             
                
                    
                    
            
            
            if self.tool == "event":
                
                
                if "GDK_BUTTON3" in str(fx): ## CANCEL with right mouse button
                    
                    self.tool = "select"
                    self.toolactive = False
                
                
                
                # Activate
                
                if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active():
                    
                    
                    if mx > 0 and mx < w-(w)/3 and my > 50:
                    
                        # saving the xy for the event
                        self.toolXY = [mx, my]
                        
                        widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.SB_H_DOUBLE_ARROW))
                        
                        self.toolactive = True
                # Active
                if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" in str(self.mpf) and self.toolactive:
                    
                    widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.SB_H_DOUBLE_ARROW))
                    
                    if tx < mx:
                        pureX = (tx -   px)/sx  - 1
                        pureS = (mx-tx)/sx
                    else:
                        pureX = (mx  -  px)/sx  - 1
                        pureS = (tx-mx)/sx
                    pureY = (my    - py   )/sy
                        
                    
                    ex = int(pureX * sx + px)
                    ey = int(pureY * sy + py)
                    esx = int(pureS * sx )
                    esy = int(sy)
                    
                        
                        
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#5c5c5c"))
                    
                    
                    # IF OVERLAPS WITH ANOTHER ONE
                    event, overlap = self.events_overlap(my, mx, ex, ey, esx, esy, this_frame_events)
                        
                        
                        
                        
                        
                        
                    if overlap:    
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#F00"))
                        
                        widget.window.draw_rectangle(xgc, False, event[0], event[1], event[2], event[3])
                            
                            
                            
                    widget.window.draw_rectangle(xgc, False, ex, ey, esx, esy)
                    
                
                
                # Release
            
                if "GDK_BUTTON1" not in str(fx) and "GDK_BUTTON1" in str(self.mpf) and self.toolactive:
                    
                    
                    
                    #WRITTING TO HYSTORY
                    history.write(os.getcwd() ,"pln/main.bos", "[Edited]")
                    
                    
                    
                    # making the math of the values before saving 
                    
                    
                    
                        
                    if tx < mx:
                        pureX = (tx -   px)/sx  - 1
                        pureS = (mx-tx)/sx
                    else:
                        pureX = (mx  -  px)/sx  - 1
                        pureS = (tx-mx)/sx
                    pureY = (my    - py   )/sy
                    
                    
                    
                    
                    
                    eventname = "Scene"
                    
                    foundtimes = 0
                    for event in self.FILE.events:
                        if event[3].startswith(eventname):
                            foundtimes = foundtimes + 1
                    
                    if foundtimes > 0:
                        eventname = eventname + "_" + str(foundtimes+1)
                    
                    
                    existing = os.walk(self.pf+"/rnd/").next()[1]
                    
                    for i in self.FILE.events:
                        if "<scene>" in i[4] and "</scene>" in i[4]:
                            
                            e = i[4]
                            
                            ep = e[e.find("<scene>"):e.rfind("</scene>")+8]
                            for s in ep.split("</scene>"):
                                
                                #s = s[s.find("<scene>")+8]
                                s = s[s.find('"')+1:]
                                s = s[:s.find('"')]
                                if s not in existing:
                                    existing.append(s)
                        
                    
                    
                    rnn = foundtimes+1
                    rn = "Scene_"
                    while rn + str(rnn) in  existing:
                        rnn = rnn + 1
                   
                    rn = rn + str(rnn)
                    
                        
                    storypart = "<scene>\""+rn+"\"\n\n</scene>"    
                    
                    
                    
                    # getting the event editor
                    
                    def ee(e=None):
                        editevent = dialogs.event(eventname, storypart, self.FILE, len(self.FILE.events)-1)
                        editevent.edit()
                        
                        try:
                            scnDATA = self.FILE.get_scenes_data()
                            scenestory = scnDATA[self.event_select][self.scene_select][3]
                            self.shotsDATA = get_shots(scenestory, scnDATA[self.event_select][self.scene_select][1])
                        except:
                            pass
                        
                        
                    glib.timeout_add(10, ee)
                    
                    self.FILE.events.append([pureX, pureS, pureY, eventname, storypart])
                    self.event_select = len(self.FILE.events)-1
                    self.image_select = False
                    
                    self.tool = "select"
                    self.toolactive = False
                    
                    self.marker_select = len(self.FILE.markers)+2
            
            
            fif = datetime.datetime.now()
            mil  = fif - stf
            perfStat.append([ "EDITING EVENTS", mil.microseconds])
            
            stf = datetime.datetime.now()
            
            # ARROW DRAW
            
            
            if self.tool == "arrow":
                
                if "GDK_BUTTON3" in str(fx): ## CANCEL with right mouse button
                    
                    self.tool = "select"
                    self.toolactive = False
                        
                # Activate
                
                if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active():
                    
                    
                    if mx > 0 and mx < w-(w)/3 and my > 50:
                    
                        # saving the xy for the event
                        self.toolXY = [mx, my]
                        
                        widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.DOT))
                        self.showcross = False
                        
                        self.toolactive = True
                
                
                
                # Active
                if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" in str(self.mpf) and self.toolactive:
                    
                    
                    tx, ty = self.toolXY
                    
                    xgc.line_width = 4
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#000"))
                    if self.arrow_selection in self.FILE.arrows:
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#888"))
                        
                    
                    
                    #FIRST TRIANGLE
                    dots = (tx-10, ty+10), (tx, ty), (tx-10, ty-10)
                    widget.window.draw_pixbuf(None, self.node_link, 0, 0, tx-5, ty-5 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                    
                    if self.arrow_to == False:
                        widget.window.draw_line(xgc, tx, ty, mx, my)
                        
                        
                        
                        
                        
                        dots = (mx, my+10), (mx+10, my), (mx, my-10)
                        widget.window.draw_pixbuf(None, self.node_link, 0, 0, mx-5, my-5 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                    
                    else:
                        widget.window.draw_line(xgc, tx, ty, self.arrow_to[0], self.arrow_to[1])
                        
                        
                        dots = (self.arrow_to[0], self.arrow_to[1]+10), (self.arrow_to[0]+10, self.arrow_to[1]), (self.arrow_to[0], self.arrow_to[1]-10)
                        widget.window.draw_pixbuf(None, self.node_link, 0, 0, self.arrow_to[0]-5, self.arrow_to[1]-5 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                    
                    
                    # Release
            
                if "GDK_BUTTON1" not in str(fx) and "GDK_BUTTON1" in str(self.mpf) and self.toolactive:
                    
                    
                    
                    
                    if False not in self.arrow_selection and self.arrow_selection[0] != self.arrow_selection[1]:
                        if self.arrow_selection not in self.FILE.arrows:
                            self.FILE.arrows.append(self.arrow_selection)
                        else:
                            self.FILE.arrows.remove(self.arrow_selection)    
                            
                            
                
            
                    self.arrow_selection = [False, False]
                    
                    self.FILE.clear_arrows()
                
                    self.marker_select = len(self.FILE.markers)+2
                
            
            fif = datetime.datetime.now()
            mil  = fif - stf
            perfStat.append([ "DRAWING ARROWS", mil.microseconds])
            
            stf = datetime.datetime.now()
            
            
            # ADD MARKER
            
            if self.tool == "marker":
                
                if "GDK_BUTTON3" in str(fx): ## CANCEL with right mouse button
                    
                    self.tool = "select"
                    self.toolactive = False
            
                xgc.line_width = 1
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#aaa"))
                widget.window.draw_line(xgc, mx, 0, mx, h)
                xgc.line_width = 2
            
            
            
            #  CLICK
                
                if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) :
                    
                    
                    self.FILE.markers.append( [ (mx - px)/sx , "MARK" ] )
                    
                    
                    def ee(e=None):
                        dialogs.marker(len(self.FILE.markers)-1, self.FILE)
                        
                    
                    glib.timeout_add(10, ee)
                        
                        
                    self.marker_select = len(self.FILE.markers)-1
                    
                    
                    self.tool = "select"
                    self.toolactive = False
            
            ### TOP N SIDE PANEL
                
                
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#3f3f3f"))
            widget.window.draw_rectangle(xgc, True, 0, 0, w-(w)/3, 50) 
            
                
            fif = datetime.datetime.now()
            mil  = fif - stf
            perfStat.append(["ADD MARKER", mil.microseconds])
            
            stf = datetime.datetime.now()
            
            
            
            ################################### TOP PANEL ICONS
            
            #SAVE BUTTON
            
            #saveshortcut = False
            #if 65507 in self.keys and 115 in self.keys:
            #    saveshortcut = True
            #if 65507 in self.keys and 83 in self.keys:
            #    saveshortcut = True
            # 
            #if mx in range(260,280) and my in range(5,45):
            #    
            #    
            #    tooltip = "[ CTRL - S ]\n\nSave File to \n/pln/main.bos"
            #    
            #    
            #    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#999"))
            #    widget.window.draw_rectangle(xgc, True, 260, 5, 40, 40)
            #    
            #    if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active() :
            #        
            #        saveshortcut = True
            #
            #if saveshortcut:
            #    
            #    
            #    
            #    widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
            #   
            #    while gtk.events_pending():
            #        gtk.main_iteration()
            #       
            #    self.FILE.save(px,py,sx,sy)
            #
            #widget.window.draw_pixbuf(None, self.saveicon, 0, 0, 260, 5 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
            
            
            # EVENT BUTTON
            
            
            #if 69 in self.keys or 101 in self.keys:   # SHORT CUT
            #    self.tool = "event"                   # PRESS E
            #    self.toolactive = False
            #
            #if self.tool == "event":
            #    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#e47649"))
            #    widget.window.draw_rectangle(xgc, True, 160, 5, 40, 40)
            #else:
            #    if mx in range(160, 200) and my in range(5,45):
            #        
            #        tooltip = "[ E ]\n\nAdd Event\nA part of scrip/story\nin relation to time"
            #        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#999"))
            #        widget.window.draw_rectangle(xgc, True, 160, 5, 40, 40)
            #        
            #        if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active():
            #            
            #            self.tool = "event"
            #            self.toolactive = False
            # 
            #widget.window.draw_pixbuf(None, self.eventicon, 0, 0, 160, 5 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
            
            
            
            # ADD SCENE BUTTON
            addscenenowshortcut = False
            if 110 in self.keys and self.win.is_active() and 65505 not in self.keys:
                if 110 in self.keys:
                    self.keys.remove(110)
                #addscenenowshortcut = True
                self.tool = "event"
                self.toolactive = False
            
            
            if self.tool == "event":
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#5175ae"))
                widget.window.draw_rectangle(xgc, True, 10, 5, 40, 40)    
                
            
            if mx in range(10,50) and my in range(5,45):
                
                tooltip = "[ N ]\nCreate a new scene"
                
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#395384"))
                widget.window.draw_rectangle(xgc, True, 10, 5, 40, 40)
                
                if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active():# and len(self.FILE.events):
                    
                    self.tool = "event"
                    self.toolactive = False
                    
                    #addscenenowshortcut = True
            if addscenenowshortcut and len(self.FILE.events):
                    
                self.tool = "select"
                self.toolactive = False
                
                event = self.FILE.events[self.event_select]
            
                name = event[3]
                story = event[4]
                
                def justdoit(v=None):
                    sae = dialogs.event(name, story, self.FILE, self.event_select)
                    sae.add_scene()
                glib.timeout_add(10, justdoit)
                    
            
            
             
            widget.window.draw_pixbuf(None, self.scenceicon, 0, 0, 10, 5 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
            
            
            
            
            # ADD CONNECTION BUTTON
            
            if 97 in self.keys or 65 in self.keys:   # SHORT CUT
                self.tool = "arrow"                   # PRESS E
                self.toolactive = False
            
            
            if self.tool == "arrow":
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#5175ae"))
                widget.window.draw_rectangle(xgc, True, 60, 5, 40, 40)
            else:
                if mx in range(60,60+40) and my in range(5,45):
                    
                    tooltip = "[ A ]\n\nArrow connection\nto guide editing of the scenes"
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#395384"))
                    widget.window.draw_rectangle(xgc, True, 60, 5, 40, 40)
                    
                    if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active() and len(self.FILE.events):
                        
                        self.tool = "arrow"
                        self.toolactive = False
            
            widget.window.draw_pixbuf(None, self.cuticon, 0, 0, 60, 5 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
            
            
            # SPLIT EVENT BETWEEN SCENES
            
            
            if 75 in self.keys or 107 in self.keys:
                
                
                self.tool = "split"                   # PRESS K
                self.toolactive = False
            
            
            if self.tool == "split":
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#5175ae"))
                widget.window.draw_rectangle(xgc, True, 110, 5, 40, 40)
            else:
                if mx in range(110,150) and my in range(5,45):
                
                
                    tooltip = "[ K ]\n\nSplit events between the scenes\nlike a Knife"
                        
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#395384"))
                    widget.window.draw_rectangle(xgc, True, 110, 5, 40, 40)
                    
                    if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active() :
                        
                        self.tool = "split"
                        self.toolactive = False
                    
                    
            widget.window.draw_pixbuf(None, self.split_event, 0, 0, 110, 5 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
            
            
            
            # ADD MARKER
            
            if 77 in self.keys or 109 in self.keys:
                
                
                self.tool = "marker"                   # PRESS M
                self.toolactive = False
            
            
            if self.tool == "marker":
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#5175ae"))
                widget.window.draw_rectangle(xgc, True, 160, 5, 40, 40)
            else:
                if mx in range(160,200) and my in range(5,45):
                    
                    tooltip = "[ M ]\n\nMark an important timepoint"
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#395384"))
                    widget.window.draw_rectangle(xgc, True, 160, 5, 40, 40)
                    
                    if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active() :
                        
                        self.tool = "marker"
                        self.toolactive = False
            
            
            
            
            widget.window.draw_pixbuf(None, self.markericon, 0, 0, 160, 5 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
            
            # Link Item
            
            if 76 in self.keys or 108 in self.keys:
                
                
                self.tool = "linkitem"               
                self.toolactive = False
            
            
            if self.tool == "linkitem":
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#5175ae"))
                widget.window.draw_rectangle(xgc, True, 210, 5, 40, 40)
            else:
                if mx in range(210,250) and my in range(5,45):
                    
                    tooltip = "[ L ]\n\nLink item to the Story Editor"
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#395384"))
                    widget.window.draw_rectangle(xgc, True, 210, 5, 40, 40)
                    
                    if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active() :
                        
                        self.tool = "linkitem"
                        self.toolactive = False
            
            
            widget.window.draw_pixbuf(None, self.item_big, 0, 0, 210, 5 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
            
            
            
            
            # LINK IMAGE
            
            
            
            if 73 in self.keys or 105 in self.keys:
                
                
                self.tool = "linkimage"                  
                self.toolactive = False
            
            
            if self.tool == "linkimage":
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#5175ae"))
                widget.window.draw_rectangle(xgc, True, 260, 5, 40, 40)
            else:
                if mx in range(260,260+40) and my in range(5,45):
                    
                    tooltip = "[ I ]\n\nLink image file to the Story Editor"
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#395384"))
                    widget.window.draw_rectangle(xgc, True, 260, 5, 40, 40)
                    
                    if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active() :
                        
                        self.tool = "linkimage"
                        self.toolactive = False
            
            widget.window.draw_pixbuf(None, self.image_add, 0, 0, 260, 5 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
            
            
            
            
            
            
            ##############   >>>>     SCENE PERSENTAGE <<<<<<   #################
            
            
            
            
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#d0d0d0"))
            widget.window.draw_rectangle(xgc, True, 400, 5, w-(w)/3-110-(450), 40)
            
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
            widget.window.draw_rectangle(xgc, True, 400, 5, int((w-(w)/3-110-(450))*self.scnPERCENT), 40)
            
            ctx.set_source_rgb(1,1,1)
            ctx.set_font_size(20)
            ctx.move_to( 320, 32)
            ctx.show_text(str(int(self.scnPERCENT*100))+"%")
            
            
            
            
            
            if "GDK_BUTTON1" not in str(fx) and "GDK_BUTTON1" in str(self.mpf) and self.win.is_active() : # IF RELEASED
            
                self.scnPERCENT = get_scenes_percentage(self.FILE)
            
            
            
            
            
            
                
            ### RENDER LISTS BUTTON ###
            
            
            if mx in range(w-(w)/3-150, w-(w)/3-110) and my in range(5, 45):
            
            
                
                tooltip = "Manage Render Lists\n\nCreate Lists to render\nmore then 1 blend file\nat ones in a sequence."
            
                if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active() : # IF CLICKED
                
                    def ee(e=None):
                        render_lists.main(self.pf)
                    
                    glib.timeout_add(10, ee)
                
                
                
                    
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#999"))
                widget.window.draw_rectangle(xgc, True, w-(w)/3-150, 5, 40, 40)
            
            
            
            
            
                
            widget.window.draw_pixbuf(None, self.render_big, 0, 0, w-(w)/3-150, 5 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
            
                
                
                
                
                
                
                
            #########   START >>>>>>>>>>> END ##########
            
            
            
            
            
            
            
            ### VIEW SCRIPT BUTTON ###
            
            
            if mx in range(w-(w)/3-50, w-(w)/3-10) and my in range(5, 45):
            
            
                if linkchained:
                    tooltip = "View Full Script"
                
                    if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active() : # IF CLICKED
                    
                        def ee(e=None):
                            editevent = dialogs.event(False, False, self.FILE, len(self.FILE.events)-1)
                            editevent.view_script(linkchainpath)
                        
                        glib.timeout_add(10, ee)
                
                
                else:
                    tooltip = "Connect arrows [ A ]\nfrom Start to End nodes\nthrough all the movie scenes\nif this icon will glow\nyou will be able to\nview full script"
                    
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#999"))
                widget.window.draw_rectangle(xgc, True, w-(w)/3-50, 5, 40, 40)
            
            
            
            
            if linkchained:
                
                widget.window.draw_pixbuf(None, self.gen_script_active, 0, 0, w-(w)/3-50, 5 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
            else:
                
                widget.window.draw_pixbuf(None, self.gen_script, 0, 0, w-(w)/3-50, 5 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
            
            
            
            
            
            #start
            #if mx in range(10, 50) and my in range(60, 110):
            #    tooltip = "Start of the film\n\n Connect to the first scene\nwith the arrow tool [ A ]"
            #    widget.window.draw_pixbuf(None, self.start_mo, 0, 0, 10, 60 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
            #else:
            #    
            #    if start_active:
            #        widget.window.draw_pixbuf(None, self.start_active, 0, 0, 10, 60 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)                  
            #    else:
            #        widget.window.draw_pixbuf(None, self.start_grey, 0, 0, 10, 60 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
            # 
            
            
            # THE NEW START WIDGET THAT LOOKS LIKE A NODE
            
            
            
            #ctx3 = widget.window.cairo_create()
            ctx3.set_source_rgba(0,0,0,0.4)
            ctx3.rectangle(5, 55, 50, 50)
            ctx3.fill()
            
            # TOP PART
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#9e343e"))
            widget.window.draw_rectangle(xgc, True, 5,55,50,50/3)
            
            #TEXT
            ctx.set_source_rgb(1,1,1)
            ctx.set_font_size(10)
            ctx.move_to( 10, 67)
            ctx.show_text("Start")
            
            if mx in range(10, 50) and my in range(60, 110):
                tooltip = "Start of the film\n\n Connect to the first scene\nwith the arrow tool [ A ]"
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#aaa"))
                widget.window.draw_rectangle(xgc, False, 5,55,50,50)
            
            
            
            if tx in range(10, 50) and ty in range(60, 110):    
               if self.tool == "arrow" and "GDK_BUTTON1" in str(fx):
               
                   self.arrow_selection[0] = [-1,"start"]
                
                
                
            
            
            
            
            
            
            
            
            
            # THE NEW END WIDGET THAT LOOKS LIKE A NODE
            
            #ctx3 = widget.window.cairo_create()
            ctx3.set_source_rgba(0,0,0,0.4)
            ctx3.rectangle(w-(w)/3-55, h-120, 50, 50)
            ctx3.fill()
            
            # TOP PART
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#9e343e"))
            widget.window.draw_rectangle(xgc, True, w-(w)/3-55,h-120,50,50/3)
            
            #TEXT
            ctx.set_source_rgb(1,1,1)
            ctx.set_font_size(10)
            ctx.move_to( w-(w)/3-50, h-110)
            ctx.show_text("End")
            
            
            #end
            if mx in range(w-(w)/3-50, w-(w)/3-10) and my in range(h-120, h-120+110):
                tooltip = "End of the film\n\n Connet the ending scene to it\nwith the arrow tool [ A ]"
                #widget.window.draw_pixbuf(None, self.end_mo, 0, 0, w-(w)/3-50, h-120 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#aaa"))
                widget.window.draw_rectangle(xgc, False, w-(w)/3-55,h-120,50,50)
                
                
                
                
                if self.tool == "arrow" and "GDK_BUTTON1" in str(fx):
                
                    self.arrow_selection[1] = [-1,"end"]
                
            #else:
            #    if end_active:
            #        widget.window.draw_pixbuf(None, self.end_active, 0, 0, w-(w)/3-50, h-120 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
            #    else:
            #        widget.window.draw_pixbuf(None, self.end_grey, 0, 0, w-(w)/3-50, h-120 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
            
            
            
            
            
            
            
            #### SEQUENCE EDITOR REACH BUTTON #####
            
            if mx in range(w-(w)/3-100, w-(w)/3-60) and my in range(5, 45):
            
            
                
                tooltip = "Edit Movie\n Open /rnd/sequence.blend"
            
                if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active() : # IF CLICKED
                    
                    cblndr = ""
                                        
                    try:
                        bv = open(self.pf+"/py_data/blenderver.data", "r")
                        bv = bv.read().split("\n")
                        
                        
                        
                        if int(bv[0]) > 0:
                            cblndr = bv[int(bv[0])]+"/"
                    except:
                        pass
                    
                    Popen([cblndr+"blender", self.pf+"/rnd/sequence.blend"])
                    #os.system(cblndr+"blender "+self.pf+"/rnd/sequence.blend")
                
                
                
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#999"))
                widget.window.draw_rectangle(xgc, True, w-(w)/3-100, 5, 40, 40)
            
            
            
            
            
                
            widget.window.draw_pixbuf(None, self.sequence, 0, 0, w-(w)/3-100, 5 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
            
            
            
            
            
            
            
            
            
            # DELETE EVENT SHORT KEY #
            
            allowdelete = False
            if not self.deletelastframe:
                allowdelete = True
            
            
            if 65535 in self.keys: #and allowdelete
                
                
                
                if self.event_select < len(self.FILE.events)  and allowdelete  and self.tool == "select":
                    
                    self.undo_record()
                    
                    self.FILE.event_delete(self.event_select)
                
                
                    self.shotsDATA = []
                    self.event_select = False
                    self.image_select = False
                    self.deletelastframe = True
                    
                    self.doundo = True
            else:
                self.deletelastframe = False
                
            
            
            
            
            
            fif = datetime.datetime.now()
            mil  = fif - stf
            perfStat.append([ "TOP PANNEL", mil.microseconds])
            
            stf = datetime.datetime.now()
            
            
            
                
                
            ##### OTHER SIDE PANEL ####
            
            
            Pstart = w-(w)/3
            Ppart = (w)/3-50
            
            
            
            
            
            
            
            
            ##### SCENE TEXT ####
            
            
            self.event_select # number of current event
            self.scene_select # number of current scene inside the event
            self.shotsSCROLL  # pixel to scroll to in the shotlist
            
            shotlistlength = 20
           
           
           
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#3f3f3f"))   #7e5349
            #widget.window.draw_rectangle(xgc, True, Pstart, 120, Ppart, h-120)
            
            ctx3 = widget.window.cairo_create()
            ctx3.set_source_rgba(0.1,0.1,0.1,0.9)
            ctx3.rectangle(Pstart, 120, Ppart, h-120)
            ctx3.fill()
            
            
                    
            #mark for faster moves
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#1c1c1c"))
            widget.window.draw_rectangle(xgc, True, w-50, 0, 200, h)
            
            #mark for faster moves
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#232323"))
            widget.window.draw_rectangle(xgc, True, w-50, 0, 200, 50)
            
            widget.window.draw_rectangle(xgc, True, w-50, h-50, 200, 50)
            
            SCnames = [] # [NAME, shotlistlength] 
            
            
            
            if self.shotsDATA:
                try:
                    
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#2c2c2c"))
                    widget.window.draw_rectangle(xgc, True, Pstart, shotlistlength+120+self.shotsSCROLL-20, Ppart, 45)
                    
                    
                    
                    SSname = scnDATA[self.event_select][self.scene_select][1]
                    
                    ctx2.set_source_rgb(1,1,1)
                    ctx2.set_font_size(20)
                    ctx2.move_to( Pstart+20+(Ppart-50)/2-len(SSname)*12/2, shotlistlength+120+self.shotsSCROLL+5)
                    ctx2.show_text(SSname)
                    
                    
                    #PREVIOUS SCENE
                    
                    for ar in self.FILE.arrows:
                        if ar[1][0] == self.event_select and ar[1][1] == SSname and ar[0][1] != "start":
                            
                            doprevious = False
                            
                            if my in range(shotlistlength+120+self.shotsSCROLL-25, shotlistlength+120+self.shotsSCROLL+20) and mx in range(Pstart+20, Pstart+60):
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#3c3c3c"))
                                widget.window.draw_rectangle(xgc, True, Pstart+20, shotlistlength+120+self.shotsSCROLL-25, 40, 40)
                            
                                if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active():
                                    doprevious = True
                                    
                            if 65361 in self.keys or doprevious:                    
                                            
                                            
                                p0, p1, p2, p3, p4 =  self.FILE.events[self.event_select] #SAVING FOR THE FOCUS
                                
                                self.event_select = ar[0][0]
                                self.image_select = False
                                
                                for ns, sc in enumerate(scnDATA[self.event_select]):
                                    if sc[1] == ar[0][1]:
                                        self.scene_select = ns
                                
                                try:
                                    scnDATA = self.FILE.get_scenes_data()
                                    scenestory = scnDATA[self.event_select][self.scene_select][3]
                                    self.shotsDATA = get_shots(scenestory, scnDATA[self.event_select][self.scene_select][1])
                                except:
                                    pass
                                self.shotsSCROLL = 0
                                
                                
                                # FOCUS THE EVENT IN THE CENTER OF THE SCREEN
                                
                                d0, d1, d2, d3, d4 =  self.FILE.events[self.event_select] # YOU CAN CHANGE THIS TO ANY EVENT
                                
                                thex = px-(d0 * sx +px) + (w/3)
                                they = py-(d2 * sy +py) + (h/2)
                                
                                
                                
                                self.animate(thex, they)
                                            
                                self.keys = []         
                                            
                                
                            widget.window.draw_pixbuf(None, self.big_left, 0, 0, Pstart+20, shotlistlength+120+self.shotsSCROLL-25 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                            
                    
                    #NEXT SCENE
                    for ar in self.FILE.arrows:
                        if ar[0][0] == self.event_select and ar[0][1] == SSname and ar[1][1] != "end":
                            
                            donext = False
                            if my in range(shotlistlength+120+self.shotsSCROLL-25, shotlistlength+120+self.shotsSCROLL+20) and mx in range(w-100, w-60):
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#3c3c3c"))
                                widget.window.draw_rectangle(xgc, True, w-100, shotlistlength+120+self.shotsSCROLL-25, 40, 40)
                            
                                if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active():
                                    
                                    donext = True
                                            
                            if 65363 in self.keys or donext:    
                                
                                p0, p1, p2, p3, p4 =  self.FILE.events[self.event_select] #SAVING FOR THE FOCUS
                                
                                self.event_select = ar[1][0]
                                self.image_select = False
                                
                                for ns, sc in enumerate(scnDATA[self.event_select]):
                                    if sc[1] == ar[1][1]:
                                        self.scene_select = ns
                                
                                try:
                                    scnDATA = self.FILE.get_scenes_data()
                                    scenestory = scnDATA[self.event_select][self.scene_select][3]
                                    self.shotsDATA = get_shots(scenestory, scnDATA[self.event_select][self.scene_select][1])
                                except:
                                    pass
                                self.shotsSCROLL = 0
                                
                                # FOCUS THE EVENT IN THE CENTER OF THE SCREEN
                                
                                d0, d1, d2, d3, d4 =  self.FILE.events[self.event_select] # YOU CAN CHANGE THIS TO ANY EVENT
                                
                                thex = px-(d0 * sx +px) + (w/3)
                                they = py-(d2 * sy +py) + (h/2)
                                
                                
                                
                                self.animate(thex, they)
                                
                                self.keys = []
                            
                            
                            widget.window.draw_pixbuf(None, self.big_right, 0, 0, w-100, shotlistlength+120+self.shotsSCROLL-25 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                            
                    
                    shotlistlength = shotlistlength + 45
                
                
                
                
                except:
                    pass
                
                
                
                anyscenedata = False
                
                
                
                for ind, i in enumerate(self.shotsDATA):
                    
                    anyscenedata = True
                    
                    
                    thisshotlistlengstart = shotlistlength
                    shotstatussidepanel = -1
                    
                    
                    
                    self.imgAT.append("")
                    
                    shotname, story, pixbuf, blends = i
                    
                    b = ""
                    
                    story = story.decode("utf-8")
                    
                    if shotname:
                        for b in shotname[shotname.rfind("/")+1:].split("\n"):
                            
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#2c2c2c"))
                            widget.window.draw_rectangle(xgc, True, Pstart, shotlistlength+120+self.shotsSCROLL-20, Ppart, 45)
                            
                            ctx2.set_source_rgb(1,1,1)
                            ctx2.set_font_size(20)
                            ctx2.move_to( Pstart+20+(Ppart-50)/2-len(b)*12/2, 7+shotlistlength+120+self.shotsSCROLL)
                            ctx2.show_text(b)
                            shotlistlength = shotlistlength + 50
                            
                            ctx2.set_font_size(15)
                        
                            

                            #MOVING TO REQUESTED SHOT
                            if self.searchshot:
                                
                                
                                if b == self.searchshot.decode("utf-8").replace("\n","_").replace("/","_").replace(" ", "_").replace('"',"_").replace("(","_").replace(")","_").replace("'","_").replace("[","_").replace("]","_").replace("{","_").replace("}","_")   :
                                    
                                    self.shotsSCROLL = self.shotsSCROLL - shotlistlength
                                    
                                    print
                                    self.searchshot = ""
                    
                    
                    
                    #xgc.set_rgb_fg_color(gtk.gdk.color_parse("#575757"))
                    #widget.window.draw_rectangle(xgc, True, Pstart+20, 15+shotlistlength+120+self.shotsSCROLL-15, w/3-90, len(story.split("\n"))*15+5)
                    
                    if '"' in story[:story.find("<item>")]:
                        story = story[story.replace('"', " ", 1).find('"')+1:] # IDK WHAT IT DID BUT IT SEEMS LIKE IT DID NOTHING
                    
                    
                    # DRAWING LITTLE ITEM LINKS
                    
                    
                    
                    
                    itemcounts = 0 # HOW MUCH WE HAVE
                    items = [] #LIST OF ITEMS         [[startintext, endintext, url], [.....
                    for item in range(story.count("<item>")):
                            
                            
                            itemcounts = itemcounts + 1
                            
                            startintext = story.find("<item>") # FINDING THE BEGINING OF THE ITEM
                            story = story[:story.find("<item>")] + story[story.find("<item>")+len("<item>"):] # DELETING THE <ITEM>
                            
                            while story.find('"') < startintext:
                                story = story.replace('"', " ", 1)
                            url = story[story.find('"')+1:story.replace('"', " ", 1).find('"')] # FINDING THE URL
                            story = story[:story.find(url)-1] + story[story.find(url)+len(url)+1:] # DELETING THE URL
                            
                            endintext = story.find("</item>") # FINDING THE ENDING OF THE ITEM
                            story = story[:story.find("</item>")] + story[story.find("</item>")+len("</item>"):] # DELETING THE </ITEM>
                            
                        
                            
                            
                            items.append([startintext, url, endintext])
                   
                   
                    # FINDING ALL THE FRASES THAT CHARACTERS SPEAK
                    
                    
                    frasecounts = 0
                    frases = []
                    
                    for frase in range(story.count(" - [")):
                        
                        frasecounts = frasecounts + 1
                        
                        # FINDING WHERE IT TEXT ARE FRASES
                        
                        startofname = story[:story.find(" - [")].rfind("\n") +1 # THIS IT THE START OF THE NAME
                        endofname = story.find(" - [")                          # THIS IS END OF THE NAME
                        startoffrase = endofname + 4                            # THIS IS START OF THE FRASE
                        endoffrase   = story.find("]")                          # THIS IS END OF THE FRASE
                        
                        
                        # DELETING THE PREVIOUS INSTANCE TO FIND NEW ONES
                        
                        story = story.replace(" - [", "    ", 1).replace("]", " ", 1)
                        
                        #APPENDING THE RESULTS
                        
                        frases.append([startofname, endofname, startoffrase, endoffrase])
                        
                        
                    
                    # MULTILINE SEPARATION
                    
                    movex = 0
                    letter = 0
                    skipto = 0
                    imagefound = False
                    for line in story.split("\n"):
                    
                        #IF LINE IMAGE
                        
                        line = line.replace("[image]", "<image>") #BACKWARD COMPATIBILITY
                        line = line.replace("[/image]", "</image>") #BACKWARD COMPATIBILITY
                        
                        
                        
                        if line.startswith("<image>"):
                            
                            imagefound = True
                            letter = letter + len(line)
                            
                            imageurl = line[7:line.find("</image>")]
                            
                            
                            
                        
                        
                        
                            loaded = False
                            for i in self.insertedimgs:
                                if i[0] == imageurl:
                                    loaded = True
                                    
                                    
                                    
                                    #image square
                                    
                                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#363636")) #403666   #6e5daf
                                    #widget.window.draw_rectangle(xgc, True, Pstart+20+movex-4, shotlistlength+120+self.shotsSCROLL+20, 154, 154)
                                    
                                    ctx3 = widget.window.cairo_create()
                                    ctx3.set_source_rgba(0,0,0,0.4)
                                    ctx3.rectangle(Pstart+20+movex-4, shotlistlength+120+self.shotsSCROLL+20, 154, 154)
                                    ctx3.fill()
                                    
                                    
                                    # MOUSE OVER
                                    if mx in range(Pstart+20+movex-2, Pstart+20+movex-2 + 154) and my in range(shotlistlength+120+self.shotsSCROLL+20, shotlistlength+120+self.shotsSCROLL+20+154):
                                        
                                        tooltip = "Open the Image \n"+imageurl
                                        
                                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#395384")) #403666   #6e5daf
                                        widget.window.draw_rectangle(xgc, True, Pstart+20+movex-4, shotlistlength+120+self.shotsSCROLL+20, 154, 154)
                                        
                                        
                                        # get mouse to show the hand
                                        widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
                                        
                                        if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active() and my in range(120, h) : 
                                            
                                            if os.path.exists(imageurl):
                                                oscalls.Open(imageurl)    
                                            else:
                                                oscalls.Open(self.pf+imageurl)
                                    
                                               
                                    
                                    
                                    
                                    
                                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#8a7d2c"))
                                    if os.path.exists(imageurl):
                                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#af5d5d"))
                                    
                                    
                                    widget.window.draw_rectangle(xgc, True, Pstart+20+movex-4, shotlistlength+120+self.shotsSCROLL, 154, 22)
                                    
                                    widget.window.draw_pixbuf(None, self.picicon, 0, 0, Pstart+20+movex-2, shotlistlength+120+self.shotsSCROLL , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                                    
                                    
                                    text = imageurl[imageurl.rfind("/")+1:]
                                    
                                    if len(text) > 14:
                                        text = text[:5]+"..."+text[:text.rfind(".")][-6:]
                                    
                                    ctx2.set_source_rgb(1,1,1)
                                    ctx2.set_font_size(15)
                                    ctx2.move_to( Pstart+20+movex + 24, 15+shotlistlength+120+self.shotsSCROLL)
                                    ctx2.show_text(text)
                                    
                                    
                                    
                                    imagex = Pstart+20+movex-2 + (150 - i[1].get_width())/2
                                    imagey = shotlistlength+120+self.shotsSCROLL+22 + (150 - i[1].get_height())/2
                                    
                                    widget.window.draw_pixbuf(None, i[1], 0, 0, imagex, imagey , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                                    
                                    movex = movex + 172
                                    
                                    if (movex) > Ppart-170:
                                        shotlistlength = shotlistlength + 150 + 40
                                        movex = 0
                                    
                                    
                            
                            if not loaded:
                                
                                if not self.IsNowProcessing:
                                
                                
                                    self.IsNowProcessing = True
                                    if os.path.exists(imageurl):
                                        pix = gtk.gdk.pixbuf_new_from_file(thumbnailer.thumbnail(imageurl, 150,150))
                                    else:
                                        pix = gtk.gdk.pixbuf_new_from_file(thumbnailer.thumbnail(self.pf+imageurl, 150,150))
                                    
                                    
                                    self.insertedimgs.append([imageurl, pix])
                                    self.IsNowProcessing = False
                                
                            #self.insertedimgs
                            
                            
                            
                            
                            continue
                        
                        elif line.startswith("<image>") == False and imagefound:
                            shotlistlength = shotlistlength + 150 + 40
                            imagefound = False
                            movex = 0
                    
                    
                    
                        for word in line.split(" "):
                            
                            # PARSING THE FRASES
                            
                            isName = False
                            isFrase = False
                            frase = [0,0,0,0]
                            
                            for frase in frases:
                                if frase[0] in range(letter, letter+len(word)):
                                    isName = True
                                    break
                                if frase[2] in range(letter, letter+len(word)):
                                    isFrase = True
                                    
                                    
                                    t = story[frase[2]:frase[3]]
                                    
                                    
                                    shotlistlength = shotlistlength + 22
                                    movex = 100
                                    
                                    
                                    
                                    for wor in t.split("\n"):
                                        GraphicsX = Pstart+20+movex-2
                                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#3c3c3c")) #403666   #6e5daf
                                        widget.window.draw_rectangle(xgc, True, GraphicsX-20, shotlistlength+120+self.shotsSCROLL, Ppart-150, 20)
                                        
                                        for wo in wor.split(" "):
                                        
                                            GraphicsX = Pstart+20+movex-2
                                            
                                            
                                        
                                            
                                            
                                            
                                            ctx2.set_source_rgb(1,1,1)
                                            ctx2.move_to( GraphicsX, 15+shotlistlength+120+self.shotsSCROLL)
                                            ctx2.show_text(wo)
                                            
                                            movex = movex + len(wo)*9+9
                                            
                                            if movex > Ppart-150:
                                                
                                                shotlistlength = shotlistlength + 20
                                                movex = 100
                                                GraphicsX = Pstart+20+movex-2
                                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#3c3c3c")) #403666   #6e5daf
                                                widget.window.draw_rectangle(xgc, True, GraphicsX-20, shotlistlength+120+self.shotsSCROLL, Ppart-150, 20)
                                            
                                            
                                            skipto = letter + len(t)+1
                                        
                                        shotlistlength = shotlistlength + 20
                                        movex = 100
                                        
                                    shotlistlength = shotlistlength + 20
                                    break
                            
                            # PARSING THE ITEMS
                            
                            for item in items:
                                if item[0] in range(letter, letter+len(word)) and letter >= skipto:
                                    
                                    if movex+(len(story[story[:item[0]+1].replace("\n", " ").rfind(" "):item[2]+story[item[2]:].replace("\n", " ").find(" ")+1].replace("\n", " "))*9+24) > Ppart-51 or isName:# or movex > Ppart - 500 and isFrase:
                                
                                        shotlistlength = shotlistlength + 20
                                        movex = 0
                                    
                                    if shotlistlength+120+self.shotsSCROLL in range(110, h):
                                        
                                        
                                        
                                        GraphicsX = Pstart+20+movex-2
                                        if isName:
                                            GraphicsX = Pstart+Ppart/2-len(story[item[0]:item[2]])*9/2
                                        
                                        #ITEM COLOR
                                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#6e5daf")) #403666   #6e5daf
                                        widget.window.draw_rectangle(xgc, True, GraphicsX, shotlistlength+120+self.shotsSCROLL+1, len(story[story[:item[0]+1].replace("\n", " ").rfind(" "):item[2]+story[item[2]:].replace("\n", " ").find(" ")+1].replace("\n", " "))*9+24, 20)
                                        
                                        #xgc.set_rgb_fg_color(gtk.gdk.color_parse("#d0d0d0")) #403666   #6e5daf
                                        #widget.window.draw_rectangle(xgc, True, GraphicsX, shotlistlength+120+self.shotsSCROLL+20, len(story[item[0]:item[2]])*9+9+22, 2)
                                        
                                        
                                        
                                        CUR = item[1][len("/dev/"):len("/dev/")+3]
                                        URL = item[1][item[1].rfind("/")+1:]
                                        
                                        #try:
                                        #    itempercent = self.itempercent[URL]
                                        #except:
                                        #    try:
                                        #        self.itempercent[URL] = checklist.partcalculate(checklist.openckecklist(self.pf+"/dev/"+CUR+"/"+name+"/"+"/asset.progress")) #GETTING ITEMS %
                                        #    except:
                                        #        self.itempercent[URL] = 0
                                        #        
                                        #    itempercent = self.itempercent[URL]
                                        ## THIS IS PERCENT        THIS IS ITEMS PART LENGHT           
                                        #lenofsecondcube = int(round(float(len(story[item[0]:item[2]])*9+9+22) * itempercent))
                                        #
                                        #xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165")) #403666   #6e5daf
                                        #widget.window.draw_rectangle(xgc, True, GraphicsX, shotlistlength+120+self.shotsSCROLL+20, lenofsecondcube, 2)
                                        
                                        
                                        
                                        # MOUSE OVER
                                        if mx in range(GraphicsX, GraphicsX + len(story[story[:item[0]+1].replace("\n", " ").rfind(" "):item[2]+story[item[2]:].replace("\n", " ").find(" ")+1].replace("\n", " "))*9+22) and my in range(shotlistlength+120+self.shotsSCROLL+1, shotlistlength+120+self.shotsSCROLL+21):
                                            
                                            tooltip = URL
                                            
                                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
                                            widget.window.draw_rectangle(xgc, True, GraphicsX, shotlistlength+120+self.shotsSCROLL+1, len(story[story[:item[0]+1].replace("\n", " ").rfind(" "):item[2]+story[item[2]:].replace("\n", " ").find(" ")+1].replace("\n", " "))*9+24, 20)
                                            
                                            # get mouse to show the hand
                                            #widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
                                            
                                            if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active() and my in range(120, h) :
                                                
                                                
                                                
                                                
                                                
                                                self.box.destroy()
                                    
                                    
                                                self.box = gtk.VBox(False)
                                                self.mainbox.pack_start(self.box, True)
                                                
                                                assets.draw_assets(os.getcwd(), self.box, self.win, CUR, URL,mainbox=self.mainbox)
                                                launchitem = False
                                        
                                        
                                        
                                        if CUR == "obj":
                                            widget.window.draw_pixbuf(None, self.objicon, 0, 0, GraphicsX, shotlistlength+120+self.shotsSCROLL , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                                        elif CUR == "chr":
                                            widget.window.draw_pixbuf(None, self.chricon, 0, 0, GraphicsX, shotlistlength+120+self.shotsSCROLL , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                                        elif CUR == "loc":
                                            widget.window.draw_pixbuf(None, self.locicon, 0, 0, GraphicsX, shotlistlength+120+self.shotsSCROLL , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                                        elif CUR == "veh":
                                            widget.window.draw_pixbuf(None, self.vehicon, 0, 0, GraphicsX, shotlistlength+120+self.shotsSCROLL , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                                        
                                        
                                        
                                        
                                        
                                        movex = movex + 22
                                        
                                        
                                        
                                        
                                        
                                        ctx2.set_source_rgb(1,1,1)
                                        ctx2.move_to( GraphicsX+22, 15+shotlistlength+120+self.shotsSCROLL)
                                        if isName:
                                            ctx2.show_text(story[item[0]-1:item[2]+story[item[2]:].replace("\n", " ").find(" ")+1].upper().replace("\n", " "))
                                        else:
                                            ctx2.show_text(story[story[:item[0]+1].replace("\n", " ").rfind(" "):item[2]+story[item[2]:].replace("\n", " ").find(" ")+1].replace("\n", " "))
                                        
                                            
                                        
                                    
                                    
                                    
                                    
                                    
                                    
                                    movex = movex + len(story[story[:item[0]+1].replace("\n", " ").rfind(" "):item[2]+story[item[2]:].replace("\n", " ").find(" ")+1].replace("\n", " "))*9+9
                                    
                                    skipto = letter + len(story[item[0]-1:item[2]])
                                    
                                    break
                            
                            
                            
                            if letter >= skipto:
                                
                                if movex+(len(word)*9) > Ppart-51 or isName:# or movex > Ppart - 500 and isFrase:
                                
                                    shotlistlength = shotlistlength + 20
                                    movex = 0
                                  
                                ctx2.set_source_rgb(1,1,1)
                                ctx2.set_font_size(15)
                                ctx2.move_to( Pstart+20+movex, 15+shotlistlength+120+self.shotsSCROLL)
                                if isName:
                                        t = story[frase[0]:frase[1]]
                                        
                                        ctx2.move_to( Pstart+Ppart/2-len(t)*9/2, 15+shotlistlength+120+self.shotsSCROLL)
                                        
                                        ctx2.show_text(t.upper())
                                        skipto = letter + len(t)+1
                                else:       
                                    ctx2.show_text(word)
                                movex = movex + len(word)*9 + 9 # 9 PIXELS IS ONE LETTER
                            letter = letter + len(word)+1
                            
                            
                            
                                
                        
                        

                        shotlistlength = shotlistlength + 20
                        movex = 0
                        
                    
                    
                        
                        
                    
                        
                    if shotname:    
                        
                        if os.path.exists(self.pf+"/"+shotname):
                            # CHECKING THAT ALL SUBFOLDERS EXIST TOO
                            
                            
                            # storyboard , opengl, test_rnd, rendered, extra
                            
                            if os.path.exists(self.pf+"/"+shotname+"/storyboard") == False:
                                os.mkdir(self.pf+"/"+shotname+"/storyboard")
                            if os.path.exists(self.pf+"/"+shotname+"/opengl") == False:
                                os.mkdir(self.pf+"/"+shotname+"/opengl")
                            if os.path.exists(self.pf+"/"+shotname+"/test_rnd") == False:
                                os.mkdir(self.pf+"/"+shotname+"/test_rnd")
                            if os.path.exists(self.pf+"/"+shotname+"/rendered") == False:
                                os.mkdir(self.pf+"/"+shotname+"/rendered")
                            if os.path.exists(self.pf+"/"+shotname+"/extra") == False:
                                os.mkdir(self.pf+"/"+shotname+"/extra")
                        
                        
                        
                            # NOW LETS CREATE THE AUUTOLINK.DATA 
                    
                            if items: #IF ANY ITEMS ARE IN THE SCENE
                                
                        
                                #clearing items. we already got them to the screen we don't nee all the data.
                                tmp = []
                                for i in items:
                                    i = i[1]
                                    if i not in tmp:
                                        tmp.append(i)
                                items = tmp
                                
                                
                                
                                # CHECKING IF THE FILE IS NOT THERE
                                if not os.path.exists(self.pf+"/"+shotname+"/extra/autolink.data"):
                                    
                                    
                                    
                                    autolink = open(self.pf+"/"+shotname+"/extra/autolink.data", "w")
                                    for i in items:
                                        autolink.write("Link : "+i+"\n")
                                        
                                    autolink.close()
                                
                        else:
                            
                            self.shotsDATA[ind][2] = "None"
                        
                        shotlistlength = shotlistlength + 10
                        
                        
                        # TRY TO FIND A PICTURE
                        
                        img = "None"
                        
                        if pixbuf == False and shotlistlength+120+self.shotsSCROLL+self.empty_frame.get_height() > 120 and shotlistlength+120+self.shotsSCROLL < h:
                            
                            
                            
                            for folder in ["rendered", "test_rnd", "opengl", "storyboard", "extra"]:
                                
                                for L in os.walk(self.pf+"/"+shotname+"/"+folder):
                                    
                                    for FILE in L[2]:
                                    
                                         
                                        
                                        
                                            
                                        for F in fileformats.images:   ### WHAT IF FOUND AN IMAGE
                                                
                                            if FILE.lower().endswith(F):
                                        
                                                img = gtk.gdk.pixbuf_new_from_file(thumbnailer.thumbnail(self.pf+"/"+shotname+"/"+folder+"/"+FILE, self.empty_frame.get_width(),self.empty_frame.get_height()))
                                                
                                                
                                                self.imgAT[ind] = shotname+"/"+folder+"/"+FILE
                                                
                                                break
                                        if img != "None":
                                            break
                                        
                                        for F in fileformats.videos:  ### WHAT IF FOUND A VIDEO
                                                
                                            if FILE.lower().endswith(F):
                                        
                                                img = gtk.gdk.pixbuf_new_from_file(thumbnailer.videothumb(self.pf+"/"+shotname+"/"+folder+"/"+FILE, self.empty_frame.get_width(),self.empty_frame.get_height()))
                                                
                                                self.imgAT[ind] = shotname+"/"+folder+"/"+FILE
                                                
                                                break  
                                            
                                    if img != "None":
                                        break        
                                            
                                if img != "None":
                                    break                    
                                                
                                            
                                        
                            
                                        
                            #if img == "None":
                                
                            
                                    
                            self.shotsDATA[ind][2] = img # NO IMAGE FOUND
                        
                        
                        # GIVE UP
                        
                        
                        
                        elif pixbuf == "None" or pixbuf == False:
                        
                            
                                
                            
                            
                            if shotlistlength+120+self.shotsSCROLL+self.empty_frame.get_height() > 120 and shotlistlength+120+self.shotsSCROLL < h: # IF IN FRAME
                                
                                picW = Pstart+10 #+Ppart/2-pixbuf.get_width()/2
                                
                                widget.window.draw_pixbuf(None, self.empty_frame, 0, 0, picW, shotlistlength+120+self.shotsSCROLL , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
                            
                            shotlistlength = shotlistlength + self.empty_frame.get_height()
                        
                        
                        else:   ##### IF THE IMAGE ACTUALLY WAS FOUND
                            
                            if shotlistlength+120+self.shotsSCROLL+pixbuf.get_height() > 120 and shotlistlength+120+self.shotsSCROLL < h: # IF IN FRAME
                                
                                picW = Pstart+10 #+Ppart/2-pixbuf.get_width()/2
                                
                                
                                # MOUSE OVER
                                if mx in range(picW, picW+pixbuf.get_width()) and my in range(shotlistlength+120+self.shotsSCROLL, shotlistlength+120+self.shotsSCROLL+pixbuf.get_height()):
                                    
                                    tooltip = self.imgAT[ind]
                                    
                                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#e47649"))
                                    widget.window.draw_rectangle(xgc, True, picW -3, shotlistlength+120+self.shotsSCROLL -3, pixbuf.get_width()+6, pixbuf.get_height()+6)
                                    
                                    # get mouse to show the hand
                                    widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
                                    
                                    if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active() and my in range(120, h) :
                                        
                                        
                                        
                                        oscalls.Open(self.pf+"/"+(self.imgAT[ind]))
                                    
                                
                                
                                widget.window.draw_pixbuf(None, pixbuf, 0, 0, picW, shotlistlength+120+self.shotsSCROLL , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
                            
                            shotlistlength = shotlistlength + self.empty_frame.get_height()
                        
                        
                        
                        
                        shotlistlength = shotlistlength + 10
                        
                        if shotlistlength+120+self.shotsSCROLL+self.empty_frame.get_height() > 120 and shotlistlength+120+self.shotsSCROLL < h: # IF IN FRAME
                            
                            
                            frmdata = {}
                            lframe = 0
                            try:
                                for rndfile in os.walk(self.pf+"/"+shotname+"/extra").next()[2]:
                                    if rndfile.endswith(".blend.rnd"):
                                        rndfile = open(self.pf+"/"+shotname+"/extra/"+rndfile, "r")
                                        rndfile = rndfile.read().split("\n")
                                        
                                        for line in rndfile:
                                            
                                            try:
                                                frm, seconds = line.split(" ")
                                                frm = "0"*(4-len(frm)) + frm
                                                seconds = int(seconds)
                                                if frm not in frmdata:
                                                    frmdata[frm] = seconds
                                                else:
                                                    frmdata[frm] = ( frmdata[frm] + seconds ) / 2
                                                if seconds > lframe:
                                                    lframe = seconds
                                                    
                                                
                                            except:
                                                pass
                            except:
                                pass
                            
                            foravarage = []
                            
                            
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#2c2c2c"))
                            widget.window.draw_rectangle(xgc, True, Pstart+8, shotlistlength+120+self.shotsSCROLL -5, Ppart-16, 104)
                                        
                            for tfrm, frm in enumerate(sorted(frmdata)):
                                
                                foravarage.append(frmdata[frm])
                                
                                frmy =  int(round(100.0/lframe*frmdata[frm]))
                                frmx =  int(round(float(Ppart-20)/len(frmdata)*tfrm)) + Pstart+10
                                frmxs = int(round(float(Ppart-20)/len(frmdata)))+1
                                
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#1c1c1c"))
                                widget.window.draw_rectangle(xgc, True, frmx, shotlistlength+120+self.shotsSCROLL -3+(100-frmy), frmxs, frmy)
                                
                                if my in range(shotlistlength+120+self.shotsSCROLL -3, shotlistlength+120+self.shotsSCROLL -3+100) and mx in range(frmx, frmx+frmxs-1):
                                    
                                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#db3c16"))
                                    widget.window.draw_rectangle(xgc, True, frmx, shotlistlength+120+self.shotsSCROLL -3+(100-frmy), frmxs, frmy)
                                    
                                    
                                    img = "None"
                                    for folder in ["rendered", "test_rnd", "opengl", "storyboard", "extra"]:
                                        for L in os.walk(self.pf+"/"+shotname+"/"+folder):
                                            for FILE in L[2]:                                        
                                                for F in fileformats.images:   ### WHAT IF FOUND AN IMAGE
                                                    if FILE.lower().endswith(F):
                                                        
                                                        imgurlthumb = self.pf+"/"+shotname+"/"+folder+"/"+frm+FILE[FILE.rfind("."):]
                                                        
                                                        if os.path.exists(imgurlthumb):
                                                            imgurlthumb = thumbnailer.thumbnail(imgurlthumb, self.empty_frame.get_width(),self.empty_frame.get_height())
                                                        
                                                            img = gtk.gdk.pixbuf_new_from_file(imgurlthumb)                                                    
                                                            self.imgAT[ind] = shotname+"/"+folder+"/"+frm+FILE[FILE.rfind("."):]
                                                            break
                                                if img != "None":
                                                    break    
                                            if img != "None":
                                                break        
                                        if img != "None":
                                            break 
                                    self.shotsDATA[ind][2] = img
                                
                                if self.imgAT[ind] == self.imgAT[ind][:self.imgAT[ind].rfind("/")+1]+frm+self.imgAT[ind][self.imgAT[ind].rfind("."):]:
                                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#db3c16"))
                                    widget.window.draw_rectangle(xgc, True, frmx, shotlistlength+120+self.shotsSCROLL -3+(100-frmy), frmxs, frmy)
                                    
                        # OUTPUTTING SOME STATISTICS
                        try:
                            ctx2.set_source_rgb(1,1,1)
                            ctx2.set_font_size(15)
                            ctx2.move_to( Pstart+20+self.empty_frame.get_width(), shotlistlength+120+self.shotsSCROLL-self.empty_frame.get_height())
                            ctx2.show_text("Frames  : "+str(len(foravarage)))
                            
                            
                            ctx2.set_source_rgb(1,1,1)
                            ctx2.set_font_size(15)
                            ctx2.move_to( Pstart+20+self.empty_frame.get_width(), shotlistlength+120+self.shotsSCROLL-self.empty_frame.get_height()+20)
                            ctx2.show_text("Time    : "+quick.timestring(sum(foravarage)))
                            
                            ctx2.set_source_rgb(1,1,1)
                            ctx2.set_font_size(15)
                            ctx2.move_to( Pstart+20+self.empty_frame.get_width(), shotlistlength+120+self.shotsSCROLL-self.empty_frame.get_height()+40)
                            ctx2.show_text("Avarage : "+quick.timestring(sum(foravarage)/len(foravarage)))
                            
                            ctx2.set_source_rgb(1,1,1)
                            ctx2.set_font_size(15)
                            ctx2.move_to( Pstart+20+self.empty_frame.get_width(), shotlistlength+120+self.shotsSCROLL-self.empty_frame.get_height()+60)
                            ctx2.show_text("Current : "+self.imgAT[ind][self.imgAT[ind].rfind("/")+1:self.imgAT[ind].rfind(".")]+ "")
                            
                        
                            ctx2.set_source_rgb(1,1,1)
                            ctx2.set_font_size(15)
                            ctx2.move_to( Pstart+20+self.empty_frame.get_width(), shotlistlength+120+self.shotsSCROLL-self.empty_frame.get_height()+80)
                            ctx2.show_text("Time    : "+quick.timestring(frmdata[self.imgAT[ind][self.imgAT[ind].rfind("/")+1:self.imgAT[ind].rfind(".")]]))
                            
                        except:
                            pass
                        
                        
                        shotlistlength = shotlistlength + 105
                        
                        if os.path.exists(self.pf+"/"+shotname) == False: # IF FOLDER DOES NOT EXISIS
                            
                            # MOUSE OVER
                            if mx in range(Pstart, w) and my in range(shotlistlength+120+self.shotsSCROLL, shotlistlength+120+self.shotsSCROLL+20):
                                
                                tooltip = "Generate Shot's Folders \n\n Every shot can have a directory\nin /rnd folder to work\non the shot directly,\ncreate blend files,\nhold footage."
                                
                                # get mouse to show the hand
                                widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
                                
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#5c5c5c"))
                                widget.window.draw_rectangle(xgc, True, Pstart, shotlistlength+120+self.shotsSCROLL, Ppart, 23)
                                
                                if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active() and my in range(120, h) :
                                    
                                    os.makedirs(self.pf+"/"+shotname)
                                
                                
                            
                            # DRAW BUTTON
                            
                            widget.window.draw_pixbuf(None, self.foldericon, 0, 0, Pstart+10, shotlistlength+120+self.shotsSCROLL , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
                            
                            ctx.set_source_rgb(1,1,1)
                            ctx.set_font_size(15)
                            ctx.move_to( Pstart+50, 15+shotlistlength+120+self.shotsSCROLL+2)
                            ctx.show_text("Generate Shot's Folders")
                            
                            
                            
                            
                            
                            
                        else:                                             # IF FOLDER EXISTS
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            # MAIN SHOT FOLDER 
                            
                            
                            
                            
                            # MOUSE OVER
                            if mx in range(Pstart, w-50) and my in range(shotlistlength+120+self.shotsSCROLL, shotlistlength+120+self.shotsSCROLL+20):
                                
                                tooltip = "/"+shotname
                                
                                # get mouse to show the hand
                                widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
                                
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#5c5c5c"))
                                widget.window.draw_rectangle(xgc, True, Pstart, shotlistlength+120+self.shotsSCROLL, Ppart, 23)
                                
                                if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active() and my in range(120, h):
                                    
                                    oscalls.Open(self.pf+"/"+shotname)
                                
                                
                            
                            # DRAW BUTTON
                            
                            widget.window.draw_pixbuf(None, self.foldericon, 0, 0, Pstart+10, shotlistlength+120+self.shotsSCROLL , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
                            
                            ctx.set_source_rgb(1,1,1)
                            ctx.set_font_size(15)
                            ctx.move_to( Pstart+50, 15+shotlistlength+120+self.shotsSCROLL+2)
                            ctx.show_text("Open Shot's Folder")
                            
                            
                            
                            
                            # SPACE
                            shotlistlength = shotlistlength + 40
                            
                            
                            
                            # storyboard
                            
                            
                            
                            if len(os.listdir(self.pf+"/"+shotname+"/storyboard")) > 0:
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#222222"))
                                widget.window.draw_rectangle(xgc, True, Pstart, shotlistlength+120+self.shotsSCROLL, Ppart/2, 23)
                                shotstatussidepanel = 1
                            # MOUSE OVER
                            if mx in range(Pstart, w-Ppart/2-60) and my in range(shotlistlength+120+self.shotsSCROLL, shotlistlength+120+self.shotsSCROLL+20):
                                
                                
                                
                                # get mouse to show the hand
                                widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
                                
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#5c5c5c"))
                                widget.window.draw_rectangle(xgc, True, Pstart, shotlistlength+120+self.shotsSCROLL, Ppart/2, 23)
                                
                                if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active() and my in range(120, h):
                                    
                                    oscalls.Open(self.pf+"/"+shotname+"/storyboard")
                                    
                                
                            
                            # DRAW BUTTON
                            
                            widget.window.draw_pixbuf(None, self.foldericon, 0, 0, Pstart+10, shotlistlength+120+self.shotsSCROLL , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
                            
                            ctx.set_source_rgb(1,1,1)
                            ctx.set_font_size(15)
                            ctx.move_to( Pstart+50, 15+shotlistlength+120+self.shotsSCROLL+2)
                            ctx.show_text("storyboard")
                            
                              
                            
                            
                            
                            # opengl
                            
                            if len(os.listdir(self.pf+"/"+shotname+"/opengl")) > 0:
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#4f4f4f"))
                                widget.window.draw_rectangle(xgc, True, Pstart+Ppart/2, shotlistlength+120+self.shotsSCROLL, Ppart/2, 23)
                                shotstatussidepanel = 0
                            
                            # MOUSE OVER
                            if mx in range(Pstart+Ppart/2, w-50) and my in range(shotlistlength+120+self.shotsSCROLL, shotlistlength+120+self.shotsSCROLL+20):
                                
                                
                                
                                # get mouse to show the hand
                                widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
                                
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#5c5c5c"))
                                widget.window.draw_rectangle(xgc, True, Pstart+Ppart/2, shotlistlength+120+self.shotsSCROLL, Ppart/2, 23)
                                
                                if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active() and my in range(120, h):
                                    
                                    oscalls.Open(self.pf+"/"+shotname+"/opengl")
                                
                                
                            
                            # DRAW BUTTON
                            
                            widget.window.draw_pixbuf(None, self.foldericon, 0, 0, Pstart+10+Ppart/2, shotlistlength+120+self.shotsSCROLL , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
                            
                            ctx.set_source_rgb(1,1,1)
                            ctx.set_font_size(15)
                            ctx.move_to( Pstart+50+Ppart/2, 15+shotlistlength+120+self.shotsSCROLL+2)
                            ctx.show_text("opengl")
                            
                            
                            # SPACE
                            shotlistlength = shotlistlength + 20
                            
                            # test_rnd
                            
                            
                            if len(os.listdir(self.pf+"/"+shotname+"/test_rnd")) > 0:
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#395384"))
                                widget.window.draw_rectangle(xgc, True, Pstart, shotlistlength+120+self.shotsSCROLL, Ppart/2, 23)
                                shotstatussidepanel = 2
                            # MOUSE OVER
                            if mx in range(Pstart, w-Ppart/2-60) and my in range(shotlistlength+120+self.shotsSCROLL, shotlistlength+120+self.shotsSCROLL+20):
                                
                                
                                
                                # get mouse to show the hand
                                widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
                                
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#5c5c5c"))
                                widget.window.draw_rectangle(xgc, True, Pstart, shotlistlength+120+self.shotsSCROLL, Ppart/2, 23)
                                
                                if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active() and my in range(120, h):
                                    
                                    oscalls.Open(self.pf+"/"+shotname+"/test_rnd")
                                
                                
                            
                            # DRAW BUTTON
                            
                            widget.window.draw_pixbuf(None, self.foldericon, 0, 0, Pstart+10, shotlistlength+120+self.shotsSCROLL , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
                            
                            ctx.set_source_rgb(1,1,1)
                            ctx.set_font_size(15)
                            ctx.move_to( Pstart+50, 15+shotlistlength+120+self.shotsSCROLL+2)
                            ctx.show_text("test_rnd")
                            
                            
                            
                            
                            # rendered
                            
                            if len(os.listdir(self.pf+"/"+shotname+"/rendered")) > 0:
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#e47649")) 
                                widget.window.draw_rectangle(xgc, True, Pstart+Ppart/2, shotlistlength+120+self.shotsSCROLL, Ppart/2, 23)
                                shotstatussidepanel = 3
                                
                            
                            
                            # MOUSE OVER
                            if mx in range(Pstart+Ppart/2, w-50) and my in range(shotlistlength+120+self.shotsSCROLL, shotlistlength+120+self.shotsSCROLL+20):
                                
                                
                                
                                # get mouse to show the hand
                                widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
                                
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#5c5c5c"))
                                widget.window.draw_rectangle(xgc, True, Pstart+Ppart/2, shotlistlength+120+self.shotsSCROLL, Ppart/2, 23)
                                
                                if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active() and my in range(120, h):
                                    
                                    oscalls.Open(self.pf+"/"+shotname+"/rendered")
                                
                                
                            
                            # DRAW BUTTON
                            
                            widget.window.draw_pixbuf(None, self.foldericon, 0, 0, Pstart+10+Ppart/2, shotlistlength+120+self.shotsSCROLL , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
                            
                            ctx.set_source_rgb(1,1,1)
                            ctx.set_font_size(15)
                            ctx.move_to( Pstart+50+Ppart/2, 15+shotlistlength+120+self.shotsSCROLL+2)
                            ctx.show_text("rendered")
                            
                            
                            
                            # SPACE
                            shotlistlength = shotlistlength + 40
                            
                            # extra
                            
                            
                            
                            
                            # MOUSE OVER
                            if mx in range(Pstart, w-Ppart/2-60) and my in range(shotlistlength+120+self.shotsSCROLL, shotlistlength+120+self.shotsSCROLL+20):
                                
                                
                                
                                # get mouse to show the hand
                                widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
                                
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#5c5c5c"))
                                widget.window.draw_rectangle(xgc, True, Pstart, shotlistlength+120+self.shotsSCROLL, Ppart-Ppart/2-60, 23)
                                
                                if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active() and my in range(120, h):
                                    Pstart
                                    oscalls.Open(self.pf+"/"+shotname+"/extra")
                                
                                
                            
                            # DRAW BUTTON
                            
                            widget.window.draw_pixbuf(None, self.foldericon, 0, 0, Pstart+10, shotlistlength+120+self.shotsSCROLL , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
                            
                            
                            
                            ctx.set_source_rgb(1,1,1)
                            ctx.set_font_size(15)
                            ctx.move_to( Pstart+50, 15+shotlistlength+120+self.shotsSCROLL+2)
                            ctx.show_text("extra")
                            
                            
                            
                            
                            
                            
                            # checklist
                            
                            
                            #trying to get the list
                            checkexist = False
                            checkpath = self.pf+"/"+shotname+"/shot.progress"
                            if os.path.exists(checkpath):
                                
                                checkexist = True
                                checkfloat = checklist.partcalculate(checklist.openckecklist(checkpath))
                                
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#2c2c2c"))
                                widget.window.draw_rectangle(xgc, True, Pstart+Ppart/2, shotlistlength+120+self.shotsSCROLL+35, Ppart-Ppart/2-100, 5)
                                
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#db3c16"))
                                widget.window.draw_rectangle(xgc, True, Pstart+Ppart/2, shotlistlength+120+self.shotsSCROLL+35, int((Ppart-Ppart/2-100)*checkfloat), 5)
                                
                                ctx.set_source_rgb(1,1,1)
                                ctx.set_font_size(15)
                                ctx.move_to( Pstart+Ppart/2+(Ppart-Ppart/2-95), 15+shotlistlength+120+self.shotsSCROLL+25)
                                ctx.show_text(str(int(checkfloat*100))+"%")
                            
                            
                            
                            # MOUSE OVER
                            if mx in range(Pstart+Ppart/2, w-50) and my in range(shotlistlength+120+self.shotsSCROLL, shotlistlength+120+self.shotsSCROLL+20):
                                
                                
                                
                                # get mouse to show the hand
                                widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
                                
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#8c8c8c"))
                                widget.window.draw_rectangle(xgc, True, Pstart+Ppart/2, shotlistlength+120+self.shotsSCROLL, Ppart/2, 23)
                                
                                if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active() and my in range(120, h):
                                    if checkexist:
                                        checklist.checkwindow(pf=self.pf, title="SHOT", FILE=checkpath)
                                    else:
                                        
                                        def ee(shotname, checkpath):   
                                            name = dialogs.choose_shot_type()
                                            
                                        
                                            
                                            refpath = self.pf+"/py_data/new_file/"+name+".progress"
                                            
                                            
                                            if os.path.exists(refpath):
                                                
                                                    o = open(refpath, "r")
                                                    w = open(checkpath, "w")
                                                    w.write(o.read())
                                                    w.close()
                                            
                                        glib.timeout_add(10, ee, shotname, checkpath)
                            
                            # DRAW BUTTON
                            
                            widget.window.draw_pixbuf(None, self.checklist, 0, 0, Pstart+10+Ppart/2, shotlistlength+120+self.shotsSCROLL , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
                            
                            
                            
                            
                            ctx.set_source_rgb(1,1,1)
                            ctx.set_font_size(15)
                            ctx.move_to( Pstart+50+Ppart/2, 15+shotlistlength+120+self.shotsSCROLL+2)
                            if checkexist:
                                ctx.show_text("Checklist")
                            else:
                                ctx.show_text("Create Checklist")
                            
                            
                            # SPACE
                            shotlistlength = shotlistlength + 40
                            
                            
                            
                            
                            ###### BLEND FILES ######
                            
                            # MAKING SURE THERE IS BLENDFILES DATA LOADED
                            if blends == False:
                                blends = []
                                for FILE in os.listdir(self.pf+"/"+shotname):   
                                    
                                    if FILE.lower().endswith(".blend"):
                                        
                                        blends.append([FILE, False])
                                        
                                
                                
                                self.shotsDATA[ind][3] = blends
                            
                            # Drawing something to the screen
                            
                            
                            #getting mesurmets
                            
                            cellsize = 160 # pixels
                            
                            xcells = (Ppart/cellsize)-1
                            
                            xstep = 0
                            
                            
                            
                            for BInd, blend in enumerate(blends): 
                                
                                BName, BPic =  blend
                                
                                
                                # TEST CELL
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#000"))
                                #widget.window.draw_rectangle(xgc, False, Pstart+20+(cellsize*xstep), shotlistlength+120+self.shotsSCROLL, cellsize, cellsize)
                                
                                
                                #IF IN FRAME
                                if shotlistlength+120+self.shotsSCROLL+20+cellsize-40 > 120 and shotlistlength+120+self.shotsSCROLL+20 < h: # IF IN FRAME
                                    
                                    
                                    
                                    
                                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#464646"))
                                    #widget.window.draw_rectangle(xgc, True, Pstart+20+(cellsize*xstep)+15, shotlistlength+120+self.shotsSCROLL+15+22, cellsize-50, cellsize-50)
                                    
                                    ctx3 = widget.window.cairo_create()
                                    ctx3.set_source_rgba(0,0,0,0.4)
                                    ctx3.rectangle(Pstart+20+(cellsize*xstep)+15, shotlistlength+120+self.shotsSCROLL+15+22, cellsize-50, cellsize-50)
                                    ctx3.fill()
                                    
                                    
                                    
                                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#526969"))
                                    widget.window.draw_rectangle(xgc, True, Pstart+20+(cellsize*xstep)+15, shotlistlength+120+self.shotsSCROLL+15, cellsize-50, 22)
                                    
                                    
                                    ctx.set_source_rgb(1,1,1)
                                    ctx.set_font_size(10)
                                    ctx.move_to( Pstart+20+(cellsize*xstep)+15+22, shotlistlength+120+self.shotsSCROLL+15+15)
                                    ctx.show_text(BName)
                                    
                                    
                                    
                                    widget.window.draw_pixbuf(None, self.blendericon, 0, 0, Pstart+20+(cellsize*xstep)+17, shotlistlength+120+self.shotsSCROLL+15 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)   
                                    
                                    # MOUSE OVER BLENDFILE
                                    if mx in range(Pstart+20+(cellsize*xstep)+20, Pstart+20+(cellsize*xstep)+20+cellsize-60) and my in range(shotlistlength+120+self.shotsSCROLL+20, shotlistlength+120+self.shotsSCROLL+20+cellsize-60+22):
                                        
                                        tooltip = "Open Blendfile\n"+BName
                                        
                                        # get mouse to show the hand
                                        widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
                                        
                                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#395384"))
                                        widget.window.draw_rectangle(xgc, True, Pstart+20+(cellsize*xstep)+15, shotlistlength+120+self.shotsSCROLL+15+22, cellsize-50, cellsize-50)
                                
                                        if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active() and my in range(120, h):
                                            
                                            
                                            cblndr = ""
                                            
                                            try:
                                                bv = open(self.pf+"/py_data/blenderver.data", "r")
                                                bv = bv.read().split("\n")
                                                
                                                
                                                
                                                if int(bv[0]) > 0:
                                                    cblndr = bv[int(bv[0])]+"/"
                                            except:
                                                pass
                                                
                                            
                                            #WRITTING TO HYSTORY
                                            history.write(self.pf ,"/"+shotname+"/"+BName, "[Openned]")
                                            Popen([cblndr+"blender", self.pf+"/"+shotname+"/"+BName])
                                            #os.system(cblndr+"blender "+self.pf+"/"+shotname+"/"+BName)
                                        
                                        thisshotlistlengstart
                                        
                                    
                                        
                                    ##### RENDER BUTTON ####
                                    
                                    # MOUSE OVER
                                    if mx in range(Pstart+20+(cellsize*xstep)+20+110, Pstart+20+(cellsize*xstep)+20+130) and my in range(shotlistlength+120+self.shotsSCROLL+20, shotlistlength+120+self.shotsSCROLL+40):
                                        
                                        tooltip = "Render The File"
                                        
                                        # get mouse to show the hand
                                        widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
                                        
                                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#5c5c5c"))
                                        widget.window.draw_rectangle(xgc, True, Pstart+20+(cellsize*xstep)+20+110, shotlistlength+120+self.shotsSCROLL+20, 20, 20)
                                        
                                        if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active() and my in range(120, h):
                                            
                                            
                                            # SHOWING WATCH CURSOR
                                            
                                            widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
                                            while gtk.events_pending():
                                                gtk.main_iteration()
                                            
                                            
                                            
                                            def ee(shotname, BName):
                                                
                                                dialogs.rendersettings(self.pf, shotname+"/"+BName)
                                            glib.timeout_add(10, ee, shotname, BName)
                                    
                                    widget.window.draw_pixbuf(None, self.render, 0, 0, Pstart+20+(cellsize*xstep)+20+110, shotlistlength+120+self.shotsSCROLL+20 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)   
                                    
                                    
                                    ##### COPY BUTTON ####
                                    
                                    # MOUSE OVER
                                    if mx in range(Pstart+20+(cellsize*xstep)+20+110, Pstart+20+(cellsize*xstep)+20+130) and my in range(shotlistlength+120+self.shotsSCROLL+50, shotlistlength+120+self.shotsSCROLL+50+22):
                                        
                                        tooltip = "Copy Blendfile to ClipBoard"
                                        
                                        # get mouse to show the hand
                                        widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
                                        
                                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#5c5c5c"))
                                        widget.window.draw_rectangle(xgc, True, Pstart+20+(cellsize*xstep)+20+110, shotlistlength+120+self.shotsSCROLL+50, 20, 20)
                                        
                                        if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active() and my in range(120, h):
                                            
                                            self.BLboard = self.pf+"/"+shotname+"/"+BName
                                    
                                    widget.window.draw_pixbuf(None, self.copy, 0, 0, Pstart+20+(cellsize*xstep)+20+110, shotlistlength+120+self.shotsSCROLL+50 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)   
                                       
                                    
                                    
                                    
                                    
                                    #### LINK CONFRIM BUTTON ####
                                    
                                    # MOUSE OVER
                                    if mx in range(Pstart+20+(cellsize*xstep)+20+110, Pstart+20+(cellsize*xstep)+20+130) and my in range(shotlistlength+120+self.shotsSCROLL+50+30, shotlistlength+120+self.shotsSCROLL+50+22+30):
                                        
                                        tooltip = "Link assets to the blendfile"
                                        
                                        # get mouse to show the hand
                                        widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
                                        
                                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#5c5c5c"))
                                        widget.window.draw_rectangle(xgc, True, Pstart+20+(cellsize*xstep)+20+110, shotlistlength+120+self.shotsSCROLL+50+30, 20, 20)
                                        
                                        if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active() and my in range(120, h):
                                            
                                            def ee(shotname, BName):
                                                
                                                if not os.path.exists(self.pf+"/"+shotname+"/extra/autolink.data"):
                                                    s = open(self.pf+"/"+shotname+"/extra/autolink.data", "w")
                                                    s.close()
                                                
                                                
                                                
                                                linkconfirm.config(self.pf,  self.pf+"/"+shotname+"/extra/autolink.data", self.pf+"/"+shotname+"/"+BName)
                                            glib.timeout_add(10, ee, shotname, BName)
                                    
                                    widget.window.draw_pixbuf(None, self.linkicon, 0, 0, Pstart+20+(cellsize*xstep)+20+110, shotlistlength+120+self.shotsSCROLL+50+30 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)   
                                       
                                    
                                    
                                    
                                    
                                    
                                    
                                    ############    L    O    G   O  ################
                                    
                                    tmp = shotlistlength
                                    shotlistlength = shotlistlength + 22
                                    
                                    
                                    
                                    thisshotlistlengstart
                                    
                                    # TRY TO LOAD THE LOGO
                                    
                                    
                                    if BPic == False:
                                        
                                        try:
                                            BPic = gtk.gdk.pixbuf_new_from_file(thumbnailer.blenderthumb(self.pf+"/"+shotname+"/"+BName, 100,100))
                                        except:
                                            BPic = "None"
                                        
                                        self.shotsDATA[ind][3][BInd][1] = BPic
                                    
                                    
                                    if BPic == False or BPic == "None":
                                    
                                    
                                    
                                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#FFF"))
                                        widget.window.draw_rectangle(xgc, True, Pstart+20+(cellsize*xstep)+20, shotlistlength+120+self.shotsSCROLL+20, cellsize-60, cellsize-60)
                                
                                    else:
                                        
                                        widget.window.draw_pixbuf(None, BPic, 0, 0, Pstart+20+(cellsize*xstep)+20, shotlistlength+120+self.shotsSCROLL+20 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
                                    
                                    
                                    shotlistlength = tmp
                                    
                                xstep = xstep + 1
                                
                                if xstep > xcells:
                                    xstep = 0
                                    
                                    
                                    
                                    shotlistlength = shotlistlength + cellsize
                            
                            
                            
                            shotlistlength = shotlistlength + cellsize
                            
                            
                        
                            shotlistlength = shotlistlength + 10
                            
                            
                            
                            ### PASTE BLEND FILE BUTTON ###
                            
                            
                            if len(self.BLboard) > 0:
                                
                                
                                # MOUSE OVER
                                if mx in range(Pstart, w) and my in range(shotlistlength+120+self.shotsSCROLL, shotlistlength+120+self.shotsSCROLL+20):
                                    
                                    tooltip = "Paste Blend File\n"+self.BLboard
                                    
                                    # get mouse to show the hand
                                    widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
                                    
                                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#5c5c5c"))
                                    widget.window.draw_rectangle(xgc, True, Pstart, shotlistlength+120+self.shotsSCROLL, Ppart, 23)
                                    
                                    if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active() and my in range(120, h):
                                        
                                        widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
                                    
                                        while gtk.events_pending():
                                            gtk.main_iteration()
                                        
                                        
                                        
                                        
                                        def ee(shotname):
                                    
                                            Pname = ""
                                            Pname = dialogs.PickName(self.BLboard[self.BLboard.rfind("/")+1:])
                                        
                                            if Pname != "":
                                                
                                                if Pname.endswith(".blend") == False:
                                                    Pname = Pname + ".blend"
                                                
                                                if Pname not in os.listdir(self.pf+"/"+shotname):
                                                
                                                    
                                                    fr = open(self.BLboard, "r")
                                                    to = open(self.pf+"/"+shotname+"/"+str(Pname), "w")
                                                    to.write(fr.read())
                                                    to.close()
                                                    
                                                    #WRITTING TO HYSTORY
                                                    history.write(self.pf ,"/"+shotname+"/"+str(Pname), "[Added]")
                                                    
                                                    #REFRASHING
                                                    
                                                    try:
                                                        scnDATA = self.FILE.get_scenes_data()
                                                        scenestory = scnDATA[self.event_select][self.scene_select][3]
                                                        self.shotsDATA = get_shots(scenestory, scnDATA[self.event_select][self.scene_select][1])
                                                    except:
                                                        pass
                                        glib.timeout_add(10, ee, shotname)
                                            
                                            
                                
                                widget.window.draw_pixbuf(None, self.paste, 0, 0, Pstart+10, shotlistlength+120+self.shotsSCROLL , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
                                
                                ctx.set_source_rgb(1,1,1)
                                ctx.set_font_size(15)
                                ctx.move_to( Pstart+50, 15+shotlistlength+120+self.shotsSCROLL-2)
                                ctx.show_text(self.BLboard[self.BLboard.rfind("/")+1:])
                                
                            shotlistlength = shotlistlength + 23
                            
                            
                            
                            
                            ### ADD BLEND FILE BUTTON ###
                            
                            # MOUSE OVER
                            if mx in range(Pstart, w) and my in range(shotlistlength+120+self.shotsSCROLL, shotlistlength+120+self.shotsSCROLL+20):
                                
                                tooltip = "Create New, Blank\nBlend File"
                                
                                # get mouse to show the hand
                                widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
                                
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#5c5c5c"))
                                widget.window.draw_rectangle(xgc, True, Pstart, shotlistlength+120+self.shotsSCROLL, Ppart, 23)
                                
                                if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active() and my in range(120, h):
                                    
                                    
                                    
                                    
                                    def ee(shotname):
                                        
                                        Pname = ""
                                        Pname = dialogs.PickName("New_File.blend")
                                    
                                        if Pname != "":
                                            
                                            if Pname.endswith(".blend") == False:
                                                Pname = Pname + ".blend"
                                            
                                            if Pname not in os.listdir(self.pf+"/"+shotname):
                                                
                                                fr = open(self.pf+"/py_data/new_file/empty.blend", "r")
                                                to = open(self.pf+"/"+shotname+"/"+str(Pname), "w")
                                                to.write(fr.read())
                                                to.close()
                                                
                                                
                                                #WRITTING TO HYSTORY
                                                history.write(self.pf ,"/"+shotname+"/"+str(Pname), "[Added]")
                                                
                                                
                                                
                                                #REFRASHING
                                                
                                                try:
                                                    scnDATA = self.FILE.get_scenes_data()
                                                    scenestory = scnDATA[self.event_select][self.scene_select][3]
                                                    self.shotsDATA = get_shots(scenestory, scnDATA[self.event_select][self.scene_select][1])
                                                except:
                                                    pass
                                    glib.timeout_add(10, ee, shotname) 
                                    
                            widget.window.draw_pixbuf(None, self.plus, 0, 0, Pstart+10, shotlistlength+120+self.shotsSCROLL , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
                                
                            ctx.set_source_rgb(1,1,1)
                            ctx.set_font_size(15)
                            ctx.move_to( Pstart+50, 15+shotlistlength+120+self.shotsSCROLL-2)
                            ctx.show_text("Add New Blend File")
                            
                            shotlistlength = shotlistlength + 23
                        
                            
                            SCnames.append([shotname[shotname.rfind("/")+1:].split("\n")[0], thisshotlistlengstart, shotstatussidepanel])
                            
                            
                            
                            
                    
                    #shotlistlength = shotlistlength + 20
                    #xgc.set_rgb_fg_color(gtk.gdk.color_parse("#424242"))
                    #widget.window.draw_rectangle(xgc, True, Pstart, shotlistlength+120+self.shotsSCROLL, Ppart, 1)
                    shotlistlength = shotlistlength + 20
                        
                
            
                
                shotlistlength = shotlistlength + 20
               
           
           ################################ COPY FROM THE TOP ##########################################
           
           # I couln't make it work using a function. So I just copied the code
           
                try:
                    
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#2c2c2c"))
                    widget.window.draw_rectangle(xgc, True, Pstart, shotlistlength+120+self.shotsSCROLL-30, Ppart, h)
                    
                    
                    
                    SSname = scnDATA[self.event_select][self.scene_select][1]
                    
                    ctx2.set_source_rgb(1,1,1)
                    ctx2.set_font_size(20)
                    ctx2.move_to( Pstart+20+(Ppart-50)/2-len(SSname)*12/2, shotlistlength+120+self.shotsSCROLL+5)
                    ctx2.show_text(SSname)
                    
                    
                    #PREVIOUS SCENE
                    
                    for ar in self.FILE.arrows:
                        if ar[1][0] == self.event_select and ar[1][1] == SSname and ar[0][1] != "start":
                            if my in range(shotlistlength+120+self.shotsSCROLL-25, shotlistlength+120+self.shotsSCROLL+20) and mx in range(Pstart+20, Pstart+60):
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#3c3c3c"))
                                widget.window.draw_rectangle(xgc, True, Pstart+20, shotlistlength+120+self.shotsSCROLL-25, 40, 40)
                            
                                if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active():
                                    
                                    
                                            
                                            
                                            
                                    p0, p1, p2, p3, p4 =  self.FILE.events[self.event_select] #SAVING FOR THE FOCUS
                                    
                                    self.event_select = ar[0][0]
                                    self.image_select = False
                                    
                                    for ns, sc in enumerate(scnDATA[self.event_select]):
                                        if sc[1] == ar[0][1]:
                                            self.scene_select = ns
                                    
                                    try:
                                        scnDATA = self.FILE.get_scenes_data()
                                        scenestory = scnDATA[self.event_select][self.scene_select][3]
                                        self.shotsDATA = get_shots(scenestory, scnDATA[self.event_select][self.scene_select][1])
                                    except:
                                        pass
                                    self.shotsSCROLL = 0
                                    
                                    
                                    # FOCUS THE EVENT IN THE CENTER OF THE SCREEN
                                    
                                    d0, d1, d2, d3, d4 =  self.FILE.events[self.event_select] # YOU CAN CHANGE THIS TO ANY EVENT
                                    
                                    #self.px = px + ((p0 * sx)-(d0 * sx))
                                    #self.py = py + ((p2 * sy)-(d2 * sy))
                                            
                                    thex = px-(d0 * sx +px) + (w/3)
                                    they = py-(d2 * sy +py) + (h/2)
                                    
                                    
                                    
                                    self.animate(thex, they)
                                    
                                            
                                
                            widget.window.draw_pixbuf(None, self.big_left, 0, 0, Pstart+20, shotlistlength+120+self.shotsSCROLL-25 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                            
                    
                    #NEXT SCENE
                    for ar in self.FILE.arrows:
                        if ar[0][0] == self.event_select and ar[0][1] == SSname and ar[1][1] != "end":
                            if my in range(shotlistlength+120+self.shotsSCROLL-25, shotlistlength+120+self.shotsSCROLL+20) and mx in range(w-100, w-60):
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#3c3c3c"))
                                widget.window.draw_rectangle(xgc, True, w-100, shotlistlength+120+self.shotsSCROLL-25, 40, 40)
                            
                                if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active():
                                    
                                    
                                            
                                    p0, p1, p2, p3, p4 =  self.FILE.events[self.event_select] #SAVING FOR THE FOCUS
                                    
                                    self.event_select = ar[1][0]
                                    self.image_select = False
                                    
                                    for ns, sc in enumerate(scnDATA[self.event_select]):
                                        if sc[1] == ar[1][1]:
                                            self.scene_select = ns
                                    
                                    try:
                                        scnDATA = self.FILE.get_scenes_data()
                                        scenestory = scnDATA[self.event_select][self.scene_select][3]
                                        self.shotsDATA = get_shots(scenestory, scnDATA[self.event_select][self.scene_select][1])
                                    except:
                                        pass
                                    self.shotsSCROLL = 0
                                    
                                    # FOCUS THE EVENT IN THE CENTER OF THE SCREEN
                                    
                                    d0, d1, d2, d3, d4 =  self.FILE.events[self.event_select] # YOU CAN CHANGE THIS TO ANY EVENT
                                    
                                    #self.px = px + ((p0 * sx)-(d0 * sx))
                                    #self.py = py + ((p2 * sy)-(d2 * sy))
                            
                                    thex = px-(d0 * sx +px) + (w/3)
                                    they = py-(d2 * sy +py) + (h/2)
                                    
                                    
                                    
                                    self.animate(thex, they)
                            
                            
                            widget.window.draw_pixbuf(None, self.big_right, 0, 0, w-100, shotlistlength+120+self.shotsSCROLL-25 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                            
                    
                    shotlistlength = shotlistlength + 20
                
                
                
                
                except:
                    pass    
           
           
           ################################ COPY FROM THE TOP END ##########################################
           
            
            elif type(self.image_select) != bool:      
                
                  url = self.image_select[1]
                  if url.startswith("[item]"):     
                        
                      #ITEM FOLDER
                      
                      shotname = url[url.find("]")+2:]
                      
                      # MOUSE OVER
                      if mx in range(Pstart, w-50) and my in range(shotlistlength+120+self.shotsSCROLL, shotlistlength+120+self.shotsSCROLL+20):
                          
                          
                          
                          tooltip = "/"+shotname
                          
                          # get mouse to show the hand
                          widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
                          
                          xgc.set_rgb_fg_color(gtk.gdk.color_parse("#5c5c5c"))
                          widget.window.draw_rectangle(xgc, True, Pstart, shotlistlength+120+self.shotsSCROLL, Ppart, 23)
                          
                          if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active() and my in range(120, h):
                              
                              oscalls.Open(self.pf+"/"+shotname)
                          
                          
                      
                      # DRAW BUTTON
                      
                      widget.window.draw_pixbuf(None, self.foldericon, 0, 0, Pstart+10, shotlistlength+120+self.shotsSCROLL , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
                      
                      ctx.set_source_rgb(1,1,1)
                      ctx.set_font_size(15)
                      ctx.move_to( Pstart+50, 15+shotlistlength+120+self.shotsSCROLL+2)
                      ctx.show_text("Item's Folder")
                      
                      
                      shotlistlength = shotlistlength + 30
                      
                      #REFERENCES
                      
                      
                      
                      # MOUSE OVER
                      if mx in range(Pstart, w-50) and my in range(shotlistlength+120+self.shotsSCROLL, shotlistlength+120+self.shotsSCROLL+20):
                          
                          
                          
                          tooltip = "/"+shotname+"/reference"
                          
                          # get mouse to show the hand
                          widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
                          
                          xgc.set_rgb_fg_color(gtk.gdk.color_parse("#5c5c5c"))
                          widget.window.draw_rectangle(xgc, True, Pstart, shotlistlength+120+self.shotsSCROLL, Ppart, 23)
                          
                          if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active() and my in range(120, h):
                              
                              oscalls.Open(self.pf+"/"+shotname+"/reference")
                          
                          
                      
                      # DRAW BUTTON
                      
                      widget.window.draw_pixbuf(None, self.foldericon, 0, 0, Pstart+10, shotlistlength+120+self.shotsSCROLL , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
                      
                      ctx.set_source_rgb(1,1,1)
                      ctx.set_font_size(15)
                      ctx.move_to( Pstart+50, 15+shotlistlength+120+self.shotsSCROLL+2)
                      ctx.show_text("References")
                      
                      shotlistlength = shotlistlength + 30
                      
                      
                      
                      #tex
                      
                      
                    
                      # MOUSE OVER
                      if mx in range(Pstart, w-50) and my in range(shotlistlength+120+self.shotsSCROLL, shotlistlength+120+self.shotsSCROLL+20):
                          
                          
                          
                          tooltip = "/"+shotname+"/tex"
                          
                          # get mouse to show the hand
                          widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
                          
                          xgc.set_rgb_fg_color(gtk.gdk.color_parse("#5c5c5c"))
                          widget.window.draw_rectangle(xgc, True, Pstart, shotlistlength+120+self.shotsSCROLL, Ppart, 23)
                          
                          if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active() and my in range(120, h):
                              
                              oscalls.Open(self.pf+"/"+shotname+"/tex")
                          
                          
                      
                      # DRAW BUTTON
                      
                      widget.window.draw_pixbuf(None, self.foldericon, 0, 0, Pstart+10, shotlistlength+120+self.shotsSCROLL , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
                      
                      ctx.set_source_rgb(1,1,1)
                      ctx.set_font_size(15)
                      ctx.move_to( Pstart+50, 15+shotlistlength+120+self.shotsSCROLL+2)
                      ctx.show_text("Textures")
                      
                      shotlistlength = shotlistlength + 30
                      
                      
                      #renders
                      
                      
                      
                      # MOUSE OVER
                      if mx in range(Pstart, w-50) and my in range(shotlistlength+120+self.shotsSCROLL, shotlistlength+120+self.shotsSCROLL+20):
                          
                            
                          
                          tooltip = "/"+shotname+"/renders"
                          
                          # get mouse to show the hand
                          widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
                          
                          xgc.set_rgb_fg_color(gtk.gdk.color_parse("#5c5c5c"))
                          widget.window.draw_rectangle(xgc, True, Pstart, shotlistlength+120+self.shotsSCROLL, Ppart, 23)
                          
                          if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active() and my in range(120, h):
                              
                              oscalls.Open(self.pf+"/"+shotname+"/renders")
                          
                          
                      
                      # DRAW BUTTON
                      
                      widget.window.draw_pixbuf(None, self.foldericon, 0, 0, Pstart+10, shotlistlength+120+self.shotsSCROLL , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
                      
                      ctx.set_source_rgb(1,1,1)
                      ctx.set_font_size(15)
                      ctx.move_to( Pstart+50, 15+shotlistlength+120+self.shotsSCROLL+2)
                      ctx.show_text("Renders")
                      
                      shotlistlength = shotlistlength + 30
                      
                      
                      #scenes
                      scnDATA = self.FILE.get_scenes_data()
                      
                      if not self.itemscenedata:
                        
                          for scn in scnDATA:
                              for sh in scn:
                                  scnname = sh[1]
                                  if shotname in sh[3]:
                                      self.itemscenedata.append(scnname)
                      
                      
                      for scn in self.itemscenedata:
                          
                          # MOUSE OVER
                          if mx in range(Pstart, w-50) and my in range(shotlistlength+120+self.shotsSCROLL, shotlistlength+120+self.shotsSCROLL+20):
                              
                              
                              
                              tooltip = "Go to "+scn+" scene."
                              
                              # get mouse to show the hand
                              widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
                              
                              xgc.set_rgb_fg_color(gtk.gdk.color_parse("#5c5c5c"))
                              widget.window.draw_rectangle(xgc, True, Pstart, shotlistlength+120+self.shotsSCROLL, Ppart, 23)
                              
                              if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active() and my in range(120, h):
                                  
                                  self.searchscene = scn
                                  self.frame = 10
                          widget.window.draw_pixbuf(None, self.scnicon, 0, 0, Pstart+10, shotlistlength+120+self.shotsSCROLL , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
                          
                          ctx.set_source_rgb(1,1,1)
                          ctx.set_font_size(15)
                          ctx.move_to( Pstart+50, 15+shotlistlength+120+self.shotsSCROLL+2)
                          ctx.show_text(scn)
                          
                          shotlistlength = shotlistlength + 30
                      
                      shotlistlength = shotlistlength + 60
                      
                      
                      xgc.set_rgb_fg_color(gtk.gdk.color_parse("#2c2c2c"))
                      widget.window.draw_rectangle(xgc, True, Pstart, shotlistlength+120+self.shotsSCROLL-30, Ppart, h)
                      
                  else:
                      xgc.set_rgb_fg_color(gtk.gdk.color_parse("#2c2c2c"))
                      widget.window.draw_rectangle(xgc, True, Pstart, shotlistlength+120+self.shotsSCROLL-30, Ppart, h)
                        
                        
            else:
                
                
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#2c2c2c"))
                widget.window.draw_rectangle(xgc, True, Pstart, shotlistlength+120+self.shotsSCROLL-30, Ppart, h)
                        
            
            
            
            #LOOK FOR SCENE /  SHOT
            #self.searchscene = "Scene_j7m1g1955j1r"
            
            
            
            if self.searchscene:
                
                try:
                    scnDATA = self.FILE.get_scenes_data()
                    
                    
                    
                    for n, e in enumerate(self.FILE.events):
                        for z, sc in enumerate(scnDATA[n]):
                            if sc[1] == self.searchscene:
                        
                        
                                self.event_select = n
                                self.image_select = False
                                self.scene_select = z
                                focusevent = True

                    scenestory = scnDATA[self.event_select][self.scene_select][3]
                    self.shotsDATA = get_shots(scenestory, scnDATA[self.event_select][self.scene_select][1])
                except:
                    pass    
                
                self.searchscene = ""
                
                
            elif self.frame == 1:
                
                focusonnow = 0
                for i in self.FILE.arrows:
                    if i[0] == [-1, 'start']:
                        focusonnow = i[1][0]
                        break
                self.event_select = focusonnow
                self.image_select = False
                self.scene_select = 0
                try:
                    scnDATA = self.FILE.get_scenes_data()
                    scenestory = scnDATA[self.event_select][self.scene_select][3]
                    self.shotsDATA = get_shots(scenestory, scnDATA[self.event_select][self.scene_select][1])
                except:
                    pass    
                
                
            #also clean if not found
            if self.frame == 20:
                self.searchscene = ""
                self.searchshot = ""
            
               
            
            
            # SCROLL
            
            if mx in range(Pstart, w) and my in range(120, h):
                
                if self.mpy > my and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf) and self.win.is_active():
                    
                    self.shotsSCROLL = self.shotsSCROLL + (my-self.mpy)
                    
                    
                
                if self.mpy < my and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf) and self.win.is_active():
                    
                    self.shotsSCROLL = self.shotsSCROLL - (self.mpy-my)
                    
            
            if 65362 in self.keys:
                self.shotsSCROLL = self.shotsSCROLL + 100
            elif 65364 in self.keys:
                self.shotsSCROLL = self.shotsSCROLL - 100
            
            
            
            
            
                
            
            
            
            
            Pofruler = h-100
            Ponruler = my-50
            
            
            
            RulerY = int(Pofruler*(float(self.shotsSCROLL*-1)/shotlistlength))+50
            
            
            # get ruler properly
            d = h
            din = h-110
            
            l = shotlistlength
            
            leng = int(float(din)*(float(d)/l))
            
            
            
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#232323"))
            widget.window.draw_rectangle(xgc, True, w-50, RulerY, 50, leng)
            
            
            if mx in range(w-50, w):
                if "GDK_BUTTON2" in str(fx) or "GDK_BUTTON3" in str(fx):
                    
                    
                    
                    PerRuler = float(Ponruler)/Pofruler
                    self.shotsSCROLL  = int(shotlistlength*PerRuler)*-1
                    
                    
                    if my in range(0, 50):
                    
                        self.shotsSCROLL = 0
                    if my in range(h-50, h):
                         
                        self.shotsSCROLL = 0-shotlistlength+(h-120)
            
            
            
            for name, loc, status in SCnames:
                
                yfloat = float(loc)/shotlistlength
                
                y = int(float(h-100)*yfloat)+50+15
                
                
                if status == 0:                         ####OPENGL
                    ctx2.set_source_rgb(0.5,0.5,0.0)
                elif status == 1:
                    ctx2.set_source_rgb(0.3,0.3,0.0)    #PREP
                elif status == 2:
                    ctx2.set_source_rgb(0.0,0.0,0.8)    #TESTING
                elif status == 3:
                    ctx2.set_source_rgb(0.0,0.5,0.0)      # DONE
                else:
                    ctx2.set_source_rgb(0.3,0.3,0.3)     ##NOTHING
                    
                ctx2.set_font_size(12)
                ctx2.move_to( w-50, y)
                ctx2.show_text(name)
                
            
            
            
            if self.shotsSCROLL < 0-shotlistlength+(h-120):
                self.shotsSCROLL = 0-shotlistlength+(h-120)
            
            if self.shotsSCROLL > 0:
                self.shotsSCROLL = 0
            
            
            
            
            ###### TOP EVENT EDIT BIG FUCKING BUTTTON
            
            
            
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#2c2c2c"))
            widget.window.draw_rectangle(xgc, True, w-(w)/3, 0, (w)/3-50, 120) ##################
            
            
            
            # loading selected event to the side panel
            
            try:        # I don't want to touch the TRY but WHY is it here. It doesn't make any sense.
                
                if type(self.event_select) != bool:
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#3f3f3f")) # BUTTON HIGHLIGHT
                    widget.window.draw_rectangle(xgc, True, w-(w)/3+50, 50, (w)/3-150, 50)
                    
                    event = self.FILE.events[self.event_select]
                    
                    name = event[3]
                    story = event[4]
                    
                    
                    
                    # IF MOUSE OVER THE TEXT
                    if mx in range(Pstart+50, w-100) and my in range(50, 100):
                        
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
                        widget.window.draw_rectangle(xgc, True, w-(w)/3+50, 50, (w)/3-150, 50)
                        
                        tooltip = "[ Tab ]\n\n  Edit the text of the scene, \nsetup shots, mark items etc."
                        
                        # IF CLICKED
                        
                        if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active() and self.frame > 2:
                            
                            def ee(e=None):
                                
                                self.undo_record()
                                
                                
                                editevent = dialogs.event(name, story, self.FILE, self.event_select)
                                editevent.edit()
                                
                                self.doundo = True
                                
                                
                                try:
                                    scnDATA = self.FILE.get_scenes_data()
                                    scenestory = scnDATA[self.event_select][self.scene_select][3]
                                    self.shotsDATA = get_shots(scenestory, scnDATA[self.event_select][self.scene_select][1])
                                except:
                                    pass
                                #self.shotsSCROLL = 0
                                
                                
                            glib.timeout_add(10, ee)
                            
                        
                    
                    
                    ctx.set_source_rgb(1,1,1)
                    ctx.set_font_size(17)
                    ctx.move_to( Pstart+20, 30)
                    ctx.show_text("Event ID: "+name)
                   
                    ctx.set_source_rgb(1,1,1)
                    ctx.set_font_size(30)
                    ctx.move_to( Pstart+20+100, 85)
                    ctx.show_text("EDIT")
                    
                    widget.window.draw_pixbuf(None, self.big_edit, 0, 0, Pstart+20+50, 55 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
                    
                
                    
                    
            except:
                pass
            
            if type(self.image_select) != bool:
                
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#3f3f3f")) # BUTTON HIGHLIGHT
                widget.window.draw_rectangle(xgc, True, w-(w)/3+50, 50, (w)/3-150, 50)
                
                url = self.image_select[1]
                
                if url.startswith("[item]"):
                    name = url[url.rfind("/")+1:]
                    
                    if "/chr/" in url:
                        widget.window.draw_pixbuf(None, self.chricon, 0, 0, Pstart+20, 12 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                    elif "/loc/" in url:
                        widget.window.draw_pixbuf(None, self.locicon, 0, 0, Pstart+20, 12 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                    elif "/veh/" in url:
                        widget.window.draw_pixbuf(None, self.vehicon, 0, 0, Pstart+20, 12 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                    elif "/obj/" in url:
                        widget.window.draw_pixbuf(None, self.objicon, 0, 0, Pstart+20, 12 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                else:
                    name = url[url.rfind("]")+1:]
                    widget.window.draw_pixbuf(None, self.picicon, 0, 0, Pstart+20, 12 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                    
                
                # IF MOUSE OVER THE TEXT
                if mx in range(Pstart+50, w-100) and my in range(50, 100):
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
                    widget.window.draw_rectangle(xgc, True, w-(w)/3+50, 50, (w)/3-150, 50)
                    
                    if url.startswith("[item]"):
                        tooltip = "Open selected item."
                    else:
                        tooltip = "Open selected image."
                    
                    # IF CLICKED
                    
                    if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and self.win.is_active() and self.frame > 2:
                        
                        def ee(e=None):
                            
                            
                            url = self.image_select[1]
                            
                            
                            
                            if url.startswith("[item]"):
                                CUR = url[:url.rfind("/")]
                                CUR = CUR[CUR.rfind("/")+1:]
                                url = url[url.rfind("/")+1:]
                                
                                
                                def ee(CUR, url):
                                    self.box.destroy()
                                    
                                    
                                    self.box = gtk.VBox(False)
                                    self.mainbox.pack_start(self.box, True)
                                    
                                    assets.draw_assets(os.getcwd(), self.box, self.win, CUR, url, mainbox=self.mainbox)
                                
                                glib.timeout_add(10, ee, CUR, url)
                                
                                launchitem = False
                                
                                
                                
                            else:   
                                
                                url = url[url.rfind("]")+1:]
                                
                                if os.path.exists(url):
                                    oscalls.Open(url)
                                else:
                                    oscalls.Open(self.pf+url)
                            
                            
                        glib.timeout_add(10, ee)
                            
                
                
                
                ctx.set_source_rgb(1,1,1)
                ctx.set_font_size(17)
                ctx.move_to( Pstart+20+30, 30)
                ctx.show_text(name)
               
                ctx.set_source_rgb(1,1,1)
                ctx.set_font_size(30)
                ctx.move_to( Pstart+20+50, 85)
                ctx.show_text("OPEN")
            
                
                
                
            fif = datetime.datetime.now()
            mil  = fif - stf
            perfStat.append([ "SIDE PANNEL", mil.microseconds])
            
            stf = datetime.datetime.now()     
                
            
            ##################################
            
            
            # NUMBER PAD .
            if 65454 in self.keys or 65452 in self.keys or focusevent:
                
                # LET'S ATTEMPT TO MOVE CAMERA TO THE SELECTED SCENE
                d0, d1, d2, d3, d4 =  self.FILE.events[self.event_select] # YOU CAN CHANGE THIS TO ANY EVENT
                                    
                thex = px-(d0 * sx +px) + (w/3)
                they = py-(d2 * sy +py) + (h/2)
                
                
                
                self.animate(thex, they)
    
                        
            # ESCAPE
            if 65307 in self.keys:  # ESCAPE BUTTON
                
                self.tool = "select"
            
            # HOME
            if 65360 in self.keys:    
                
                self.shotsSCROLL = 0
                
                try:
                    found = False
                    
                    for i in self.FILE.arrows:
                        if i[0] == [-1, 'start']:
                            self.searchscene = i[1][1]
                            found = True
                            break
                                            
                     
                    
                    
                    if not found:
                        d0, d1, d2, d3, d4 =  self.FILE.events[0] # YOU CAN CHANGE THIS TO ANY EVENT
                                            
                        #self.px = px-(d0 * sx +px) + (w/3)
                        #self.py = py-(d2 * sy +py) + (h/2)
                        
                        
                        thex = px-(d0 * sx +px) + (w/3)
                        they = py-(d2 * sy +py) + (h/2)
                        
                        
                        
                        self.animate(thex, they)
            
                        
                        
                        
                        
                        self.event_select = 0
                        self.image_select = False
                        self.scene_select = 0
                        try:
                            scnDATA = self.FILE.get_scenes_data()
                            scenestory = scnDATA[self.event_select][self.scene_select][3]
                            self.shotsDATA = get_shots(scenestory, scnDATA[self.event_select][self.scene_select][1])
                        except:
                            pass 
                        
                except:
                    pass
                
                self.keys = []
                
            # END
            if 65367 in self.keys:    
                
                self.shotsSCROLL = 0
                
                try:
                    focusonnow = 0
                    
                    for i in self.FILE.arrows:
                        if i[1] == [-1, 'end']:
                            self.searchscene = i[0][1]
                            break
                     
                except:
                    pass
                
                self.keys = []
                
            #65367
            
            ####################################
            
            
            ##### TOOLTIP
            
            
            
            if tooltip:
                
                b = 0
                for i in str(tooltip).split("\n"):
                    if len(i) > b:
                        
                        b = len(i)
                
                xsize = b*9+2
                ysize = len(str(tooltip).split("\n"))*16
                
                
                
                ctx3 = widget.window.cairo_create()
                ctx3.set_source_rgba(0,0,0,0.75)
                ctx3.rectangle(mx+10, my+8, xsize,ysize)
                ctx3.fill()
                
                for n, i in enumerate(str(tooltip).split("\n")):
                    
                    
                    ctx2.set_source_rgb(1,1,1)
                    ctx2.set_font_size(15)
                    ctx2.move_to( mx+11, my+20+(n*15)+2)
                    ctx2.show_text(i)
            
            
            # I FOUND AN OVERFLOW BUG IN GTK DRAWABLE. IF YOU MOVE SOMETHING TOO FAR AWAY FROM 
            # THE SCREEN IT'S GOING TO COME BACK FROM THE OTHER SIDE...
            
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#f00"))
            #widget.window.draw_rectangle(xgc, True, w/2, self.frame, 20,20) # RESTORE THIS...
            
            ctx2.set_source_rgb(1,0,0)
            ctx2.set_font_size(20)
            ctx2.move_to( w/2, 50)
            #ctx2.show_text(str(self.frame)) # ... AND THIS TO SEE THE TESTER IN ACTION
            
            #                                  ####                      ####
            # FOUND IT RETURNED BACK AT ROUGLY ####      66K PIXELS      #### FROM THE TOP.
            #                                  ####                      ####
            # IT DOESN'T DO IT WITH CAIRO THO... INTERESTING... DOES ANYBODY HAVE A MORE ACCURATE MEASURE?
            
            
            # TESTING SOMETHING
            ctx.set_font_size(20)
            ctx.move_to( mx, my)
            #ctx.show_text(str(mx)+":"+str(my)+"  "+str(self.winactive)+"   "+str(fx)) 
            
            
            
            #AUTOSAVE
            if (self.frame % 10) == 0 and "GDK_BUTTON" not in str(fx) and "GDK_BUTTON" not in str(self.mpf):
                self.FILE.save(px,py,sx,sy)
                
                
                
                if self.doundo:
                    self.undo_record()
                    self.doundo = False
            
            if self.previousactive != self.win.is_active(): # ON GNOME SOMETMES THE CTRL IS PRESSED WHEN YOU COME FROM A 
                self.keys = []                              # DIFFRENT PROGRAM. SO I'M CLEANING THE BUTTONS JUST IN CASE.
            
                
            
            
            
            self.dW = w
            self.DH = h
            
            self.mpx = mx
            self.mpy = my
            self.mpf = fx
            
            self.previousactive = self.win.is_active() 
            
            
            #UNDO
            if 65507 in self.keys and 122 in self.keys:
                self.undo()
                self.undo()
                self.keys.remove(122)
                #self.keys.remove(65507)
            elif 65507 in self.keys and 121 in self.keys:
                self.redo()
                self.redo()
                self.keys.remove(121)
                #self.keys.remove(65507)
            
            
            
            
            fif = datetime.datetime.now()
            mil  = fif - stf
            perfStat.append([ "TOOLTIPS AND AUTOSAVE", mil.microseconds])
            
            
            ########################
            
            
            #          PERFORMANCE ANALYTICS                   #
            
            ###########################
            
            
            rue = mx in range(0, 200) and my in range(h-200, h)
            
            
            
            if rue:  # CHANGE TO FALSE WHEN YOU DON'T NEED TO CHECK PERFORMANCE
                
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#000"))
                widget.window.draw_rectangle(xgc, True, 10, h-(len(perfStat)*15)-30, 500,len(perfStat)*15+30)
                
                l = 0
                s = 0
                for i in perfStat:
                    if int(i[1]) > l:
                        l = int(i[1])
                    s = s + int(i[1])
                for n, i in enumerate(perfStat):
                    ctx2.set_source_rgb(1,1,1)
                    if int(i[1]) == l:
                        ctx2.set_source_rgb(1,0,0)
                    elif int(i[1]) < 1000:
                        ctx2.set_source_rgb(0,1,0)
                    ctx2.set_font_size(10)
                    ctx2.move_to( 20, h-(len(perfStat)*15)+15*n)
                    
                    p = float(i[1]) / s *100
                    
                    ctx2.show_text(str(i[0])+" - "+str(i[1])+" MCRS "+str(int(round(p)))+"%")
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#222"))
                    widget.window.draw_rectangle(xgc, True, 20 + 270, h-(len(perfStat)*15)-20+10+15*n, 200,10)
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#fff"))
                    widget.window.draw_rectangle(xgc, True, 20 + 270, h-(len(perfStat)*15)-20+10+15*n, int(round(p))*2,10)
            
            
            
            def callback():
                if self.allowed == True:
                    widget.queue_draw()

            glib.timeout_add(1, callback)     
                    
            
        graph = gtk.DrawingArea()
        graph.set_size_request(500,700)
        
        self.box.pack_start(graph)
        graph.connect("expose-event", framegraph) 
        
        
        def motion_cb(wid, context, x, y, time):
    
            context.drag_status(gtk.gdk.ACTION_COPY, time)
            return True
        def drop_cb(wid, context, x, y, time):
            wid.drag_get_data(context, context.targets[-1], time)
            return True
        def got_data_cb(wid, context, x, y, data, info, time):
            
            import urllib
            data.get_text()
            urllib.unquote(data.get_text())[7:]
            x, y
            u = urllib.unquote(data.get_text())[7:].split("\n")[0]
            
            imageNOT = True
            for i in fileformats.images:
                
                if u.lower().endswith(i):
                    imageNOT = False
                    
                    # FOUND THE IMAGE
                    
                    #making athumb and saving it using a random name
                    
                    #making sure that thumb directory exists
                    if not os.path.exists(self.pf+"/pln/thumbs/"):
                        os.makedirs(self.pf+"/pln/thumbs/")
                    
                    
                    #chosing a random name for the thumb
                    rndname = ""
                    rndchar = "QWERTYUIOPASDFGHJKLZXCVBNM1234567890"
                    while os.path.exists(self.pf+"/pln/thumbs/"+rndname+".png") or rndname == "":
                        rndname = ""
                        for l in range(20):
                            rndname = rndname + random.choice(rndchar)
                        
                    
                    #thumbnailer.thumbnail
                    
                    fromr  = open(thumbnailer.thumbnail(u, x=150, y=150), "r")
                    saveto = open(self.pf+"/pln/thumbs/"+rndname+".png", "w")
                    saveto.write(fromr.read())
                    saveto.close()
                    pureX = (x -   self.px)/self.sx  - 1
                    pureY = int((y    - self.py   )/self.sy)
                    
                    if u.startswith(self.pf):
                        self.FILE.images.append([pureX, pureY, "RELATIVE", u.replace(self.pf, ""), rndname, gtk.gdk.pixbuf_new_from_file(self.pf+"/pln/thumbs/"+rndname+".png")])
                    else:
                        self.FILE.images.append([pureX, pureY, "ABSOLUTE", u, rndname, gtk.gdk.pixbuf_new_from_file(self.pf+"/pln/thumbs/"+rndname+".png")])
                    
                    
                    
                    
            if imageNOT:
                try:
                    MT = open(urllib.unquote(data.get_text().split("\n")[0])[7:], "r")
                    lets = "    qwertyuiop[]asdfghjkl;'\\zxcvbnm,./`1234567890-=\nQWERTYUIOP{}ASDFGHJKL:\"|ZXCVBNM<>?~!@#$%^&*()_+"
                    MT = MT.read()
                    for i in MT:
                        if i not in lets:
                            
                            return
                    
                    pureX = (x -   self.px)/self.sx  - 1
                    pureS = 100.0
                    pureY = (y    - self.py   )/self.sy
                    
                    
                    self.FILE.events.append([pureX, pureS, pureY, urllib.unquote(data.get_text().split("\n")[0])[urllib.unquote(data.get_text().split("\n")[0]).rfind("/")+1:], MT])
                
                except:
                    raise
            
            context.finish(True, False, time)
            

        graph.drag_dest_set(0,[],0)
        graph.connect("drag_motion", motion_cb)
        graph.connect("drag_drop", drop_cb)
        graph.connect("drag_data_received", got_data_cb)
        
        
        
        ## GETTING BUTTON PRESS EVENTS
        def bpe( w, event):
            
            
            if event.keyval not in self.keys:
                self.keys.append( event.keyval )
            print "\033[1;31m ⬥ ACTIVE KEYS : \033[1;m"
            for i in self.keys:
                print "\033[1;32m     ⬦ "+str(i)+"  \033[1;m"
            
        def bre (w, event):    
            
            try:
                self.keys.remove( event.keyval )
            except:
                pass
            
            
            
        self.win.connect("key_press_event", bpe)
        self.win.connect("key_release_event", bre)
        
        
        self.box.show_all() 




# BOS FILES LOADER AND WRITER



class bos:
    
    
    def __init__(self, filename):
        
        
        
        self.filename = filename
        
        if not os.path.exists(filename):
            self.new(filename)
        
        
        self.events = []
        self.arrows = []
        self.markers = []
        self.images = []
        self.tree = [] # THIS IS THE PLACE WEHRE STORED THE [IND, NAME] of scenes in the connected line from START to END of the movie
        
    def new(self, name):
        
        make = open(name, "w")
        make.write("# BOS blender- organizer story")
        make.close()
    
    def clear_arrows(self):
        
        ## THIS FUNCTION WILL CLEAR ALL DUPLICATIONS IN ARROWS...
        ## USE IT IN EVERY ARROW ADDITION TO MAKE SURE THERE IS NO
        ## WEIRD PATHS OF ARROWS
        
        # REMOVING DOUBLE CONNECTION TO ONE POINT
        
        for num, arrow in enumerate(self.arrows):
            
            for num2, arrow2 in enumerate(self.arrows):
                
                
                if arrow[0] == arrow2[0] or arrow[1] == arrow2[1]:
                    
                    self.arrows[num] = arrow2
        
        
        
        
        
        
        # removing doubles
        
        tmp = []
        
        for i in self.arrows:
            if i not in tmp:
                tmp.append(i)
        self.arrows = tmp
        
        
        
        return self.arrows # JUST IN CASE
    
            
    # THIS WILL OUTPUT THE SCENES DATA OUT FROM ALL EVENTS
    def get_scenes_data(self):
        
        scenes = []  # [[ event, name, dots,  text ] ,...]
        
        for IND, event in enumerate(self.events):
            
            name = event[3]
            story = event[4]
            
            eventscenes  = []
            
            if "<scene>" in story and "</scene>" in story:
                    
                sa = story.count("<scene>") # COUNT AMOUNT OF SCENES
                
                ts = story
                
                dot = 0
                dots = []
                
                # getting the values of the dots
                for i in range(sa):
                    
                    dot = dot + ts.find("<scene>")
                    d = [dot]
                    
                    ts = ts[ts.find("<scene>"):]
                    dot = dot + ts.find("</scene>")+8
                    
                    
                    # Adding scenes to a list to process later
                    
                    scene_text = ts[7:ts.find("</scene>")]
                    
                    
                    
                    
                    
                    ts = ts[ts.find("</scene>")+8:]
                    
                    d.append(dot)
                    dots.append(d)
                    
                    if '"' in scene_text[:scene_text.find("<")]:
                        name = scene_text[scene_text.find('"')+1:scene_text.replace('"', " ", 1).find('"')]
                        scene_text = scene_text.replace('"'+name+'"', "", 1)
                    else:
                        name = "Uknnown Scene"
                    
                    name = name.replace("\n","_").replace("/","_").replace(" ", "_").replace('"',"_").replace("(","_").replace(")","_").replace("'","_").replace("[","_").replace("]","_").replace("{","_").replace("}","_")   
                    
                    
                    eventscenes.append(  [IND, name, d, scene_text]  )
            
            scenes.append(eventscenes)
        
        return scenes
    
        
    def load(self):
    
        
        self.events = []
        self.arrows = []
        self.markers = []
        self.images = []
        
        openfile = open(self.filename, "r")
        openfile = openfile.read()
        
        
        if "<event>" in openfile and "</event>" in openfile:
            
            # GETTING THE LIST OF EVENTS
            ep = openfile[openfile.find("<event>"):openfile.rfind("</event>")+8]# EP stants for events parts
            
            
            for event in ep.split("</event>")[:-1]:
                event = event[event.find("<event>")+8:] # CLEAFIYING THE TEXT OF THE EVENT
                
                
                #EVENT NAME
                
                name = event[event.find('"')+1:event.replace('"'," ",1).find('"')]
                
                
                
                # COORDINATES
                
                coordtext = event[event.find('[')+1:event.find(']')]
                
                print "\033[1;32m     ⬦ EVENT: "+name+" "+coordtext+" "+str(event.count("\n"))+" lines \033[1;m"
                
                coordinates =  coordtext.split(",")
                
                # EVENT TEXT
                
                story = event[event.find(']')+2:-1]
                
                #making coordinates into FLOATS
                
                tmp = []
                
                for i in coordinates:   
                
                    tmp.append(float(i))
                
                coordinates = tmp
                
                coordinates.append(name)
                coordinates.append(story)
                
                self.events.append( coordinates )
        
        if "<arrow>" in openfile and "</arrow>" in openfile:
            
            
            # GETTING THE LIST OF ARROWS
            ap = openfile[openfile.find("<arrow>"):openfile.rfind("</arrow>")+8]# AP stants for arrow parts
                
            for arrow in ap.split("</arrow>")[:-1]:
                
                arrow = arrow[arrow.find("<arrow>")+7:]
                
                # getting 2 sides
                
                arrow = arrow.split(" --> ")   
                
                
                arr = []
                
                
                for i in arrow: 
                    
                    side = i.split(",")
                    side = [ int(side[0]), side[1][side[1].find('"')+1:side[1].replace('"'," ",1).find('"')   ].replace("\n","_").replace("/","_").replace(" ", "_").replace('"',"_").replace("(","_").replace(")","_").replace("'","_").replace("[","_").replace("]","_").replace("{","_").replace("}","_") ]
                    
                    arr.append(side)
                
                self.arrows.append(arr)
        
        
        #### GETTING MARKERS
        
        if "<marker>" in openfile and "</marker>" in openfile:
            
            #GETTING THE LIST OF MARKERS
            
            mp = openfile[openfile.find("<marker>"):openfile.rfind("</marker>")+9]# MP stants for markers parts
            
            for marker in mp.split("</marker>")[:-1]:
                
                mark = []
                
                marker = marker[marker.find("<marker>")+8:].split(",")
                
                
                mark.append(float(marker[0]))
                mark.append(str(marker[1][marker[1].find('"')+1:marker[1].replace('"'," ",1).find('"') ]))
                
                self.markers.append(mark)
        
        
        
        
        
        
        
        tmpopenfile = openfile
        if "</arrow>" in openfile:
            openfile = openfile[openfile.rfind("</arrow>"):]
        elif "</scene>" in openfile:
            openfile = openfile[openfile.rfind("</scene>"):]
        
        
        
        #### GETTING IMAGES
        if "<image>" in openfile and "</image>" in openfile:
            
            allpixs = openfile[openfile.find("<image>"):openfile.rfind("</image>")+8]
            
            for img in allpixs.split("</image>")[:-1]:
                
                image = []
                
                img = img[img.find("<image>")+7:].split(",")
                
                image.append(float(img[0]))
                image.append(float(img[1]))
                image.append(str(img[2][img[2].find('"')+1:img[2].replace('"'," ",1).find('"') ]))
                image.append(str(img[3][img[3].find('"')+1:img[3].replace('"'," ",1).find('"') ]))
                image.append(str(img[4][img[4].find('"')+1:img[4].replace('"'," ",1).find('"') ]))
                image.append("NO PIXBUF")
                
                self.images.append(image)
                
                
            
            
        
        #for image in self.images:
        #    
        #    imX, imY, mode, url, thumb, pixthumb = image
        #    savefile.write('<image>'+str(imX)+',"'+str(imY)+',"'+str(mode)+',"'+str(url)+',"'+str(thumb)+'"</image>\n')
        
        
        
        
        openfile = tmpopenfile
        
        #### GETTING CAMERA DIMENTIONS ####
        
        if "<camera>" in openfile and "</camera>" in openfile:
            
            camera = openfile[openfile.find("<camera>")+8:openfile.rfind("</camera>")].split(",")
            
            
            # clearing  the camera list
            tmp = []
            
            for i in camera:
                tmp.append(float(i))
            
            camera = tmp
            
            return camera #outputiing the camera data and shutting the fuck up
                
        
    
        return 0.0,0.0,0.6, 61.5
    
    
    def event_delete(self, num):
        
        try:
            
            if type(num) != bool:
                del self.events[num]
                
                
                
                
                # deleting all arrows connected
                
                new = []
                for n, i in enumerate(self.arrows):
                    
                    
                    
                    if i[0][0] == num or i[1][0] == num:
                        
                        pass
                    else:
                        
                        new.append(i)
                
                
                self.arrows = new
                
                
                # REARANGE
                
                for n, i in enumerate(self.arrows):
                    
                    
                    
                    if i[0][0] > num:
                    
                        self.arrows[n][0][0] = i[0][0] - 1
                    
                    if i[1][0] > num:
                    
                        self.arrows[n][1][0] = i[1][0] - 1
            
        except:
            pass        
        
        
    
    def split(self, event, LETTER, END, PIXEL, scnIND):    
        
        
        pos, size, Y, name, story = self.events[event]
        
        
        if END:
            first = [pos, PIXEL-pos, Y, name, story[:LETTER[1]]]
            last  = [PIXEL, size-(PIXEL-pos), Y, name+"_split", story[LETTER[1]:]]
        
        else:
            first = [pos, PIXEL-pos, Y, name, story[:LETTER[0]]]
            last  = [PIXEL, size-(PIXEL-pos), Y, name+"_split", story[LETTER[0]:]]
           
        
            
        
        
        
        
        
        
        # FIXING ALL THE ARROWS AS ALWAYS OMG WTF WHY
        
        oldDATA = self.get_scenes_data() #SAVE OLD LOCATIONS OF THINGS
        
        # ASSIGNING THE SHIT
        self.events[event] = first
        self.events.insert(event+1, last)
        
        
        newDATA = self.get_scenes_data() #GETTING NEW LOCATIONS
        
        #CLEARING THE newDATA and oldDATA
        
        old = []
        
        for e in oldDATA:   # for all events in the data
            for s in e: # for all the scenes in the event
                old.append([s[0],s[1]])
        
        new = []
        
        for e in newDATA:   # for all events in the data
            for s in e: # for all the scenes in the event
                new.append([s[0],s[1]])
        
        
        # GETTING THE SCNAGES ONTO THE ARROWS
        
        for AN, arrow in enumerate(self.arrows):
            
            for SN, side in enumerate(arrow):
                
                for DN, data in enumerate(old):
                    
                    if data == side:    
                        
                        self.arrows[AN][SN] = new[DN] 
                    
        
        
            
            
        
        
    
    def save(self, px, py, sx, sy):
        
        savefile = open(self.filename, "w")
        
        savefile.write("<camera>"+str(px)+","+str(py)+","+str(sx)+","+str(sy)+"</camera>\n")
        
        #EVENTS
        for event in self.events:   
        
            savefile.write('<event>\n"'+str(event[3])+'"\n['+str(event[0])+","+str(event[1])+","+str(event[2])+"]\n"+str(event[4])+"\n</event>\n\n")
        
        #ARROWS
        
        for arrow in self.arrows:
            
            savefile.write('<arrow>'+str(arrow[0][0])+',"'+str(arrow[0][1])+'" --> '+str(arrow[1][0])+',"'+str(arrow[1][1])+'"</arrow>\n')
        
        
        for marker in self.markers:
            savefile.write('<marker>'+str(marker[0])+',"'+str(marker[1])+'"</marker>\n')
        
        for image in self.images:
            
            imX, imY, mode, url, thumb, pixthumb = image
            savefile.write('<image>'+str(imX)+','+str(imY)+',"'+str(mode)+'","'+str(url)+'","'+str(thumb)+'"</image>\n')
                        
            
        savefile.close()
        
        
        
        
        
        return


def get_shots(story, scenename):
    
    
    LIST = []
    
    if "<shot>" in story and "</shot>" in story:
        
        sa = story.count("<shot>")
        
        ts = story
        
        for i in range(sa):
            
            LIST.append( [False, ts[:ts.find("<shot>")], False, False] )   #[scenename, "TEXT", pixbuf, blends]
    
    
            ts = ts[ts.find("<shot>")+6:]
            
            if ts.count('"') > 1:
                shotname = "rnd/"+scenename+"/"+ts[ts.find('"')+1:ts.replace('"', " ", 1).find('"')]
                
            else:
                shotname = "Unnamed"
                
            LIST.append( [shotname.replace(" ", "_"), ts[:ts.find("</shot>")], False, False] )
            ts = ts[ts.find("</shot>")+7:]
            
    
        LIST.append( [False, ts, False, False] )
    else:
        
        LIST.append( [False, story, False, False] )
    
    
    
    return LIST
    
    
    
def get_scenes_percentage(FILE):
    
    
    arrows = FILE.arrows
    scnDATA =  FILE.get_scenes_data()
    
    #trying to get whether the start actually connects to end
    linkchained = False
    
    linkchainpath = []
    
    startlink = False
    
    for i in FILE.arrows:
        
        if i[0][0] == -1:
            
            linkchainpath.append(i)
            startlink = True
            
            
    while startlink: # dangerous motherfucker
        
        found = False
        
        for i in FILE.arrows:
            
            
            
            if linkchainpath[-1][1] == i[0]:
                
                
                
                found = True
                linkchainpath.append(i)
                
                if i[1][0] == -1:
                    linkchained = True
                    break
            
        if found == False:
            break
    
    
    
    
    persantage = 1.0
    valueslist = []
    
    for event in scnDATA:
        for scene in event:
            LIST = []
            
            
            story = scene[3]
            scenename = scene[1]
            
            links = []
            for n in linkchainpath: 
                links.append(n[1])
            
            if [scene[0], scene[1]] in links:
            
                scenevalues = []
    
                if "<shot>" in story and "</shot>" in story:
                    
                    sa = story.count("<shot>")
                    
                    ts = story
                    
                    for i in range(sa):
                        
                        #LIST.append( [False, ts[:ts.find("<shot>")], False, False] )   #[scenename, "TEXT", pixbuf, blends]
                
                
                        ts = ts[ts.find("<shot>")+6:]
                        
                        if ts.count('"') > 1:
                            shotname = "rnd/"+scenename+"/"+ts[ts.find('"')+1:ts.replace('"', " ", 1).find('"')]
                            
                        else:
                            shotname = "Unnamed"
                            
                        LIST.append( [shotname.replace(" ", "_"), ts[:ts.find("</shot>")], False, False] )
                        ts = ts[ts.find("</shot>")+7:]
                        
                
                    #LIST.append( [False, ts, False, False] )
        
                if LIST == []:
                    
                    
                    
                    
                    scenevalues.append(0)
                
                
                for i in LIST:
                    
                    try:
                    
                        if len(os.listdir(i[0]+"/rendered")) > 0:
                            scenevalues.append(1.0)
                        
                        elif len(os.listdir(i[0]+"/test_rnd")) > 0:
                            scenevalues.append(0.8) 
                        
                        elif len(os.listdir(i[0]+"/opengl")) > 0:
                            scenevalues.append(0.6) 
                            
                        elif len(os.listdir(i[0]+"/storyboard")) > 0:
                            scenevalues.append(0.4)
                        
                        elif len(os.listdir(i[0]+"/extra")) > 0:
                            scenevalues.append(0.2) 
                    except:
                        scenevalues.append(0.0) 
                     
                try:
                    scenevalue = float(sum(scenevalues))/len(scenevalues)
                except:
                    scenevalue = 0.0
                valueslist.append(scenevalue)
                     
    try:
        persantage = float(sum(valueslist))/len(valueslist)
    except:
        persantage = 0.0
    return persantage
    
    
    
    
    
    
    
    
    
    
    
    
        
    
    
    
    
