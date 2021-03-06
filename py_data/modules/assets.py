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
import dialogs
import fileformats
import linkconfig
import history
import oscalls
import imageselector
import story_editor

from subprocess import *

#### AN ASSET IS AN OBJECT THAT WILL HOLD INFORMATION ABOUT A PARTICULAR ASSET
#    IN THE PROJECT
#    IT'S PERSENTAGE, NAME, PREVIEW PIC, etc....
class asset:
    def __init__(self, pf, path, CUR, name):
        
        self.pf = pf
        self.path = path
        self.name = name
        self.CUR = CUR
        
        self.IsNowProcessing = False
        #making sure all NESSESARY FOLDERS ARE IN THE DIRECTIORY
        
        # tex, reference, renders
        
        try:
            os.mkdir(path+"/tex") 
            os.mkdir(path+"/renders")
            os.mkdir(path+"/reference")
        
        except:
            pass
        
        # now the nessesary files
        # blend, asset.progress
        
        # asset.progress
        if os.path.exists(path+"/asset.progress") == False:
            
            try:
                o = open("py_data/new_file/"+CUR+".progress", "r")
            except:
                o = open("py_data/new_file/asset.progress", "r")
            w = open(path+"/asset.progress", "w")
            w.write(o.read())
            w.close()
        # blend file
        if os.path.exists(path+"/"+name+".blend") == False:
            o = open("py_data/new_file/empty.blend", "r")
            w = open(path+"/"+name+".blend", "w")
            w.write(o.read())
            w.close()
            
            #WRITTING TO HYSTORY
            history.write(self.pf , path+"/"+name+".blend", "[Added]")
        
        
        
        ###### READING DATA  #####
        
        
        
        
        # checking if the item is finished...
        # looking into the ast folder instead of dev
        
        
        self.done = self.name+".blend" in os.walk(self.pf+"/ast/"+CUR).next()[2]
        
            
        # getting the persentage from the checklist
        
        self.percent = checklist.partcalculate(checklist.openckecklist(path+"/asset.progress"))
        
        #if self.done:
        #    self.percent = 1.0 # just making sure
            
        self.preview = "NO PIXBUF"
        self.pic = "NO PIXBUF"
        # getting the icon
        
        #if os.path.exists(self.path+"/renders/Preview.png"):
        #    self.pic = thumbnailer.thumbnail(self.path+"/renders/Preview.png", 182, 124)
        #    self.pic = gtk.gdk.pixbuf_new_from_file(self.pic)
        #    self.preview = thumbnailer.thumbnail(self.path+"/renders/Preview.png", 400, 400)
        #    self.preview = gtk.gdk.pixbuf_new_from_file(self.preview)
        # 
        #elif os.path.exists(self.path+"/renders/Preview.jpg"):
        # 
        #    self.pic = thumbnailer.thumbnail(self.path+"/renders/Preview.jpg", 182, 124)
        #    self.pic = gtk.gdk.pixbuf_new_from_file(self.pic)
        #    self.preview = thumbnailer.thumbnail(self.path+"/renders/Preview.jpg", 400, 400)
        #    self.preview = gtk.gdk.pixbuf_new_from_file(self.preview)
        #
        #
        #
        #else:
        #self.pic = self.pf+"/py_data/icons/"+CUR+"_prev.png"
        #self.pic = gtk.gdk.pixbuf_new_from_file(self.pic)
        
        #self.preview = self.pic
        
        
        # getting the asset /ast/ if it's finished
        
        if self.done:
            astpath = self.pf+"/ast/"+self.CUR+"/"+self.name+".blend"
            
            self.ast = ["NO PIXBUF", astpath]
            
            
            #
            #try:
            #    astpic = thumbnailer.blenderthumb(astpath, 100, 100)
            #    astpic = gtk.gdk.pixbuf_new_from_file(astpic)
            #    
            #except:
            #    astpic = self.pf+"/py_data/icons/blendfile_big.png"
            #    astpic = gtk.gdk.pixbuf_new_from_file(astpic)
            #
            #self.ast = [astpic, astpath]
        else:
            self.ast = [None, None]
        
        
        
    def info(self):
        
        return {
                "PATH:": self.path,
                "NAME:": self.name ,
                "DIRE:": self.CUR,
                "DONE:": self.done,
                "PERS:": self.percent
                }
    

