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
import story_editor # to get scene percentage
import schedule
    


class draw_analytics:
    
    def __init__(self, pf, box, win):
    
        self.pf = pf # pf stands for project folder. It's a string to know
                     # where the project's folders start with
        
        self.box = box # the gtk.Box() container to put this widget into
        
        self.win = win
        
        self.mainchecklist = checklist.partcalculate(checklist.openckecklist("project.progress"))
        
        
        
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
        
        self.editicon  = gtk.gdk.pixbuf_new_from_file(pf+"/py_data/icons/edit.png")
        self.scheduleicon  = gtk.gdk.pixbuf_new_from_file(pf+"/py_data/icons/schedule.png")
        
        ####### DATA
            
            
        
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
        
        astlist = []
        
        for f in asstfols:
            
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
                
                astlist.append(sum(flist)/len(flist))
            
            else:            
                print f, "EMPTY"
                astlist.append(1.0)
        
        astlist.append(scenpercent)
        projectpercent = (sum(astlist)/len(astlist))*100
        
        
        
        #### SPANISH LANGUAGE EXCEPTION #####
        
        
        try:
            
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
            
            print "PASSED", passed, self.alltime
            
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
                schedule_date_format = "%Y/%m/%d"
                
                psdate = "0000/00/00"
                ypos = 0
                for task in schedulefile:   
                    
                    
                    today = False
                    xpos = 0
                    done = False
                    taskstring = "Task"
                    taskfile = "progect.progress"
                    
                    try:
                        sdate = task[:task.find(" ")]
                        if psdate == sdate:
                            ypos = ypos + 1
                        else:
                            ypos = 0
                            psdate = sdate
                        
                        print ypos    
                        print sdate
                        
                        if sdate == datetime.datetime.today().strftime(schedule_date_format):
                            today = True
                        
                        a = datetime.datetime.strptime(self.startdate, date_format)
                        b = datetime.datetime.strptime(sdate, schedule_date_format)
                        delta = b - a
                        
                        xpos = float(delta.days)/self.alltime
                        
                        print xpos, sdate
                        
                        taskfile = task[task.find(" ")+1:task.replace(" ", ".", 1).find(" ")]
                        print taskfile
                        taskstring = task[task.replace(" ", ".", 2).find(" "):].replace("=:>", " >")
                        print taskstring
                        
                        self.schedule.append([today, xpos, ypos, done, taskstring, taskfile, task])
                        
                    except Exception as exception:
                        print exception
                    
                    
                  
                
        except:
            
            print """

IF YOU SEE THIS ERROR MESSAGE IT'S Probably
because of your language system settings.

Reference: https://blenderartists.org/t/new-blender-organizer-forget-about-making-folders-work-faster/1126110/40

Change you Region & Language setting to English.

thx to c17vfx ( member of blenderartists.org ) for this workarround


"""         
            
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
        
        
        
        
        
        
        
        
        
        
        
        ##########################################################################################################
        ##                                  DRAWING GRAPH THINGY DOWN HERE                                      ##
        ##                                  JUST GO AND LOOK THERE MOTHER...                                    ##
        ##########################################################################################################
        
        
        
        
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
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#3a3a3a")) ## CHOSE COLOR
            widget.window.draw_rectangle(xgc, True, 0, 0, w, h)  ## FILL FRAME            
            
            
            
            
            
            
            
            
            
            # creating the image
            if self.dW != w and self.DH != h:
                print "THEY ARE NOT"
                
                self.banner = thumbnailer.thumbnail(pf+"/py_data/banner.png", w/3-60, h/2-60)
                self.pixbuf = gtk.gdk.pixbuf_new_from_file(self.banner)
            
            
            
            #frame
            
            
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#4c4c4c"))    
            widget.window.draw_rectangle(xgc, True , 25, 25, self.pixbuf.get_width()+10, self.pixbuf.get_height()+10)
            
            # image mouse over
            
            if mx > 25 and mx < 25+self.pixbuf.get_width()+10 and my > 25 and my < 25+self.pixbuf.get_height()+10:
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#000"))    
                
                  
                widget.window.draw_rectangle(xgc, True , 25, 25, self.pixbuf.get_width()+10, self.pixbuf.get_height()+10)
                
                
                
            
            #image
            
            
            widget.window.draw_pixbuf(None, self.pixbuf, 0, 0, 30, 30, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
            
            if mx > 25 and mx < 25+self.pixbuf.get_width()+10 and my > 25 and my < 25+self.pixbuf.get_height()+10:
                
                
                # AN EARLY DRAFT OF IMAGE OPENING ITSELF
                if "GDK_BUTTON1" in str(fx) and self.allowed and win.is_active(): #####   IF MOUSE CLICKED #####
                    
                    if "GDK_BUTTON1" not in str(self.mpf) :
                        
                        
                        # making sure it's not on the other button inside that one
                        
                        if mx > 30+self.pixbuf.get_width()-24 and mx > 32 and my < 30+self.pixbuf.get_width()-24+22 and my < 32+22:
                            pass
                        else:
                            os.system("xdg-open "+pf+"/py_data/banner.png")
                
                
                
                ## little edit image icon
                
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#ff9900"))    
                
                # IF MOUSE OVER
                
                
                
                if mx > 30+self.pixbuf.get_width()-24 and mx > 32 and my < 30+self.pixbuf.get_width()-24+22 and my < 32+22:
                    
                    
                    
                    
                    
                    
                    if "GDK_BUTTON1" in str(fx) and self.allowed and "GDK_BUTTON1" not in str(self.mpf) and win.is_active(): #####   IF MOUSE CLICKED #####
                        
                         
                        
                        self.allowed = False
                        
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#4c4c4c")) 
                        #self.banner_changer()
                        
                        glib.timeout_add(20, self.banner_changer)
                        
                    widget.window.draw_rectangle(xgc, True , 30+self.pixbuf.get_width()-26, 30, 24,24)
                    ctx.set_source_rgb(1,0.8,0.5)
                    ctx.set_font_size(15)
                    ctx.move_to( 30+self.pixbuf.get_width()-50, 20)
                    ctx.show_text("Change The Banner Image")
                
                
                widget.window.draw_pixbuf(None, self.editicon, 0, 0, 30+self.pixbuf.get_width()-24, 32, -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
                
                
            
            
            
            
            
            
            
            
            # DRAW
            
            xgc.set_line_attributes(4, gtk.gdk.LINE_ON_OFF_DASH, gtk.gdk.CAP_NOT_LAST, gtk.gdk.JOIN_MITER)
            
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#7c7c7c"))
            widget.window.draw_line(xgc,0, h, w, h/2)
            
            xgc.set_line_attributes(2, gtk.gdk.LINE_SOLID, gtk.gdk.CAP_NOT_LAST, gtk.gdk.JOIN_MITER) 
            
            
            
            for dln, date in enumerate(perhys):
                if date.startswith("DATE"):
                    
                    
                    
                    lastpercent = float( date.split(" ")[2][:-1] )
                    
                    
                    
                    
                    
                    
                    
                    prevV = lastpercent
            
            prevW = 0
            prevH = h
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
                    
                    nowW = int(float(w)/self.alltime*pos)
                    nowH = int( h/2 / 100 * thepercent )*-1+h
                    
                    xgc.line_width = 4
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
                    widget.window.draw_polygon(xgc, True, [(prevW, prevH),(nowW,nowH),(nowW,h),(prevW,h)])
                    
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#4c4c4c"))
                    
                    
                    
                    
                        
                        
                        
                    widget.window.draw_line(xgc,prevW, prevH, nowW, nowH)
                    
                    
                    
                    
                    if True:#nowW - prevLB > 20:
                        
                        # MOUSE OVER AND INFRO REVEAL
                        if mx > nowW-10 and mx < nowW+10 and toshowwidget:
                            toshowwidget = False
                            pointshouldbe = int(float(h/2)/self.alltime*pos)*-1+h
                            shouldbepercent = int(100.0/self.alltime*pos)
                            
                            # VERTICAL LINE
                            widget.window.draw_line(xgc, nowW, pointshouldbe, nowW, nowH)    
                            widget.window.draw_rectangle(xgc, True , nowW-5, pointshouldbe-2, 10, 10)  
                            
                            # PROGRESS BAR WIDGET
                            
                            
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#000"))
                            xgc.line_width = 2
                            widget.window.draw_rectangle(xgc, False , nowW+2, pointshouldbe-30-2, 200+6, 15+4)  
                            xgc.line_width = 4
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#395384"))
                            widget.window.draw_rectangle(xgc, True , nowW+4, pointshouldbe-30, int(200.0*float(shouldbepercent)/100), 15)
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
                            widget.window.draw_rectangle(xgc, True , nowW+4, pointshouldbe-30, int(200.0*float(thepercent)/100), 15)
                            
                            # TEXT THINGY
                            ctx.set_source_rgb(1,1,1)
                            ctx.set_font_size(20)
                            ctx.move_to( nowW+5, pointshouldbe-100)
                            ctx.show_text(str(thedate))
                            
                            ctx.set_source_rgb(0.8,0.8,0.8)
                            ctx.set_font_size(20)
                            ctx.move_to( nowW+5+int(200.0*float(shouldbepercent)/100), pointshouldbe-70)
                            ctx.show_text(str(shouldbepercent)+"% should be done")
                            
                            ctx.set_source_rgb(1,0.2,0.2)
                            ctx.set_font_size(20)
                            ctx.move_to( nowW+5+int(200.0*float(thepercent)/100), pointshouldbe-40)
                            ctx.show_text(str(thepercent)+"% done")
                            
                        # THOSE LITTLE SQUARES TO REPRESEND VERTICES
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#0faa96"))    
                        widget.window.draw_rectangle(xgc, True , prevW-5, prevH-5, 10, 10)    
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#3a3a3a"))    
                        widget.window.draw_rectangle(xgc, True , prevW-2, prevH-2, 4, 4) 
                        prevLB = nowW
                    
                    #PASSING TO THE NEXT VECTOR
                    prevH = nowH
                    prevW = nowW
                    prevV = thepercent
            
            
            
             # avarage
        
            
            
            
            self.enddateval = avrgval * ( self.alltime - passed ) + thepercent
            
            
            xgc.set_line_attributes(4, gtk.gdk.LINE_ON_OFF_DASH, gtk.gdk.CAP_NOT_LAST, gtk.gdk.JOIN_MITER)
            
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#4c4c4c"))
            widget.window.draw_line(xgc,prevW+2, prevH, w, int(  h /2 / 100 * self.enddateval  )*-1+h)
            
            xgc.set_line_attributes(2, gtk.gdk.LINE_SOLID, gtk.gdk.CAP_NOT_LAST, gtk.gdk.JOIN_MITER)
            
            # a little thing to show the estimated percentage by the deadline
            
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#000"))
            widget.window.draw_rectangle(xgc, False, w-260, int(  h /2 / 100 * self.enddateval  )*-1+h-20, 250, 10)
            
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
            widget.window.draw_rectangle(xgc, True, w-260+2, int(  h /2 / 100 * self.enddateval  )*-1+h-20+2, int(250*self.enddateval/100), 10-4)
            
            ctx.set_source_rgb(1,1,1)
            ctx.set_font_size(12)
            ctx.move_to( w-260, int(  h /2 / 100 * self.enddateval  )*-1+h-20-10)
            ctx.show_text(str(int(self.enddateval))+"% by the deadline")
            
            
            
            # let's get the w of each thing
            
            wfortext = 640#self.pixbuf.get_width()+80 # for the start of text
            wstCubes = 620#self.pixbuf.get_width()+60
            
            
            tboxsH = int(     h/2/5*0.8    )
            tintsH = int(     h/2/5    )
            boxendH = int(      w-30-wstCubes       ) 
            
            # DONE
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#d0d0d0"))
            widget.window.draw_rectangle(xgc, True, wstCubes, 30, boxendH, tboxsH)
            
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
            widget.window.draw_rectangle(xgc, True, wstCubes, 30, int((boxendH)*(float(projectpercent)/100)), tboxsH)
            
            ctx.set_source_rgb(1,1,1)
            ctx.set_font_size(tintsH/2)
            ctx.move_to( wfortext, 30+tintsH-tintsH/2)
            ctx.show_text("Done : "+str(projectpercent)+"%")
            
            
            
            # Time Passed
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#d0d0d0"))
            widget.window.draw_rectangle(xgc, True, wstCubes, 30+tintsH, boxendH, tboxsH)
            
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
            widget.window.draw_rectangle(xgc, True, wstCubes, 30+tintsH, int((boxendH)*(1.0/self.alltime*passed)), tboxsH)
            
            
            
            ctx.move_to( wfortext, 30+tintsH*2-tintsH/2)
            ctx.show_text("Time Passed : "+str(int(deadline))+"%  "+str(self.alltime-passed)+" days left")
            
            # Checklist
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#d0d0d0"))
            widget.window.draw_rectangle(xgc, True, wstCubes, 30+tintsH*2, boxendH, tboxsH)
            
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
            widget.window.draw_rectangle(xgc, True, wstCubes, 30+tintsH*2, int((boxendH)*self.mainchecklist), tboxsH)
            
            
            
            ctx.move_to( wfortext, 30+tintsH*3-tintsH/2)
            ctx.show_text("Checklist : "+str(int(self.mainchecklist*100))+"%")    
            
            # Assets / Scenes
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#d0d0d0"))
            widget.window.draw_rectangle(xgc, True, wstCubes, 30+tintsH*3, boxendH, tboxsH)
            
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#cb9165"))
            widget.window.draw_rectangle(xgc, True, wstCubes, 30+tintsH*3, int((boxendH)*(float(assetpercent)/100)), tboxsH)
            
            
            
            ctx.move_to( wfortext, 30+tintsH*4-tintsH/2)
            ctx.show_text("Assets / Scenes : "+str(assetpercent)+"%")
            
            
            ### BASINC PROJECT INFO
            
            
            
            infostr = open("project.data")
            infostr = infostr.read()
            
            
            ### 3 THINGS ONLY #### NAME, STATUS, DIRECTOR
            
            def edit(s, arg):
                                
                s = s.split("\n")
                if s[-1] == "":
                    s = s[:-1]
                
                
                
                
                for n, i in enumerate(s):
                    
                    if arg in i:
                        newname = dialogs.PickName(i[i.find(":")+1:])
                        if newname == "":
                            newname = i[i.find(":")+1:]
                            
                        s[n] = arg+newname
                
                
                save = open("project.data", "w")
                for i in s:
                    save.write(i+"\n")
                save.close()
                    
            
            for l in infostr.split("\n"):
                
                for ind, arg in enumerate(["Project  :", "Status   :", "Director :"]):
                
                    if arg in l:   
                        
                        
                        if mx in range(30, w-30) and my in range(30+self.pixbuf.get_height()+25*ind+10, 30+self.pixbuf.get_height()+25*ind+25+10):
                            
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#6c6c6c"))
                            widget.window.draw_rectangle(xgc, True, 30, 30+self.pixbuf.get_height()+25*ind+10, 500, 25 )
                            
                            if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and win.is_active(): ## IF CLICKED
                                
                                
                                    
                                    
                                
                                glib.timeout_add(10, edit, infostr, arg)
                        
                        
                        
                        prefix = ""
                        if ind == 2:
                            prefix = "directed by : "
                        
                        ctx.set_font_size(20)
                        ctx.move_to( 30, 30+self.pixbuf.get_height()+30+25*ind)
                        ctx.show_text(prefix+l[l.find(":")+1:])         
                
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
                    
            
            a = datetime.datetime.strptime(self.startdate, date_format)
            b = datetime.datetime.strptime(self.enddate, date_format)
            delta = b - a
            self.alltime = int(delta.days)
            
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
                
            
            if mx in range(30, 300) and my in range(30+self.pixbuf.get_height()+90, 30+self.pixbuf.get_height()+90+30):
                
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#6c6c6c"))
                widget.window.draw_rectangle(xgc, True, 30, 30+self.pixbuf.get_height()+110-20, 220, 25 )
                
                if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and win.is_active(): ## IF CLICKED
                
                    
                        
                        
                    glib.timeout_add(10, ee, "STR", self.startdate)
            
            
            ctx.set_font_size(20)
            ctx.move_to( 30, 30+self.pixbuf.get_height()+110)
            ctx.show_text("From: "+self.startdate) 
            
            
            #### END TIME ###
                
            if mx in range(300, 600) and my in range(30+self.pixbuf.get_height()+90, 30+self.pixbuf.get_height()+90+30):
                
                xgc.set_rgb_fg_color(gtk.gdk.color_parse("#6c6c6c"))
                widget.window.draw_rectangle(xgc, True, 300, 30+self.pixbuf.get_height()+110-20, 230, 25 )
            
                
                if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and win.is_active(): ## IF CLICKED
                
                    
                        
                        
                    glib.timeout_add(10, ee, "FIN", self.enddate)
                
            ctx.set_font_size(20)
            ctx.move_to( 300, 30+self.pixbuf.get_height()+110)
            ctx.show_text("Deadline: "+self.enddate) 
            
            
            
            ### DRAWING TASKS TO THE WINDOW
            
            
            #makingsuretodrawlasttasks
            if self.schedulesize != os.path.getsize(self.pf+"/schedule.data"):
                get_schedule()
                
            
            
            # self.schedule  [today, xpos, ypos, done, taskstring, taskfile]
            showtooltip = True
            for task in self.schedule:  
            
                today, xpos, ypos, done, taskstring, taskfile, rawline = task
            
                xpos = 20 #int(w*xpos)-5
                
                ypos = h - (ypos*22) - 20 -h/5    
                
                
                
                if today:
                    
                    
                #else:
                #    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#2c2c2c"))
                #    widget.window.draw_rectangle(xgc, True, xpos, ypos, 5, 5 )
            
                    
                    ctx.select_font_face("Monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
                    
                    
                    istx = xpos
                    isty = len(taskstring)*9+5
                    isty2 = len(taskfile)*6+50
                    
                    if istx + len(taskstring)*9+5 > w:
                        istx = w-(len(taskstring)*9+5)
                    if istx + len(taskfile)*6 > w:
                        istx = w-len(taskfile)*6
                    
                    #xgc.set_rgb_fg_color(gtk.gdk.color_parse("#e47649"))
                    #widget.window.draw_rectangle(xgc, True, xpos-1, ypos, 10, 10 )
                    
                    #xgc.set_rgb_fg_color(gtk.gdk.color_parse("#5c5c5c"))
                    #widget.window.draw_rectangle(xgc, True, istx, ypos, isty, 40 )
                    
                    
                    # THE BLACK VERSION WAS TOO OPACE AND WAS COVERING PARTS OF THE GRAPH
                    
                    #xgc.set_rgb_fg_color(gtk.gdk.color_parse("#1c1c1c"))
                    #widget.window.draw_rectangle(xgc, True, xpos-1, ypos, isty+100, 20 )
                    
                    ctx3 = widget.window.cairo_create()
                    ctx3.set_source_rgba(0.1,0.1,0.1,0.75)
                    ctx3.rectangle(xpos-1, ypos, isty+isty2, 20)
                    ctx3.fill()
                    
                    if mx in range(xpos-1, xpos+isty+100) and my in range(ypos, ypos+20):
                        
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#4f4f4f"))
                        widget.window.draw_rectangle(xgc, True, xpos-1, ypos, isty+isty2, 20 )
                        
                        
                        if "GDK_BUTTON1" in str(fx) and "GDK_BUTTON1" not in str(self.mpf) and win.is_active(): ## IF CLICKED
                            
                            if taskfile == "project.progress":
                                checklist.checkwindow(pf=self.pf, title="[ "+taskstring[taskstring.rfind("/")+1:]+" ] in ", FILE=taskfile, highlight=rawline)
                            else:
                                checklist.checkwindow(pf=self.pf, title="[ "+taskstring[taskstring.rfind("/")+1:]+" ] in ", FILE=self.pf+taskfile, highlight=rawline)
                    
                    
                    ctx.set_source_rgb(1,1,1)
                    ctx.set_font_size(15)
                    ctx.move_to( istx+22, ypos+16)
                    ctx.show_text(taskstring)
                    
                    ctx.set_font_size(10)
                    ctx.move_to( istx+isty+30, ypos+16)
                    
                    if taskfile == "project.progress":
                        ctx.show_text("Main")
                    else:
                        ctx.show_text(taskfile)
                    
                    widget.window.draw_pixbuf(None, self.scheduleicon, 0, 0, istx, ypos-1 , -1, -1, gtk.gdk.RGB_DITHER_NONE, 0, 0)  
                    
                    showtooltip = False
                    
                    
                    
                    
                        
                        
                        
                        
            
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

            glib.timeout_add(10, callback)
            
            
            
                   
        
        graph = gtk.DrawingArea()
        graph.set_size_request(500,500)
        
        self.box.pack_start(graph)
        graph.connect("expose-event", framegraph) 
        
        self.box.show_all()
    
    def banner_changer(self, w=None):
        
        
       
        
        # FILE CHOOSER
        self.box.set_sensitive(False)
        addbuttondialog = gtk.FileChooserDialog("CHOOSE NEW BANNER IMAGE",
                                         None,
                                         gtk.FILE_CHOOSER_ACTION_OPEN,
                                        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                         gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        addbuttondialog.set_default_response(gtk.RESPONSE_OK)
        addbuttondialog.set_current_folder(self.pf)
        
        
        
        response = addbuttondialog.run()
        if response == gtk.RESPONSE_OK:
            
            get = addbuttondialog.get_filename()
            
            
            # OPENING AND COPEING
            
            if get.lower().endswith(".jpg") or get.lower().endswith(".png") and "py_data/banner.png" not in get:
                source = open(get, "r")
                
                to = open("py_data/banner.png", "w")
                to.write(source.read())
                to.close()
            
        self.box.set_sensitive(True)    
        self.allowed = True
        addbuttondialog.destroy()
        
        self.dW = 0
        self.DH = 0
        
        
    
       
