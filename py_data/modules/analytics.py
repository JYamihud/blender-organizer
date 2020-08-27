# -*- coding: utf-8 -*-

# system
import os
import socket
import random

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
import story_editor # to get scene percentage
import schedule
import assets
import imageselector
import oscalls
import settingsfile

class draw_analytics:
    
    def __init__(self, pf, box, win, mainbox=None):
    
        self.pf = pf # pf stands for project folder. It's a string to know
                     # where the project's folders start with
        
        
        
        
        
        self.box = box # the gtk.Box() container to put this widget into
        self.mainbox = mainbox
        self.win = win
        
        self.mainchecklist = checklist.partcalculate(checklist.openckecklist("project.progress"))
        
        
        
        # drawing it's own box cutting in 2 for right and left halfs
        
        
        self.schedule_date_format = "%Y/%m/%d"
        
        
        # reading persentages
        
        
        
        self.toolx = 0
        self.tooly = 0
        
        
        
        
        
        ####   DRAWING TO THE SCREEN ####
        
        self.allowed = True # a value for the redrawing of the drawable for the next frame
        
        self.dW = 0
        self.DH = 0
        self.banner = pf+"/py_data/banner.png"#thumbnailer.thumbnail(pf+"/py_data/banner.png", 500, 500)
        self.pixbuf = gtk.gdk.pixbuf_new_from_file(self.banner)
        self.mpx = 0
        self.mpy = 0
        self.mpf = ""
        
        self.editicon  = gtk.gdk.pixbuf_new_from_file(pf+"/py_data/icons/edit.png")
        self.scheduleicon  = gtk.gdk.pixbuf_new_from_file(pf+"/py_data/icons/schedule.png")
        self.checklist  = gtk.gdk.pixbuf_new_from_file(pf+"/py_data/icons/checklist.png")
        self.deleteicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/delete.png")
        self.okicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/ok.png")
        self.blendericon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/blender.png")
        self.settingsicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/settings.png")
        self.moveicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/move.png")
        self.staricon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/star.png")
        
        
        #getting icons into place OMG WHY????
        self.objicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/obj_asset_undone.png")
        self.chricon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/chr_asset_undone.png")
        self.vehicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/veh_asset_undone.png")
        self.locicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/loc_asset_undone.png")
        self.scnicon = gtk.gdk.pixbuf_new_from_file(self.pf+"/py_data/icons/scn_asset_undone.png")
        ####### DATA
            
        self.scroll = 0
        self.ifpos = 10
        self.hscroll = 0
        self.tscroll = 0
        
        print "\033[1;31m ⬥ READING ANALYTICS DATA : \033[1;m"
        
        
        #selecting days for analytics
        self.selectdate = "0000/00/00"
        self.dateicons = {}
        
        self.taskmove = -1
        
        # MOTIVATING WORDS
        motivatingwords = ["Nice!", "Wow!", "Yeah!", "Crazy!", "Win!", "Rocks!", "Lit!", "Cool!", "Best!", "Super!", "Amazing!"]
        okaywords = ["Alright", "Fine", "Not Bad", "Keep This Pace"]
        nahword = ["Nah", "Come On", "You Can Do Better"]
        wtfwords = ["WTF", "NO!", "LOL", "WHY?!", "What Happened!?", "OMG!"]
        justdoit = ["JUST DO IT!", "MAKE IT BE!", "WE CAN DO THIS TOGETHER!", "DON'T WASTE YOUR TIME!", "IT'S NOT HARD!"]
        justdoitsting = random.choice(justdoit)
        otherword = {}
        starsword = {}
        
        
        
        #NEW STORY EDITOR CODE
        story = story_editor.bos("pln/main.bos")
        story.load()
        scenpercent = story_editor.get_scenes_percentage(story)
        #NEW CODE FINISHED HERE
        
        
        
        # TRYING TO WRITE A BETTER CODE
        
        
        # lets dich the idea of reading into a file to get how much needed to be done
        # fuck it
        
        # we are focusing on the actuall folders
        
        
        asstfols = ["chr", "veh", "loc", "obj"]
        opnames  = ["Character", "Vehicles", "Locations", "Objects", "Scenes"]
        
        
        astlist = []
        
        for n , f in enumerate(asstfols):
            
            flist = []
            
            if len(os.listdir("dev/"+f)) > 0:
            
                for asset in os.listdir("dev/"+f):
                    
                    if asset+".blend" in os.listdir("ast/"+f):
                        
                        flist.append(1.0)
                    
                    else:
                        
                        try:    
                            
                            flist.append(checklist.partcalculate(checklist.openckecklist("dev/"+f+"/"+asset+"/asset.progress")))
                        except:
                            flist.append(0.0)
                
                rawmultiply = settingsfile.get(opnames[n])
                print f,   rawmultiply
                try:
                    multiply = int(rawmultiply)
                except:
                    multiply = 1
                
                for m in range(multiply):
                    astlist.append(sum(flist)/len(flist))
            
        
        rawmultiply = settingsfile.get(opnames[4])  
        print "scn",   rawmultiply
        try:
            multiply = int(rawmultiply)
        except:
            multiply = 1
        for m in range(multiply):
            astlist.append(scenpercent)
        
        projectpercent = (sum(astlist)/len(astlist))*100
        
        
        print "\033[1;32m     ⬦ Project is at "+str(projectpercent)+"%  \033[1;m"
        
        #### SPANISH LANGUAGE EXCEPTION #####
        
        
        
        try:
            
            #TESTING TRY
            #1.0 / 0
            
            #TIME
            
        
            #getting time values
            
            timefile = open("project.progress", "r")
            timefile = timefile.read()
            self.startdate = "00/00/00"
            self.enddate = "00/00/00"
            for timeline in timefile.split("\n"):
                if timeline.startswith("STR"):
                    self.startdate = timeline[4:]
                if timeline.startswith("FIN"):
                    self.enddate = timeline[4:]
            
            print "\033[1;32m     ⬦ Startdate is "+str(self.startdate)+"  \033[1;m"
            print "\033[1;32m     ⬦ Deadline is "+str(self.enddate)+"  \033[1;m"
            
            # CALCULATING DAYS
            deadline = 0.2
            
            date_format = "%d/%m/%Y"
            a = datetime.datetime.strptime(self.startdate, date_format)
            b = datetime.datetime.strptime(self.enddate, date_format)
            delta = b - a
            self.alltime = int(delta.days)
            
            a = datetime.datetime.strptime(self.startdate, date_format)
            b = datetime.datetime.today()
            delta =  b - a
            
            passed = int(delta.days)
            
            
            self.passed = passed
            
            print "\033[1;32m     ⬦ Passed days "+str(self.passed)+"  \033[1;m"
            
            
            
            try:
                deadline = (1.0/self.alltime)*passed
            except:
                deadline = 0
            
            deadline = deadline  * 100
            
            
            
            assetpercent = projectpercent
            projectpercent = str((float(assetpercent)+self.mainchecklist*100)/2)
            projectpercent = projectpercent[:projectpercent.find(".")+3]
            
            #### GETTING ALL CURRENT TASKS ###
            self.schedule = []
            self.schedulesize = 0
            def get_schedule():
                schedulefile = open(self.pf+"/schedule.data","r")
                schedulefile = schedulefile.read().split("\n")
                self.schedulesize = os.path.getsize(self.pf+"/schedule.data")
                self.schedule = []
                self.schedule_date_format = "%Y/%m/%d"
                
                psdate = "0000/00/00"
                ypos = 0
                over = True
                daystring = " Today"
                gypos = self.dateicons
                for task in schedulefile:   
                    
                    
                    today = False
                    under = False
                    xpos = 0
                    done = False
                    taskstring = "Task"
                    taskfile = "progect.progress"
                    
                    
                    
                    try:
                        sdate = task[:task.find(" ")]
                        if psdate == sdate:
                            gypos = gypos + 1
                        else:
                            gypos = 1
                            psdate = sdate
                        ypos = ypos + 1
                        
                        if sdate:
                            
                            #gypos = gypos +1
                            
                            
                            if sdate == self.selectdate:#datetime.datetime.today().strftime(self.schedule_date_format):
                                today = True
                                over = False
                            
                            if sdate == "1997/07/30":
                                sdate = datetime.datetime.strftime(datetime.datetime.today(), self.schedule_date_format)
                                today = True
                                over = True 
                            
                            #if self.selectdate != datetime.datetime.today().strftime(self.schedule_date_format):
                            #    over = True
                            #    today = False
                            #else:
                            #    today = True
                                
                            if not today:
                                a = datetime.datetime.today()
                                b = datetime.datetime.strptime(sdate, self.schedule_date_format)
                                delta = b - a
                            
                            
                                s = ""
                                
                                if datetime.datetime.strptime(sdate, self.schedule_date_format) == datetime.datetime.today():
                                    daystring = "Today"
                                    
                                elif delta.days < 0:
                                    
                                    if not (delta.days)*-1-1 > 1:
                                        daystring = "Yesterday"
                                    else:
                                        daystring = str((delta.days)*-1-1)+" Days Ago"
                                
                                    under = True
                                
                                else:
                                    if not delta.days+1 > 1:
                                        daystring = "Tomorrow"
                                    else:
                                        daystring = "In "+str(delta.days+1)+" Days"
                                    
                            #print daystring, "DAYSTRING"
                            
                            
                            a = datetime.datetime.strptime(self.startdate, date_format)
                            b = datetime.datetime.strptime(sdate, self.schedule_date_format)
                            delta = b - a
                            
                            xpos = float(delta.days)/self.alltime
                            
                            
                            
                            #print xpos, sdate
                            
                            taskfile = task[task.find(" ")+1:task.replace(" ", ".", 1).find(" ")]
                            #print taskfile
                            taskstring = task[task.replace(" ", ".", 2).find(" "):].replace("=:>", " >")
                            #print taskstring
                            
                            #print
                            #print
                            
                            self.schedule.append([today, over, under, xpos, ypos, gypos, done, taskstring, taskfile, task, daystring])
                            
                    except Exception as exception:
                        print exception
                    
                    
                  
                
        except:
            
            import troubleshooter
            troubleshooter.shoot(4)
            
            
            
            raw_input()
            exit()

        
        
        get_schedule()
        
        
        ##### MAIN BOTTOM GRAPH #####
        
        ## CREATING THE DATA FILE
        try:
            percenthystory = open("percentage_hystory.data", "r")
        except:
            percenthystory = open("percentage_hystory.data", "w")
            
            percenthystory.write("### PERCENTTAGE HYSTORY FILE\n")
            percenthystory.write("### WRITES DOWN THE WHOLE PROJECT\n")
            percenthystory.write("### PERCENTTAGE HYSTORY FOR STATISTICS\n")
            percenthystory.write("DATE "+datetime.datetime.now().strftime("%y-%m-%d")+" "+projectpercent+"%\n")
            
            percenthystory.close()
            percenthystory = open("percentage_hystory.data", "r")
        
        # CORRECTING THE DATA FILE IF NEEDED
        
        percenthystory = percenthystory.read()
        
        perhys = percenthystory.split("\n")
        foundtoday = False
        for dln, date in enumerate(perhys):
            if datetime.datetime.now().strftime("%y-%m-%d") in date:
                foundtoday = True
                if date.split(" ")[-1] not in  (projectpercent+"%  "):
                    
                    
                    perhys[dln] = "DATE "+datetime.datetime.now().strftime("%y-%m-%d")+" "+projectpercent+"%"
                    
                
        
        if foundtoday == False:
            perhys.append("DATE "+datetime.datetime.now().strftime("%y-%m-%d")+" "+projectpercent+"%")
        percenthystory = open("percentage_hystory.data", "w")
        
        for date in perhys:
            if len(date) > 0:
                percenthystory.write(date+"\n")
        
        percenthystory.close()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        def framegraph(widget, event):
                                                    
            w, h = widget.window.get_size()
            xgc = widget.window.new_gc()
            
            mx, my, fx  = widget.window.get_pointer()
            
            if "GDK_BUTTON1" in str(fx) and self.allowed and "GDK_BUTTON1" not in str(self.mpf) and win.is_active(): 
                self.toolx = mx
                self.tooly = my
            
            
            # GETTING WHETHER THE WINDOW IS ACTIVE
            
            self.winactive = win.is_active()
            

            stf = datetime.datetime.now()
            perfStat = []
            
            
            ctx = widget.window.cairo_create()
            #ctx.select_font_face("Sawasdee", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            ctx.set_source_rgb(1,1,1)
            ctx2 = widget.window.cairo_create()
            ctx2.select_font_face("Monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            
            ## tooltips
            tooltip = False
            
            xgc.line_width = 2
            
            # BACKGROUND COLOR
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#1c1c1c")) ## CHOSE COLOR
            widget.window.draw_rectangle(xgc, True, 0, 0, w, h)  ## FILL FRAME 
            
            
            ##########################################################################################################
            ##                                  DRAWING GRAPH THINGY DOWN HERE                                      ##
            ##                                  JUST GO AND LOOK THERE MOTHER...                                    ##
            ##########################################################################################################
            
            
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
            ctx3.set_source_rgba(0.2,0.2,0.2,0.7)
            ctx3.rectangle(0, 0, w, h)
            ctx3.fill()
            
            ###########################
            
            border = 10 #pixels between elements
            elementsX = 3
            elementsY = 2
            todayongrapth = int(round(float(w)/self.alltime*passed))
            
            
            
            
            ###########################
            
            
            
            fif = datetime.datetime.now()
            mil  = fif - stf
            perfStat.append([ "IMAGE BACKGROUND - ", mil.microseconds ])
            
            stf = datetime.datetime.now()
            
            
            
            
            
            
            ######## UI Box 1 ######## BASIC ANALYTICS ######### BANNER IMAGE ##########
            
            stX = border / 4 * 3
            stY = 0
            ubX = w / elementsX - border
            ubY = h / elementsY - border
            
            ctx3 = widget.window.cairo_create()
            ctx3.set_source_rgba(0,0,0,0.4)
            ctx3.rectangle(stX, stY, ubX, ubY)
            ctx3.fill()
            
            
            #SMALL IMAGE
            
            scaledownY = ubY - (150) #EDIT HERE TO ADD MORE UNDER IMAGE
            
            
            
            
            scaleimageW =  int( float(self.pixbuf.get_width()) / self.pixbuf.get_height() * scaledownY) 
            
            if scaleimageW < ubX - border:
                
                #under image 
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#1c1c1c"))    
                widget.window.draw_rectangle(xgc, True , border, border / 2, ubX - border, scaledownY )
                
                
                #scaling image to the frame
                drawpix = self.pixbuf.scale_simple( scaleimageW, scaledownY, gtk.gdk.INTERP_NEAREST) 
                #drawing image
                widget.window.draw_pixbuf(None, drawpix, 0, 0, border / 2 + (ubX - drawpix.get_width()) / 2, border / 2, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
            
            
            else:
                
                scaleimageW =  int( float(self.pixbuf.get_height()) / self.pixbuf.get_width() * (ubX - border)) 
                #scaling image to the frame
                drawpix = self.pixbuf.scale_simple( (ubX - border), scaleimageW, gtk.gdk.INTERP_NEAREST) 
                #drawing image
                widget.window.draw_pixbuf(None, drawpix, 0, 0, border, border / 2, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
            
            
            #if mouse over the banner image
            if mx in range(border, ubX - border) and my in range(border / 2, drawpix.get_height() + border / 2):
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#fff"))    
                widget.window.draw_rectangle(xgc, False , border, border / 2, ubX - border, drawpix.get_height())
                
                tooltip = "Banner : /py_data/banner.png"
                
                if "GDK_BUTTON1" in str(fx) and self.allowed and "GDK_BUTTON1" not in str(self.mpf) and win.is_active(): #####   IF MOUSE CLICKED #####
                    oscalls.Open(pf+"/py_data/banner.png")
            
            
            UIY = drawpix.get_height() + border / 2
            
            #editing the banner
            if mx in range(ubX - border - 20, ubX - border) and my in range(UIY + border, UIY + border + 20):
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#1c1c1c"))    
                widget.window.draw_rectangle(xgc, True , ubX - border - 20, UIY + border, 20, 20)
                
                tooltip = "Change Banner Image"
                
                if "GDK_BUTTON1" in str(fx) and self.allowed and "GDK_BUTTON1" not in str(self.mpf) and win.is_active(): #####   IF MOUSE CLICKED #####                
                    self.allowed = False
                    glib.timeout_add(20, self.banner_changer)
            
            
            widget.window.draw_pixbuf(None, self.editicon, 0, 0, ubX - border - 20, UIY + border, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                    
            
            
            
            #filmname, status, director
            
            infostr = open("project.data") # FILE WHERE THE NAMES ARE STORED
            infostr = infostr.read()
            
            #EMPTIES
            filmname = "No Name"
            statusname = "No Status"
            directorname = "Unknown"
            
            #READING FILE
            for l in infostr.split("\n"):
                if l.startswith("Project  :"):
                    filmname = l[l.find(":")+1:]
                elif l.startswith("Status   :"):
                    statusname = l[l.find(":")+1:]
                elif l.startswith("Director :"):
                    directorname = l[l.find(":")+1:]
            
            
                
            
            # EDIT FILE IF YOU WANT TO CHANGE NAMES
            def edit(s, arg):
                                
                s = s.split("\n")
                if s[-1] == "":
                    s = s[:-1]
                
                for n, i in enumerate(s):
                    
                    if arg in i:
                        newname = dialogs.PickName(i[i.find(":")+1:])
                        
                        if newname == "playsnake":
                            import snake
                        
                        if newname == "" or newname == "playsnake":
                            newname = i[i.find(":")+1:]
                        
                        
                        
                            
                        s[n] = arg+newname
                
                
                save = open("project.data", "w")
                for i in s:
                    save.write(i+"\n")
                save.close()
                    
            
            #film name
              
            
            #if mouse over
            if mx in range(border+20, border+ubX/2-40) and my in range(UIY+border+2, UIY+20+border+2):
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#1c1c1c"))
                widget.window.draw_rectangle(xgc, True, border+20 , UIY+border+2, ubX/2-60, 20)
                #icon
                widget.window.draw_pixbuf(None, self.editicon, 0, 0, mx, my-20, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                tooltip = "Edit Project's Name"
                #if cliked
                if "GDK_BUTTON1" in str(fx) and self.allowed and "GDK_BUTTON1" not in str(self.mpf) and win.is_active(): #####   IF MOUSE CLICKED #####    
                    glib.timeout_add(10, edit, infostr, "Project  :")
                
            ctx.set_font_size(20)
            ctx.move_to( border+30, UIY+20+border)
            ctx.show_text(filmname)    
            
            #director's name
            #if mouse over
            if mx in range(border+20, border+ubX/2-40) and my in range(UIY+20+border+2, UIY+20+border+2+15):
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#1c1c1c"))
                widget.window.draw_rectangle(xgc, True, border+20 , UIY+border+2+20, ubX/2-60, 15)
                #icon
                widget.window.draw_pixbuf(None, self.editicon, 0, 0, mx, my-20, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                tooltip = "Change Director"
                #if cliked
                if "GDK_BUTTON1" in str(fx) and self.allowed and "GDK_BUTTON1" not in str(self.mpf) and win.is_active(): #####   IF MOUSE CLICKED #####    
                    glib.timeout_add(10, edit, infostr, "Director :")
            
            ctx.set_font_size(15)
            ctx.move_to( border+30, UIY+20+border+15)
            ctx.show_text("by : "+directorname) 
            
            #status
            #if mouse over
            if mx in range(border+20, border+ubX/2-40) and my in range(UIY+20+border+2+15, UIY+20+border+2+15+10):
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#1c1c1c"))
                widget.window.draw_rectangle(xgc, True, border+20 , UIY+20+border+2+15, ubX/2-60, 10)
                #icon
                widget.window.draw_pixbuf(None, self.editicon, 0, 0, mx, my-20, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                tooltip = "Edit Status"
                #if cliked
                if "GDK_BUTTON1" in str(fx) and self.allowed and "GDK_BUTTON1" not in str(self.mpf) and win.is_active(): #####   IF MOUSE CLICKED #####    
                    glib.timeout_add(10, edit, infostr, "Status   :")
            
            ctx.set_font_size(10)
            ctx.move_to( border+30, UIY+20+border+12+15)
            ctx.show_text(statusname) 
            
            
            
            
            
            
            
            ###### CHECKLIST PROGRESSBAR ######
            
            
            #BACKGROUND
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#d0d0d0"))
            widget.window.draw_rectangle(xgc, True, border+ubX/2 , UIY+17, ubX/2 - border-40, 15)
            #PROGRESSBAR
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
            widget.window.draw_rectangle(xgc, True, border+ubX/2 , UIY+17, int(float(ubX/2 - border-40)*self.mainchecklist), 15)
            #TEXT
            ctx.set_source_rgb(1,1,1)
            ctx.set_font_size(15)
            ctx.move_to( border+ubX/2, UIY+15)
            ctx.show_text("Main Checklist")
            # % TEXT
            ctx.set_source_rgb(1,1,1)
            ctx.set_font_size(13)
            ctx.move_to( border+ubX/2+2, UIY+15+14)
            ctx.show_text(str(int(self.mainchecklist*100))+"%")
            
            #ICON
            widget.window.draw_pixbuf(None, self.checklist, 0, 0, border+ubX/2-25, UIY+15, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
            
            
            
            ###### ASSETS PROGRESSBAR ######
            
            
            #BACKGROUND
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#d0d0d0"))
            widget.window.draw_rectangle(xgc, True, border+ubX/2 , UIY+17+34, ubX/2 - border-40, 15)
            #PROGRESSBAR
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
            widget.window.draw_rectangle(xgc, True, border+ubX/2 , UIY+17+34, int(float(ubX/2 - border-40)*(float(assetpercent)/100)), 15)
            #TEXT
            ctx.set_source_rgb(1,1,1)
            ctx.set_font_size(15)
            ctx.move_to( border+ubX/2, UIY+15+34)
            ctx.show_text("Assets and Scenes")
            # % TEXT
            ctx.set_source_rgb(1,1,1)
            ctx.set_font_size(13)
            ctx.move_to( border+ubX/2+2, UIY+15+14+34)
            ctx.show_text(str(int(assetpercent))+"%")
            #ICON
            widget.window.draw_pixbuf(None, self.scnicon, 0, 0, border+ubX/2-25, UIY+15+34, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
            
            
            
            
            ############   MAIN PROGRESS BAR ################
            
            #BACKGROUND
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#d0d0d0"))
            widget.window.draw_rectangle(xgc, True, border , ubY-50-10, ubX - border, 30)
            
            #TIME BAR
            
            timespace = int((ubX - border)*(1.0/self.alltime*passed))
            if timespace > ubX - border:
                timespace = ubX - border
            
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#395384"))
            widget.window.draw_rectangle(xgc, True, border, ubY-50-10, timespace, 30)
            
            
            
            #PGRESSBAR
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
            widget.window.draw_rectangle(xgc, True, border, ubY-50-10, int((ubX - border)*(float(projectpercent)/100)), 30)
            
            #TEXT
            ctx.set_source_rgb(1,1,1)
            ctx.set_font_size(20)
            ctx.move_to( border*2, ubY-50+15)
            ctx.show_text(str(projectpercent)+"%")
            
            #timepassedstring = "Time Passed : "+str(int(deadline))+"%  "+str(self.alltime-passed)+" days left"
            timepassedstring = str(self.alltime-passed)+" days left"
            timegonestring   = str(passed)+" days gone"
            
            time1X = border+4+(timespace+(ubX-timespace)/2) - (len(timepassedstring)*6)/2
            time1Y = ubY-52-10
            time2X = border+4+((timespace-border)/2) - (len(timegonestring)*6)/2
            time2Y = ubY-52-10          
            
            arrow1 = True
            arrow2 = True
            
            if time2X+len(timegonestring)*6+5 > timespace-10:
                time2X = border + 5
                time2Y = time2Y - 10
                arrow2 = False
                
            if time1X+len(timepassedstring)*6+5 > ubX-10:
                time1X = ubX-50
                time1Y = time1Y - 10
                arrow1 = False
            
            ctx.set_source_rgb(1,1,1)
            ctx.set_font_size(10)
            ctx.move_to( time1X, time1Y)
            ctx.show_text(timepassedstring)
            
            ctx.set_source_rgb(1,1,1)
            ctx.set_font_size(10)
            ctx.move_to( time2X, time2Y)
            ctx.show_text(timegonestring)
            
            ctx.set_source_rgb(1,1,1)
            ctx.set_font_size(10)
            ctx.move_to( timespace, ubY-52-10)
            ctx.show_text(str(int(deadline))+"%")
            
            
            
            #timeline
            xgc.line_width = 1
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#fff"))
            widget.window.draw_rectangle(xgc, True, border+timespace, ubY-60, 1, 30)
            
            
            time1Y = ubY-52-10
            time2Y = ubY-52-10 
            
            #passet arrow
            
            if arrow2:
                widget.window.draw_line(xgc, border+5, time2Y-5, time2X-10, time2Y-5) 
                widget.window.draw_line(xgc, time2X+len(timegonestring)*6+5, time2Y-5, timespace-10, time2Y-5) 
                
                widget.window.draw_line(xgc, border+5, time2Y-5, border+5+5, time2Y-10) 
                widget.window.draw_line(xgc, border+5, time2Y-5, border+5+5, time2Y) 
                widget.window.draw_line(xgc, timespace-11, time2Y-5, timespace-16, time2Y-10) 
                widget.window.draw_line(xgc, timespace-11, time2Y-5, timespace-16, time2Y)
            
            #Left arrow
            if arrow1:
                widget.window.draw_line(xgc, timespace+30, time1Y-5, time1X-10, time1Y-5) 
                widget.window.draw_line(xgc, time1X+len(timepassedstring)*6+5, time1Y-5, ubX-10, time1Y-5) 
                
                widget.window.draw_line(xgc, timespace+30, time1Y-5, timespace+30+5, time1Y-10) 
                widget.window.draw_line(xgc, timespace+30, time1Y-5, timespace+30+5, time1Y) 
                widget.window.draw_line(xgc, ubX-11, time1Y-5, ubX-16, time1Y-10) 
                widget.window.draw_line(xgc, ubX-11, time1Y-5, ubX-16, time1Y)
                
                
            
            if self.toolx in range(border, ubX) and mx in range(border, ubX) and self.tooly in range(ubY-50-10, ubY-50-10+30) and "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" in str(self.mpf):
            
                widget.window.draw_line(xgc, self.toolx, ubY-50-10+23, mx+1, ubY-50-10+23) 
                
                t1 = self.toolx
                t2 = mx
                
                if t1 > t2:
                    t1 = t2
                    t2 = self.toolx
                
                if t2 - t1 > 10:
                
                    widget.window.draw_line(xgc, t1, ubY-50-10+23, t1+6, ubY-50-10+23-6) 
                    widget.window.draw_line(xgc, t1, ubY-50-10+23, t1+6, ubY-50-10+23+6) 
                    widget.window.draw_line(xgc, t2, ubY-50-10+23, t2-5, ubY-50-10+23-5) 
                    widget.window.draw_line(xgc, t2, ubY-50-10+23, t2-5, ubY-50-10+23+5)
                
                
                allpix   = ubX - (border)
                t1pix    = t1  - (border)
                t2pix    = t2  - (border)
                fraction = 100.0/allpix * (t2pix - t1pix)
                tdays    = float(self.alltime)/allpix * (t2pix - t1pix)
                
                ctx.set_source_rgb(1,1,1)
                if border + int((ubX - border)*(float(projectpercent)/100)) < (t1+t2)/2-(len(str(int(tdays))+" days")*6/2)+(len(str(int(tdays))+" days")*6):
                    if timespace < (t1+t2)/2-(len(str(int(tdays))+" days")*6/2)+(len(str(int(tdays))+" days")*6):
                        ctx.set_source_rgb(0,0,0)
                ctx.set_font_size(10)
                ctx.move_to( (t1+t2)/2-(len(str(int(tdays))+" days")*6/2), ubY-50-10+10)
                ctx.show_text(str(int(tdays))+" days")
                
                ctx.set_source_rgb(1,1,1)
                if border + int((ubX - border)*(float(projectpercent)/100)) < (t1+t2)/2-(len(str(int(fraction))+"%")*6/2)+(len(str(int(fraction))+"%")*6):
                    if timespace < (t1+t2)/2-(len(str(int(fraction))+"%")*6/2)+(len(str(int(fraction))+"%")*6):
                        ctx.set_source_rgb(0,0,0)
                ctx.set_font_size(10)
                ctx.move_to( (t1+t2)/2-(len(str(int(fraction))+"%")*6/2), ubY-50-10+20)
                ctx.show_text(str(int(fraction))+"%")
                
                
                
                
                ctx.set_source_rgb(1,1,1)
            ## FROM AND DEADLINE STUFF ##
            
            #getting time values
            
            
            
            timefile = open("project.progress", "r")
            timefile = timefile.read()
            self.startdate = "30/07/1997"
            self.enddate = "24/12/1998"
            for timeline in timefile.split("\n"):
                if timeline.startswith("STR"):
                    self.startdate = timeline[4:]
                if timeline.startswith("FIN"):
                    self.enddate = timeline[4:]             
                    
            
            if self.startdate == "30/07/1997":
                self.startdate = datetime.datetime.strftime(datetime.datetime.today(), date_format)
                self.enddate = datetime.datetime.strftime(datetime.datetime.today()+datetime.timedelta(days=30), date_format)
                #datetime.datetime.strftime(datetime.datetime.strptime(self.startdate, date_format)+datetime.timedelta(days=i-2), self.schedule_date_format)
                
                read = open("project.progress", "r")
                s = read.read().split("\n")
                if s[-1] == "":
                    s = s[:-1]
                
                for n, i in enumerate(s):
                    
                    what = "STR"
                    newdate = self.startdate
                    
                    if i.startswith(what):  
                        s[n] = what+" "+newdate
                    
                    
                    what = "FIN"
                    newdate = self.enddate
                    
                    if i.startswith(what):  
                        s[n] = what+" "+newdate    
                        
                    
                
                save = open("project.progress", "w")
                for i in s:
                    save.write(i+"\n")
                save.close()
                
            
            
            ### START TIME ###
            def ee(what, date):
                        
                p = date.split("/")
                
                y, m, d = int(p[2]), int(p[1])-1, int(p[0])
                
                
                y, m, d = dialogs.GetDate(y, m, d)
                
                
                y, m, d = str(y), str(m+1), str(d)
                if len(m) < 2:
                    m = "0"+m
                if len(d) < 2:
                    d = "0"+d
                
                newdate = d+"/"+m+"/"+y
                
                
                # MAKING SURE STR NOT THE SAME DATE AS FIN ( it might crash the software )
                
                if what == "STR" and newdate == self.enddate:
                    d = str ( int( d ) - 1 ) 
                    if len(d) < 2:
                        d = "0"+d
                    newdate = d+"/"+m+"/"+y
                    
                    
                if what == "FIN" and newdate == self.startdate:
                    d = str ( int( d ) + 1 ) 
                    if len(d) < 2:
                        d = "0"+d
                    newdate = d+"/"+m+"/"+y
                    
                
                read = open("project.progress", "r")
                s = read.read().split("\n")
                if s[-1] == "":
                    s = s[:-1]
                
                for n, i in enumerate(s):
                    
                    if i.startswith(what):  
                        s[n] = what+" "+newdate
                
                save = open("project.progress", "w")
                for i in s:
                    save.write(i+"\n")
                save.close()
            
            # MOUSE OVER
            if mx in range(border*2-5, border*2+105) and my in range(ubY-5-12, ubY):
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#1c1c1c"))
                widget.window.draw_rectangle(xgc, True, border*2-5 , ubY-5-12, 105, 15)
                #icon
                widget.window.draw_pixbuf(None, self.editicon, 0, 0, mx, my-20, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                tooltip = "Change Starting Date"
                #if cliked
                if "GDK_BUTTON1" in str(fx) and self.allowed and "GDK_BUTTON1" not in str(self.mpf) and win.is_active(): #####   IF MOUSE CLICKED #####    
                    glib.timeout_add(10, ee, "STR", self.startdate)
                
                
            ctx.set_font_size(10)
            ctx.move_to( border*2, ubY-5)
            ctx.show_text("Started: "+self.startdate) 
            
            
            # MOUSE OVER
            if mx in range(ubX-100-border-5, ubX-100-border+110) and my in range(ubY-5-12, ubY):
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#1c1c1c"))
                widget.window.draw_rectangle(xgc, True, ubX-100-border-5 , ubY-5-12, 110, 15)
                #icon
                widget.window.draw_pixbuf(None, self.editicon, 0, 0, mx, my-20, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                tooltip = "Change Starting Date"
                #if cliked
                if "GDK_BUTTON1" in str(fx) and self.allowed and "GDK_BUTTON1" not in str(self.mpf) and win.is_active(): #####   IF MOUSE CLICKED #####    
                    glib.timeout_add(10, ee, "FIN", self.enddate)
            
            
            ctx.set_font_size(10)
            ctx.move_to( ubX-100-border, ubY-5)
            ctx.show_text("Deadline: "+self.enddate)
            
            
            #BY DEADLINE PROGRESSBAR
            
            try:
                avrgval = float(projectpercent) / passed
            except:
                avrgval = 0.0
            self.enddateval = avrgval * ( self.alltime - passed ) + float(projectpercent)
            
            #BACKGROUND
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#d0d0d0"))
            widget.window.draw_rectangle(xgc, True, border*2+ubX/3, ubY-22, ubX/3, 15)
            #PROGRESSBAR
            percentvalue = int(ubX/3*self.enddateval/100)
            if percentvalue > ubX/3:
                percentvalue = ubX/3
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
            widget.window.draw_rectangle(xgc, True, border*2+ubX/3, ubY-22, percentvalue , 15)
            #TEXT
            ctx.set_source_rgb(1,1,1)
            ctx.set_font_size(13)
            ctx.move_to( border*2+ubX/3+5, ubY-23+12)
            ctx.show_text("Performance : "+str(int(self.enddateval))+"%")
            
            
                        
            ######## UI Box 2 ######## SCHEDULED TASKS ##########
            
            stX = border/2 + w / elementsX
            stY = 0
            ubX = w / elementsX - border
            ubY = h / elementsY - border
            
            ctx3 = widget.window.cairo_create()
            ctx3.set_source_rgba(0,0,0,0.4)
            ctx3.rectangle(stX, stY, ubX, ubY)
            ctx3.fill()
            
            
            fif = datetime.datetime.now()
            mil  = fif - stf
            perfStat.append([" BANNER BOX - ", mil.microseconds])
            
            stf = datetime.datetime.now()
            
            
            ######## UI Box 3 ######## HISTORY ##########
            
            stX = border/2 + w / elementsX * 2
            stY = 0
            ubX = w / elementsX - border
            ubY = h / elementsY - border
            
            ctx3 = widget.window.cairo_create()
            ctx3.set_source_rgba(0,0,0,0.4)
            ctx3.rectangle(stX, stY, ubX, ubY)
            ctx3.fill()
            
            
            
            #self.selectdate
            
            
            # let's open the hystory file
            
            hf = open(self.pf+"/history.data", "r")
            hf = hf.read()
            
            ln = 0
            
            hlist = {} # HERE I GONNA STORE DATA BY THE URL OF THE HISTORY
                       # IMO PEOPLE ARE NOT LOOKING FOR LIST, BUT MORE FOR
                       # WHAT THEY'VE DONE AT A PARTICULAR DAY
            
            sumofthings = 0 # I WANT TO MAKE A LITTLE GRAPH. LIKE WHAT YOU WAS WORKING ON MORE AND OTHERS.
                       
            for n, l in enumerate(hf.split("\n")[::-1]): # READING THE DATA
                
                if l.startswith(self.selectdate): # IF IT'S TODAY
                    
                    sumofthings = sumofthings + 1 # COUNTING HOW MUCH IS TODAY
                    
                    
                    
                    if "project.progress" in l:
                        urlofentry = "project.progress"
                    
                    elif "/ast/" in l:
                        urlofentry = l[l.replace(" ", ".", 1).find(" ")+1:l.rfind(".")]
                        urlofentry = urlofentry.replace("/ast/", "/dev/")
                    
                    elif "[Added Asset]" in l:
                        urlofentry = l[l.replace(" ", ".", 1).find(" ")+1:l.replace(" ", ".", 2).find(" ")]
                    
                    else: 
                        urlofentry = l[l.replace(" ", ".", 1).find(" ")+1:l.replace(" ", ".", 2).find(" ")][:l.rfind("/")]
                        urlofentry = urlofentry[:urlofentry.rfind("/")] #GETTING THE URL
                    
                    
                    if urlofentry not in hlist:
                        hlist[urlofentry] = []
                    
                    hlist[urlofentry].append(l)
            
            
            drawhistory = ""
            
            for n, l in enumerate(hlist): #REAING THE DOUCHE
                
                ln = ln + 1
                
                ypart = (ubY-ln*42) + self.hscroll
                
                if  ypart < stY + ubY - 41 and ypart > 1: #MAKING SURE THAT WE DRAW ONLY WHAT'S IN THE SCREEN. (OPTIMIZATION)
                    
                    
                    ctx3.set_source_rgba(0.1,0.1,0.1,0.75)
                    ctx3.rectangle(stX+border/2, ypart-1,  ubX-border, 40)
                    ctx3.fill()
                    
                    printname = l
                    CUR = ""
                    
                    needicon = self.scnicon
                    if "obj" in l:
                        needicon = self.objicon
                        printname = l[l.rfind("/")+1:]
                        CUR = "obj"
                    elif "chr" in l:
                        needicon = self.chricon
                        printname = l[l.rfind("/")+1:]
                        CUR = "chr"
                    elif "loc" in l:
                        needicon = self.locicon
                        printname = l[l.rfind("/")+1:]
                        CUR = "loc"
                    elif "veh" in l:
                        needicon = self.vehicon
                        printname = l[l.rfind("/")+1:]
                        CUR = "veh"
                    elif "pln" in l:
                        printname = "Edited Story"
                        CUR = "rnd"
                    elif "project.progress" in l:
                        printname = "Main Checklist"
                        needicon = self.checklist
                        CUR = "Checklist"
                    elif "/rnd/" in l:
                        printname = l.replace("/rnd/", "").replace("/", " > ")
                        CUR = "rnd"
                    
                    ctx.set_source_rgb(1,1,1)
                    ctx.set_font_size(15)
                    ctx.move_to( stX+border+30, ypart+15)
                    ctx.show_text(printname)
                    
                    widget.window.draw_pixbuf(None, needicon, 0, 0, stX + border + 2, ypart, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                    
                    
                    # PROGRESS BAR WIDGET
                            
                            
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#0c0c0c"))
                    widget.window.draw_rectangle(xgc, True , stX+border/2+10, ypart+30, ubX-border-10, 4)  
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#4c4c4c"))
                    widget.window.draw_rectangle(xgc, True , stX+border/2+10, ypart+30, (ubX-border-10)/sumofthings*len(hlist[l]), 4)  
                    
                    # NOT LET'S SHOW ALL OF THEM
                    
                    if my in range(ypart-1, ypart-1+40) and mx in range(stX+border/2, stX+border/2+ubX-border):
                        
                        xgc.line_width = 1
                        
                        
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#aaa"))
                        widget.window.draw_rectangle(xgc, False , stX+border/2, ypart-1,  ubX-border, 40)
                        
                        drawhistory = l
                        
                        
                        # IF CLICKED
                        if "GDK_BUTTON1" in str(fx) and self.allowed and "GDK_BUTTON1" not in str(self.mpf) and win.is_active() and CUR:
                            
                            if CUR != "Checklist":
                                self.box.destroy()
                                self.box = gtk.VBox(False)
                                self.mainbox.pack_start(self.box, True)
                                
                                if CUR == "rnd":
                                    
                                    
                                    gscene = printname[:printname.find(" > ")]
                                    gshot = printname[printname.rfind(" > ")+3:]
                                        
                                    
                                    story_editor.story(os.getcwd(), self.box, self.win, self.mainbox, scene=gscene, shot=gshot)
                                
                                else:                            
                                    assets.draw_assets(os.getcwd(), self.box, self.win, CUR, printname, mainbox=self.mainbox)
                            else:
                                checklist.checkwindow(pf=self.pf, title="Main Checklist", FILE="project.progress")
                        
            
            
            fif = datetime.datetime.now()
            mil  = fif - stf
            perfStat.append([" HISTORY - ", mil.microseconds])
            
            stf = datetime.datetime.now()
            
            
            
            
            ######## UI Box 4 ######## BIG GRAPH ##########
            
            bstX = 0
            bstY = h / elementsY + border / 4
            bubX = w
            bubY = h / elementsY - border - ( h / elementsY / 4)
            
            ctx3 = widget.window.cairo_create()
            ctx3.set_source_rgba(0,0,0,0.4)
            ctx3.rectangle(bstX, bstY, bubX, bubY)
            ctx3.fill()
            
            
            
            
            
            
            ######## UI Box 4 ######## SMALL GRAPH ##########
            
            stX = 0
            stY = h / elementsY + border / 4 + ( h / elementsY - border - ( h / elementsY / 4) ) + border
            ubX = w
            ubY = h / elementsY / 4
            
            ctx3 = widget.window.cairo_create()
            ctx3.set_source_rgba(0,0,0,0.4)
            ctx3.rectangle(stX, stY, ubX, ubY)
            ctx3.fill()
            
            
            
            
            
            
            
            ############################################################       GRAPH      ###############################################33
            
            
            #this is gonna be used for when you use ruler mesurment on the small graph.
            rulerdata = {}
            rulerdata["percent"]   = 0
            rulerdata["scheduled"] = 0
            
            
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#202020"))
            #widget.window.draw_polygon(xgc, True, [(border, h),(todayongrapth, h-int(ubY*(1.0/self.alltime*passed))),(todayongrapth,h)])
            
            #xgc.set_line_attributes(4, gtk.gdk.LINE_ON_OFF_DASH, gtk.gdk.CAP_NOT_LAST, gtk.gdk.JOIN_MITER)
            #xgc.set_rgb_fg_color(gtk.gdk.color_parse("#aaa"))
            #xgc.line_width = 1
            #widget.window.draw_line(xgc, 0, ubY/2+stY, todayongrapth, ubY/2+stY)    
            #widget.window.draw_line(xgc, 0, bubY/2+bstY, w, bubY/2+bstY) 
            
            #xgc.set_line_attributes(2, gtk.gdk.LINE_SOLID, gtk.gdk.CAP_NOT_LAST, gtk.gdk.JOIN_MITER) 
            
            ctx.select_font_face("Monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            
            
            for dln, date in enumerate(perhys):
                if date.startswith("DATE"):
                    
                    
                    
                    lastpercent = float( date.split(" ")[2][:-1] )
                    
                    
                    
                    
                    
                    
                    
            prevV = 0        
            
            prevW = 0
            prevH = h
            bprevH = bstY+bubY
            bprevW = self.scroll
            prevPH = ubY/2+stY
            prevbnowRH = 0
            prevwordabouthepart = ""
            prevtextY = 0
            
            stars = 0 # THIS IS COUNTING THE STARS TO MOTIVATE
            
            insultcheck = [] #HARD TO EXPLAIN LOOK FOR IT LOWER
            
            bprevPH = bubY/2+bstY
            
            try:
                avrgval = lastpercent / passed
            except:
                avrgval = 0.0
            prevLB = 0
            toshowwidget = True
            for dln, date in enumerate(perhys):
                if date.startswith("DATE"):
                
                    thedate = date.split(" ")[1]
                    thepercent = float( date.split(" ")[2][:-1] )
                    
                    
                    #getting date's position
                    
                    a = datetime.datetime.strptime(self.startdate, date_format)
                    b = datetime.datetime.strptime(thedate, "%y-%m-%d")
                    delta =  b - a
                    
                    pos = int(delta.days)
                    
                    nowW = int(round(float(w)/self.alltime*pos)) - int(round(float(w)/self.alltime))
                    nowH = int(round( float(ubY) / 100 * thepercent ))*-1+h
                    
                    bnowW = pos*20 + self.scroll + 20
                    bnowH = int(round( float(bubY) / 100 * thepercent ))*-1 +bstY +bubY #- 20
                    bnowRH = 0-int(round( float(bubY) / 100 * thepercent ))*-1 +20
                    
                    
                    #assigining some values to ruler
                    
                    if self.tooly in range(stY, h) and "GDK_BUTTON1" in str(fx) and win.is_active():
                        if nowW in range( self.toolx, mx ) or nowW in range( mx, self.toolx ):
                        
                            rulerdata["percent"]   = rulerdata["percent"] + ( thepercent - prevV )
                    
                    
                    
                    
                    
                    
                    try:
                        shouldbepercent = float(100.0/self.alltime*pos)
                    
                        if dln == 0:
                            nowPH = ubY/2+stY
                            bnowPH = bubY/2+bstY
                        
                        else:
                            #nowPH = int( round(float(ubY)/2 / shouldbepercent * (thepercent) ))*-1+h
                            #bnowPH = int( round(float(bubY)/2 / shouldbepercent * (thepercent) ))*-1+bstY+bubY
                            
                            nowPH = int( round(float(ubY)/2 / prevV * (thepercent) ))*-1+h
                            bnowPH = int( round(float(bubY)/2 / prevV * (thepercent) ))*-1+bstY+bubY
                            
                    except:
                        
                        shouldbepercent = 1
                        nowPH = ubY/2+stY
                        bnowPH = bubY/2+bstY
                    
                    
                    
                    
                    if prevW < nowW-5:
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
                        xgc.set_line_attributes(4, gtk.gdk.LINE_ON_OFF_DASH, gtk.gdk.CAP_NOT_LAST, gtk.gdk.JOIN_MITER)
                        xgc.line_width = 1
                        widget.window.draw_polygon(xgc, False, [(prevW+int(round(float(w)/self.alltime)), prevH),(nowW,nowH),(nowW,h),(prevW+int(round(float(w)/self.alltime)),h)])
                        widget.window.draw_polygon(xgc, False, [(bprevW+20, bprevH),(bnowW-1,bnowH),(bnowW-1,stY-border-1),(bprevW+20,stY-border-1)])
                        xgc.set_line_attributes(2, gtk.gdk.LINE_SOLID, gtk.gdk.CAP_NOT_LAST, gtk.gdk.JOIN_MITER) 
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#4c4c4c"))
                    
                    
                    
                    
                    
                        
                        
                        
                    #widget.window.draw_line(xgc,prevW, prevH, nowW, nowH)
                    
                    
                    
                    
                    if True:#nowW - prevLB > 20:
                        
                        # MOUSE OVER AND INFRO REVEAL
                        if mx in range( bnowW, bnowW+20) and toshowwidget and my in range(bstY, stY):
                            toshowwidget = False
                            pointshouldbe = int(float(ubY)/self.alltime*pos)*-1+h
                            
                        
                            
                            # VERTICAL LINE
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#aaa"))
                            xgc.line_width = 1
                            #widget.window.draw_line(xgc, nowW, stY, nowW, nowH)  
                            widget.window.draw_rectangle(xgc, False , nowW, stY, int(round(float(w)/self.alltime)+1), ubY)  
                            #xgc.line_width = 4
                            
                            #xgc.set_rgb_fg_color(gtk.gdk.color_parse("#0f0"))
                            #if thepercent < shouldbepercent:
                            #    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#00f"))
                            #    widget.window.draw_line(xgc, nowW, pointshouldbe-2, nowW, nowH)    
                            #    #widget.window.draw_rectangle(xgc, True , nowW-2, pointshouldbe-2, 5, pointshouldbe-nowH)  
                            # 
                            #    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#f00"))
                            
                            
                            xgc.line_width = 1
                            widget.window.draw_line(xgc, nowW, ubY/2+stY, nowW, nowPH)    
                            
                            
                            tmp = nowW
                            btmp = bnowW
                            if nowW + 30 > todayongrapth:
                                nowW = nowW -30
                                if nowW + 30 > w:
                                    nowW = nowW - 30
                                bnowW = bnowW -150
                                if bnowW + 150 > w:
                                    bnowW = bnowW - 150
                                   
                            #box
                            
                            
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#1c1c1c"))
                            widget.window.draw_rectangle(xgc, True , bnowW+24, bstY, 104+10, h/2+17+40-h/2)  
                            
                            widget.window.draw_rectangle(xgc, True , nowW+int(round(float(w)/self.alltime)+1)+1, stY, 20, 10)  
                            
                            # PROGRESS BAR WIDGET
                            
                            
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#d0d0d0"))
                            widget.window.draw_rectangle(xgc, True , bnowW+26, bstY+2, 100, 5)  
                            xgc.line_width = 4
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#395384"))
                            widget.window.draw_rectangle(xgc, True , bnowW+26, bstY+2, int(100.0*float(shouldbepercent)/100), 5)
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
                            widget.window.draw_rectangle(xgc, True , bnowW+26, bstY+2, int(100.0*float(thepercent)/100), 5)
                            
                            
                            
                            
                            # TEXT THINGY
                            #ctx.set_source_rgb(1,1,1)
                            #ctx.set_font_size(10)
                            #ctx.move_to( nowW+5, stY+17)
                            #ctx.show_text(str(thedate))
                            
                            ctx.set_source_rgb(0.4,0.5,0.8)
                            ctx.set_font_size(10)
                            ctx.move_to( bnowW+25, bstY+17+10+2)
                            ctx.show_text("Expected : "+str(int(shouldbepercent))+"%")
                            
                            ctx.set_source_rgb(1,0.2,0.2)
                            if thepercent > shouldbepercent:
                                ctx.set_source_rgb(0.2, 1 ,0.2)
                            ctx.set_font_size(10)
                            ctx.move_to( bnowW+25, bstY+17+20+2)
                            ctx.show_text("Delivered : "+str(int(thepercent))+"%")
                            
                            ctx.set_font_size(10)
                            ctx.move_to( bnowW+25, bstY+17+30+2)
                            ctx.show_text("Performance : "+str(int(100 / shouldbepercent * (thepercent)))+"%")
                            
                            
                            
                            nowW = tmp
                            bnowW = btmp
                            
                        # GRAPH OUTPUT
                        
                        ctx3 = widget.window.cairo_create()
                        ctx3.set_source_rgba(0.79,0.56,0.39,0.25)
                        ctx3.rectangle(prevW, prevH, nowW-prevW, h)
                        ctx3.fill()
                        
                        
                        #xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))    
                        #widget.window.draw_rectangle(xgc, True , prevW, prevH, int(round(float(w)/self.alltime)+1), h) 
                        prevLB = nowW
                        
                        #BIG GRAPH
                        
                        ctx3 = widget.window.cairo_create()
                        ctx3.set_source_rgba(0.79,0.56,0.39,0.25)
                        ctx3.rectangle(bprevW, bprevH, bnowW-bprevW, prevbnowRH-20)
                        ctx3.fill()
                        
                        #xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))    
                        #widget.window.draw_rectangle(xgc, True , bprevW, bprevH, 20, prevbnowRH-20) 
                        
                         
                         
                    
                    # DRAWING PULSE
                    xgc.line_width = 6
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#000"))
                    widget.window.draw_line(xgc,prevW, prevPH, nowW, nowPH)
                    widget.window.draw_line(xgc,bprevW, bprevPH, bnowW, bnowPH)
                    
                    
                    # LAST FEW DAYS DRAWER
                    
                    if nowPH < ubY/2+stY-ubY/10:
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#0F0"))
                        
                        
                        
                    elif nowPH < ubY/2+stY-ubY/20:
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#ff0"))
                        
                         
                        
                    elif nowPH < ubY/2+stY-ubY/35:
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#f70"))
                        

                    else:
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#f00"))
                        
                    xgc.line_width = 3
                    widget.window.draw_line(xgc,prevW, prevPH, nowW, nowPH)
                    widget.window.draw_line(xgc,bprevW, bprevPH, bnowW, bnowPH)
                    
                    
                    #print prevV,  thepercent, prevV < thepercent, nowPH, thedate
                    
                    # LET'S INSULT PEOPLE FOR NOT WORKING
                    largestnowPH = h
                    textavarageX = []
                    textavarageY = []
                    
                    if len(insultcheck) > 2:
                    
                        wordabouthepart = ""
                    
                        for day in insultcheck:
                            if largestnowPH > day[0][3]:
                                largestnowPH = day[0][3]
                    
                        
                    
                        
                        
                        
                        
                        for day in insultcheck:    
                            xgc.line_width = 3
                            
                            textavarageX.append(day[1][2])
                            textavarageY.append(day[1][3])
                            
                            #dln #index of where we are
                            #okaywords 
                            #nahword
                            #wtfwords
                            #otherword
                            
                            
                               
                            if largestnowPH < ubY/2+stY-ubY/10:
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#0F0"))
                                wordabouthepart = ""
                                if str(dln)+wordabouthepart not in otherword:
                                    otherword[str(dln)] = "" 
                                
                                
                            elif largestnowPH < ubY/2+stY-ubY/20:
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#ff0"))
                                wordabouthepart = "Okay"
                                if str(dln)+wordabouthepart not in otherword:
                                    otherword[str(dln)+wordabouthepart] = random.choice(okaywords)
                                 
                                
                            elif largestnowPH < ubY/2+stY-ubY/35:
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#f70"))
                                wordabouthepart = "Nah..."
                                if str(dln)+wordabouthepart not in otherword:
                                    otherword[str(dln)+wordabouthepart] = random.choice(nahword) 

                            else:
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#f00"))
                                wordabouthepart = "NO!"
                                if str(dln)+wordabouthepart not in otherword: 
                                    otherword[str(dln)+wordabouthepart] = random.choice(wtfwords)
                                    
                           
                            
                            
                            widget.window.draw_line(xgc,day[0][0],   day[0][1],  day[0][2],   day[0][3])
                            widget.window.draw_line(xgc,day[1][0],   day[1][1],  day[1][2],   day[1][3])
                            xgc.line_width = 4
                                
                        
                        textavarageX = int( sum(textavarageX)/len(textavarageX) )
                        textavarageY = int( sum(textavarageY)/len(textavarageY) )
                        
                        textY = textavarageY - 40
                        if prevtextY in range(textY-5, textY+15):
                            textY = textY - 20
                        
                        if wordabouthepart != prevwordabouthepart:
                            ctx.set_source_rgb(1,1,1)
                            ctx.set_font_size(10)
                            ctx.move_to( textavarageX-(len(otherword[str(dln)+wordabouthepart])/2)*6, textY) #
                            ctx.show_text(otherword[str(dln)+wordabouthepart])
                            
                            prevtextY =  textY   
                            
                        prevwordabouthepart = wordabouthepart
                        insultcheck = []
                        
                        
                                      #  day[0][0]   day[0][1]  day[0][2]   day[0][3]   day[1][0]   day[1][1]  day[1][2]   day[1][3]  day[2]
                    insultcheck.append([[prevW,     prevPH,     nowW,      nowPH],    [bprevW,    bprevPH,     bnowW,     bnowPH], bnowH])
                    
                    startheight = bnowPH-30
                    if startheight+30 > bnowH:
                        startheight = bnowH-30
                    
                    if nowPH < ubY/2+stY-ubY/10:
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#fff"))    
                        widget.window.draw_rectangle(xgc, True , nowW-2, nowPH-10, 4,4) 
                        
                        
                        
                        widget.window.draw_pixbuf(None, self.staricon, 0, 0, bnowW-10, startheight , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                        
                        stars = stars +1
                        
                        
                        if str(stars) not in starsword:
                            fornow = random.choice(motivatingwords)
                        
                           
                            if stars != 1:
                                while starsword[str(stars-1)] ==  fornow:
                                    fornow = random.choice(motivatingwords)
                            starsword[str(stars)] = fornow
                    
                        textY = startheight - 5
                        if prevtextY in range(textY-5, textY+15):
                            textY = textY - 20
                    
                    
                        ctx.set_source_rgb(1,1,1)
                        ctx.set_font_size(10)
                        ctx.move_to( bnowW-10, textY)
                        ctx.show_text(starsword[str(stars)])
                        
                        prevtextY =  textY   
                    
                    
                    
                    
                    
                    
                    
                    #PASSING TO THE NEXT VECTOR
                    prevH = nowH
                    prevW = nowW
                    prevV = thepercent
                    prevPH = nowPH
                    bprevH = bnowH
                    bprevW = bnowW
                    prevbnowRH = bnowRH
                    bprevPH = bnowPH
            
            
            
            
            
            
            
            
            ################################################################  END OF GRAPH #########################################################
            fif = datetime.datetime.now()
            mil  = fif - stf
            perfStat.append([ "PERCENTAGE GRAPH - ", mil.microseconds])
            
            stf = datetime.datetime.now()
            
            ################################################################  SCHEDULES #########################################################
            # TRYING TO GET IF TODAY WAS
            
            #makingsuretodrawlasttasks
            #if self.schedulesize != os.path.getsize(self.pf+"/schedule.data"):
            get_schedule()
            
            
            underwas = False
            highestypos = 0
            gyposdata = []
            lastgpos = 0
            lastxpos = 0
            for task in self.schedule:  
                today, over, under, xpos, ypos, gypos, done, taskstring, taskfile, rawline, daystring = task
                
                if lastxpos != xpos:
                    lastxpos = xpos
                    for i in range(lastgpos):
                        gyposdata.append(lastgpos)
                lastgpos = gypos
                
                
                
                if gypos > highestypos:
                    highestypos = gypos
                
                
                
                if under:
                    underwas = True
            
            for i in range(lastgpos):
                        gyposdata.append(lastgpos)
            
            
            
            draw_date_data = True
            
            thisposeditable  = 1
            isty = w / elementsX - border
            chekedmovethingidk = True
            insersto = -1
            
            for tind, task in enumerate(self.schedule):
            
                today, over, under, xpos, ypos, gypos, done, taskstring, taskfile, rawline, daystring = task
            
                
                thisypos = gypos
                
                
                gxpos = int(float(w)*xpos) - int(float(w)/self.alltime)+1
                gypos = h - int(float(ubY)/highestypos*gypos) 
                
                
                
                bgxpos = int(xpos*self.alltime*20 +self.scroll) +20
                bgypos = bstY+bubY - int(float(bubY)/highestypos*thisypos)
                
                
                
                #if today:
                #    #xgc.set_rgb_fg_color(gtk.gdk.color_parse("#1c1c1c"))
                #    #widget.window.draw_rectangle(xgc, True, w/2, h/2-10, gxpos-w/2, h/4 )
                #    
                #    ctx3.set_source_rgba(0,0,0,0.1)
                #    ctx3.rectangle(w/2, h/2-10,  gxpos-w/2, h/4)
                #    ctx3.fill()
                
                
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#395384"))
                ctx3.set_source_rgba(0,0,0.5,0.5)
                
                if under:
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#e13d3d"))
                    ctx3.set_source_rgba(0.5,0,0,0.5)
                
                if rawline.startswith(datetime.datetime.today().strftime(self.schedule_date_format)):
                    ctx3.set_source_rgba(0,0,0,0.5)
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#000"))
                
                if rawline.startswith(self.selectdate):
                    ctx3.set_source_rgba(0.5,0.5,0.5,0.5)
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#aaa"))
                
                
                    
                if self.tooly in range(stY, h) and "GDK_BUTTON1" in str(fx) and win.is_active():
                    if gxpos in range( self.toolx, mx ) or gxpos in range( mx, self.toolx ):
                        
                        rulerdata["scheduled"]   = rulerdata["scheduled"] + 1  
                    
                        
                    
                widget.window.draw_rectangle(xgc, True, gxpos, gypos, int(float(w)/self.alltime)+1, int(float(ubY)/highestypos) )
                #widget.window.draw_rectangle(xgc, True, bgxpos, bgypos, 20, int(float(bubY)/highestypos) )
                
                ctx3.rectangle(bgxpos, bgypos,  20, int(float(bubY)/highestypos))
                ctx3.fill()
                
                
                
                #Lines to separate each task's number 
                #xgc.set_line_attributes(4, gtk.gdk.LINE_ON_OFF_DASH, gtk.gdk.CAP_NOT_LAST, gtk.gdk.JOIN_MITER)
                #xgc.set_rgb_fg_color(gtk.gdk.color_parse("#aaa"))
                #xgc.line_width = 1
                #widget.window.draw_line(xgc, todayongrapth+5, gypos, w, gypos)    
                #xgc.set_line_attributes(2, gtk.gdk.LINE_SOLID, gtk.gdk.CAP_NOT_LAST, gtk.gdk.JOIN_MITER)
                
                #ctx.set_source_rgb(1,1,1)
                #ctx.set_font_size(10)
                #ctx.move_to( w-10, gypos+10)
                #ctx.show_text(str(thisypos))
                
                xgc.line_width = 1
                
                # outputting data if mouse over the dategrapth
                
                
                if my in range(bstY, stY) and mx in range(bgxpos, bgxpos+20) and draw_date_data:
                    
                    tmp = gxpos
                    btmp = bgxpos
                    movedmx = 0
                    if gxpos + 180 > w:
                        gxpos = gxpos - 180
                        movedmx = 180
                    
                    bgxpos = bgxpos + 20
                    bstmp = bstY
                    bstY = bstY + 30
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#1c1c1c"))
                    widget.window.draw_rectangle(xgc, True , gxpos+2+int(float(w)/self.alltime)+3, stY, 20, 10) 
                    
                    widget.window.draw_rectangle(xgc, True , bgxpos+2, bstY-30, 180+4, 100) 
                    
                    busyness =  1.0 / highestypos * gyposdata[tind] 
                    
                    #Busyness Percentage progress bar
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#aaa"))
                    widget.window.draw_rectangle(xgc, False, gxpos+movedmx, stY, int(float(w)/self.alltime)+1, h )
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#d0d0d0"))
                    widget.window.draw_rectangle(xgc, True, bgxpos+4, bstY-28, 100, 5 )
                    
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
                    widget.window.draw_rectangle(xgc, True, bgxpos+4, bstY-28, int(100*busyness), 5 )
                    
                    # when
                    ctx.set_source_rgb(1,1,1)
                    ctx.set_font_size(10)
                    ctx.move_to( bgxpos+4, bstY+2+15)
                    if not today:
                        ctx.show_text(daystring)
                    else:
                        ctx.show_text("Today")
                    
                    
                    #how many
                    ctx.set_source_rgb(1,1,1)
                    ctx.set_font_size(10)
                    ctx.move_to( bgxpos+4, bstY+2+25)
                    ctx.show_text("Scheduled : "+str(gyposdata[tind] )+" tasks")
                    
                    #how many
                    ctx.set_source_rgb(1,1,1)
                    ctx.set_font_size(10)
                    ctx.move_to( bgxpos+4, bstY+2+35)
                    ctx.show_text("Maximum Scheduled : "+str(highestypos)+" tasks")
                    
                    # how busy
                    ctx.set_source_rgb(1,1,1)
                    ctx.set_font_size(10)
                    ctx.move_to( bgxpos+4, bstY+2+45)
                    ctx.show_text("From maximum : "+str(int(busyness*100))+"%")
                    
                    
                    
                    if gyposdata[tind] == thisypos:
                    
                    
                        draw_date_data = False
                
                    gxpos = tmp
                    bgxpos = btmp
                    bstY = bstmp
                    
                tstX = border/2 + w / elementsX
                tstY = 0
                tubX = w / elementsX - border
                tubY = h / elementsY - border
                
                
                
                
                
                xpos = tstX + border / 2#int(w*xpos)-5
                ypos = tubY - (thisposeditable*45) + self.tscroll
                
                
                #thisposeditable = thisposeditable + 1
                
                
                
                if today or over:
                    
                    if not rawline.startswith(self.selectdate) and self.selectdate != datetime.datetime.today().strftime(self.schedule_date_format) and over:
                        if not rawline.startswith("1997/07/30"):
                            continue
                    
                     
                    
                    chekedmovethingidk = True
                    
                    # STUFF RELATED TO MOVING TASKS
                    
                    #RESEALE MOVING
                    
                    if my in range(ypos, ypos+45) and self.taskmove != -1 and not over:
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#aaa"))
                        widget.window.draw_rectangle(xgc, False, xpos-1, ypos, tubX, 45 )
                        
                        insersto = tind
                        #tooltip = str(insersto)
                    
                    
                    #MOVING THEM UP
                    
                    if self.taskmove != -1 and my > ypos:
                        ypos = ypos - 45
                    
                    # IF IN MOVING
                    if self.taskmove == tind:
                        xpos = mx - tubX+22+46
                        ypos = my - 11
                    else:
                        thisposeditable = thisposeditable + 1
                        pass
                    
                    
                    
                    
                    
                    if ypos < tstY + tubY - 44 or self.taskmove == tind:
                        
                        
                        # DRAWING THE TASKS 
                        
                        istx = xpos
                        isty = tubX - border*2  - 10    #len(taskstring)*9+5
                        isty2 = len(taskfile)*9+50+22
                        if taskfile != "project.progress" and taskfile.startswith("/dev/"):
                            #we need to get type of the file the CUR
                            isty2 = (len(taskfile[9:taskfile.rfind("/")]))*9+50+22
                        
                        if istx + len(taskstring)*9+5 > w:
                            istx = w-(len(taskstring)*9+5)
                        if istx + len(taskfile)*9 > w:
                            istx = w-len(taskfile)*9
                        
                        if rawline.startswith("1997/07/30"):
                            ctx3.set_source_rgba(0.1,0.3,0.1,0.75)
                            daystring = "Always"
                        elif today:
                            ctx3.set_source_rgba(0.1,0.1,0.1,0.75)
                        elif under:
                            ctx3.set_source_rgba(0.3,0.1,0.1,0.75)
                        elif over and not under:
                            ctx3.set_source_rgba(0.1,0.1,0.3,0.75)
                        ctx3.rectangle(xpos-1, ypos, isty+22, 42)
                        ctx3.fill()
                        
                        #ctx3.rectangle(xpos+isty+44, ypos, isty2+22, 22)
                        #ctx3.fill()
                        
                        if over:
                            #ctx3.rectangle(xpos+isty+isty2+44+44, ypos, len(daystring)*9+22, 22)
                            #ctx3.fill()
                            
                            ctx.set_source_rgb(1,1,1)
                            ctx.set_font_size(15)
                            ctx.move_to( xpos+isty-150, ypos+16)
                            ctx.show_text(daystring)
                        
                        if mx in range(xpos-1, xpos+isty+22) and my in range(ypos+22, ypos+44) and self.taskmove == -1:
                            
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#4f4f4f"))
                            widget.window.draw_rectangle(xgc, True, xpos-1, ypos+22, isty, 22 )
                            tooltip = "Open Checklist"
                            
                            if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and win.is_active(): ## IF CLICKED
                                
                                if taskfile == "project.progress":
                                    checklist.checkwindow(pf=self.pf, title="[ "+taskstring[taskstring.rfind("/")+1:]+" ] in ", FILE=taskfile, highlight=rawline)
                                else:
                                    checklist.checkwindow(pf=self.pf, title="[ "+taskstring[taskstring.rfind("/")+1:]+" ] in ", FILE=self.pf+taskfile, highlight=rawline)
                        
                        
                        
                        # ICON OF THE TYPE OF ITEM OF THE CHECKLIST
                        needicon = self.checklist
                        
                        if taskfile.startswith("/dev/chr"):
                            needicon = self.chricon
                        elif taskfile.startswith("/dev/veh"):
                            needicon = self.vehicon
                        elif taskfile.startswith("/dev/loc"):
                            needicon = self.locicon
                        elif taskfile.startswith("/dev/obj"):
                            needicon = self.objicon
                        elif taskfile.startswith("/rnd/"):
                            needicon = self.scnicon
                        # IF WE HAVE AN ITEM
                        
                        if taskfile != "project.progress" and taskfile.startswith("/dev/") or taskfile.startswith("/rnd/") :
                            #we need to get type of the file the CUR
                            CUR = taskfile[5:8]
                            
                            
                            name = taskfile[9:taskfile.rfind("/")]
                            
                            
                            if taskfile.startswith("/rnd/"):
                                CUR = "rnd"
                            
                            
                                name = taskfile[5:taskfile.rfind("/")].replace("/", " > ")
                            
                                
                            
                            taskfile = name
                            
                            
                            
                            
                        
                            if mx in range(xpos-1, xpos+isty-44) and my in range(ypos, ypos+22) and self.taskmove == -1: #IF MOUSE OVER
                                
                                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#4f4f4f"))
                                widget.window.draw_rectangle(xgc, True, xpos-1, ypos, isty-44, 22 )
                                tooltip = "Go to "+name
                            
                                if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and win.is_active(): ## IF CLICKED
                            
                                    #CUR = "veh"
                                     
                                    
                                    self.box.destroy()
                                    
                                    
                                    self.box = gtk.VBox(False)
                                    self.mainbox.pack_start(self.box, True)
                                    
                                    print CUR, "CUR"
                                
                                    if CUR == "rnd":
                                        
                                        gscene = taskfile[:taskfile.find(" > ")]
                                        gshot = taskfile[taskfile.rfind(" > ")+3:]
                                        
                                        
                                        story_editor.story(os.getcwd(), self.box, self.win, self.mainbox, scene=gscene, shot=gshot)
                                    else:
                                        assets.draw_assets(os.getcwd(), self.box, self.win, CUR, name, mainbox=self.mainbox)
                                        
                                        
                                    
                        
                        
                        ctx.set_source_rgb(1,1,1)
                        ctx.set_font_size(10)
                        ctx.move_to( istx+22, ypos+16+20)
                        ctx.show_text(taskstring)
                        
                        ctx.set_font_size(15)
                        ctx.move_to( istx+30+44, ypos+16)
                        
                        if taskfile == "project.progress":
                            ctx.show_text("Main Checklist")
                        else:
                            ctx.show_text(taskfile)
                        
                        widget.window.draw_pixbuf(None, needicon, 0, 0, istx+44, ypos-1 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                        widget.window.draw_pixbuf(None, self.scheduleicon, 0, 0, istx, ypos-1 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
                        
                        showtooltip = False
                        
                        
                        if mx in range(tubX+tstX-24, tubX+tstX-24+22) and my in range(ypos, ypos+22) and self.taskmove == -1: #IF MOUSE OVER
                                
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#4f4f4f"))
                            widget.window.draw_rectangle(xgc, True, tubX+tstX-24, ypos, 22, 22 )
                            
                            tooltip = "Delete The Task"
                            
                            if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and win.is_active(): ## IF CLICKED
                                
                                print "TRYING TO DELETE", rawline
                                removing = rawline
                                
                                o = open(self.pf+"/schedule.data","r")
                                o = o.read().split("\n")
                                
                                if o[-1] == "":
                                    o = o[:-1]
                                
                                try:
                                    #print removing, "REMOVING"
                                    #print self.FILENAME.replace(self.pf, ""), "FILEPATH"
                                    
                                    for i in o:
                                        if i.endswith(removing):
                                            o.remove(i)
                                    
                                    
                                    
                                    s = open(self.pf+"/schedule.data","w")
                                    for i in o:
                                        #print i
                                        s.write(i+"\n")
                                    s.close()
                                    #self.highlight = None
                                except Exception as e:
                                    print "WTF", e
                        
                        if self.taskmove == -1:
                            widget.window.draw_pixbuf(None, self.deleteicon, 0, 0, tubX+tstX-21, ypos+3 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                        
                        
                        
                        if mx in range(tubX+tstX-24-44, tubX+tstX-24-44+22) and my in range(ypos, ypos+22) and self.taskmove == -1 and not over: #IF MOUSE OVER
                                
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#4f4f4f"))
                            widget.window.draw_rectangle(xgc, True, tubX+tstX-24-44, ypos, 22, 22 )
                            
                            tooltip = "Move the Task"
                            
                            if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and win.is_active(): ## IF CLICKED
                                self.taskmove = tind
                        
                        if self.taskmove == -1 and not over:
                            widget.window.draw_pixbuf(None, self.moveicon, 0, 0, tubX+tstX-22-46, ypos+1 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                    
                    
                else:
                            
                    if my in range(ypos, ypos+45) and self.taskmove != -1 and chekedmovethingidk:
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#aaa"))
                        widget.window.draw_rectangle(xgc, False, xpos-1, ypos, tubX, 45 )
                        
                        
                        insersto = tind
                        #tooltip = str(insersto)
                        
                        chekedmovethingidk = False
            
            
            if insersto != -1 and "GDK_BUTTON1" not in str(fx) and "GDK_BUTTON1" in str(self.mpf) and self.taskmove != -1:
                
                
                o = []
                neededline = ""
                #get data from file
                for tind, task in enumerate(self.schedule):
                    today, over, under, xpos, ypos, gypos, done, taskstring, taskfile, rawline, daystring = task
                    
                    if self.taskmove == tind:
                        
                        o.append("")
                        neededline = rawline
                    else:
                        o.append(rawline)
                
                
                o.insert(insersto, neededline)
                
                
                for i in o:
                    print i
                
                
                
                
                
                s = open(self.pf+"/schedule.data","w")
                for task in o:
                    if task != "":
                        s.write(task+"\n")
                
                s.close()
                
            
            ################################################################  OLD CODE #########################################################
            
            # MOTIVATION THING
            
            #stars = 0    #testing for the new project
            
            bnowW = 0            
            
            ctx3.set_source_rgba(0,0,0,0.75)
            ctx3.rectangle( bnowW+30-5, bstY+bubY-100+30-5, 250, 75)
            ctx3.fill()
            
            ctx.set_source_rgb(1,1,1)
            ctx.set_font_size(15)
            ctx.move_to( bnowW+30,  bstY+bubY-80+30)
            ctx.show_text("We've got     X "+str(stars))
            
            widget.window.draw_pixbuf(None, self.staricon, 0, 0, bnowW+135, bstY+bubY-80+13 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
            
            if stars > 0:
                ctx.set_source_rgb(1,1,1)
                ctx.set_font_size(15)
                ctx.move_to( bnowW+30,  bstY+bubY-80+30+20)
                ctx.show_text("We can make   X "+str(int(stars*1.5)))
            else:
                ctx.set_source_rgb(1,1,1)
                ctx.set_font_size(15)
                ctx.move_to( bnowW+30,  bstY+bubY-80+30+20)
                ctx.show_text("We can make   X 1")
            widget.window.draw_pixbuf(None, self.staricon, 0, 0, bnowW+135, bstY+bubY-80+13+20 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
            
            ctx.set_source_rgb(1,1,1)
            ctx.set_font_size(15)
            ctx.move_to( bnowW+30,  bstY+bubY-80+30+40)
            ctx.show_text(justdoitsting)
            
            
            
            
            fif = datetime.datetime.now()
            mil  = fif - stf
            perfStat.append([ "SCHEDULE GRAPH - ", mil.microseconds])
            
            stf = datetime.datetime.now()
            
            
            
            
            #if self.taskmove != -1:
            #    tooltip = "Moving "+str(self.taskmove)
            
                
            
            ### SELECTABLE DAY
            notfound = True
            
            for i in range(0-self.scroll/20,  self.alltime+3):
                
                #i = i + 1
                
                if  i*20-20+self.scroll > w:
                    break
                
                if  i*20-20+self.scroll in range(10, w - 10) and i > 1:
                    
                    notfound = False
                
                    selectingdate = datetime.datetime.strftime(datetime.datetime.strptime(self.startdate, date_format)+datetime.timedelta(days=i-2), self.schedule_date_format)
                    
                    
                    if selectingdate == datetime.datetime.strftime(datetime.datetime.strptime(self.startdate, date_format), self.schedule_date_format):
                        
                        ctx3 = widget.window.cairo_create()
                        ctx3.set_source_rgba(0,0,0,0.5)
                        ctx3.rectangle(0, bstY, i*20-20+self.scroll, bubY)
                        ctx3.fill()
                    
                    elif selectingdate == datetime.datetime.strftime(datetime.datetime.strptime(self.enddate, date_format), self.schedule_date_format):
                        
                        ctx3 = widget.window.cairo_create()
                        ctx3.set_source_rgba(0,0,0,0.5)
                        ctx3.rectangle(i*20+self.scroll, bstY, w-self.scroll, bubY)
                        ctx3.fill()
                    
                    if selectingdate == datetime.datetime.strftime(datetime.datetime.today(), self.schedule_date_format):
                        xgc.set_line_attributes(4, gtk.gdk.LINE_ON_OFF_DASH, gtk.gdk.CAP_NOT_LAST, gtk.gdk.JOIN_MITER)
                        xgc.line_width = 1
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#aaa"))
                        widget.window.draw_rectangle(xgc, False, i*20-20+self.scroll, bstY, 20, bubY)
                        xgc.set_line_attributes(2, gtk.gdk.LINE_SOLID, gtk.gdk.CAP_NOT_LAST, gtk.gdk.JOIN_MITER)
                    
                    if my in range(bstY, bstY+bubY) and mx in range(i*20-20+self.scroll, i*20+self.scroll):
                        xgc.line_width = 1
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#fff"))
                        widget.window.draw_rectangle(xgc, False, i*20-20+self.scroll, bstY, 20, bubY)
                        
                        
                        
                        
                        
                        ctx.set_source_rgb(1,1,1)
                        ctx.set_font_size(10)
                        ctx.move_to( i*20+5+self.scroll, bstY+20)
                        if selectingdate == datetime.datetime.strftime(datetime.datetime.today(), self.schedule_date_format):
                            ctx.show_text("Today")
                        else:
                            ctx.show_text(selectingdate)
                        
                        # SELECTING THE DAY
                        if "GDK_BUTTON1" in str(fx) and win.is_active() and self.taskmove == -1: ## IF CLICKED
                            self.selectdate = selectingdate
                            self.hscroll = 0
                            self.tscroll = 0
                        
                        # Moving taks around
                        if "GDK_BUTTON1" not in str(fx) and "GDK_BUTTON1" in str(self.mpf) and self.taskmove != -1:
                            
                            
                            
                            
                            o = []
                            
                            #get data from file
                            for tind, task in enumerate(self.schedule):
                                today, over, under, xpos, ypos, gypos, done, taskstring, taskfile, rawline, daystring = task
                                if self.taskmove == tind:
                                    
                                    newline = selectingdate + rawline[rawline.find(" "):]
                                    
                                    
                                    o.append(newline)
                                else:
                                    o.append(rawline)
                            
                            
                            #o.append(newline)
                                
                            # SORTING WHEN ADDING
                            try:
                                dl = []
                                d = o[0][:o[0].find(" ")]
                                tdl = []
                                for task in o:
                                    if task[:task.find(" ")] == d:
                                        tdl.append(task)
                                        
                                    
                                    else:
                                        #if newline[:newline.find(" ")] == d:
                                        #    tdl.append(newline)
                                        dl.append(tdl)
                                        tdl = []
                                        tdl.append(task)
                                        d = task[:task.find(" ")]
                                
                                
                                dl.append(tdl)
                                tdl = []
                                tdl.append(task)
                                d = task[:task.find(" ")]
                                        
                                
                                dl = sorted(dl)
                                
                                o = []
                                for task in dl:
                                    for b in task:
                                        
                                        if b != "":
                                            o.append(b)
                                        
                            except Exception as c:
                                
                                
                                o = sorted(o)
                            
                            
                            s = open(self.pf+"/schedule.data","w")
                            for task in o:
                                s.write(task+"\n")
                            
                            s.close()
                            
                            
                            
                            
                        
                    if self.selectdate == selectingdate:
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
                        widget.window.draw_rectangle(xgc, False, i*20-20+self.scroll, bstY, 20, bubY)
                        ctx.set_source_rgb(1,0.7,0.5)
                        ctx.set_font_size(10)
                        ctx.move_to( i*20+5+self.scroll, bstY+10)
                        if selectingdate == datetime.datetime.strftime(datetime.datetime.today(), self.schedule_date_format):
                            ctx.show_text("Today")
                        else:
                            ctx.show_text(selectingdate)
                    actualthign = 0
                    for jjabrams in range(10):
                        if my in range(bstY, bstY+(bubY/10*jjabrams)):
                            actualthign = actualthign + 20
                    
                    if my in range(bstY, bstY+bubY) and mx in range(i*20-20+self.scroll-actualthign, i*20+self.scroll+actualthign):
                        if selectingdate in self.dateicons:
                        
                            
                            hdata = self.dateicons[selectingdate]
                         
                               
                            for n, p in enumerate(hdata):
                                
                                widget.window.draw_pixbuf(None, p, 0, 0, i*20-20+self.scroll, bstY+bubY-n*20-22 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                        else:    
                            needicon = False
                            hdata = []
                            found = False
                            for n, l in enumerate(hf.split("\n")[::-1]):
                                
                                if l.startswith(selectingdate):
                                    if "Scheduled" in l:
                                        needicon = self.scheduleicon
                                    elif "/rnd/" in l:
                                        needicon = self.scnicon
                                    elif "/obj/" in l:
                                        needicon = self.objicon
                                    elif "/chr/" in l:
                                        needicon = self.chricon
                                    elif "/loc/" in l:
                                        needicon = self.locicon
                                    elif "/veh/" in l:
                                        needicon = self.vehicon
                                    elif ".progress" in l:
                                        needicon = self.checklist
                                    
                                    if needicon not in hdata and needicon:
                                        hdata.append(needicon)
                           
                                    self.dateicons[selectingdate] = hdata
                                    found = True
                            if not found:
                                self.dateicons[selectingdate] = hdata
                            
            fif = datetime.datetime.now()
            mil  = fif - stf
            perfStat.append([ "DATES AND TINY ICONS - ", mil.microseconds])
            
            stf = datetime.datetime.now()
            
            #MIDDLE LINE
            xgc.set_line_attributes(4, gtk.gdk.LINE_ON_OFF_DASH, gtk.gdk.CAP_NOT_LAST, gtk.gdk.JOIN_MITER)
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#aaa"))
            xgc.line_width = 1
            #widget.window.draw_line(xgc, w/2, bstY, w/2, bstY+bubY)    
            xgc.set_line_attributes(2, gtk.gdk.LINE_SOLID, gtk.gdk.CAP_NOT_LAST, gtk.gdk.JOIN_MITER)
            
            
            #BOTTOM SCROLLING SELECTION WIDGET
            
            
            position = int((float(w)/self.alltime) * (1-float(self.scroll+40)/20))
            size = int((float(w)/self.alltime) * (w/20))
            
            
            #MIDDLE LINE
            xgc.set_line_attributes(4, gtk.gdk.LINE_ON_OFF_DASH, gtk.gdk.CAP_NOT_LAST, gtk.gdk.JOIN_MITER)
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#aaa"))
            xgc.line_width = 1
            #widget.window.draw_line(xgc, position+size/2, stY-1, position+size/2, stY-1+ubY-6)    
            xgc.set_line_attributes(2, gtk.gdk.LINE_SOLID, gtk.gdk.CAP_NOT_LAST, gtk.gdk.JOIN_MITER)
            
            xgc.line_width = 1
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#fff"))
            #widget.window.draw_rectangle(xgc, False, position, stY-1, size,ubY-6)
            
            if notfound:
                ctx3 = widget.window.cairo_create()
                ctx3.set_source_rgba(0,0,0,0.5)
                ctx3.rectangle(0, bstY, w, bubY)
                ctx3.fill()
                ctx3.set_source_rgba(0,0,0,0.5)
                ctx3.rectangle(0, stY, w, h)
                ctx3.fill()
                
                
                
            else:
                
                ctx3 = widget.window.cairo_create()
                ctx3.set_source_rgba(0,0,0,0.5)
                ctx3.rectangle(0, stY, position, h)
                ctx3.fill()
                ctx3.set_source_rgba(0,0,0,0.5)
                ctx3.rectangle(size+position, stY, w, h)
                ctx3.fill()
            
            
            if my in range(stY, h):
                if "GDK_BUTTON2" in str(fx) and win.is_active(): ## IF DRAGGED
                    self.scroll = int(float(20*self.alltime)/w*(mx-size/2)) * -1          
             
            
            
            
            rulerdata["days"] = 0
            rulerdata["expected"] = 0
            
            if self.tooly in range(stY, h) and "GDK_BUTTON1" in str(fx) and win.is_active():
                
                t1 = self.toolx
                t2 = mx
                if mx < self.toolx:
                    t2 = self.toolx
                    t1 = mx
                
                
                
                rulerdata["days"]     = int(float(self.alltime) / w  * (t2 - t1))
                rulerdata["expected"] =     float(100)          / w  * (t2 - t1)
                
                xgc.line_width = 1
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#fff"))
                widget.window.draw_line(xgc, self.toolx, h-10, mx+1, h-10) 
                
                if t2 - t1 > 10:
                
                    widget.window.draw_line(xgc, t1, h-10, t1+6, h-10-6) 
                    widget.window.draw_line(xgc, t1, h-10, t1+6, h-10+6) 
                    widget.window.draw_line(xgc, t2, h-10, t2-5, h-10-5) 
                    widget.window.draw_line(xgc, t2, h-10, t2-5, h-10+5)
                
                ctx3.set_source_rgba(0,0,0,0.75)
                ctx3.rectangle( (t1+t2)/2-(len(str(int(rulerdata["percent"]))+" delivered")*6/2)-10,h-20-55, (len(str(int(rulerdata["percent"]))+" delivered")*6)+25, 50)
                ctx3.fill()
                
                ctx.set_source_rgb(1,1,1)
                ctx.set_font_size(10)
                ctx.move_to( (t1+t2)/2-(len(str(int(rulerdata["days"]))+" days")*6/2), h-20-40)
                ctx.show_text(str(int(rulerdata["days"]))+" days")
                
                ctx.set_source_rgb(1,1,1)
                ctx.set_font_size(10)
                ctx.move_to( (t1+t2)/2-(len(str(int(rulerdata["expected"]))+"% expected")*6/2), h-20-30)
                ctx.show_text(str(int(rulerdata["expected"]))+"% expected")
                
                ctx.set_source_rgb(1,1,1)
                ctx.set_font_size(10)
                ctx.move_to( (t1+t2)/2-(len(str(int(rulerdata["percent"]))+"% delivered")*6/2), h-20-20)
                ctx.show_text(str(int(rulerdata["percent"]))+"% delivered")
                
                ctx.set_source_rgb(1,1,1)
                ctx.set_font_size(10)
                ctx.move_to( (t1+t2)/2-(len(str(int(rulerdata["scheduled"]))+" tasks")*6/2), h-20-10)
                ctx.show_text(str(int(rulerdata["scheduled"]))+" tasks")               
            
                
            
            
             
            # LIST OF THINGS TOOLTIP
            if drawhistory:
            
                for p, d in enumerate(hlist[drawhistory]):
                    
                    tmp = n, l, ypart, stX, ubX
                    n = p
                    l = d
                    stX = mx
                    ubX = w/3
                    
                    
                    t = l[11:20]
                    
                    ypart = my + n*20
            
                    while ypart > h-10:
                        ypart = ypart - (h - my)
                        stX = stX - ubX
                
                
                    ctx3.set_source_rgba(0,0,0,0.75)
                    ctx3.rectangle(stX+border/2, ypart-20,  ubX-border, 20)
                    ctx3.fill()
                    
                    ypart = ypart - 5
                    
                    ctx.set_source_rgb(0.8,0.8,1)
                    ctx.set_font_size(15)
                    ctx.move_to( stX+border/2+2, ypart)
                    ctx.show_text(t)
                    
                    
                    needicon = self.scnicon
                    if "obj" in l:
                        needicon = self.objicon
                    elif "chr" in l:
                        needicon = self.chricon
                    elif "loc" in l:
                        needicon = self.locicon
                    elif "veh" in l:
                        needicon = self.vehicon
                    
                    if "pln/main.bos" in l:
                        
                        widget.window.draw_pixbuf(None, self.scnicon, 0, 0, stX+104-24, ypart-17, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                        
                        ctx.set_source_rgb(1,1,1)
                        ctx.set_font_size(15)
                        ctx.move_to( stX+104, ypart)
                        ctx.show_text("Edited Story")
                    
                    elif "Project Started" in l:
                        
                        ctx.set_source_rgb(0,1,0)
                        ctx.set_font_size(15)
                        ctx.move_to( stX+104, ypart)
                        ctx.show_text("Ready for work ; )")
                    
                    elif "Project Exited" in l:
                        
                        ctx.set_source_rgb(1,0,0)
                        ctx.set_font_size(15)
                        ctx.move_to( stX+104, ypart)
                        ctx.show_text("Where are you going :`(")
                    
                    
                    
                    elif "[Added Asset]" in l:
                        widget.window.draw_pixbuf(None, needicon, 0, 0, stX+104-24, ypart-17, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                        ctx.set_source_rgb(1,1,1)
                        ctx.set_font_size(15)
                        ctx.move_to( stX+104, ypart)
                        ctx.show_text("New : "+l[l.find("/dev/")+9:l.rfind("[")])
                    
                    elif "autolink.data" in l:
                        widget.window.draw_pixbuf(None, needicon, 0, 0, stX+104-24, ypart-17, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                        
                        nameofasset = l[l.find("/dev/")+9:l.rfind("autolink.data")-1]
                        ctx2.set_source_rgb(1,1,1)
                        ctx2.set_font_size(15)
                        ctx2.move_to( stX+104, ypart)
                        ctx2.show_text(nameofasset)
                        
                        sp = len(nameofasset)*9 + 30
                        
                        widget.window.draw_pixbuf(None, self.settingsicon, 0, 0, stX+104-24+sp, ypart-17, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                        
                        ctx.set_source_rgb(1,1,1)
                        ctx.set_font_size(10)
                        ctx.move_to( stX+170-48+sp, ypart)
                        ctx.show_text("Asset Configured")
                    
                    elif "/dev/" in l and ".progress" in l:
                        widget.window.draw_pixbuf(None, needicon, 0, 0, stX+104-24, ypart-17, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                        
                        nameofasset = l[l.find("/dev/")+9:l.rfind("asset.progress")-1]
                        ctx2.set_source_rgb(1,1,1)
                        ctx2.set_font_size(15)
                        ctx2.move_to( stX+104, ypart)
                        ctx2.show_text(nameofasset)
                        
                        sp = len(nameofasset)*9 + 30
                        
                        widget.window.draw_pixbuf(None, self.checklist, 0, 0, stX+104-24+sp, ypart-17, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                        if "[V]" in l:
                            widget.window.draw_pixbuf(None, self.okicon, 0, 0, stX+150-48+sp, ypart-17-4, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                        elif "Scheduled" in l:
                            
                            widget.window.draw_pixbuf(None, self.scheduleicon, 0, 0, stX+150-48+sp, ypart-17, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                            
                        else:
                            ctx3.set_source_rgba(1,1,1,0.4)
                            ctx3.rectangle(stX+152-48+sp, ypart-17+6,  12, 12)
                            ctx3.fill()
                        
                        ctx.set_source_rgb(1,1,1)
                        ctx.set_font_size(10)
                        ctx.move_to( stX+170-48+sp, ypart)
                        ctx.show_text(l[l.find(".progress ")+9:l.find("[")].replace("=:>", " > "))
                   
                    elif "/rnd/" in l and ".progress" in l:
                        widget.window.draw_pixbuf(None, needicon, 0, 0, stX+104-24, ypart-17, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                        
                        nameofasset = l[l.find("/rnd/")+5:l.rfind("shot.progress")-1]
                        ctx2.set_source_rgb(1,1,1)
                        ctx2.set_font_size(10)
                        ctx2.move_to( stX+104, ypart)
                        ctx2.show_text(nameofasset)     
                        
                        sp = len(nameofasset)*6 + 30
                        
                        
                        widget.window.draw_pixbuf(None, self.checklist, 0, 0, stX+104-24+sp, ypart-17, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                        if "[V]" in l:
                            widget.window.draw_pixbuf(None, self.okicon, 0, 0, stX+150-48+sp, ypart-17-4, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                        elif "Scheduled" in l:
                            
                            widget.window.draw_pixbuf(None, self.scheduleicon, 0, 0, stX+150-48+sp, ypart-17, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                        else:
                            ctx3.set_source_rgba(1,1,1,0.4)
                            ctx3.rectangle(stX+152-48+sp, ypart-17+6,  12, 12)
                            ctx3.fill()
                        
                        ctx.set_source_rgb(1,1,1)
                        ctx.set_font_size(10)
                        ctx.move_to( stX+170-48+sp, ypart)
                        ctx.show_text(l[l.find(".progress ")+9:l.find("[")].replace("=:>", " > "))
                        
                        
                    
                    elif ".progress" in l:
                        
                        widget.window.draw_pixbuf(None, self.checklist, 0, 0, stX+104-24, ypart-17, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                        if "[V]" in l:
                            widget.window.draw_pixbuf(None, self.okicon, 0, 0, stX+150-48, ypart-17-4, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                        elif "Scheduled" in l:
                            
                            widget.window.draw_pixbuf(None, self.scheduleicon, 0, 0, stX+150-48, ypart-17, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                        
                        else:
                            ctx3.set_source_rgba(1,1,1,0.4)
                            ctx3.rectangle(stX+152-48, ypart-17+6,  12, 12)
                            ctx3.fill()
                        
                        
                        ctx.set_source_rgb(1,1,1)
                        ctx.set_font_size(10)
                        ctx.move_to( stX+170-48, ypart)
                        ctx.show_text(l[l.find(".progress ")+9:l.find("[")].replace("=:>", " > "))
                    
                    
                    elif "/dev/" in l and ".blend" in l:
                        widget.window.draw_pixbuf(None, needicon, 0, 0, stX+104-24, ypart-17, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                        
                        nameofasset = l[l.find("/dev/")+9:l.rfind("[")-1]
                        nameofasset, blendfile = nameofasset.split("/")
                        ctx2.set_source_rgb(1,1,1)
                        ctx2.set_font_size(15)
                        ctx2.move_to( stX+104, ypart)
                        ctx2.show_text(nameofasset)
                        
                        sp = len(nameofasset)*9 + 30
                        
                        widget.window.draw_pixbuf(None, self.blendericon, 0, 0, stX+150-48+sp, ypart-17, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                        
                        ctx.set_source_rgb(1,1,1)
                        ctx.set_font_size(10)
                        ctx.move_to( stX+104+sp+22, ypart)
                        ctx.show_text(blendfile+"  "+l[l.rfind("[")+1:l.rfind("]")])
                    
                    
                        
                    elif "/ast/" in l and ".blend" in l:
                        widget.window.draw_pixbuf(None, needicon, 0, 0, stX+104-24, ypart-17, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                        
                        nameofasset = l[l.find("/ast/")+9:l.rfind("[")-1]
                        ctx2.set_source_rgb(1,1,1)
                        ctx2.set_font_size(15)
                        ctx2.move_to( stX+104, ypart)
                        ctx2.show_text(nameofasset.replace(".blend", ""))
                        
                        
                        sp = len(nameofasset)*9 + 30
                        
                        ctx3.set_source_rgba(0.4,0,0.6,0.5)
                        ctx3.rectangle(stX+border/2+22+sp, ypart-15,  ubX-border-22-sp, 20)
                        ctx3.fill()
                        
                        
                        widget.window.draw_pixbuf(None, self.blendericon, 0, 0, stX+150-48+sp, ypart-17, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                        
                        ctx.set_source_rgb(1,1,1)
                        ctx.set_font_size(10)
                        ctx.move_to( stX+104+sp+22, ypart)
                        ctx.show_text(nameofasset+"  "+l[l.rfind("[")+1:l.rfind("]")])
                    
                    elif "/rnd/" in l and ".blend" in l:
                        widget.window.draw_pixbuf(None, needicon, 0, 0, stX+104-24, ypart-17, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0) 
                        
                        nameofasset = l[l.find("/rnd/")+5:l.rfind("[")-1]
                        
                        blendfile = nameofasset[nameofasset.rfind("/")+1:]
                        nameofasset = nameofasset[:nameofasset.rfind("/")]
                        
                        ctx2.set_source_rgb(1,1,1)
                        ctx2.set_font_size(15)
                        ctx2.move_to( stX+104, ypart)
                        ctx2.show_text(nameofasset)
                        
                        sp = len(nameofasset)*9 + 30
                        
                        widget.window.draw_pixbuf(None, self.blendericon, 0, 0, stX+150-48+sp, ypart-17, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)
                        
                        ctx.set_source_rgb(1,1,1)
                        ctx.set_font_size(10)
                        ctx.move_to( stX+104+sp+22, ypart)
                        ctx.show_text(blendfile+"  "+l[l.rfind("[")+1:l.rfind("]")])
                    
                    else:
                        ctx.set_source_rgb(1,1,1)
                        ctx.set_font_size(15)
                        ctx.move_to( stX+104, ypart)
                        ctx.show_text("["+l[21:]+"]")
                    
                    
                    
                    
                    
                    n, l, ypart, stX, ubX = tmp
             
             
                 
            ##### TOOLTIP
            
            
            
            if tooltip:
                
                b = 0
                for i in str(tooltip).split("\n"):
                    if len(i) > b:
                        
                        b = len(i)
                
                xsize = b*6+2
                ysize = len(str(tooltip).split("\n"))*11
                
                
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#424242"))
                widget.window.draw_rectangle(xgc, True, mx+10, my+10, xsize,ysize)
                
                
                for n, i in enumerate(str(tooltip).split("\n")):
                    
                    
                    
                    
                
                
                
                
                    ctx2.set_source_rgb(1,1,1)
                    ctx2.set_font_size(10)
                    ctx2.move_to( mx+11, my+20+(n*10))
                    ctx2.show_text(i)
            
            
            
            fif = datetime.datetime.now()
            mil  = fif - stf
            perfStat.append([ "TOOLTIPS", mil.microseconds])
            
            
            ########################
            
            
            #          PERFORMANCE ANALYTICS                   #
            
            ###########################
            
            
            rue = mx in range(0, 50) and my in range(h-50, h)
            
            
            
            if rue:  # CHANGE TO FALSE WHEN YOU DON'T NEED TO CHECK PERFORMANCE
                
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#000"))
                widget.window.draw_rectangle(xgc, True, 10, h-(len(perfStat)*15)-30-300, 500,len(perfStat)*15+30)
                
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
                    ctx2.move_to( 20, h-(len(perfStat)*15)+15*n-300)
                    
                    p = float(i[1]) / s *100
                    
                    ctx2.show_text(str(i[0])+" - "+str(i[1])+" MCRS "+str(int(round(p)))+"%")
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#222"))
                    widget.window.draw_rectangle(xgc, True, 20 + 270, h-(len(perfStat)*15)-20+10+15*n-300, 200,10)
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#fff"))
                    widget.window.draw_rectangle(xgc, True, 20 + 270, h-(len(perfStat)*15)-20+10+15*n-300, int(round(p))*2,10)
            
            ##########################################################################################################
            ##                                  DONE DRAWING HERE ALREADY                                           ##
            ##                                  JUST GO AND LOOK THERE MOTHER...                                    ##
            ##########################################################################################################
            
            
            if self.ifpos > 0:
                self.scroll = passed*-20 + w/2 +10
                self.selectdate = datetime.datetime.strftime(datetime.datetime.today(), self.schedule_date_format)
                self.ifpos = self.ifpos - 1
            
            self.hscroll
            # SCROLLING IT SELF
            # the scroll is done with the middle mouse button
            if self.mpx > mx and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf) and my in range(bstY, bstY+bubY) and self.winactive:
                self.scroll = self.scroll + (mx-self.mpx)
                
            if self.mpx < mx and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf) and my in range(bstY, bstY+bubY) and self.winactive:
                self.scroll = self.scroll - (self.mpx-mx)
            
            
            #if self.scroll < 0-((n+al)*20)+h-33:  #THOSE VALUES HAVE TO BE REDONE
            #    self.scroll = 0-((n+al)*20)+h-33
                
            #if self.scroll > 0:
            #    self.scroll = 0
            
            
            
            # DISABLING THE MOVEMENT IF MOUSE IS NO LONGER CLICKER   
            if "GDK_BUTTON1" not in str(fx) and "GDK_BUTTON1" in str(self.mpf):
                self.taskmove = -1
            
            
            # SCROLLING HYSTORY
            # the scroll is done with the middle mouse button
            if self.mpy > my and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf) and my in range(0, bstY) and mx in range(w/3*2,w) and self.winactive:
                self.hscroll = self.hscroll + (my-self.mpy)
                
            if self.mpy < my and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf) and my in range(0, bstY) and mx in range(w/3*2,w) and self.winactive:
                self.hscroll = self.hscroll - (self.mpy-my)
            
            
            #if self.scroll < 0-((n+al)*20)+h-33:  #THOSE VALUES HAVE TO BE REDONE
            #    self.scroll = 0-((n+al)*20)+h-33
                
            if self.hscroll < 0:
                self.hscroll = 0
            
            
            # SCROLLING TASK
            # the scroll is done with the middle mouse button
            if self.mpy > my and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf) and my in range(0, bstY) and mx in range(w/3,w/3*2) and self.winactive:
                self.tscroll = self.tscroll + (my-self.mpy)
                
            if self.mpy < my and "GDK_BUTTON2" in str(fx) and "GDK_BUTTON2" in str(self.mpf) and my in range(0, bstY) and mx in range(w/3,w/3*2) and self.winactive:
                self.tscroll = self.tscroll - (self.mpy-my)
            
            
            #if self.scroll < 0-((n+al)*20)+h-33:  #THOSE VALUES HAVE TO BE REDONE
            #    self.scroll = 0-((n+al)*20)+h-33
                
            if self.tscroll < 0:
                self.tscroll = 0
            
            
            # TESTING SOMETHING
            ctx.set_font_size(20)
            ctx.move_to( mx, my)
            #ctx.show_text(str(mx)+":"+str(my)+"  "+str(self.winactive))    
            
            
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
        graph.set_size_request(500,500)
        
        self.box.pack_start(graph)
        graph.connect("expose-event", framegraph) 
        
        self.box.show_all()
    
    def banner_changer(self, w=None):
        
        
        self.box.set_sensitive(False)   
        
        get = imageselector.select(self.pf)
        if get: 
            
            
            
            # OPENING AND COPEING
            
            if get.lower().endswith(".jpg") or get.lower().endswith(".png") and "py_data/banner.png" not in get:
                source = open(get, "r")
                
                to = open("py_data/banner.png", "w")
                to.write(source.read())
                to.close()
            
        self.box.set_sensitive(True)    
        self.allowed = True
        
        self.dW = 0
        self.DH = 0
        
        
    
       