####   ACTUALL DRAWING OF THE DIALOG ( WITH DRAWABLE BECAUSE WHY NOT )
class draw_assets:
    
    def __init__(self, pf, box, win, CUR, Goto=None, mainbox=False):
    
        self.pf = pf # pf stands for project folder. It's a string to know
                     # where the project's folders start with
        
        self.box = box # the gtk.Box() container to put this widget into
        self.mainbox = mainbox
        
        self.win = win
        self.CUR = CUR
        
        self.assets = []
        
        self.itemscenedata = []
        
        
        ## THIS IS WHERE THE READING OF THE FOLDER HAPPENDS
        
        self.folder_read()
        
        self.makesuretooutputhatyouareinafuckingassetsmotherfucker = True
            
        
        self.IsNowProcessing = False
        self.IsNowProcessingBlends = False
        
        
        # PREPARATION TO DRAW
        
        self.Goto = Goto   # THIS IS THE ITEM NAME IF YOU WANT TO LINK IT FROM SOME OTHER PLACE
        self.screen = "selection"
        self.allowed = True
        
        self.scroll = 0
        #in item scrolls
        self.iscroll = [0,0,0,0]
        self.blscroll = 0
        
        self.dW = 0
        self.DH = 0
        
        self.mpx = 0
        self.mpy = 0
        self.mpf = None
        
        self.newitem = None # Placeholder for a name of the new item if such created
        self.justadded = False
        
        
        # ICONS
        self.donepic = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/"+CUR+"_asset_done.png")
        self.plus_big = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/plus_big.png")
        self.undonepic = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/"+CUR+"_asset_undone.png")
        self.rendericon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/pic.png")
        self.foldericon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/folder.png")
        self.checklisticon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/checklist.png")
        self.editicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/edit.png")
        self.blendericon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/blender.png")
        self.blendfileicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/blendfile_big.png")
        self.okicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/ok.png")
        self.vidicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/vid.png")
        self.settingsicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/settings.png")
        self.scn_asset_undone = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/scn_asset_undone.png")
        
        
        self.refresh = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/refresh.png")
        self.plusicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/plus.png")
        self.fade_01 = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/INT/fade_01.png")
        self.fade_02 = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/INT/fade_02.png")
        self.fade_03 = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/INT/fade_03.png")
        self.fade_04 = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/INT/fade_04.png")
        
        self.iteminfo = None
        self.blends = None
        
        def framegraph(widget, event):
                                                    
            w, h = widget.window.get_size()
            xgc = widget.window.new_gc()
            
            mx, my, fx  = widget.window.get_pointer()
            
            
            # GETTING WHETHER THE WINDOW IS ACTIVE
            
            self.winactive = win.is_active()
            

                
            
            
            
            ctx = widget.window.cairo_create()
            #ctx.select_font_face("Sawasdee", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            ctx.set_source_rgb(1,1,1)
            
            xgc.line_width = 2
            
            # BACKGROUND COLOR
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#2b2b2b")) ## CHOSE COLOR
            widget.window.draw_rectangle(xgc, True, 0, 0, w, h)  ## FILL FRAME    
            
            
            inthescreen = False
            if my > 50:
                inthescreen = True
            
            
            
            
            mouseoverany = False
            
            #### SELECTION ITEM SCREEN
            if self.screen == "selection":
                
                #widget.set_size_request(500,500)
                
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
                
                
                
                
                
                
                
                # SELECTABLE CELLLS
                
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#9F8b78"))
                if "GDK_BUTTON1" in str(fx) and self.allowed and "GDK_BUTTON1" not in str(self.mpf) and win.is_active():
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#555"))
                
                
                #widget.window.draw_rectangle(xgc, True, mx/200*200, (my+self.scroll)/200*200-self.scroll, 200, 200)
                
            
                try:
                    avarage = self.assets[0].percent
                except:
                    avarage = 1.0
                
                
                ### CELLS
                
                
                
                xc = 0
                yc = 0
                
                
                ############# CELLS DRAING  ##################
                
                
                for x, i in enumerate(self.assets):
                    
                    if self.Goto == i.name:
                        self.blends = self.loadBlendFiles(i)
                        self.iteminfo = self.loaditem(i)
                        self.screen = i
                        
                        break
                        
                    nx = xc*200
                    ny = yc*200-self.scroll+50
                    
                    
                    # NEW ITEM ( in case it was just created )
                    
                    if i.name == self.newitem:
                        
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#aaa"))
                        widget.window.draw_rectangle(xgc, True, nx, ny, 200, 200)
                    
                        #adjust the scroll
                        
                        
                        if self.justadded:
                            self.scroll = ny*200
                            self.justadded = False
                        
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#464646")) 
                    #widget.window.draw_rectangle(xgc, True, nx+10, ny+5, 180, 195) 
                    
                    ctx3 = widget.window.cairo_create()
                    ctx3.set_source_rgba(0,0,0,0.4)
                    ctx3.rectangle(nx+10, ny+5, 180, 195)
                    ctx3.fill()
                     
                    ### MOUSE OVER
                    
                    mouseover = False
                    if mx > nx and mx < nx+200 and my > ny and my < ny+200 and inthescreen:
                        
                        
                        mouseover = True
                        mouseoverany = True
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#395384"))
                        
                        ## MOUSE PRESSED
                        
                        if "GDK_BUTTON1" in str(fx) and self.allowed and "GDK_BUTTON1" not in str(self.mpf) and win.is_active() and inthescreen:
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#000"))
                            
                            
                            widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
                            
                            
                
                            while gtk.events_pending():
                                gtk.main_iteration()
                            
                            self.blends = self.loadBlendFiles(i)
                            self.iteminfo = self.loaditem(i)
                            self.screen = i
                            
                        widget.window.draw_rectangle(xgc, True, nx+10, ny+5, 180, 195)
                        
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#4c4c4c"))
                        
                        
                        
                        xgc.line_width = 4
                        #widget.window.draw_rectangle(xgc, False, nx, ny, 200, 200)
                        xgc.line_width = 2
                    
                       
                        
                    
                    # top line
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#6e5daf"))
                    widget.window.draw_rectangle(xgc, True, nx+10, ny+5, 180, 20)
                    
                    
                    
                    
                    # little icon
                    # nod to the original design
                    self.donepic
                    
                    #if i.done:
                    #    widget.window.draw_pixbuf(None, self.donepic, 0, 0, nx+12, ny+4, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
                    #else:
                    widget.window.draw_pixbuf(None, self.undonepic, 0, 0, nx+12, ny+4, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)     
                            
                    # name
                    
                    
                    
                    ctx.set_font_size(15)
                    ctx.move_to( nx+35, ny+20)
                    ctx.show_text(i.name[:15])
                    #ctx.move_to( nx+33, ny+40)
                    #ctx.show_text(i.name[15:])
                    
                    
                    # preview draw
                    if i.pic != "NO PIXBUF":
                        yoffset = (100-i.pic.get_height())/2 # get_width
                        xoffset = (100-i.pic.get_width())/2
                        
                        
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#727272"))
                        #widget.window.draw_rectangle(xgc, True, nx+50, ny+50, 100, 100)
                        
                        
                        widget.window.draw_pixbuf(None, i.pic, 0, 0, nx+50+xoffset, ny+50+yoffset, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
                    else:
                        if not self.IsNowProcessing:
                            
                            self.IsNowProcessing = True
                            def ee(x):
                                it = self.assets[x]
                                if os.path.exists(it.path+"/renders/Preview.png"):
                                    it.pic = thumbnailer.thumbnail(it.path+"/renders/Preview.png", 182, 124)
                                    it.pic = gtk.gdk.pixbuf_new_from_file(it.pic)
                                    #it.preview = thumbnailer.thumbnail(it.path+"/renders/Preview.png", 400, 400)
                                    #it.preview = gtk.gdk.pixbuf_new_from_file(it.preview)
                                 
                                elif os.path.exists(it.path+"/renders/Preview.jpg"):
                                 
                                    it.pic = thumbnailer.thumbnail(it.path+"/renders/Preview.jpg", 182, 124)
                                    it.pic = gtk.gdk.pixbuf_new_from_file(it.pic)
                                    #it.preview = thumbnailer.thumbnail(it.path+"/renders/Preview.jpg", 400, 400)
                                    #it.preview = gtk.gdk.pixbuf_new_from_file(it.preview)
                                else:
                                    it.pic = it.pf+"/py_data/icons/"+CUR+"_prev.png"
                                    it.pic = gtk.gdk.pixbuf_new_from_file(it.pic)
                                
                                self.IsNowProcessing = False
                            glib.timeout_add(10, ee, x)
                    # percentage widget
                    
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#d0d0d0"))
                    
                    widget.window.draw_rectangle(xgc, True, nx+10, ny+180, 180, 10)
                    
                    avarage = (avarage + i.percent)/2
                    
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
                    #if mouseover:
                    #    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#4c4c4c"))
                    widget.window.draw_rectangle(xgc, True, nx+10, ny+180, int(180*i.percent), 10)
                    
                    ctx.set_font_size(10)
                    ctx.move_to( nx+10, ny+175)
                    ctx.show_text(str(int(i.percent*100))+" %")
                     
                    
                        
                    
                    ### SAVING TO THE NEXT ONE
                    if i != self.assets[-1]:
                    
                        if xc + 1 > w/200-1:
                            xc = 0
                            yc = yc + 1
                        else:
                            xc = xc + 1
                    
                        
                
                 
                
                
                
                    
                ### SCROOL ###
                
                # the scroll is done with the middle mouse button
                if self.mpy > my and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf):
                    
                    self.scroll = self.scroll + (self.mpy-my)
                
                if self.mpy < my and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf):
                    
                    self.scroll = self.scroll - (my-self.mpy)
               
                
                
                
                
                
                
                pixtdall = (yc+1)*200-h+50
                
                if self.scroll > pixtdall:
                    self.scroll = pixtdall
                
                if self.scroll < 0:
                    self.scroll = 0
                
                
                ## top pannel
                try:
                    x = []
                    for i in self.assets:
                        x.append(i.percent)

                    avarage = sum(x)/len(x)
                except:
                    avarage = 1.0 #CHANGE THIS VALUE WHEN YOU FIGURE OUT THE CALCULATION WITHOUT CATEGORIES
                
                
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#393939")) ## CHOSE COLOR
                widget.window.draw_rectangle(xgc, True, 0, 0, w, 50)
                     
                
                # BIG PERCENTAGE BAR FOR THE ENTIRE CATEGORY
                ctx.set_font_size(20)
                ctx.move_to( 100, 30)
                ctx.show_text(str(int(avarage*100))+" %")
                
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#d0d0d0")) ## CHOSE COLOR
                widget.window.draw_rectangle(xgc, True, 200, 5, w-210, 40)
                
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
                
                widget.window.draw_rectangle(xgc, True, 200, 5, int((w-210)*avarage), 40)
                
                
                
                #### ADD BUTTON
                
                plus = [(20,10),(20,20),(10,20),(10,30),(20,30),(20,40),(30,40),(30,30),(40,30),(40,20),(30,20),(30,10)]
                
                if mx > 10 and my > 10 and mx < 40 and my < 40:
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
                    if "GDK_BUTTON1" in str(fx) and self.allowed and "GDK_BUTTON1" not in str(self.mpf) and win.is_active():
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#000"))
                        
                        
                        # just incase all freezes
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#3c3c3c"))    
                        xgc.line_width = 2
                        widget.window.draw_polygon(xgc, False, plus)
                        
                        # RUNNING THE DIALOG
                        
                        glib.timeout_add(20, self.call_add_dialog)
                        
                        
                    
                    #widget.window.draw_polygon(xgc, True, plus)
                    widget.window.draw_rectangle(xgc, True, 10, 5, 40, 40)
                    
                    # TOOLTIP
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#1c1c1c"))   
                    widget.window.draw_rectangle(xgc, True, mx+20, my+5, 200, 20)
                    ctx.set_font_size(15)
                    ctx.move_to( mx+30, my+20)
                    ctx.show_text("ADD NEW ITEM")
                    
                    
                    
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#3c3c3c"))    
                xgc.line_width = 2
                #widget.window.draw_polygon(xgc, False, plus)
                widget.window.draw_pixbuf(None, self.plus_big, 0, 0, 10, 5, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                
                
                
                
                
                
                
                ## scroller
                
                pixtdall = (yc+1)*200
                
                
                scs = int ( 70+ (float((h-70))/pixtdall*(self.scroll ) ) )   # IF YOU TOUCH THAT CODE I GONNA FUCK YOU AND YOUR FAMILY
                scf = int ( (float((h-70))/pixtdall*(    h-50 ) )) + scs -20 # DON'T EVEN FUCKING DARE... THIS WAS A NIGHTMARE
                
                if scf < h-19: 
                    
                
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#727272")) 
                    widget.window.draw_line(xgc, w-20, 70, w-20, h-20)  ### SCROLL LINE
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#000"))
                    widget.window.draw_line(xgc, w-20, scs, w-20, scf)  ### SCROLLER
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            ###### IF ITEM SELSECTED
            
            
            
            
            else: # to the if self.screen = "select"
                
                ctx.set_source_rgb(1,1,1)
                #widget.set_size_request(500,900)
                
                if self.screen.preview != "NO PIXBUF":
                    
                    mmx = self.screen.preview.get_width()
                    mmy = self.screen.preview.get_height()
                    
                    if mmy < 120:
                        mmy = 120
                else:
                    mmx = 120
                    mmy = 120
                
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
                
                
                
                
                
                
                
                ##### IMAGES IN THE renders, tex, reference FOLDERS ####
                
                
                
                
                
                
                # I GONNA REORDER THEM BECAUSE AHHH
                #rawnames = ["Renders", "Textures", "References"]
                #rawdirs = ["renders", "tex","reference"]
                
                rawnames = ["References", "Textures", "Renders"]
                rawdirs = ["reference", "tex","renders"]
                
                        
                
                
                #basic math to get the sizes of stuff
                
                raws = 4#len(self.iteminfo) #how much raws
                                          # so far it's like 3
                                          # look def loaditem():
                
                
                margin = 10 # space between raws
                
                raw_true_w = (w / raws)
                raw_w = (w / raws) - (margin * 2) # getting the width of the raw
                
                raw_start = mmy + 180 # starting height
                raw_h = h - raw_start # height
                
                
                for raw, data in enumerate(self.iteminfo):  # stating the loop of 3 raws
                    
                    # a little more math
                    the_raw_w_start = raw_true_w*raw+10
                    
                    
                    #an attemt to bring Tetures and references up a little
                    if raw != 0 and (mmx+80) < the_raw_w_start:
                        raw_start = 105 + 140
                        raw_h = h - raw_start
                    
                    
                    
                    
                    
                    
                    # raws frames
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#222222")) ## CHOSE COLOR
                    #widget.window.draw_rectangle(xgc, True, the_raw_w_start , raw_start, raw_w, raw_h)
                    
                    ctx3 = widget.window.cairo_create()
                    ctx3.set_source_rgba(0,0,0,0.4)
                    ctx3.rectangle(the_raw_w_start, raw_start,raw_w, raw_h)
                    ctx3.fill()
                    
                    
                    
                    
                    ## IMAGES ##
                    
                    ix = 0
                    iy = 0
                    
                    
                    mouseinraw = False
                    if my in range( raw_start, h ) and mx in range( the_raw_w_start, the_raw_w_start+raw_w  ):
                        mouseinraw = True   
                        
                    
                    
                    for ind, render in enumerate(data): # look to the previous indentantion
                                                        # for the data reference
                        
                        
                        
                        center_X = 50
                        center_Y = 50
                        
                        mox = ix*100 + the_raw_w_start + ix*10 + 10 
                        moy = iy*130 + raw_start + iy*10       + 10 + self.iscroll[raw] +10
                       
                        if not self.IsNowProcessing and render[0] == "NO PIXBUF" and moy in range(raw_start-20, h):
                            self.IsNowProcessing = True
                            def ee(ind, raw, FILE):
                                
                                

                                    
                                pic = "NO PIXBUF"
                                for f in fileformats.images:
                    
                    
                    
                                    if FILE.endswith(f):
                                        
                                        #try making a thubnail
                                        
                                        
                                        try:
                                            pic = thumbnailer.thumbnail(FILE, 100, 100)
                                            pic = gtk.gdk.pixbuf_new_from_file(pic)
                                        except:
                                            pic = self.pf+"/py_data/icons/pic_big.png"
                                            pic = gtk.gdk.pixbuf_new_from_file(pic)
                                            
                                        self.iteminfo[raw][ind][0] = pic
                                                  
                                for f in fileformats.videos:
                                    
                                    
                                    
                                    if FILE.endswith(f):
                                        
                                        #try making a thubnail
                                        
                                        
                                        try:
                                            pic = thumbnailer.videothumb(FILE, 100)
                                            pic = gtk.gdk.pixbuf_new_from_file(pic)
                                        except:
                                            pic = self.pf+"/py_data/icons/pic_big.png"
                                            pic = gtk.gdk.pixbuf_new_from_file(pic)
                                            
                                        self.iteminfo[raw][ind][0] = pic 
                                   
                                self.IsNowProcessing = False
                            glib.timeout_add(10, ee, ind, raw, render[1])
                            
                            
                        
                        if render[0] != "NO PIXBUF":
                            
                            
                            ### MATH ###
                            
                            
                            center_X = (100-render[0].get_width())/2
                            center_Y = (100-render[0].get_height())/2 # GETTING THE PICTURE TO THE CENTER IN RELATION TO It'S SIZE
                            
                        
                            
                        
                        
                        
                        imx = mox   + center_X
                        imy = moy   + center_Y
                            
                        if moy in range(raw_start-20, h):
                        
                        
                            mouseover = False
                            
                            #### MOUSE OVER ####
                            
                            if mx > mox and mx < mox+100 and my > moy and my < moy+100 and mouseinraw:
                                mouseover = True
                                mouseoverany = True
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#395384"))
                                
                                
                                widget.window.draw_rectangle(xgc, True, mox-2, moy, 104, 122)
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#4c4c4c"))
                                
                                
                                
                                xgc.line_width = 4
                                #widget.window.draw_rectangle(xgc, False, mox-5, moy-5, 110, 110)
                                xgc.line_width = 2
                                
                                # IF CLICKED
                                if "GDK_BUTTON1" in str(fx) and self.allowed and "GDK_BUTTON1" not in str(self.mpf) and win.is_active():
                                    
                                    oscalls.Open(render[1])
                            
                            
                            
                            
                            ### DRAWING
                            
                            if not mouseover:
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#464646"))
                                #widget.window.draw_rectangle(xgc, True, mox-2, moy, 104, 122)
                                
                                ctx3 = widget.window.cairo_create()
                                ctx3.set_source_rgba(0,0,0,0.4)
                                ctx3.rectangle(mox-2, moy, 104, 122)
                                ctx3.fill()
                            
                            
                            
                            
                            
                            if render[1][render[1].rfind(".")+1:] in fileformats.images:
                                
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#8a7d2c"))
                                widget.window.draw_rectangle(xgc, True, mox-2, moy, 104, 22)
                                widget.window.draw_pixbuf(None, self.rendericon, 0, 0, mox-2, moy, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                                
                            elif render[1][render[1].rfind(".")+1:] in fileformats.videos: #4987af
                                
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#4987af"))
                                widget.window.draw_rectangle(xgc, True, mox-2, moy, 104, 22)
                                widget.window.draw_pixbuf(None, self.vidicon, 0, 0, mox-2, moy, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                            
                            if render[0] != "NO PIXBUF":
                                widget.window.draw_pixbuf(None, render[0], 0, 0, imx, imy+22, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                            
                            # text ( the picture filename )
                            
                            ctx.set_font_size(10)
                            
                            #if mouseover:
                            #    ctx.set_font_size(20)
                            
                            ctx.move_to( mox+22, moy+12)
                            ctx.show_text(render[2][:12])
                            
                            
                        # TO THE NEXT FRAME
                        ix = ix + 1
                        if (ix * 100 + ix*10) > raw_w-120:
                            iy = iy + 1
                            ix = 0
                    
                    
                    
                    ### SCROLL ###
                        
                    if mouseinraw:
                        
                        if self.mpy > my and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf):
                            
                            
                            self.iscroll[raw] = self.iscroll[raw] + (my-self.mpy)
                        
                        if self.mpy < my and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf):
                            
                            self.iscroll[raw] = self.iscroll[raw] - (self.mpy-my) 
                        
                        
                    Yinpix = raw_h+(iy*130 + iy*10)*-1-200
                        
                    if self.iscroll[raw] < Yinpix:
                        self.iscroll[raw] = Yinpix
                        
                    if self.iscroll[raw] > 0:
                        self.iscroll[raw] = 0
                    
                    
                    
                    ## scrolled indicator ###
                    
                    # fade 03
                    
                    #if self.iscroll[raw] < 0:
                    #    widget.window.draw_pixbuf(None, self.fade_03, 0, 0, the_raw_w_start, raw_start, raw_w, 40, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                    #
                    #if (iy*100 + iy*10)+130 > raw_h and Yinpix != self.iscroll[raw]:
                    #    widget.window.draw_pixbuf(None, self.fade_04, 0, 0, the_raw_w_start, h-40, raw_w, 40, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                    
                    
                    
                    
                    
                    
                    
                    
                    # CLEANING #
                    
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#2b2b2b")) ## CHOSE COLOR
                    #widget.window.draw_rectangle(xgc, True, raw_true_w*raw, 50, raw_true_w, raw_start-50)
                    
                    ## tab thingy
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#222222")) ## CHOSE COLOR
                    widget.window.draw_rectangle(xgc, True, the_raw_w_start , raw_start-30, raw_w, 30)
                    
                    
                    # tab icons
                    
                    #widget.window.draw_pixbuf(None, self.rendericon, 0, 0, the_raw_w_start+5, raw_start-28, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                    
                    
                    # teb name
                    
                    ctx.set_font_size(15)
                    ctx.set_source_rgb(1,1,1)
                    ctx.move_to( the_raw_w_start+14+30, raw_start-10)
                    ctx.show_text(rawnames[raw])
                
                
                    # foldrer button
                    
                    icon_x = the_raw_w_start+2
                    icon_y = raw_start-28
                    icon_s = 22
                    
                    
                    ### MOUSE OVER
                    if mx > icon_x and mx < icon_x+icon_s and my > icon_y and my < icon_y+icon_s:
                        
                        mouseoverany = True
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
                        widget.window.draw_rectangle(xgc, True, icon_x, icon_y, icon_s, icon_s)
                        
                        
                        
                        
                        # IF CLICKED
                        if "GDK_BUTTON1" in str(fx) and self.allowed and "GDK_BUTTON1" not in str(self.mpf) and win.is_active():
                            
                            oscalls.Open(self.pf+"/dev/"+self.CUR+"/"+self.screen.name+"/"+rawdirs[raw])
                        
                        
                        
                        
                     
                    widget.window.draw_pixbuf(None, self.foldericon, 0, 0, icon_x, icon_y, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                    
                    
                    # ADD IMAGES TO THE FOLDER
                    icon_x = the_raw_w_start+raw_w-30
                    icon_y = raw_start-28
                    icon_s = 22
                    
                    ### MOUSE OVER
                    if mx > icon_x and mx < icon_x+icon_s and my > icon_y and my < icon_y+icon_s:
                        
                        mouseoverany = True
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
                        widget.window.draw_rectangle(xgc, True, icon_x, icon_y, icon_s, icon_s)
                        
                        
                        
                        
                        # IF CLICKED
                        if "GDK_BUTTON1" in str(fx) and self.allowed and "GDK_BUTTON1" not in str(self.mpf) and win.is_active():
                            
                            def ee(raw):
                                frurl = imageselector.select(self.pf, "/dev/ "+rawdirs[raw])
                                
                                puturl = "/dev/"+self.CUR+"/"+self.screen.name+"/"+rawdirs[raw]+frurl[frurl.rfind("/"):]
                                
                                while os.path.exists(self.pf+puturl):
                                    puturl = puturl[:puturl.rfind(".")]+"_copy"+puturl[puturl.rfind("."):]
                                
                                fr = open(frurl, "r")
                                tr = open(self.pf+puturl, "w")
                                tr.write(fr.read())
                                tr.close()
                                
                                
                                self.blends = self.loadBlendFiles(self.screen)
                                self.iteminfo = self.loaditem(self.screen)
                                
                                self.screen.preview = thumbnailer.thumbnail(self.screen.path+"/renders/Preview.png", 400, 400)
                                self.screen.preview = gtk.gdk.pixbuf_new_from_file(self.screen.preview)
                                
                                
                            glib.timeout_add(10, ee, raw)
                        
                    
                    
                    widget.window.draw_pixbuf(None, self.plusicon, 0, 0, icon_x, icon_y, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                
                
                
                # SCENES LIST
                
                
                        
                
                if not self.itemscenedata:
                    
                    story = story_editor.bos("pln/main.bos")
                    story.load()
                    scnDATA = story.get_scenes_data()
                    
                    for scn in scnDATA:
                        
                        
                        
                        for sh in scn:
                            
                            
                            scnname = sh[1]
                            if "/dev/"+self.CUR+"/"+self.screen.name in sh[3]:
                                self.itemscenedata.append(scnname)
                
                
                
                
                raw = 3
                
                the_raw_w_start = raw_true_w*raw+10
                    
                    
                #an attemt to bring Tetures and references up a little
                if raw != 0 and (mmx+80) < the_raw_w_start:
                    raw_start = 105 + 140
                    raw_h = h - raw_start
                
                
                ctx3 = widget.window.cairo_create()
                ctx3.set_source_rgba(0,0,0,0.4)
                ctx3.rectangle(the_raw_w_start, raw_start,raw_w, raw_h)
                ctx3.fill()
                
                
                for n, scn in enumerate(self.itemscenedata):
                    
                    if raw_start+10+45*n+self.iscroll[raw] in range(raw_start, h):
                    
                    
                        ctx3.set_source_rgba(0.1,0.1,0.1,0.75)
                        ctx3.rectangle(the_raw_w_start, raw_start+10+45*n + self.iscroll[raw],  raw_w, 40)
                        ctx3.fill()
                    
                        
                        widget.window.draw_pixbuf(None, self.scn_asset_undone, 0, 0, the_raw_w_start+5, raw_start+17+45*n + self.iscroll[raw], -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                
                        ctx.set_font_size(15)
                        ctx.set_source_rgb(1,1,1)
                        ctx.move_to( the_raw_w_start+14+30, raw_start+20+15+45*n + self.iscroll[raw])
                        ctx.show_text(scn)
                        
                        if my in range(raw_start+10+45*n + self.iscroll[raw], raw_start+10+45*n + self.iscroll[raw]+40) and mx in range(the_raw_w_start, the_raw_w_start+raw_w):
                            
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#aaa")) ## CHOSE COLOR
                            widget.window.draw_rectangle(xgc, False,the_raw_w_start, raw_start+10+45*n + self.iscroll[raw],  raw_w, 40)
                            
                            mouseoverany = True
                            
                            # IF CLICKED
                            if "GDK_BUTTON1" in str(fx) and self.allowed and "GDK_BUTTON1" not in str(self.mpf) and win.is_active():
                                
                                
                                self.box.destroy()
                                self.box = gtk.VBox(False)
                                self.mainbox.pack_start(self.box, True)
                                
                                story_editor.story(os.getcwd(), self.box, self.win, self.mainbox, scene=scn)
                            
                            
                if my in range(raw_start, h) and mx in range(the_raw_w_start, the_raw_w_start+raw_w):
                
                
                    if self.mpy > my and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf):
                                
                                
                        self.iscroll[raw] = self.iscroll[raw] + (my-self.mpy)
                    
                    if self.mpy < my and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf):
                        
                        self.iscroll[raw] = self.iscroll[raw] - (self.mpy-my) 
                
                Yinpix = raw_h+(45*len(self.itemscenedata))*-1-20
                        
                if self.iscroll[raw] < Yinpix:
                    self.iscroll[raw] = Yinpix
                    
                if self.iscroll[raw] > 0:
                    self.iscroll[raw] = 0
                
                ## tab thingy
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#222222")) ## CHOSE COLOR
                widget.window.draw_rectangle(xgc, True, the_raw_w_start , raw_start-30, raw_w, 30)
                
                
                # tab icons
                
                widget.window.draw_pixbuf(None, self.scn_asset_undone, 0, 0, the_raw_w_start+5, raw_start-28, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                
                
                # teb name
                
                ctx.set_font_size(15)
                ctx.set_source_rgb(1,1,1)
                ctx.move_to( the_raw_w_start+14+30, raw_start-10)
                ctx.show_text("Scenes List")
                
                
                
                
                ######### BLEND FILES
                
                tmp_mmy = mmy # I'm Redesigning the UI and trying to bring the blendfiles up.
                mmy = 105 # comment this setting to see how low they were originally
                
                #xgc.set_rgb_fg_color(gtk.gdk.color_parse("#363636")) ## CHOSE COLOR
                #widget.window.draw_rectangle(xgc, True, mmx-15, mmy-45, w, 100)
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#222222")) ## CHOSE COLOR
                #widget.window.draw_rectangle(xgc, True, 0, mmy-15-30, w, 115+30)
                
                
                ctx3.set_source_rgba(0,0,0,0.4)
                ctx3.rectangle(mmx+110, mmy-15-30, w, 115+30)
                ctx3.fill()
                
                
                #blender icon
                #widget.window.draw_pixbuf(None, self.blendericon, 0, 0, mmx+105, mmy-41, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                
                
                #ctx.set_font_size(20)
                #ctx.set_source_rgb(1,1,1)
                #ctx.move_to( mmx+130, mmy-24)
                #ctx.show_text("Blender Files")
                
                
                
                
                #526969 undone blend color
                
                
                #### SCROLL OF BLEN FILES ####
                
                
                
                if my > mmy-12 and my < mmy-12+100 and mx > mmx + 117+110:
                    
                    if self.mpx > mx and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf):
                        
                        
                        self.blscroll = self.blscroll + (mx-self.mpx)
                    
                    if self.mpx < mx and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf):
                        
                        
                        self.blscroll = self.blscroll - (self.mpx-mx)
                
                if self.blscroll < (w-(mmx+117+110))+(len(self.blends)*110+60)*-1:
                        self.blscroll = (w-(mmx+117+110))+(len(self.blends)*110+60)*-1
                    
                if self.blscroll > 0:
                    self.blscroll = 0    
                
                
                
                
                for num, blend in enumerate(self.blends):
                
                    
                    if mmx + 115+110 +(num*110)+self.blscroll in range(mmx+117+100, w):
                    
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#526969"))
                        widget.window.draw_rectangle(xgc, True, mmx + 115+110 +(num*110)+self.blscroll, mmy-14-22, 104, 22)
                        
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#464646"))
                        #widget.window.draw_rectangle(xgc, True, mmx + 115+110 +(num*110)+self.blscroll, mmy-14, 104, 104)
                        
                        ctx3 = widget.window.cairo_create()
                        ctx3.set_source_rgba(0,0,0,0.4)
                        ctx3.rectangle(mmx + 115+110 +(num*110)+self.blscroll, mmy-14, 104, 104)
                        ctx3.fill()
                        
                        
                        
                        
                        ### MOUSE OVER
                        
                        if mx > mmx + 117+110 and mx > mmx + 117+110 +(num*110)+self.blscroll and mx < mmx + 117+110 +(num*110)+self.blscroll+100 and my > mmy-12 and my < mmy-12+100:
                            mouseoverany = True
                            
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#395384"))
                            widget.window.draw_rectangle(xgc, True, mmx + 115+110 +(num*110)+self.blscroll, mmy-14, 104, 104)
                            
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#4c4c4c"))
                            
                            xgc.line_width = 4
                            #widget.window.draw_rectangle(xgc, False, mmx + 115+110 +(num*110)+self.blscroll, mmy-14, 104, 104)
                            xgc.line_width = 2
                            
                            # IF CLICKED
                            if "GDK_BUTTON1" in str(fx) and self.allowed and "GDK_BUTTON1" not in str(self.mpf) and win.is_active():
                                
                                cblndr = ""
                                            
                                try:
                                    bv = open(self.pf+"/py_data/blenderver.data", "r")
                                    bv = bv.read().split("\n")
                                    
                                    
                                    
                                    if int(bv[0]) > 0:
                                        cblndr = bv[int(bv[0])]+"/"
                                except:
                                    pass
                                Popen([cblndr+"blender", blend[1]])
                                #os.system(cblndr+"blender "+blend[1])
                                
                                #WRITTING TO HYSTORY
                                history.write(self.pf ,blend[1], "[Openned]")
                                
                                
                        #BLEND PREVIEW 
                        if blend[0] != "NO PIXBUF":
                            widget.window.draw_pixbuf(None, blend[0], 0, 0, mmx + 117 +110 +(num*110)+self.blscroll, mmy-12, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                        
                        
                        if not self.IsNowProcessingBlends and blend[0] == "NO PIXBUF" :
                            self.IsNowProcessingBlends = True
                            def ee(num, FILE):
                                
                               
                                    
                                pic = "NO PIXBUF"
                                try:
                                    pic = thumbnailer.blenderthumb(FILE, 100, 100)
                                    pic = gtk.gdk.pixbuf_new_from_file(pic)
                                    
                                except:
                                    pic = self.pf+"/py_data/icons/pic_big.png"
                                    pic = gtk.gdk.pixbuf_new_from_file(pic)
                                
                                
                                self.blends[num][0] = pic
                                self.IsNowProcessingBlends = False
                                
                            glib.timeout_add(10, ee, num, blend[1])   
                        ctx.set_font_size(10)
                            
                        ctx.move_to(mmx + 117+110 +(num*110)+self.blscroll+22,mmy-12-22+12  )
                        ctx.show_text(blend[2][:15])
                        
                        #blender icon
                        widget.window.draw_pixbuf(None, self.blendericon, 0, 0, mmx + 117+110 +(num*110)+self.blscroll, mmy-12-24, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                    
                    
                
                
                
                
                #### AST BLEND FILE #####
                
                
                
                
                
                # little separator line if scrolled
                
                #if (w-(mmx+117+110)) < (len(self.blends)*110+60):
                #    widget.window.draw_pixbuf(None, self.fade_02, 0, 0, w-38 , mmy-12, -1, 111, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                
                #if self.blscroll < -10:
                    
                    
                    
                #    widget.window.draw_pixbuf(None, self.fade_01, 0, 0, mmx+217 , mmy-22, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                    
                
                if self.screen.done:
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#222222"))
                    #widget.window.draw_rectangle(xgc, True, mmx , mmy-12,217,110)
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#6e5daf"))
                    widget.window.draw_rectangle(xgc, True, mmx + 117-2, mmy-14-22, 104, 22)
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#464646"))
                    #widget.window.draw_rectangle(xgc, True, mmx + 117-2, mmy-14, 104, 104)
                    
                    ctx3 = widget.window.cairo_create()
                    ctx3.set_source_rgba(0,0,0,0.4)
                    ctx3.rectangle(mmx + 117-2, mmy-14, 104, 104)
                    ctx3.fill()
                    
                    
                    
                    if mx > mmx + 117 and mx < mmx + 117 + 100 and my > mmy-12 and my < mmy-12 + 100:
                        
                        mouseoverany = True
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#395384"))
                        widget.window.draw_rectangle(xgc, True, mmx + 117, mmy-12,100,100)
                    
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#4c4c4c"))
                    
                        xgc.line_width = 4
                        #widget.window.draw_rectangle(xgc, False, mmx + 117, mmy-12,100,100)
                        xgc.line_width = 2
                    
                        # IF CLICKED
                        if "GDK_BUTTON1" in str(fx) and self.allowed and "GDK_BUTTON1" not in str(self.mpf) and win.is_active():
                            cblndr = ""
                                        
                            try:
                                bv = open(self.pf+"/py_data/blenderver.data", "r")
                                bv = bv.read().split("\n")
                                
                                
                                
                                if int(bv[0]) > 0:
                                    cblndr = bv[int(bv[0])]+"/"
                            except:
                                pass
                            Popen([cblndr+"blender", self.screen.ast[1]])
                            #os.system(cblndr+"blender "+self.screen.ast[1])
                            
                            #WRITTING TO HYSTORY
                            history.write(self.pf ,self.screen.ast[1], "[Openned]")
                    
                    
                    if self.screen.ast[0] != "NO PIXBUF":
                        widget.window.draw_pixbuf(None, self.screen.ast[0], 0, 0, mmx + 117 , mmy-12, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                    else:
                        if not self.IsNowProcessingBlends:
                            self.IsNowProcessingBlends = True
                            def ee():
                                
                                FILE = self.screen.ast[1]
                                    
                                pic = "NO PIXBUF"
                                try:
                                    pic = thumbnailer.blenderthumb(FILE, 100, 100)
                                    pic = gtk.gdk.pixbuf_new_from_file(pic)
                                    
                                except:
                                    pic = self.pf+"/py_data/icons/pic_big.png"
                                    pic = gtk.gdk.pixbuf_new_from_file(pic)
                                
                                
                                self.screen.ast[0] = pic
                                self.IsNowProcessingBlends = False
                                
                            glib.timeout_add(10, ee)   
                    
                    ctx.set_font_size(10)
                        
                    ctx.move_to(mmx + 117+20,mmy-12-22+12  )
                    ctx.show_text(self.screen.name[:15])
                    
                    #blender icon
                    
                    widget.window.draw_pixbuf(None, self.blendericon, 0, 0, mmx + 117-2, mmy-12-24, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                
                
                
                    
                    
                    
                    # OK ICON
                    #widget.window.draw_pixbuf(None, self.okicon, 0, 0, mmx + 117 +85 , mmy-12-5, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                    
                    
                    
                else:
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#222222"))
                    #widget.window.draw_rectangle(xgc, True, mmx , mmy-12,217,110)
                    widget.window.draw_pixbuf(None, self.blendfileicon, 0, 0, mmx + 117 , mmy-12, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                    #widget.window.draw_rectangle(xgc, True, mmx + 117, mmy-12+75,100,25)
                    ctx.set_font_size(10)
                    ctx.move_to(mmx + 117+15, mmy-12+75+15  )
                    ctx.show_text("/ast/ Asset is")
                    ctx.move_to(mmx + 117+15, mmy-12+75+15 + 12 )
                    ctx.show_text("not yet finished.")
                        
                
                
                        
                        
                    
                    
                
                
                
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#2b2b2b")) ## CHOSE COLOR
                #widget.window.draw_rectangle(xgc, True, 0,50, mmx+100, mmy+50) 
                
                
                
                
                
                ### MAIN MENU  ####
                mmy = tmp_mmy + 22
                
                
                
                
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#363636"))
                #widget.window.draw_rectangle(xgc, True, 40, 60, mmx+50, mmy+20)
                
                
                ctx3 = widget.window.cairo_create()
                ctx3.set_source_rgba(0.2,0.2,0.2,0.8)
                ctx3.rectangle(40+mmx+18, 60, 24, mmy+20)
                ctx3.fill()
                
                ctx3 = widget.window.cairo_create()
                ctx3.set_source_rgba(0,0,0,0.4)
                ctx3.rectangle(40, 60, mmx+18, mmy+20)
                ctx3.fill()
                
                
                #folder
                
                #mouse over
                if mx in range(mmx+60, mmx+60+22) and my in range(65, 65+22):
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
                    widget.window.draw_rectangle(xgc, True, mmx+60, 65, 22, 22)
                
                    # TOOLTIP
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#1c1c1c"))   
                    widget.window.draw_rectangle(xgc, True, mx+20, my+5, 200, 20)
                    ctx.set_font_size(15)
                    ctx.set_source_rgb(1,1,1)
                    ctx.move_to( mx+30, my+20)
                    ctx.show_text("Open item's folder")
                    
                    # IF CLICKED
                    if "GDK_BUTTON1" in str(fx) and self.allowed and "GDK_BUTTON1" not in str(self.mpf) and win.is_active():
                        
                        oscalls.Open(self.screen.path)
                    
                    
                widget.window.draw_pixbuf(None, self.foldericon, 0, 0, mmx+60, 65, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                
                
                
                
                
                
                #checklist
                #mouse over
                if mx in range(mmx+60, mmx+60+22) and my in range(90, 90+22):
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
                    widget.window.draw_rectangle(xgc, True, mmx+60, 90, 22, 22)
                    
                    # TOOLTIP
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#1c1c1c"))   
                    widget.window.draw_rectangle(xgc, True, mx+20, my+5, 200, 20)
                    ctx.set_font_size(15)
                    ctx.set_source_rgb(1,1,1)
                    ctx.move_to( mx+30, my+20)
                    ctx.show_text("Item's checklist")
                    ctx.set_source_rgb(1,1,1)
                    
                    if "GDK_BUTTON1" in str(fx) and self.allowed and "GDK_BUTTON1" not in str(self.mpf) and win.is_active():
                        
                        checklist.checkwindow(pf=self.pf, title=self.screen.name, FILE=self.screen.path+"/asset.progress")
                    
                    
                widget.window.draw_pixbuf(None, self.checklisticon, 0, 0, mmx+60, 90, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                
                # ADD THE NEW BLEND FILE OPTION 
                
                if mx in range (mmx+60, mmx+60+20) and my in range (115, 110+20):
                    mouseoverany = True
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165")) ## CHOSE COLOR
                    widget.window.draw_rectangle(xgc, True, mmx+60, 115, 20, 20)
                    
                    # TOOLTIP
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#1c1c1c"))   
                    widget.window.draw_rectangle(xgc, True, mx+20, my+5, 200, 20)
                    ctx.set_font_size(15)
                    ctx.set_source_rgb(1,1,1)
                    ctx.move_to( mx+30, my+20)
                    ctx.show_text("Add another .blend file")
                    
                    
                    # IF CLICKED
                    if "GDK_BUTTON1" in str(fx) and self.allowed and "GDK_BUTTON1" not in str(self.mpf) and win.is_active():
                        
                        def ee():
                                    
                            Pname = ""
                            Pname = dialogs.PickName("New_File.blend")
                        
                            if Pname != "":
                                
                                if Pname.endswith(".blend") == False:
                                    Pname = Pname + ".blend"
                                
                                if Pname not in os.listdir(self.screen.path):
                                    
                                    fr = open(self.pf+"/py_data/new_file/empty.blend", "r")
                                    to = open(self.screen.path+"/"+str(Pname), "w")
                                    to.write(fr.read())
                                    to.close()
                                    self.blends = self.loadBlendFiles(self.screen)
                                    
                                    #WRITTING TO HYSTORY
                                    history.write(self.pf , self.screen.path+"/"+str(Pname), "[Added]")
                                    
                        glib.timeout_add(10, ee) 
                        
                    
                widget.window.draw_pixbuf(None, self.plusicon, 0, 0, mmx+60, 115, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                
                
                
                # CONFIGURE ASSET
                
                if mx in range (mmx+60, mmx+60+20) and my in range (115+22, 110+20+22):
                    mouseoverany = True
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165")) ## CHOSE COLOR
                    widget.window.draw_rectangle(xgc, True, mmx+60, 115+22, 20, 20)
                    
                    # TOOLTIP
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#1c1c1c"))   
                    widget.window.draw_rectangle(xgc, True, mx+20, my+5, 150, 20)
                    ctx.set_font_size(15)
                    ctx.set_source_rgb(1,1,1)
                    ctx.move_to( mx+30, my+20)
                    ctx.show_text("Configure item")
                    
                    
                    # IF CLICKED
                    if "GDK_BUTTON1" in str(fx) and self.allowed and "GDK_BUTTON1" not in str(self.mpf) and win.is_active():
                        
                        def ee():
                                    
                            
                                    
                            linkconfig.config(self.pf, self.screen.CUR+"/"+self.screen.name )
                                    
                        glib.timeout_add(10, ee) 
                        
                    
                widget.window.draw_pixbuf(None, self.settingsicon, 0, 0, mmx+60, 115+22, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                
                
                
                
                
                # edit preview
                #mouse over
                if mx in range(mmx+60, mmx+60+22) and my in range(80+mmy-27, 80+mmy-27+22):
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
                    widget.window.draw_rectangle(xgc, True, mmx+60, 80+mmy-27, 22, 22)
                    
                    # TOOLTIP
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#1c1c1c"))   
                    widget.window.draw_rectangle(xgc, True, mx+20, my+5, 200, 20)
                    ctx.set_font_size(15)
                    ctx.set_source_rgb(1,1,1)
                    ctx.move_to( mx+30, my+20)
                    ctx.show_text("Change preview image")
                    
                    # IF CLICKED
                    if "GDK_BUTTON1" in str(fx) and self.allowed and "GDK_BUTTON1" not in str(self.mpf) and win.is_active():
                        
                        def dobutton(w=None):
                            dialogs.editPreview(self.screen.path, box, self.pf)
                            self.blends = self.loadBlendFiles(self.screen)
                            self.iteminfo = self.loaditem(self.screen)
                            
                            self.screen.preview = thumbnailer.thumbnail(self.screen.path+"/renders/Preview.png", 400, 400)
                            self.screen.preview = gtk.gdk.pixbuf_new_from_file(self.screen.preview)
                            
                            
                            
                            
                        glib.timeout_add(10, dobutton)
                    
                widget.window.draw_pixbuf(None, self.editicon, 0, 0, mmx+60, 80+mmy-27, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                
                
                # Refresh
                #mouse over
                if mx in range(mmx+60, mmx+60+22) and my in range(80+mmy-27-27, 80+mmy-27-5):
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
                    widget.window.draw_rectangle(xgc, True, mmx+60, 80+mmy-27-27, 22, 22)
                    
                    # TOOLTIP
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#1c1c1c"))   
                    widget.window.draw_rectangle(xgc, True, mx+20, my+5, 200, 20)
                    ctx.set_font_size(15)
                    ctx.set_source_rgb(1,1,1)
                    ctx.move_to( mx+30, my+20)
                    ctx.show_text("Refresh")
                    
                    # IF CLICKED
                    if "GDK_BUTTON1" in str(fx) and self.allowed and "GDK_BUTTON1" not in str(self.mpf) and win.is_active():
                        
                        self.blends = self.loadBlendFiles(self.screen)
                        self.iteminfo = self.loaditem(self.screen)
                        #self.screen.preview = gtk.gdk.pixbuf_new_from_file(self.screen.preview)
                        self.screen.percent = checklist.partcalculate(checklist.openckecklist(self.screen.path+"/asset.progress"))
                    
                widget.window.draw_pixbuf(None, self.refresh, 0, 0, mmx+60, 80+mmy-27-27, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                
                
                
                
                # draw preview
                
                
                
                
                if self.screen.preview != "NO PIXBUF":
                    widget.window.draw_pixbuf(None, self.screen.preview, 0, 0, 50, 70, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                
                else:
                    
                    def ee():
                        it = self.screen
                        if os.path.exists(it.path+"/renders/Preview.png"):
                            #it.pic = thumbnailer.thumbnail(it.path+"/renders/Preview.png", 182, 124)
                            #it.pic = gtk.gdk.pixbuf_new_from_file(it.pic)
                            it.preview = thumbnailer.thumbnail(it.path+"/renders/Preview.png", 400, 400)
                            it.preview = gtk.gdk.pixbuf_new_from_file(it.preview)
                         
                        elif os.path.exists(it.path+"/renders/Preview.jpg"):
                         
                            #it.pic = thumbnailer.thumbnail(it.path+"/renders/Preview.jpg", 182, 124)
                            #it.pic = gtk.gdk.pixbuf_new_from_file(it.pic)
                            it.preview = thumbnailer.thumbnail(it.path+"/renders/Preview.jpg", 400, 400)
                            it.preview = gtk.gdk.pixbuf_new_from_file(it.preview)
                        else:
                            it.preview = it.pf+"/py_data/icons/"+CUR+"_prev.png"
                            it.preview = gtk.gdk.pixbuf_new_from_file(it.preview)
                        
                        
                        
                    glib.timeout_add(10, ee)
                
                ## top pannel
                
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#363636")) ## CHOSE COLOR
                widget.window.draw_rectangle(xgc, True, 0, 0, w, 50)
                     
                
                
                self.screen.percent = checklist.partcalculate(checklist.openckecklist(self.screen.path+"/asset.progress"))
                
                # BIG PERCENTAGE BAR 
                ctx.set_source_rgb(1,1,1)
                ctx.set_font_size(20)
                ctx.move_to( 20, 30)
                ctx.show_text(str(int(self.screen.percent*100))+" %")
                
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#d0d0d0")) ## CHOSE COLOR
                widget.window.draw_rectangle(xgc, True, 100, 5, w-110, 40)
                
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
                
                widget.window.draw_rectangle(xgc, True, 100, 5, int((w-110)*self.screen.percent), 40)
                
                ctx.move_to( 150, 30)
                ctx.show_text(self.screen.name)
                
                
                        
                    
                        
            
            if mouseoverany:
                widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))     
            else:  # IF MOUSE NOT IN EDITOR
                widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.ARROW))    
                
                
                
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
        graph.set_size_request(500,700)
        
        
        
        
        
        
        
        
        self.box.pack_start(graph)
        graph.connect("expose-event", framegraph) 
        
        self.box.show_all()        
        
        
    def call_add_dialog(self):
               
        self.newitem = dialogs.AddAsset(self.pf, self.CUR)
        
        
        
        self.newitem = self.newitem.getpath()
        self.newitem = self.newitem[self.newitem.rfind("/")+1:]
        
        
        
        self.justadded = True
        self.folder_read()
    
    
    
    def loaditem(self, i): 
        
        #### LOADING RENDERS, TEXTURES AND ALL THAT CRAP TO MEMORY
        # as previews and their links
        
        
        
        info = []  #PLACE HOLDER FOR ALL THE ICONS AND STUFF
        
        
        
        ## Renders
        
        
        
        for part in ["reference", "tex", "renders"]: # I REORDERED THEM
            
            renders = []
            
            for FILE in sorted(os.walk(self.pf+"/dev/"+self.CUR+"/"+i.name+"/"+part).next()[2]):
                
                # getting photos, images
                
                pic = self.pf+"/py_data/icons/pic_big.png"
                pic = gtk.gdk.pixbuf_new_from_file(pic)
                
                for f in fileformats.images:
                    
                    
                    
                    if FILE.endswith(f):
                        
                        #try making a thubnail
                        
                        pic = "NO PIXBUF"
                        #try:
                        #    pic = thumbnailer.thumbnail(self.pf+"/dev/"+self.CUR+"/"+i.name+"/"+part+"/"+FILE, 100, 100)
                        #    pic = gtk.gdk.pixbuf_new_from_file(pic)
                        #except:
                        #    pic = self.pf+"/py_data/icons/pic_big.png"
                        #    pic = gtk.gdk.pixbuf_new_from_file(pic)
                            
                        renders.append( [pic, self.pf+"/dev/"+self.CUR+"/"+i.name+"/"+part+"/"+FILE, FILE, "IMAGE"] )
                                  
                for f in fileformats.videos:
                    
                    
                    
                    if FILE.endswith(f):
                        
                        #try making a thubnail
                        
                        pic = "NO PIXBUF"
                        #try:
                        #    pic = thumbnailer.videothumb(self.pf+"/dev/"+self.CUR+"/"+i.name+"/"+part+"/"+FILE, 100)
                        #    pic = gtk.gdk.pixbuf_new_from_file(pic)
                        #except:
                        #    pic = self.pf+"/py_data/icons/pic_big.png"
                        #    pic = gtk.gdk.pixbuf_new_from_file(pic)
                            
                        renders.append( [pic, self.pf+"/dev/"+self.CUR+"/"+i.name+"/"+part+"/"+FILE, FILE, "VIDEO"] )             
            
                # getting videos
            
            
            
            
            info.append(renders)
        
        return info
        
    def loadBlendFiles(self, i):
        
        blends = []
        
        
        for FILE in os.walk(self.pf+"/dev/"+self.CUR+"/"+i.name).next()[2]:
            
            if FILE.endswith(".blend"):
                
                pic = "NO PIXBUF"
                #try:
                #    pic = thumbnailer.blenderthumb(self.pf+"/dev/"+self.CUR+"/"+i.name+"/"+FILE, 100, 100)
                #    pic = gtk.gdk.pixbuf_new_from_file(pic)
                #    
                #except:
                #    pic = self.pf+"/py_data/icons/pic_big.png"
                #    pic = gtk.gdk.pixbuf_new_from_file(pic)
        
                blends.append( [pic, (self.pf+"/dev/"+self.CUR+"/"+i.name+"/"+FILE), FILE, "BLEND"] )
        
        return blends
        
            
    
    def folder_read(self):
        
        self.assets = []
        
        tmp = []         
        for i in os.walk(self.pf+"/dev/"+self.CUR).next()[1]:
            tmp.append(i)
            
        for i in sorted(tmp): 
            
            print "\033[1;32m     ⬦ "+i+"  \033[1;m"
               
            thisasset = asset(self.pf, self.pf+"/dev/"+self.CUR+"/"+i, self.CUR, i)
            
            self.assets.append(thisasset)
         
