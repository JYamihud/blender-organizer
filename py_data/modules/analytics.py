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
        
        ####### DATA
            
            
            
            
        prgData = tuple(open("project.data", "r"))
        
        projectname   = prgData[0][11:][:-1]
        projectstatus = prgData[1][11:][:-1]
        projectleader = prgData[2][11:][:-1]
        projectchar   = prgData[5][11:][:-1]
        projectloca   = prgData[6][11:][:-1]
        projectobje   = prgData[7][11:][:-1]
        projectvehi   = prgData[8][11:][:-1]
        projectscen   = prgData[9][11:][:-1]
        
        
        pathsdata = tuple(open("custompaths.data", "r"))
        
        custompath    = pathsdata[0][11:][:-1]
        
        astchar = os.walk(os.getcwd()+"/ast/chr").next()[2]
        clearify = []
        for i in astchar:
            if i[-6:] == ".blend":
                clearify.append(i)
        astchar = clearify
        
        astloca = os.walk(os.getcwd()+"/ast/loc").next()[2]
        clearify = []
        for i in astloca:
            if i[-6:] == ".blend":
                clearify.append(i)
        astloca = clearify
        
        astvehi = os.walk(os.getcwd()+"/ast/veh").next()[2]
        clearify = []
        for i in astvehi:
            if i[-6:] == ".blend":
                clearify.append(i)
        astvehi = clearify
        
        astobje = os.walk(os.getcwd()+"/ast/obj").next()[2]
        clearify = []
        for i in astobje:
            if i[-6:] == ".blend":
                clearify.append(i)
        astobje = clearify
        
        donechar = len(astchar)
        doneloca = len(astloca)
        doneobje = len(astobje)
        donevehi = len(astvehi)
        
        # renders scenes LOL WTF
        donescen = len(os.walk(os.getcwd()+"/rnd").next()[1])
        
        
        scenpercent = 0.0 #NOT ACTUALL % BUT A FRACTION FROM 0 to 1
        
        
        sceneslist = []
        scenesinfolist = []
        
        
        
        for i in os.walk(os.getcwd()+"/rnd").next()[1]:
            
            sceneslist.append(i)
            scenesinfolist.append([i])
        
        for x, i in enumerate(sceneslist):
            
            scenelist = []
            scenescore = 0.0
            
            
            
            for b in os.listdir(os.getcwd()+"/rnd/"+i):
                if os.path.isdir(os.getcwd()+"/rnd/"+i+"/"+b):
                   
                    scenelist.append(b)
                    
                    shotscore = 0
                    
                    try:
                        if len(os.listdir(os.getcwd()+"/rnd/"+i+"/"+b+"/storyboard")) > 0:
                            shotscore = 1
                    except:
                        pass
                    try:
                        if len(os.listdir(os.getcwd()+"/rnd/"+i+"/"+b+"/opengl")) > 0:
                            shotscore = 2
                    except:
                        pass
                    try:
                        if len(os.listdir(os.getcwd()+"/rnd/"+i+"/"+b+"/rendered")) > 0:
                            shotscore = 3
                    except:
                        pass
                    
                
                    scenescore = scenescore + (1.0/3)*shotscore
                    print b, scenescore
                    
                    scenesinfolist[x].append([b, shotscore])
            try:        
                scenescore = 1.0/len(scenelist)*scenescore
            except:
                scenescore = 0
            scenpercent = scenpercent + scenescore
            
            
            scenesinfolist[x].append(scenescore)
            
        print scenesinfolist
        
        try:    
            scenpercent = 1.0/float(projectscen)*scenpercent 
        except:
            scenpercent = 0.0
        
        
        donescen = float(projectscen)*float(scenpercent)
        
        
        
        
        donetotal = donechar + doneloca + doneobje + donevehi+donescen
        prototal = int(projectchar)+int(projectloca)+int(projectobje)+int(projectvehi)+(int(projectscen)*3)
        
        
        
        
        
        
        
        try:
            percentchar = ((float(donechar))/float(projectchar))*100.0
            percentchar = int(percentchar*100)
            percentchar = str(float(percentchar)/100.0)
        except:
            percentchar = "100.0"
            
        try:
            percentvehi = ((float(donevehi))/float(projectvehi))*100.0
            percentvehi = int(percentvehi*100)
            percentvehi = str(float(percentvehi)/100.0)
        except:
            percentvehi = "100.0"
            
        try:
            percentobje = ((float(doneobje))/float(projectobje))*100.0
            percentobje = int(percentobje*100)
            percentobje = str(float(percentobje)/100.0)
        except:
            percentobje = "100.0"
            
        try:
            percentloca = ((float(doneloca))/float(projectloca))*100.0
            percentloca = int(percentloca*100)
            percentloca = str(float(percentloca)/100.0)
        except:
            percentloca = "100.0"
        
        listofpercents = [float(percentchar), float(percentvehi), float(percentobje), float(percentloca), float(donescen)]
        
        #projectpercent = ((float(donetotal))/float(prototal))*100.0 # OLD CODE BAD
        projectpercent = sum(listofpercents)/len(listofpercents)
        projectpercent = int(projectpercent*100)
        projectpercent = str(float(projectpercent)/100.0)
        
        
        
        
        
        #TIME
    
    
        #getting time values
        
        timefile = open("project.progress", "r")
        timefile = timefile.read()
        startdate = "00/00/00"
        enddate = "00/00/00"
        for timeline in timefile.split("\n"):
            if timeline.startswith("STR"):
                startdate = timeline[4:]
            if timeline.startswith("FIN"):
                enddate = timeline[4:]
        
        
        # CALCULATING DAYS
        deadline = 0.2
        
        date_format = "%d/%m/%Y"
        a = datetime.datetime.strptime(startdate, date_format)
        b = datetime.datetime.strptime(enddate, date_format)
        delta = b - a
        alltime = int(delta.days)
        
        a = datetime.datetime.strptime(startdate, date_format)
        b = datetime.datetime.today()
        delta =  b - a
        
        passed = int(delta.days)
        
        print "PASSED", passed, alltime
        
        try:
            deadline = (1.0/alltime)*passed
        except:
            deadline = 0
        
        deadline = deadline  * 100
        
        assetpercent = projectpercent
        projectpercent = str((float(assetpercent)+self.mainchecklist*100)/2)
        projectpercent = projectpercent[:projectpercent.find(".")+3]
        
        
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
            ctx.select_font_face("Sawasdee", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            
            xgc.line_width = 2
            
            # BACKGROUND COLOR
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#868686")) ## CHOSE COLOR
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
            avrgval = lastpercent / passed
            prevLB = 0
            
            for dln, date in enumerate(perhys):
                if date.startswith("DATE"):
                
                    thedate = date.split(" ")[1]
                    thepercent = float( date.split(" ")[2][:-1] )
                    
                    
                    #getting date's position
                    
                    a = datetime.datetime.strptime(startdate, date_format)
                    b = datetime.datetime.strptime(thedate, "%y-%m-%d")
                    delta =  b - a
                    
                    pos = int(delta.days)
                    
                    nowW = int(float(w)/alltime*pos)
                    nowH = int( h/2 / 100 * thepercent )*-1+h
                    
                    xgc.line_width = 4
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#e47649"))
                    widget.window.draw_polygon(xgc, True, [(prevW, prevH),(nowW,nowH),(nowW,h),(prevW,h)])
                    
                    
                    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#4c4c4c"))
                    
                    
                    
                    
                        
                        
                        
                    widget.window.draw_line(xgc,prevW, prevH, nowW, nowH)
                    
                    
                    
                    
                    if nowW - prevLB > 20:
                        
                        # MOUSE OVER AND INFRO REVEAL
                        if mx > nowW-10 and mx < nowW+10:
                            
                            pointshouldbe = int(float(h/2)/alltime*pos)*-1+h
                            shouldbepercent = int(100.0/alltime*pos)
                            
                            # VERTICAL LINE
                            widget.window.draw_line(xgc, nowW, pointshouldbe, nowW, nowH)    
                            widget.window.draw_rectangle(xgc, True , nowW-5, pointshouldbe-2, 10, 10)  
                            
                            # PROGRESS BAR WIDGET
                            
                            
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#000"))
                            xgc.line_width = 2
                            widget.window.draw_rectangle(xgc, False , nowW+2, pointshouldbe-30-2, 200+6, 15+4)  
                            xgc.line_width = 4
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#4c4c4c"))
                            widget.window.draw_rectangle(xgc, True , nowW+4, pointshouldbe-30, int(200.0*float(shouldbepercent)/100), 15)
                            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#a54118"))
                            widget.window.draw_rectangle(xgc, True , nowW+4, pointshouldbe-30, int(200.0*float(thepercent)/100), 15)
                            
                            # TEXT THINGY
                            ctx.set_source_rgb(0,0,0)
                            ctx.set_font_size(20)
                            ctx.move_to( nowW+5, pointshouldbe-100)
                            ctx.show_text(str(thedate))
                            
                            ctx.set_source_rgb(.1,.1,.1)
                            ctx.set_font_size(20)
                            ctx.move_to( nowW+5+int(200.0*float(shouldbepercent)/100), pointshouldbe-70)
                            ctx.show_text(str(shouldbepercent)+"% should be done")
                            
                            ctx.set_source_rgb(1,0,0)
                            ctx.set_font_size(20)
                            ctx.move_to( nowW+5+int(200.0*float(thepercent)/100), pointshouldbe-40)
                            ctx.show_text(str(thepercent)+"% done")
                            
                        # THOSE LITTLE SQUARES TO REPRESEND VERTICES
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#a54118"))    
                        widget.window.draw_rectangle(xgc, True , prevW-5, prevH-5, 10, 10)    
                        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#FFF"))    
                        widget.window.draw_rectangle(xgc, True , prevW-2, prevH-2, 4, 4) 
                        prevLB = nowW
                    
                    #PASSING TO THE NEXT VECTOR
                    prevH = nowH
                    prevW = nowW
                    prevV = thepercent
            
            
            
             # avarage
        
            
            
            
            enddateval = avrgval * ( alltime - passed ) + thepercent
            
            
            xgc.set_line_attributes(4, gtk.gdk.LINE_ON_OFF_DASH, gtk.gdk.CAP_NOT_LAST, gtk.gdk.JOIN_MITER)
            
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#4c4c4c"))
            widget.window.draw_line(xgc,prevW+2, prevH, w, int(  h /2 / 100 * enddateval  )*-1+h)
            
            xgc.set_line_attributes(2, gtk.gdk.LINE_SOLID, gtk.gdk.CAP_NOT_LAST, gtk.gdk.JOIN_MITER)
            
            # a little thing to show the estimated percentage by the deadline
            
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#000"))
            widget.window.draw_rectangle(xgc, False, w-260, int(  h /2 / 100 * enddateval  )*-1+h-20, 250, 10)
            
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#db3c16"))
            widget.window.draw_rectangle(xgc, True, w-260+2, int(  h /2 / 100 * enddateval  )*-1+h-20+2, int(250*enddateval/100), 10-4)
            
            ctx.set_source_rgb(0,0,0)
            ctx.set_font_size(12)
            ctx.move_to( w-260, int(  h /2 / 100 * enddateval  )*-1+h-20-10)
            ctx.show_text(str(int(enddateval))+"% by the deadline")
            
            
            
            # let's get the w of each thing
            
            wfortext = self.pixbuf.get_width()+80 # for the start of text
            wstCubes = self.pixbuf.get_width()+60
            
            
            tboxsH = int(     h/2/5*0.8    )
            tintsH = int(     h/2/5    )
            boxendH = int(      w-30-wstCubes       ) 
            
            # DONE
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#000"))
            widget.window.draw_rectangle(xgc, False, wstCubes, 30, boxendH, tboxsH)
            
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#CCC"))
            widget.window.draw_rectangle(xgc, True, wstCubes+2, 30+2, int((boxendH-2)*(float(projectpercent)/100)), tboxsH-3)
            
            ctx.set_source_rgb(0,0,0)
            ctx.set_font_size(tintsH/2)
            ctx.move_to( wfortext, 30+tintsH-tintsH/2)
            ctx.show_text("Done : "+str(projectpercent)+"%")
            
            
            
            # Time Passed
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#000"))
            widget.window.draw_rectangle(xgc, False, wstCubes, 30+tintsH, boxendH, tboxsH)
            
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#db3c16"))
            widget.window.draw_rectangle(xgc, True, wstCubes+2, 30+tintsH+2, int((boxendH-2)*(1.0/alltime*passed)), tboxsH-3)
            
            
            
            ctx.move_to( wfortext, 30+tintsH*2-tintsH/2)
            ctx.show_text("Time Passed : "+str(int(deadline))+"%  "+str(alltime-passed)+" days left")
            
            # Checklist
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#000"))
            widget.window.draw_rectangle(xgc, False, wstCubes, 30+tintsH*2, boxendH, tboxsH)
            
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#aaa"))
            widget.window.draw_rectangle(xgc, True, wstCubes+2, 30+tintsH*2+2, int((boxendH-2)*self.mainchecklist), tboxsH-3)
            
            
            
            ctx.move_to( wfortext, 30+tintsH*3-tintsH/2)
            ctx.show_text("Checklist : "+str(int(self.mainchecklist*100))+"%")    
            
            # Assets / Scenes
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#000"))
            widget.window.draw_rectangle(xgc, False, wstCubes, 30+tintsH*3, boxendH, tboxsH)
            
            xgc.set_rgb_fg_color(gtk.gdk.color_parse("#ff9900"))
            widget.window.draw_rectangle(xgc, True, wstCubes+2, 30+tintsH*3+2, int((boxendH-2)*(float(assetpercent)/100)), tboxsH-3)
            
            
            
            ctx.move_to( wfortext, 30+tintsH*4-tintsH/2)
            ctx.show_text("Assets / Scenes : "+str(assetpercent)+"%")
            
            
            ### BASINC PROJECT INFO
            
            
            
            infostr = open("project.data")
            infostr = infostr.read()
            
            
            for x,l in enumerate(infostr.split("\n")):
                
                ctx.set_font_size(20)
                ctx.move_to( 30, 30+self.pixbuf.get_height()+30+25*x)
                ctx.show_text(l)         
            
            
            
            
            
            
            
            
            
            
            
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
        
        
    
       
