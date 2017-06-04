# -*- coding: utf-8 -*-
#IMPORTING PYTHON MODULES

VERSION = 1.0

import os #to work with folders files and stuff liek this
import gtk #for graphical interface
import threading #so I could start muliple things in the same time
import datetime #to manage dates and time realed things
import pango #For text formatting
import zipfile #For Updates and shit

### IMAGE FOR LOADING THRUMBNAILS OF RENDERS
try:
    import Image
except:
    try:
        from PIL import Image
    except:
        print "\n\nIMAGE MODULE NOT FOUND"
        print "to fix it use commands"
        print ""
        print "sudo apt-get install python-pip"
        print "sudo pip2 install Image"
        print "\n\n"
        exit()

### getting data from project.data
projectname = None
projectstatus = None
projectleader = None
projectpercent = None
projectchar = None
projectloca = None
projectobje = None
projectvehi = None
projectscen = None

percentchar = None
percentvehi = None
percentobje = None
percentloca = None

assetpercent = None
checklistpercent = None

custompath = "~/Desktop/BlenderVer/blender-2.74-linux-glibc211-i686/blender"

def readData():
    
    global projectname
    global projectstatus
    global projectleader
    global projectpercent
    global projectchar
    global projectloca
    global projectobje
    global projectvehi
    global projectscen
    
    global percentchar
    global percentvehi
    global percentobje
    global percentloca
    
    global assetpercent
    global checklistpercent
    
    global custompath
    
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
    
    
    
    
    
    projectpercent = ((float(donetotal))/float(prototal))*100.0
    projectpercent = int(projectpercent*100)
    projectpercent = str(float(projectpercent)/100.0)
    
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
        percentvehi = ((float(donevehi))/float(projectvehi))*100.0
        percentvehi = int(percentvehi*100)
        percentvehi = str(float(percentvehi)/100.0)
    except:
        percentvehi = "100.0"
    
    
    # project.progress
    
    
    if "project.progress" in os.walk(os.getcwd()).next()[2]:
        projectProgress = tuple(open("project.progress", "r"))
                    
                    
        EMPTY = 0.0
        DONE = 0.0
        #OTHER = 0
        DONEi = False
        DONEc = 0
        DONEd = 0
        print "START READING"
        for i in projectProgress:
            if i[:4] in ["[ ] ", "[V] ", "[X] "]:
                            
                EMPTY = EMPTY + 1
                            
            if i[:4] == "[ ] ":
                            
                DONEi = False
                            
                            
            elif i[:4] in ["[V] ", "[X] "]:
                    DONE = DONE + 1
                    DONEi = True
                            
                    print "NO INENTATION"
                    print "\nDONE  = "+str(DONE)+"\n"
            elif i[:4] == "    " and DONEi == False:
                            
                if i[:8] in ["    [ ] ", "    [V] ", "    [X] "]:
                    if i[:8] in ["    [V] ", "    [X] "]:
                        DONEd = DONEd + 1
                    DONEc = DONEc + 1
            if i[:4] != "    ":
                try:
                    DONE = DONE + ((float(DONEd))/float(DONEc))
                    print "DONEc  = "+str(DONEc)
                    print "DONEd  = "+str(DONEd)
                    print "\nDONE  = "+str(DONE)+"\n"
                    DONEc = 0.0
                    DONEd = 0.0
                except:
                    print "NO INENTATION"
                    
        try:
            ASSERPERCENT = ((float(DONE))/float(EMPTY))*100.0
            ASSERPERCENT = int(ASSERPERCENT*100)
            ASSERPERCENT = str(float(ASSERPERCENT)/100.0)
        except:
            ASSERPERCENT = "100.0"
                    
        print "EMPTY = "+str(EMPTY)
        print "FINISH READING" + ASSERPERCENT
        
        assetpercent = projectpercent
        checklistpercent = ASSERPERCENT
        projectpercent = str((float(projectpercent) + float(ASSERPERCENT)) / 2)

readData()

#showing basic project data in console

print "Welcome to orginiser.py"
print "Project name      : "+projectname
print "Project status    : "+projectstatus
print "Progect director  : "+projectleader
print "Project done      : "+projectpercent  + "%"
print "Project assets    : "+assetpercent    + "%"
print "Project checklist : "+checklistpercent+ "%"



### Welcoming window is the one that remain MAIN
### Closing this window will cause closing the whole software
### This window will be most of the time minimized

#setting up all the needed global variables
welWin = None
prbanner = None

def welcome_window():

    global welWin
    global prbanner
    
    welWin = gtk.Window()
    welWin.set_title(("Organizer for "+projectname))
    gtk.window_set_default_icon_from_file("py_data/icon.png")
    welWin.connect("destroy", lambda w: gtk.main_quit())
    
    welWin.set_position(gtk.WIN_POS_CENTER_ALWAYS)
    
    
    welBox = gtk.VBox(False, 10)
    welWin.add(welBox)
    
    prbanner = gtk.Image()
    prbanner.set_from_file("py_data/banner.png")
    
    
    welText = " Project name    : "+projectname+" \n"\
               +" Project status  : "+projectstatus+" \n"\
               +" Progect director: "+projectleader+" "
    
    welL = gtk.Label("Organizer v1.0 by J.Y.Amihud")
    welWAR = gtk.Label(" WARNING! Closing this window \n will quit the program ")
    welT = gtk.Label(welText)
    
    welDbutton = gtk.Button()
    welDbutton.set_tooltip_text("Start Managing the "+projectname+" Project")
    
    welDbox = gtk.VBox(False)
    #welDbox.set_layout(gtk.BUTTONBOX_START)
    welDbutton.add(welDbox)
    
    
    
    
    
    welD = gtk.ProgressBar()
    welD.set_text(("◀ "+projectname+": "+projectpercent+"% ▶"))
    welD.set_fraction((float(projectpercent)/100))
    
    welDbox.pack_start(welD)
    welDbutton.connect("clicked", main_window)
    
    startB = gtk.Label("Start Organizer")
    welDbox.pack_start(startB)
    
    welBox.pack_start(welL)
    welBox.pack_start(prbanner)
    welBox.pack_start(welWAR)
    welBox.pack_start(welT)
    welBox.pack_start(welDbutton)
    welBox.pack_end(startB)
    
    
    
    
    
    welWin.show_all()
    






### MAIN WINDOW
### THE ACTUAL PLACE WHERE THE ORGANIZATION HAPPENING

#setting up nessesary global variables
curwid = "char"
mainbox = None

def main_window(widget):
    global mainbox
    global curwid
    
    welWin.iconify()
    print "Opening main Orginizer window"
    
    mainwin = gtk.Window()
    mainwin.set_title((os.getcwd()+" Progect: "+projectname+" "+projectpercent+"%"))
    mainwin.maximize()
    mainwin.connect("destroy", lambda w: gtk.main_quit())
    
    mainbox = gtk.VBox(False, 5)
    mainwin.add(mainbox)
    
    
    
    menubox = gtk.HBox(True, 5)
    mainbox.pack_start(menubox, False)
    
    ### macking menu buttons
    
    char = gtk.Button()
    char.set_tooltip_text("Manage Assets in:\n/dev/chr/\n/ast/chr/")
    
    charbox = gtk.HBox(False)
    char.add(charbox)
    
    chricon = gtk.Image()
    
    chricon.set_from_file("py_data/icons/chr_asset_done.png")
    charbox.pack_start(chricon)
    
    chartitle = gtk.Label("Characters")
    charbox.pack_start(chartitle)
    
    #" Characters "
    
    
    vehi = gtk.Button()
    vehi.set_tooltip_text("Manage Assets in:\n/dev/veh/\n/ast/veh/")
    
    vehibox = gtk.HBox(False)
    vehi.add(vehibox)
    
    vehicon = gtk.Image()
    
    vehicon.set_from_file("py_data/icons/veh_asset_done.png")
    
    
    vehibox.pack_start(vehicon)
    
    vehititle = gtk.Label("Vehicles")
    vehibox.pack_start(vehititle)
    
    obje = gtk.Button()
    obje.set_tooltip_text("Manage Assets in:\n/dev/obj/\n/ast/obj/")
    
    objebox = gtk.HBox(False)
    obje.add(objebox)
    
    objeicon = gtk.Image()
    objeicon.set_from_file("py_data/icons/obj_asset_done.png")
    objebox.pack_start(objeicon)
    
    objetitle = gtk.Label("Objects")
    objebox.pack_start(objetitle)
    
    loca = gtk.Button()
    loca.set_tooltip_text("Manage Assets in:\n/dev/loc/\n/ast/loc/")
   
    
    locabox = gtk.HBox(False)
    loca.add(locabox)
    
    locaicon = gtk.Image()
    locaicon.set_from_file("py_data/icons/loc_asset_done.png")
    locabox.pack_start(locaicon)
    
    locatitle = gtk.Label("Locations")
    locabox.pack_start(locatitle)
    
    scen = gtk.Button()
    scen.set_tooltip_text("Manage Scenes:\nStoryboards\nRecordings\nAnimations\nRenders")
    
    scenbox = gtk.HBox(False)
    scen.add(scenbox)
    
    scenicon = gtk.Image()
    scenicon.set_from_file("py_data/icons/scn_asset_done.png")
    scenbox.pack_start(scenicon)
    
    scentitle = gtk.Label("Scenes")
    scenbox.pack_start(scentitle)
    
    update = gtk.Button()
    update.set_tooltip_text("Manage updatees:\nStoryboards\nRecordings\nAnimations\nRenders")
    
    updatebox = gtk.HBox(False)
    update.add(updatebox)
    
    updateicon = gtk.Image()
    updateicon.set_from_file("py_data/icons/update.png")
    updatebox.pack_start(updateicon)
    
    updatetitle = gtk.Label("Updates")
    updatebox.pack_start(updatetitle)
    
    menubox.pack_start(char)
    menubox.pack_start(vehi)
    menubox.pack_start(obje)
    menubox.pack_start(loca)
    menubox.pack_start(scen)
    menubox.pack_start(update)
    
    char.connect("clicked", curwid_changer, "char")
    vehi.connect("clicked", curwid_changer, "vehi")
    obje.connect("clicked", curwid_changer, "obje")
    loca.connect("clicked", curwid_changer, "loca")
    scen.connect("clicked", curwid_changer, "scen")
    
    def updater(w):
        try:
    
            import urllib2

            updatefile = urllib2.urlopen("https://raw.githubusercontent.com/JYamihud/blender-organizer/master/UPDATE")
            updatefile = updatefile.read() 
            
            
            if float(updatefile.split("\n")[0]) > VERSION:
                
                
                
                
                
                #update window
                
                updwin = gtk.Window()
                updwin.set_title("Update Available !!!   CURRENT VERSION IS: "+str(VERSION))
                updwin.set_position(gtk.WIN_POS_CENTER)
                
                updbox = gtk.VBox(False)
                updwin.add(updbox)
                
                updscroll = gtk.ScrolledWindow()
                updscroll.set_size_request(800,400)
                
                
                uplabel = gtk.Label(updatefile)
                uplabel.modify_font(pango.FontDescription("Monospace"))
                updscroll.add_with_viewport(uplabel)
                
                updbox.pack_start(updscroll, False)
                
                def on_update(widget):
                    updwin.destroy()
                    
                    while gtk.events_pending():
                        gtk.main_iteration_do(False)
                    
                    run_update()
                
                
                updateb = gtk.Button("Update")
                updateb.connect("clicked", on_update)
                updbox.pack_start(updateb)        
                
                
                
                
                updwin.show_all()
            else:
                updwin = gtk.Window()
                updwin.set_title("UP TO DATE!   CURRENT VERSION IS: "+str(VERSION))
                updwin.set_position(gtk.WIN_POS_CENTER)    
                updwin.set_size_request(300,300)
                updwin.add(gtk.Label("\nYOUR orginizer.py\nIs UP TO DATE\n"))
                
                updwin.show_all()
        except:
            raise
    update.connect("clicked", updater)
    
    
    
    ##### HOT KEYS BUTTONS ####
    
    
    
    
    
    
    
    
    # running all the nessesary widget
    
    if curwid in ["char", "vehi", "obje","loca"]:
        organ(True)
    elif curwid == "scen":
    
        scene_box(True)
    elif curwid == "update":
        
        updater(True)
        
    
    
    
    
    
    
    
    
    mainwin.show_all()


def run_update():
    
    saveproject_progress = open("project.progress", "r")
    saveproject_progress = saveproject_progress.read()
    
    savepy_data_icon = open("py_data/icon.png", "r")
    savepy_data_icon = savepy_data_icon.read()
    
    savepy_data_banner = open("py_data/banner.png", "r")
    savepy_data_banner = savepy_data_banner.read()
    
    import urllib2
    
 
    updatefile = urllib2.urlopen("https://github.com/JYamihud/blender-organizer/archive/master.zip")
    updatefile = updatefile.read()
    
    
    tmpzip = open("../tmpzip.zip", "w")
    tmpzip.write(updatefile)
    tmpzip.close()
    
    
    thedir = os.getcwd()
    
    #os.system("rm -rf py_data")
    
    
    #for i in os.listdir(thedir):
        #os.remove(i)
    
    zipfile.ZipFile('../tmpzip.zip').extractall(thedir)
    
    os.system("mv "+thedir+"/blender-organizer-master/* "+thedir+"/ --force")
    os.system("rm -rf blender-organizer-master")
    
    
    os.system("rm -rf .git")
    
    project_progress = open("project.progress", "w")
    project_progress.write(saveproject_progress)
    project_progress.close()
    
    project_progress = open("py_data/icon.png", "w")
    project_progress.write(savepy_data_icon)
    project_progress.close()
    
    project_progress = open("py_data/banner.png", "w")
    project_progress.write(savepy_data_banner)
    project_progress.close()
    
    updwin = gtk.Window()
    updwin.set_title("UP TO DATE!")
    updwin.set_position(gtk.WIN_POS_CENTER)    
    updwin.set_size_request(300,300)
    updwin.add(gtk.Label("\nYOUR orginizer.py\nIs UP TO DATE\n\nRESTART TO SEE CHANGES!\n"))
    
    updwin.show_all()
    
    
def curwid_changer(widget, ncwid):
    
    global curwid
    global orgabox1
    global curfile
    
    curfile = " "
    
    curwid = ncwid
    
    Refresher()

def savewidamount(widget):
    global curwid
    global orgabox1
    
    
    number = mustbe.get_text()
    with open("project.data", "r") as current:
        data = current.readlines()
    
    if len(number) == 0:
        number = "0"
    
    
    if curwid == "char":
        if int(number) < len(os.walk(os.getcwd()+"/dev/chr").next()[1]):
            number = str(len(os.walk(os.getcwd()+"/dev/chr").next()[1]))
        data[5] = "Character: "+number+"\n"
    elif curwid == "loca":
        if int(number) < len(os.walk(os.getcwd()+"/dev/loc").next()[1]):
            number = str(len(os.walk(os.getcwd()+"/dev/loc").next()[1]))
        data[6] = "Locations: "+number+"\n"
    elif curwid == "obje":
        if int(number) < len(os.walk(os.getcwd()+"/dev/obj").next()[1]):
            number = str(len(os.walk(os.getcwd()+"/dev/obj").next()[1]))
        data[7] = "Objects  : "+number+"\n"
    elif curwid == "vehi":
        if int(number) < len(os.walk(os.getcwd()+"/dev/veh").next()[1]):
            number = str(len(os.walk(os.getcwd()+"/dev/veh").next()[1]))
        data[8] = "Vehicles : "+number+"\n"
    
    
    with open("project.data", "w") as saving:
        saving.writelines(data)
        
    Refresher()

def make_new_asset(widget):
    
    
    foldername = newassetname.get_text()
    
    tmpn = 0
    while foldername in os.walk(os.getcwd()+"/dev/"+cfplease).next()[1]:
        
        try:
        #if True:
            
            tmp = int((foldername[-3:]))
            foldername = foldername[:-3]+"00"+str(int((foldername+"_00"+str(tmpn))[-3:])+1)
        except:
            #tmp = int((foldername+"00"+str(tmpn))[-3:])
            foldername = foldername+"_001"
        tmpn = tmpn + 1
    if newsubfolder == True:
        os.mkdir(os.getcwd()+"/dev/"+cfplease+"/"+foldername)
        os.mkdir(os.getcwd()+"/dev/"+cfplease+"/"+foldername+"/reference")
        os.mkdir(os.getcwd()+"/dev/"+cfplease+"/"+foldername+"/renders")
        os.mkdir(os.getcwd()+"/dev/"+cfplease+"/"+foldername+"/tex")
    else:
        os.mkdir(os.getcwd()+"/dev/"+cfplease+"/"+foldername)
    
    if newmypaint == True:
        
        source = open(os.getcwd()+"/py_data/empty.ora", "r")
        output = open(os.getcwd()+"/dev/"+cfplease+"/"+foldername+"/reference/scatch.ora", 'w')
        
    
    
        output.write(source.read())
        output.close()
        
        sysopen("mypaint "+os.getcwd()+"/dev/"+cfplease+"/"+foldername+"/reference/scatch.ora")
    
    savewidamount(True)
    Refresher()


    
def showdevelop(widget):
    global showdev
    global check274tf
    global newsubfolder
    global newmypaint
    
    showdev = show_dev.get_active()
    check274tf = widget.get_active()
    
    newsubfolder = makesubfol.get_active()
    newmypaint = startconcept.get_active()
    
    Refresher()



### ORGANIZATION WIDGET
### for all except animations and renders
orgabox1 = None
mustbe = None
showdev = True
show_dev = None
orgafun = None

check274tf = True
check274 = None

newsubfolder = True
newmypaint = False
makesubfol = None
startconcept = None
newassetname = None

cfplease = None

def organ(widget):
    
    global orgabox1
    global mainbox
    global prbanner
    global curwid
    global mustbe
    global showdev
    global show_dev
    global orgafun
    global curfile
    global curfiledev
    
    global check274tf
    global check274
    global makesubfol
    global startconcept
    global newsubfolder
    global newmypaint
    global newassetname
    
    global cfplease
    
    cfplease = ""
        
    if curwid == "char":
        cfplease = "chr"
        
    elif curwid == "vehi":
        cfplease = "veh"
        
    elif curwid == "loca":
        cfplease = "loc"
        
    elif curwid == "obje":
        cfplease = "obj"
    
    
    
    
    
    
    readData()
    orgabox1 = gtk.VBox(False, 5)
    mainbox.pack_start(orgabox1)
    
    progresbox = gtk.HBox(False, 0)
    orgabox1.pack_start(progresbox, False)
    
    
    
    
    
    #assetpercent checklistpercent ◀▶
    
    welDbutton = gtk.Button()
    welDbutton.set_tooltip_text("Open Project's Checklist")
    
    welDbox = gtk.HBox(False)
    #welDbox.set_layout(gtk.BUTTONBOX_START)
    welDbutton.add(welDbox)
    
    checklisticon = gtk.Image()
    checklisticon.set_from_file("py_data/icons/checklist.png")
    
    welDbox.pack_start(checklisticon, False)
    
    welD = gtk.ProgressBar()
    welD.set_text(("◀ Assets/scenes: "+assetpercent+"% ▶    ◀ Project checklist: "+checklistpercent+"% ▶     ◀ Avarage: "+projectpercent+"% ▶"))
    welD.set_fraction((float(projectpercent)/100))
    
    welDbox.pack_start(welD)
    welDbutton.connect("clicked", projectchecklist)
    
    progresbox.pack_start(welDbutton)
    
    
    
    titlesbox = gtk.HBox(True, 10)
    orgabox1.pack_start(titlesbox, False)
    
    abovelistbox = gtk.VBox(False)
    titlesbox.pack_start(abovelistbox)
    
    ### TITLE OF A CURWID
    if curwid == "char":
        listtitle = gtk.Label("Characters")
        abovelistbox.pack_start(listtitle, False)
    elif curwid == "vehi":
        listtitle = gtk.Label("Vehicles")
        abovelistbox.pack_start(listtitle, False)
    elif curwid == "obje":
        listtitle = gtk.Label("Objects")
        abovelistbox.pack_start(listtitle, False)
    elif curwid == "loca":
        listtitle = gtk.Label("Locations")
        abovelistbox.pack_start(listtitle, False)
    
    listfolbox = gtk.HBox(False)
    
    
    foldericon2 = gtk.Image()
    foldericon2.set_from_file("py_data/icons/folder.png")
    
    foldericon3 = gtk.Image()
    foldericon3.set_from_file("py_data/icons/folder.png")
    
    astfolbox = gtk.HBox(False)
    devfolbox = gtk.HBox(False)
    
    astfollabel = gtk.Label("/ast/"+cfplease+"/")
    devfollabel = gtk.Label("/dev/"+cfplease+"/")
    
    astfolbox.pack_start(foldericon2)
    astfolbox.pack_start(astfollabel)
    devfolbox.pack_start(foldericon3)
    devfolbox.pack_start(devfollabel)
    
    astfol = gtk.Button()
    astfol.set_tooltip_text("Open Folder /ast/"+cfplease+"/\nFinished Assets Location\nIn Nautilus\n(Default File Manager)")
    devfol = gtk.Button()
    devfol.set_tooltip_text("Open Folder /dev/"+cfplease+"/\nDevelopment Folders Location\nIn Nautilus\n(Default File Manager)")
    astfol.add(astfolbox)
    devfol.add(devfolbox)
    
    listfolbox.pack_start(astfol)
    listfolbox.pack_start(devfol)
    
    if curwid == "char":
        astfol.connect("clicked", lambda w: os.system("nautilus "+os.getcwd()+"/ast/chr"))
        devfol.connect("clicked", lambda w: os.system("nautilus "+os.getcwd()+"/dev/chr"))
    
    elif curwid == "vehi":
        astfol.connect("clicked", lambda w: os.system("nautilus "+os.getcwd()+"/ast/veh"))
        devfol.connect("clicked", lambda w: os.system("nautilus "+os.getcwd()+"/dev/veh"))
    
    elif curwid == "obje":
        astfol.connect("clicked", lambda w: os.system("nautilus "+os.getcwd()+"/ast/obj"))
        devfol.connect("clicked", lambda w: os.system("nautilus "+os.getcwd()+"/dev/obj"))
    
    elif curwid == "loca":
        astfol.connect("clicked", lambda w: os.system("nautilus "+os.getcwd()+"/ast/loc"))
        devfol.connect("clicked", lambda w: os.system("nautilus "+os.getcwd()+"/dev/loc"))
    
    #### PROGRESS BAR FOR CURWID
    if curwid == "char":
        charac_progress = gtk.ProgressBar()
        charac_progress.set_text(("Characters: "+percentchar+"%"))
        charac_progress.set_fraction((float(percentchar)/100))
        abovelistbox.pack_start(charac_progress, False)
    elif curwid == "vehi":
        charac_progress = gtk.ProgressBar()
        charac_progress.set_text(("Vehicles: "+percentvehi+"%"))
        charac_progress.set_fraction((float(percentvehi)/100))
        abovelistbox.pack_start(charac_progress, False)
    elif curwid == "obje":
        charac_progress = gtk.ProgressBar()
        charac_progress.set_text(("Objects: "+percentobje+"%"))
        charac_progress.set_fraction((float(percentobje)/100))
        abovelistbox.pack_start(charac_progress, False)
    elif curwid == "loca":
        charac_progress = gtk.ProgressBar()
        charac_progress.set_text(("Locations: "+percentvehi+"%"))
        charac_progress.set_fraction((float(percentvehi)/100))
        abovelistbox.pack_start(charac_progress, False)
    
    try:
        charac_progress.set_tooltip_text("This Progress shows the current percent\nof assets done in /ast/"+cfplease+"/...\n(The ones with colour icon in the list below)\n...from the amount written down below.\nYou can edit this amount and click save button\nand the progress will update accordingly.")
    except:
        return
    
    if curwid == "char":
        
        numbering = gtk.HBox(False)
        abovelistbox.pack_start(numbering, False)
        
        inast = os.walk(os.getcwd()+"/ast/chr").next()[2]
        clearing = []
    
        for i in inast:
            if i[-6:] == ".blend":
                clearing.append(i)
        inast = clearing
        
        
        indev = len(os.walk(os.getcwd()+"/dev/chr").next()[1])
        
        numberlable = gtk.Label(" "+str(len(inast))+" done, "+str(indev-len(inast))+" developing. From ")
        numbering.pack_start(numberlable, False)
        
        mustbe = gtk.Entry()
        mustbe.set_text(projectchar)
        numbering.pack_start(mustbe, False)
        mustbe.connect("activate", savewidamount)
        
        saveb = gtk.Button("Save")
        numbering.pack_start(saveb, False)
        saveb.connect("clicked", savewidamount)
        
        
    elif curwid == "vehi":
        
        numbering = gtk.HBox(False)
        abovelistbox.pack_start(numbering, False)
        
        inast = os.walk(os.getcwd()+"/ast/veh").next()[2]
        clearing = []
    
        for i in inast:
            if i[-6:] == ".blend":
                clearing.append(i)
        inast = clearing
        
        
        indev = len(os.walk(os.getcwd()+"/dev/veh").next()[1])
        
        numberlable = gtk.Label(" "+str(len(inast))+" done, "+str(indev-len(inast))+" developing. From ")
        numbering.pack_start(numberlable, False)
        
        mustbe = gtk.Entry()
        mustbe.set_text(projectvehi)
        numbering.pack_start(mustbe, False)
        mustbe.connect("activate", savewidamount)
        
        saveb = gtk.Button("Save")
        numbering.pack_start(saveb, False)
        saveb.connect("clicked", savewidamount)
        
    
        
    elif curwid == "obje":
        
        numbering = gtk.HBox(False)
        abovelistbox.pack_start(numbering, False)
        
        inast = os.walk(os.getcwd()+"/ast/obj").next()[2]
        clearing = []
    
        for i in inast:
            if i[-6:] == ".blend":
                clearing.append(i)
        inast = clearing
        
        
        indev = len(os.walk(os.getcwd()+"/dev/obj").next()[1])
        
        numberlable = gtk.Label(" "+str(len(inast))+" done, "+str(indev-len(inast))+" developing. From ")
        numbering.pack_start(numberlable, False)
        
        mustbe = gtk.Entry()
        mustbe.set_text(projectobje)
        numbering.pack_start(mustbe, False)
        mustbe.connect("activate", savewidamount)
        
        saveb = gtk.Button("Save")
        numbering.pack_start(saveb, False)
        saveb.connect("clicked", savewidamount)
    
    elif curwid == "loca":
        
        numbering = gtk.HBox(False)
        abovelistbox.pack_start(numbering, False)
        
        
        
        inast = os.walk(os.getcwd()+"/ast/loc").next()[2]
        clearing = []
    
        for i in inast:
            if i[-6:] == ".blend":
                clearing.append(i)
        inast = clearing
        
        
        indev = len(os.walk(os.getcwd()+"/dev/loc").next()[1])
        
        numberlable = gtk.Label(" "+str(len(inast))+" done, "+str(indev-len(inast))+" developing. From ")
        numbering.pack_start(numberlable, False)
        
        mustbe = gtk.Entry()
        mustbe.set_text(projectloca)
        numbering.pack_start(mustbe, False)
        mustbe.connect("activate", savewidamount)
        
        saveb = gtk.Button("Save")
        numbering.pack_start(saveb, False)
        saveb.connect("clicked", savewidamount)
    
    numbering.pack_end(listfolbox, False)
    
    #### creating new asset folder ###
    
    cfirstline = gtk.HBox(False)
    abovelistbox.pack_start(cfirstline, False)
    
    
    
    
    createnewT = gtk.Label("New:")
    cfirstline.pack_start(createnewT, False)
    
    
    newassetname = gtk.Entry()
    newassetname.set_text("Name")
    cfirstline.pack_start(newassetname, False)
    newassetname.connect("activate", make_new_asset)
    
    createNew = gtk.Button("Create")
    cfirstline.pack_start(createNew, False)
    createNew.connect("clicked", make_new_asset)
    
    
    makesubfol = gtk.CheckButton("SubFolders")
    cfirstline.pack_start(makesubfol, False)
    makesubfol.set_active(newsubfolder)
    makesubfol.connect("clicked", showdevelop)
    
    startconcept = gtk.CheckButton("MyPaint")
    cfirstline.pack_start(startconcept, False)
    startconcept.set_active(newmypaint)
    startconcept.connect("clicked", showdevelop)
    
    
    ### SHOW IN DEVELOPMENT CHECK ###
    
    show_dev = gtk.CheckButton("Show Unfinished Assets (in Developing)")
    abovelistbox.pack_start(show_dev, False)
    show_dev.set_active(showdev)
    show_dev.connect("clicked", showdevelop)
    
    
    
    ##### HERE WAS FORCE BUTTONS TO WORK LOL
    
    #messagebox = gtk.VBox(False)
    #titlesbox.pack_start(messagebox)
    
    
    
    #Force = gtk.Button("⚒ FORCE BUTTONS TO WORK ⚒")
    #Force.set_tooltip_text("Some buttons do not work at first click")
    #messagebox.pack_start(Force)
    #Force.connect("clicked", savewidamount)
    
    
    
    
    
    
    
    orgabox2 = gtk.HBox(False, 10)
    orgabox1.pack_start(orgabox2)
    
    #### LIST OF ITEMS ####
    
    orgalist = gtk.VBox(False)
    orgabox2.pack_start(orgalist)
    
    list_scroll = gtk.ScrolledWindow()
    list_scroll.set_size_request(200,200)
    orgalist.pack_start(list_scroll)
    
    box_files = gtk.VBox()#True, 0)
    #box_files.set_layout(gtk.BUTTONBOX_START)
    list_scroll.add_with_viewport(box_files)
    
    astunits = []
    devunits = []
    
    if curwid == "char":
        
        astunits = os.walk(os.getcwd()+"/ast/chr").next()[2]
        devunits = os.walk(os.getcwd()+"/dev/chr").next()[1]
        
    elif curwid == "vehi":
        
        astunits = os.walk(os.getcwd()+"/ast/veh").next()[2]
        devunits = os.walk(os.getcwd()+"/dev/veh").next()[1]
    
    elif curwid == "loca":
        
        astunits = os.walk(os.getcwd()+"/ast/loc").next()[2]
        devunits = os.walk(os.getcwd()+"/dev/loc").next()[1]
    
    elif curwid == "obje":
        
        astunits = os.walk(os.getcwd()+"/ast/obj").next()[2]
        devunits = os.walk(os.getcwd()+"/dev/obj").next()[1]
    print "BEFORE"
    print astunits
    
    clearing = []
    
    for i in astunits:
        if i[-6:] == ".blend":
            clearing.append(i)
    astunits = clearing
    print "AFTER"
    print astunits
    
    if showdev == True:
        
        for i in astunits:
            if i[:-6] in devunits:
                devunits.remove(i[:-6])
            devunits.append(i[:-6])
    
    devunits = sorted(devunits)
    astunits = sorted(astunits)
    
    filesShow = []
    
    for i in astunits:
        filesShow.append(i[:-6])
    astunits = filesShow
    
    
    
    filesShow = []
    if showdev == True:
        filesShow = devunits
    else:
        filesShow = astunits


            
    #filesShow.sort()
    
    for i in astunits:
        print i
    
    # EXPANDING THE SIZES OF LABELS
    
    assetnamesize = 0
    
    filelabels = []
    
    for i in filesShow:
        if len(i) > assetnamesize:
            assetnamesize = len(i)
    for x, i in enumerate(filesShow):
        append = i
        if len(i) < assetnamesize:
            spaces = ""
            for b in range(0, (assetnamesize-len(i))):
                spaces = spaces + " "
            append = i + spaces
        filelabels.append(append)
    
    # WRIING IN DEVELOPING SO OTHER SHIT CAN UNDERSTAND
    
    if showdev == True:
        filesShow = devunits
        inum = 0
        for n,i in enumerate(filesShow):
            
            if i not in astunits:
                filesShow[n] = filesShow[n]+" (in Developing)"
                
    else:
        
        filesShow = astunits


    
    index2 = 0
    for i in filesShow:
        #print i
        index = "_"+str(index2)
        globals()["file%s" % index] = gtk.Button()
        add_button = "box_files.pack_start(file_"+str(index2)+", False)"
        exec (add_button) in globals(), locals()
        
        
        globals()["bbox%s" % index] = gtk.HBox()
        #bboxfix = "bbox_"+str(index2)+".set_layout(gtk.BUTTONBOX_START)"
        #exec (bboxfix) in globals(), locals()
        
        add_bb = "file_"+str(index2)+".add(bbox_"+str(index2)+")"
        exec (add_bb) in globals(), locals()
        
        
        
        
        asseticon = gtk.Image()
        asseticon.set_from_file("py_data/icons/"+cfplease+"_asset_undone.png")
        asseticon.set_tooltip_text("The black and white Icon means that\nthe Asset is in developing,\nnot yet in /ast/"+cfplease+"/")
        
        #if showdev == True:
        assetlabel = gtk.Label(filelabels[index2])
        assetlabel.set_tooltip_text("Click to manage asset "+i)
        #else:
        #    assetlabel = gtk.Label(i)
        
        if i in astunits:
            asseticon = gtk.Image()
            asseticon.set_from_file("py_data/icons/"+cfplease+"_asset_done.png")
            asseticon.set_tooltip_text("The colored Icon means that\nthe Asset is done,\nexist in /ast/"+cfplease+"/")
        asseticonbox = gtk.VBox()
        asseticonbox.pack_start(asseticon)
        
        assetlabelbox = gtk.HButtonBox()
        
        assetlabelbox.set_layout(gtk.BUTTONBOX_START)
        assetlabelbox.pack_start(assetlabel)
        
        add_icon = "bbox_"+str(index2)+".pack_start(asseticonbox, False)"
        exec (add_icon) in globals(), locals()
        
        add_icon = "bbox_"+str(index2)+".pack_start(assetlabelbox, False)"
        exec (add_icon) in globals(), locals()
        
        underscores = "file_"+str(index2)+".set_use_underline(False)"
        exec (underscores) in globals(), locals()
        con_button = "file_"+str(index2)+".connect('clicked', changefile, i)"
        exec (con_button) in globals(), locals()
        index2 = index2+1
    
    
    
    
    
    
    
    
    orgafun = gtk.VBox(False, 5)
    orgabox2.pack_start(orgafun)
    
    ### ACTUAL FUNCTIONs GO HERE ###
    
    
    
    
    
    
    FUNCTIONS = gtk.VBox()
    orgafun.pack_start(FUNCTIONS)
    
    filetitle = gtk.Label("ASSET: [ "+curfile+" ]")
    FUNCTIONS.pack_start(filetitle)
    
    openstfol = gtk.HBox(True)
    FUNCTIONS.pack_start(openstfol, False)
    
    openchecklist = gtk.Button()
    
    
    if curfile != " ":
        
        
        
        if curfiledev == False:
            
            ASSET_progress = gtk.ProgressBar()
            #ASSET_progress.set_text(("ASSET: "+percentchar+"%"))
            #ASSET_progress.set_fraction((float(percentchar)/100))
            ASSET_progress.set_text((curfile+" 100%"))
            ASSET_progress.set_fraction(1)
            openstfol.pack_start(ASSET_progress)
        if curfiledev == True:
            
            
            try:
                if "asset.progress" in os.walk(os.getcwd()+"/dev/"+cfplease+"/"+curfile).next()[2]:
                
                    ASSET_progress = gtk.ProgressBar()
                    
                    assetProgress = tuple(open(os.getcwd()+"/dev/"+cfplease+"/"+curfile+"/asset.progress", "r"))
                    
                    
                    
                    
                    EMPTY = 0.0
                    DONE = 0.0
                    #OTHER = 0
                    DONEi = False
                    DONEc = 0
                    DONEd = 0
                    print "START READING"
                    for i in assetProgress:
                        if i[:4] in ["[ ] ", "[V] ", "[X] "]:
                            
                            EMPTY = EMPTY + 1
                            
                        if i[:4] == "[ ] ":
                            
                            DONEi = False
                            
                            
                        elif i[:4] in ["[V] ", "[X] "]:
                            DONE = DONE + 1
                            DONEi = True
                            
                            print "NO INENTATION"
                            print "\nDONE  = "+str(DONE)+"\n"
                        elif i[:4] == "    " and DONEi == False:
                            
                            if i[:8] in ["    [ ] ", "    [V] ", "    [X] "]:
                                if i[:8] in ["    [V] ", "    [X] "]:
                                    DONEd = DONEd + 1
                                DONEc = DONEc + 1
                        if i[:4] != "    ":
                            try:
                                DONE = DONE + ((float(DONEd))/float(DONEc))
                                print "DONEc  = "+str(DONEc)
                                print "DONEd  = "+str(DONEd)
                                print "\nDONE  = "+str(DONE)+"\n"
                                DONEc = 0.0
                                DONEd = 0.0
                            except:
                                print "NO INENTATION"
                    
                    try:
                        ASSERPERCENT = ((float(DONE))/float(EMPTY))*100.0
                        ASSERPERCENT = int(ASSERPERCENT*100)
                        ASSERPERCENT = str(float(ASSERPERCENT)/100.0)
                    except:
                        ASSERPERCENT = "100.0"
                    
                    print "EMPTY = "+str(EMPTY)
                    print "FINISH READING"
                    
                    #print "OTHER = "+str(OTHER)
                    
                    checklisticon2 = gtk.Image()
                    checklisticon2.set_from_file("py_data/icons/checklist.png")
                    
                    openchecklistbox = gtk.HBox(False)
                    openchecklistbox.pack_start(checklisticon2, False)
                    
                    ASSET_progress.set_text((curfile+" "+ASSERPERCENT+"%"))
                    ASSET_progress.set_fraction((float(ASSERPERCENT)/100))
                    
                    openchecklistbox.pack_start(ASSET_progress)
                    openchecklist.add(openchecklistbox)
                    openstfol.pack_start(openchecklist)
                    openchecklist.connect("clicked", thechecklist)
                else:
                    makechecklist = gtk.Button("Create Checklist File")
                    makechecklist.connect("clicked", create_check_list)
                    openstfol.pack_start(makechecklist)
            except:
                    openchecklist = gtk.Label("asset.progress Error")
        
        opendevdictbox = gtk.HBox(False)
        
        foldericon = gtk.Image()
        foldericon.set_from_file("py_data/icons/folder.png")
        opendevdictbox.pack_start(foldericon)
        
        opendevdictlabel = gtk.Label("/dev/"+cfplease+"/"+curfile+"/")
        
        opendevdictbox.pack_start(opendevdictlabel)
        
        opendevdict = gtk.Button()
        opendevdict.add(opendevdictbox)
        opendevdict.set_tooltip_text("Open Folder /dev/"+cfplease+"/"+curfile+"/\nIn Nautilus\n(Default File Manager)")
    
    else:
        ASSET_progress = gtk.Label("ASSET: Unknown%")
        opendevdict = gtk.Label("No Development Folder")
    ################################## HERHEREHREHREHERHEREREHREHERHERHERHERHERHR #############
    
    
    
    
    openstfol.pack_start(opendevdict)
    
    #openchecklist = gtk.Button("Open"+curfile+"'s Check List")
    #FUNCTIONS.pack_start(openchecklist)
    
    blendfileslabel = gtk.Label("...Blend Files...")
    FUNCTIONS.pack_start(blendfileslabel, False)
    
    check274 = gtk.CheckButton("Use Custom Blender") ### just for functions to work LOL
    check274.set_active(check274tf)
    check274.connect("clicked", showdevelop)
    
    if curwid == "char" and curfile != " ":
        opendevdict.connect("clicked", lambda w: os.system("nautilus "+os.getcwd()+"/dev/chr/"+curfile))
    elif curwid == "vehi" and curfile != " ":
        opendevdict.connect("clicked", lambda w: os.system("nautilus "+os.getcwd()+"/dev/veh/"+curfile))
    elif curwid == "loca" and curfile != " ":
        opendevdict.connect("clicked", lambda w: os.system("nautilus "+os.getcwd()+"/dev/loc/"+curfile))
    elif curwid == "obje" and curfile != " ":
        opendevdict.connect("clicked", lambda w: os.system("nautilus "+os.getcwd()+"/dev/obj/"+curfile))
        
    if curfiledev == True:
        openasset = gtk.Label("Asset Unfinished (in Developing)")
        FUNCTIONS.pack_start(openasset, False)
    else:
        openasset = gtk.HBox(True)
        FUNCTIONS.pack_start(openasset, False)
        
        opennorm = gtk.Label("Open in Blender /ast/"+cfplease+"/")
        
        
        
        if curfile != " ":
            open274  = gtk.Button(curfile+".blend")
        
            if curwid == "char":
                if check274tf == False:
                    open274.connect("clicked", lambda w: os.system("xdg-open "+os.getcwd()+"/ast/chr/"+curfile+".blend"))
                if check274tf == True:
                    open274.connect("clicked", lambda w: sysopen(""+custompath+" "+os.getcwd()+"/ast/chr/"+curfile+".blend"))
            
            elif curwid == "vehi":
                if check274tf == False:
                    open274.connect("clicked", lambda w: os.system("xdg-open "+os.getcwd()+"/ast/veh/"+curfile+".blend"))
                if check274tf == True:
                    open274.connect("clicked", lambda w: sysopen(""+custompath+" "+os.getcwd()+"/ast/veh/"+curfile+".blend"))
        
            elif curwid == "loca":
                if check274tf == False:
                    open274.connect("clicked", lambda w: os.system("xdg-open "+os.getcwd()+"/ast/loc/"+curfile+".blend"))
                if check274tf == True:
                    open274.connect("clicked", lambda w: sysopen(""+custompath+" "+os.getcwd()+"/ast/loc/"+curfile+".blend"))
        
            elif curwid == "obje":
                if check274tf == False:
                    open274.connect("clicked", lambda w: os.system("xdg-open "+os.getcwd()+"/ast/obj/"+curfile+".blend"))
                if check274tf == True:
                    open274.connect("clicked", lambda w: sysopen(""+custompath+" "+os.getcwd()+"/ast/obj/"+curfile+".blend"))
        else:
            open274  = gtk.Label("No ASSET Selected!")
        openasset.pack_start(opennorm)
        openasset.pack_start(open274)
    
    
    FUNCTIONS.pack_start(gtk.HSeparator(), False)
    #### BLENDER FILES #####
    
    
    blendFilesBox = gtk.HBox(True, 0)
    FUNCTIONS.pack_start(blendFilesBox)
    
    blenFileSettings = gtk.VBox(False, 30)
    blendFilesBox.pack_start(blenFileSettings)
    
    openblendStitle = gtk.Label("...Settings...  /dev/"+cfplease+"/")
    blenFileSettings.pack_start(openblendStitle)
    
    
    
    customblenderbox = gtk.HBox(False)
    blenFileSettings.pack_end(customblenderbox, False)
    
    
    customblenderbox.pack_start(check274, False)
    
    
    def edit_custompath(w):
        
        path = w.get_text()
        
        global custompath
        custompath = path
        
        pathsdata = tuple(open("custompaths.data", "r"))
        
        tmp = []
        
        for i in pathsdata:
            tmp.append(i)
        
        pathsdata = tmp
        
        for x, i in enumerate(pathsdata):
            if i.startswith("Blndrpath: "):
                pathsdata[x] = "Blndrpath: "+custompath
        
        tmp = ""
        for i in pathsdata:
            tmp = tmp + i + "\n"
        
        tmp = tmp[:-1]
        pathsdata = tmp
        
        save = open("custompaths.data", "w")
        save.write(pathsdata)
        save.close()
       
        
    custompathentry = gtk.Entry()
    custompathentry.connect("changed", edit_custompath)
    customblenderbox.pack_start(custompathentry)
    custompathentry.set_tooltip_text("Custom Blender Path")
    custompathentry.set_text(custompath)
    
    def on_openb(widget):
        widget.set_sensitive(False)
        
        addbuttondialog = gtk.FileChooserDialog("Open..",
                                         None,
                                         gtk.FILE_CHOOSER_ACTION_OPEN,
                                        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                         gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        addbuttondialog.set_default_response(gtk.RESPONSE_OK)
        
        
        
        
        response = addbuttondialog.run()
        if response == gtk.RESPONSE_OK:
            
            get = addbuttondialog.get_filename()
            custompathentry.set_text(get)
            
        widget.set_sensitive(True)
        addbuttondialog.destroy()
    
    
    chose_blenderfolder = gtk.Button("Path")
    chose_blenderfolder.connect("clicked", on_openb)
    customblenderbox.pack_end(chose_blenderfolder, False)
    chose_blenderfolder.set_tooltip_text("Choose the blender executable file")
    
    #scrolled
    
    blendscrl = gtk.ScrolledWindow()
    blendFilesBox.pack_start(blendscrl)
    
    blendLbox = gtk.VBox(False, 0)
    blendscrl.add_with_viewport(blendLbox)
    
    blendfiles = []
    
    if curwid == "char":
        try:
            blendfiles = sorted(os.walk(os.getcwd()+"/dev/chr/"+curfile+"/").next()[2])
        except:
            blendfiles = []
    elif curwid == "vehi":
        try:
            blendfiles = sorted(os.walk(os.getcwd()+"/dev/veh/"+curfile+"/").next()[2])
        except:
            blendfiles = []
    
    elif curwid == "obje":
        try:
            blendfiles = sorted(os.walk(os.getcwd()+"/dev/obj/"+curfile+"/").next()[2])
        except:
            blendfiles = []
    
    elif curwid == "loca":
        try:
            blendfiles = sorted(os.walk(os.getcwd()+"/dev/loc/"+curfile+"/").next()[2])
        except:
            blendfiles = []
    
    
    show_blends = []
    
    for i in blendfiles:
        
        if i[-6:] == ".blend":
            show_blends.append(i)
    
    
    indexblends = 0
    for i in show_blends:
        if i in show_blends:
            #print i
            index = "_"+str(indexblends)
            globals()["file%s" % index] = gtk.Button(i)
            add_button = "blendLbox.pack_start(file_"+str(indexblends)+")"
            exec (add_button) in globals(), locals()
            underscores = "file_"+str(indexblends)+".set_use_underline(False)"
            exec (underscores) in globals(), locals()
        
            if curwid == "char":
                if check274tf == False:
                    con_button = "file_"+str(indexblends)+".connect('clicked',lambda w: sysopen('blender "+os.getcwd()+"/dev/chr/"+curfile+"/"+i+"'))"
                    exec (con_button) in globals(), locals()
                else:
                    con_button = "file_"+str(indexblends)+".connect('clicked',lambda w: sysopen('"+custompath+" "+os.getcwd()+"/dev/chr/"+curfile+"/"+i+"'))"
                    exec (con_button) in globals(), locals()
                
            elif curwid == "vehi":
                if check274tf == False:
                    con_button = "file_"+str(indexblends)+".connect('clicked',lambda w: sysopen('blender "+os.getcwd()+"/dev/veh/"+curfile+"/"+i+"'))"
                    exec (con_button) in globals(), locals()
                else:
                    con_button = "file_"+str(indexblends)+".connect('clicked',lambda w: sysopen('"+custompath+" "+os.getcwd()+"/dev/veh/"+curfile+"/"+i+"'))"
                    exec (con_button) in globals(), locals()
                
            elif curwid == "obje":
                if check274tf == False:
                    con_button = "file_"+str(indexblends)+".connect('clicked',lambda w: sysopen('blender "+os.getcwd()+"/dev/obj/"+curfile+"/"+i+"'))"
                    exec (con_button) in globals(), locals()
                else:
                    con_button = "file_"+str(indexblends)+".connect('clicked',lambda w: sysopen('"+custompath+" "+os.getcwd()+"/dev/obj/"+curfile+"/"+i+"'))"
                    exec (con_button) in globals(), locals()
                
            elif curwid == "loca":
                if check274tf == False:
                    con_button = "file_"+str(indexblends)+".connect('clicked',lambda w: sysopen('blender "+os.getcwd()+"/dev/loc/"+curfile+"/"+i+"'))"
                    exec (con_button) in globals(), locals()
                else:
                    con_button = "file_"+str(indexblends)+".connect('clicked',lambda w: sysopen('"+custompath+" "+os.getcwd()+"/dev/loc/"+curfile+"/"+i+"'))"
                    exec (con_button) in globals(), locals()
    
    # ☹☺
    if len(show_blends) == 0:
        noblendes = gtk.Label("☹ No Blend files ☹")
        blendLbox.pack_start(noblendes)
        if curfile != " ":
            generate = gtk.Button("☺ Generate:\n"+curfile+".blend")
            generate.set_use_underline(False)
            blendLbox.pack_start(generate)
            generate.connect("clicked", generateblend)
    
    
    FUNCTIONS.pack_start(gtk.HSeparator(), False)
    ##### RENDERS #####
    
    renders_label = gtk.Label("...Renders...")
    FUNCTIONS.pack_start(renders_label)
    
    renders_f_box = gtk.HBox(True)
    FUNCTIONS.pack_start(renders_f_box)
    
    rendersbuttons = gtk.HBox(False)  ####################
    renders_f_box.pack_start(rendersbuttons)
    
    
    
    
    
    
    Preview = None
    Wired = None
    
    if curfile != " ":
    
            
        try:
            if "Preview.jpg" in os.walk(os.getcwd()+"/dev/"+cfplease+"/"+curfile+"/renders/").next()[2]:
            
                
                thrumb = Image.open(os.getcwd()+"/dev/"+cfplease+"/"+curfile+"/renders/Preview.jpg")
                size = 200, 200
                thrumb.thumbnail(size, Image.ANTIALIAS)
                thrumb.save("py_data/tmp.jpg", "JPEG")
                
                
                
                Preview = gtk.Button()
                Previewim = gtk.Image()
                Preview.add(Previewim)
                Previewim.set_from_file("py_data/tmp.jpg")
                rendersbuttons.pack_start(Preview)
            else:
                Preview = gtk.Label("Error Loading Preview.jpg")
                rendersbuttons.pack_start(Preview)
            
            Preview.connect("clicked", lambda w: os.system("xdg-open "+os.getcwd()+"/dev/"+cfplease+"/"+curfile+"/renders/Preview.jpg"))
            
        except:
            pass
        
        try:
            if "Wired.jpg" in os.walk(os.getcwd()+"/dev/"+cfplease+"/"+curfile+"/renders/").next()[2]:
                
                thrumb = Image.open(os.getcwd()+"/dev/"+cfplease+"/"+curfile+"/renders/Wired.jpg")
                size = 200, 200
                thrumb.thumbnail(size, Image.ANTIALIAS)
                thrumb.save("py_data/tmp.jpg", "JPEG")
                
                
                
                Wired = gtk.Button()
                Wiredim = gtk.Image()
                Wired.add(Wiredim)
                Wiredim.set_from_file("py_data/tmp.jpg")
                rendersbuttons.pack_start(Wired)
                
                
                
            else:
                Wired = gtk.Label("Error Loading Wired.jpg")
                rendersbuttons.pack_start(Wired)
        
            
            Wired.connect("clicked", lambda w: os.system("xdg-open "+os.getcwd()+"/dev/"+cfplease+"/"+curfile+"/renders/Wired.jpg"))
            
        except:
            pass
        
    
    
    
    
    #### RENDERS LIST ###
    
    Rendscrl = gtk.ScrolledWindow()
    renders_f_box.pack_start(Rendscrl)
    
    RendLbox = gtk.VBox(False, 0)
    Rendscrl.add_with_viewport(RendLbox)
    
    RenderPath = []
    
    if curwid == "char":
        try:
            RenderPath = sorted(os.walk(os.getcwd()+"/dev/chr/"+curfile+"/renders/").next()[2])
        except:
            RenderPath = []
    elif curwid == "vehi":
        try:
            RenderPath = sorted(os.walk(os.getcwd()+"/dev/veh/"+curfile+"/renders/").next()[2])
        except:
            RenderPath = []
    
    elif curwid == "obje":
        try:
            RenderPath = sorted(os.walk(os.getcwd()+"/dev/obj/"+curfile+"/renders/").next()[2])
        except:
            RenderPath = []
    
    elif curwid == "loca":
        try:
            RenderPath = sorted(os.walk(os.getcwd()+"/dev/loc/"+curfile+"/renders/").next()[2])
        except:
            RenderPath = []
    
    
    indexRenders = 0
    for i in RenderPath:
        #print i
        index = "_"+str(indexRenders)
        globals()["file%s" % index] = gtk.Button(i)
        add_button = "RendLbox.pack_start(file_"+str(indexRenders)+")"
        exec (add_button) in globals(), locals()
        underscores = "file_"+str(indexRenders)+".set_use_underline(False)"
        exec (underscores) in globals(), locals()
        
        if curwid == "char":
            con_button = "file_"+str(indexRenders)+".connect('clicked',lambda w: os.system('xdg-open "+os.getcwd()+"/dev/chr/"+curfile+"/renders/"+i+"'))"
            exec (con_button) in globals(), locals()
        elif curwid == "vehi":
            con_button = "file_"+str(indexRenders)+".connect('clicked',lambda w: os.system('xdg-open "+os.getcwd()+"/dev/veh/"+curfile+"/renders/"+i+"'))"
            exec (con_button) in globals(), locals()
        elif curwid == "obje":
            con_button = "file_"+str(indexRenders)+".connect('clicked',lambda w: os.system('xdg-open "+os.getcwd()+"/dev/obj/"+curfile+"/renders/"+i+"'))"
            exec (con_button) in globals(), locals()
        elif curwid == "loca":
            con_button = "file_"+str(indexRenders)+".connect('clicked',lambda w: os.system('xdg-open "+os.getcwd()+"/dev/loc/"+curfile+"/renders/"+i+"'))"
            exec (con_button) in globals(), locals()
        
        
        indexRenders = indexRenders+1
    if len(RenderPath) == 0:
        norenders = gtk.Label("Folder /renders\nis empty,\nor not exist")
        RendLbox.pack_start(norenders)
    
    
    # ☹☺
        
    try:
        ckeck = os.walk(os.getcwd()+"/dev/"+cfplease+"/"+curfile+"/tex").next()[1]
        TexturesFolder = gtk.Button("Open Textures folder")
        FUNCTIONS.pack_start(TexturesFolder, False)
        TexturesFolder.connect("clicked", lambda w: os.system("nautilus "+os.getcwd()+"/dev/"+cfplease+"/"+curfile+"/tex"))
    except:
        TexturesFolder = gtk.Button("☹ Textures Folder /tex not found ☹")
        FUNCTIONS.pack_start(TexturesFolder, False)
    
   
    
    #### bottom
    
    bottom = gtk.HBox(False)
    mainbox.pack_end(bottom, False)
    
    editprojectbutton = gtk.Button("Edit project.data")
    bottom.pack_start(editprojectbutton)
    editprojectbutton.connect("clicked", editprojectdata)
    
    quit = gtk.Button("Quit Project")
    quit.connect("clicked", lambda w: gtk.main_quit())
    bottom.pack_end(quit)

def generateblend(widget, custom=False):
    
    template = open(os.getcwd()+"/py_data/empty.blend", "r")
    if custom == False:
        newblend = open(os.getcwd()+"/dev/"+cfplease+"/"+curfile+"/"+curfile+".blend", 'w')
    else:
        newblend = open(custom, 'w')
    newblend.write(template.read())
    newblend.close()
    
    
    Refresher()

def create_check_list(widget):
    
    
    source = open(os.getcwd()+"/py_data/asset.progress", "r")
    output = open(os.getcwd()+"/dev/"+cfplease+"/"+curfile+"/asset.progress", 'w')
    
    
    
    output.write(source.read())
    output.close()
    
    
    Refresher()









nameE = None
statE = None
direE = None
charE = None
vehiE = None
obgeE = None
locaE = None
scenE = None
editproject = None

def editprojectdata(widget):
    
    global nameE
    global statE
    global direE
    global charE
    global vehiE
    global objeE
    global locaE
    global scenE
    
    global editproject
    
    
    editproject = gtk.Window()
    editproject.set_title("Edit project.data")
    editproject.set_default_size(500, 0)
    
    editV = gtk.VBox(False, 5)
    editproject.add(editV)
    
    editTitle = gtk.Label(" Editing project's settings \n file: project.data ")
    editV.pack_start(editTitle)
    
    readData()
    
    global projectname
    global projectstatus
    global projectleader
    
    
    global projectchar
    global projectloca
    global projectobje
    global projectvehi
    global projectscen
    
    nameB = gtk.HBox(True, 5)
    editV.pack_start(nameB)
    nameL = gtk.Label(" Project name     : ")
    nameB.pack_start(nameL)
    nameE = gtk.Entry()
    nameE.set_text(projectname)
    nameB.pack_start(nameE)
    
    statB = gtk.HBox(True, 5)
    editV.pack_start(statB)
    statL = gtk.Label(" Project status   : ")
    statB.pack_start(statL)
    statE = gtk.Entry()
    statE.set_text(projectstatus)
    statB.pack_start(statE)
    
    direB = gtk.HBox(True, 5)
    editV.pack_start(direB)
    direL = gtk.Label(" Project director : ")
    direB.pack_start(direL)
    direE = gtk.Entry()
    direE.set_text(projectleader)
    direB.pack_start(direE)
    
    assetsLabel = gtk.Label("Amount of ASSETS to make")
    editV.pack_start(assetsLabel)
    
    charB = gtk.HBox(True, 5)
    editV.pack_start(charB)
    charL = gtk.Label(" Characters       : ")
    charB.pack_start(charL)
    charE = gtk.Entry()
    charE.set_text(projectchar)
    charB.pack_start(charE)
    
    vehiB = gtk.HBox(True, 5)
    editV.pack_start(vehiB)
    vehiL = gtk.Label(" Vehicles         : ")
    vehiB.pack_start(vehiL)
    vehiE = gtk.Entry()
    vehiE.set_text(projectvehi)
    vehiB.pack_start(vehiE)
    
    objeB = gtk.HBox(True, 5)
    editV.pack_start(objeB)
    objeL = gtk.Label(" Objects          : ")
    objeB.pack_start(objeL)
    objeE = gtk.Entry()
    objeE.set_text(projectobje)
    objeB.pack_start(objeE)
    
    locaB = gtk.HBox(True, 5)
    editV.pack_start(locaB)
    locaL = gtk.Label(" Locations        : ")
    locaB.pack_start(locaL)
    locaE = gtk.Entry()
    locaE.set_text(projectloca)
    locaB.pack_start(locaE)
    
    scenesexp = gtk.Label("Storyboards, Animations, Renders")
    editV.pack_start(scenesexp)
    
    scenB = gtk.HBox(True, 5)
    editV.pack_start(scenB)
    scenL = gtk.Label(" Scenes           : ")
    scenB.pack_start(scenL)
    scenE = gtk.Entry()
    scenE.set_text(projectscen)
    scenB.pack_start(scenE)
    
    banneredit = gtk.Label(" The banner image and Icon \n is located at")
    editV.pack_start(banneredit)
    
    
    address = gtk.Label(os.getcwd()+"/py_data/")
    address.set_selectable(True)
    editV.pack_start(address)
    
    
    
    openpy_data = gtk.Button("Open Forlder Containting\n      Banner & Icon      ")
    openpy_data.connect("clicked", lambda w: os.system("nautilus "+os.getcwd()+"/py_data/"))
    editV.pack_start(openpy_data)
    
    
    
    prbanner = gtk.Image()
    prbanner.set_from_file("py_data/banner.png")
    editV.pack_start(prbanner)
    
    save_exit = gtk.HBox(True, 5)
    editV.pack_start(save_exit)
    
    
    
    savebutt = gtk.Button("Save Changes")
    save_exit.pack_start(savebutt)
    savebutt.connect("clicked",editprojectsave)
    
    exitbutt = gtk.Button("Discard Changes")
    save_exit.pack_start(exitbutt)
    exitbutt.connect("clicked", lambda w: editproject.destroy())
    
    
    
    
    
    
    
    
    
    
    
    
    
    editproject.show_all()

def editprojectsave(widget):

    global nameE
    global statE
    global direE
    global charE
    global vehiE
    global objeE
    global locaE
    global scenE
    
    global editproject
    
    data = []
    
    data.append("Project  : "+nameE.get_text()+"\n")
    data.append("Status   : "+statE.get_text()+"\n")
    data.append("Director : "+direE.get_text()+"\n")
    data.append("           \n")
    data.append("___Needs___\n")
    
    if int(charE.get_text()) < len(os.walk(os.getcwd()+"/dev/chr").next()[1]):
        charE = str(len(os.walk(os.getcwd()+"/dev/chr").next()[1]))
        data.append("Character: "+charE+"\n")
    else:
        data.append("Character: "+charE.get_text()+"\n")
    
    if int(locaE.get_text()) < len(os.walk(os.getcwd()+"/dev/loc").next()[1]):
        locaE = str(len(os.walk(os.getcwd()+"/dev/loc").next()[1]))
        data.append("Locations: "+locaE+"\n")
    else:
        data.append("Locations: "+locaE.get_text()+"\n")
    
    if int(objeE.get_text()) < len(os.walk(os.getcwd()+"/dev/obj").next()[1]):
        objeE = str(len(os.walk(os.getcwd()+"/dev/obj").next()[1]))
        data.append("Objects  : "+objeE+"\n")
    else:
        data.append("Objects  : "+objeE.get_text()+"\n")
    
    if int(vehiE.get_text()) < len(os.walk(os.getcwd()+"/dev/veh").next()[1]):
        vehiE = str(len(os.walk(os.getcwd()+"/dev/veh").next()[1]))
        data.append("Vehicles : "+vehiE+"\n")
    else:
        data.append("Vehicles : "+vehiE.get_text()+"\n")
    
    # if int(vehiE.get_text()) < len(os.walk(os.getcwd()+"/dev/chr").next()[1]):
    #        vehiE.set_text() = str(len(os.walk(os.getcwd()+"/dev/chr").next()[1]))
    data.append("Scenes   : "+scenE.get_text()+"\n")
    
    
    
    with open("project.data", "w") as saving:
        saving.writelines(data)
    
    editproject.destroy()
    orgabox1.destroy()
    
    Refresher()
    
##### refresher

def Refresher():

    orgabox1.destroy()
    if curwid in ["char", "vehi", "obje","loca"]:
        organ(True)
        orgabox1.show_all()
    else:
        scene_box(True)
        orgabox1.show_all()


curfile = " "
curfiledev = False
def changefile(widget, selectedfile):

    global curfile
    global curfiledev
    
    if selectedfile[-16:] == " (in Developing)":
        selectedfile = selectedfile[:-16]
        curfiledev = True
    else:
        curfiledev = False
    
    curfile = selectedfile
    Refresher()

    
    
    
### simple command to start a software in a new thread
def sysopen(command):
    
    import subprocess
    
    tmp = open("py_data/last_command.sh", "w")
    tmp.write(command)
    tmp.close()
    
    
    p = subprocess.Popen(['/bin/sh', os.path.expanduser(os.getcwd()+"/py_data/last_command.sh")])
    
    #thread = threading.Thread(target=systemcommad, args=(command,))
    #thread.daemon = True
    #thread.start()


def systemcommad(word):
    print "trying to start blender"
    os.system(word)
    

########### ________ SCENE _____ ############

selectedscene = None
def scene_box(widget):

    global orgabox1
    global mainbox
    global prbanner
    global curwid
    global mustbe
    global showdev
    global show_dev
    global orgafun
    global curfile
    global curfiledev
    
    global check274tf
    global check274
    
    cfplease = ""
        
    if curwid == "char":
        cfplease = "chr"
        
    elif curwid == "vehi":
        cfplease = "veh"
        
    elif curwid == "loca":
        cfplease = "veh"
        
    elif curwid == "obje":
        cfplease = "obj"
    
    
    
    
    
    
    readData()
    orgabox1 = gtk.VBox(False, 5)
    mainbox.pack_start(orgabox1)
    
    progresbox = gtk.VBox(False)
    orgabox1.pack_start(progresbox)
    
    
    
    
    
    
    
    welDbutton = gtk.Button()
    welDbutton.set_tooltip_text("Open Project's Checklist")
    
    welDbox = gtk.HBox(False)
    #welDbox.set_layout(gtk.BUTTONBOX_START)
    welDbutton.add(welDbox)
    
    checklisticon = gtk.Image()
    checklisticon.set_from_file("py_data/icons/checklist.png")
    
    welDbox.pack_start(checklisticon, False)
    
    welD = gtk.ProgressBar()
    welD.set_text(("◀ Assets/scenes: "+assetpercent+"% ▶    ◀ Project checklist: "+checklistpercent+"% ▶     ◀ Avarage: "+projectpercent+"% ▶"))
    welD.set_fraction((float(projectpercent)/100))
    
    welDbox.pack_start(welD)
    welDbutton.connect("clicked", projectchecklist)
    
    progresbox.pack_start(welDbutton, False)
    
    SCENEStitle = gtk.Label("Scenes")
    progresbox.pack_start(SCENEStitle, False)
    
    titlesbox = gtk.HBox(False)
    orgabox1.pack_start(titlesbox, False)
    
    abovelistbox = gtk.VBox(False)
    titlesbox.pack_start(abovelistbox, False)
    
    ### EVALUATING THE PERSENTAGE OF DONE SCENES
    
    # projectscen
    
    
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
    
    print "scenpercent", scenpercent
    
    scenesinfolist = sorted(scenesinfolist)
    
    #MAKING THE PROGRESS BAR
    
    sceneprogress = gtk.ProgressBar()
    sceneprogress.set_fraction(scenpercent)
    sceneprogress.set_text("Scenes "+str(int(scenpercent*100))+"% Done")
    progresbox.pack_start(sceneprogress, False)
    
    ### LET"S DO IT
    
    folderbuttons = gtk.HBox(False)
    progresbox.pack_start(folderbuttons, False)
    
    def openrndfolder(w):
        os.system("nautilus "+os.getcwd()+"/rnd/")
    
    opendevdictbox = gtk.HBox(False)
        
    foldericon = gtk.Image()
    foldericon.set_from_file("py_data/icons/folder.png")
    opendevdictbox.pack_start(foldericon)
    
    opendevdictlabel = gtk.Label("/rnd")
    
    opendevdictbox.pack_start(opendevdictlabel)
    
    
    
    opendevdict = gtk.Button()
    opendevdict.add(opendevdictbox)
    opendevdict.set_tooltip_text("Open Folder /rnd/ \nIn Nautilus\n(Default File Manager)")
    opendevdict.connect("clicked", openrndfolder)
    
    folderbuttons.pack_end(opendevdict, False)
    
    
    ## LIST OF SCENES
    
    
    scenesHbox = gtk.HBox(False)
    progresbox.pack_start(scenesHbox)
    
    scenelistscroll = gtk.ScrolledWindow()
    scenelistscroll.set_size_request(400,400)
    scenesHbox.pack_start(scenelistscroll, False)
    
    scenelistbox = gtk.VBox(False)
    scenelistscroll.add_with_viewport(scenelistbox)
    
    
    def open_scene(w, scene):
        
        global selectedscene
        selectedscene = scene
        
        Refresher()
        
    for x, i in enumerate(scenesinfolist):
        
        # scn_asset_done.png
        
        n = str(x)
        
        
        
        
        com = "scncallbutton"+n+" = gtk.Button()"
        exec(com) in locals(), globals()
        
        com = "scncallicon"+n+" = gtk.Image()"
        exec(com) in locals(), globals()
        
        if i[-1] == 1.0:
            com = "scncallicon"+n+".set_from_file('py_data/icons/scn_asset_done.png')"
            exec(com) in locals(), globals()
        else:
            com = "scncallicon"+n+".set_from_file('py_data/icons/scn_asset_undone.png')"
            exec(com) in locals(), globals()
        
        com = "scncallbox"+n+" = gtk.HBox(False)"
        exec(com) in locals(), globals()
        
        com = "scncallbox"+n+".pack_start(scncallicon"+n+", False)"
        exec(com) in locals(), globals()
        
        
        com = "scncallprogress"+n+" = gtk.ProgressBar()"
        exec(com) in locals(), globals()
        
        com = "scncallprogress"+n+".set_fraction("+str(i[-1])+")"
        exec(com) in locals(), globals()
        
        
        com = "scncallbox"+n+".pack_end(scncallprogress"+n+", False)"
        exec(com) in locals(), globals()
        
        com = "scncallbox"+n+".pack_start(gtk.Label('"+i[0]+"'), False)"
        exec(com) in locals(), globals()
        
        com = "scncallbutton"+n+".add(scncallbox"+n+")"
        exec(com) in locals(), globals()
        
        com = "scncallbutton"+n+".connect('clicked', open_scene, x)"
        exec(com) in locals(), globals()
        
        com = "scenelistbox.pack_start(scncallbutton"+n+", False)"
        exec(com) in locals(), globals()
    
    ## ADD NEW SCENE
    scenelistbox.pack_start(gtk.HSeparator(), False)
    
    newscenebox = gtk.HBox(False)
    scenelistbox.pack_start(newscenebox, False)
    newscenebox.pack_start(gtk.Label(" New Scene: "), False)
    
    def createnewscene(w):
        path = os.getcwd()+"/rnd/"+newscenename.get_text().replace(" ", "_")
        
        if not os.path.exists(path):
            os.mkdir(path)
            
            Refresher()
        
        
    newscenename = gtk.Entry()
    newscenename.connect("activate", createnewscene)
    newscenename.set_text("Scene_Name")
    newscenebox.pack_start(newscenename)
    
    createscene = gtk.Button("Create New Scene")
    createscene.connect("clicked", createnewscene)
    newscenebox.pack_end(createscene, False)


    
    scenelistbox.pack_start(gtk.HSeparator(), False)
    
    ## ACTUAL SCENES
    
    
    
    
    
    
    selectedscenebox = gtk.VBox(False)
    scenesHbox.pack_end(selectedscenebox)
    
    
    
    
    
    customblenderbox = gtk.HBox(False)
    selectedscenebox.pack_end(customblenderbox, False)
    
    
    
    
    check274 = gtk.CheckButton("Use Custom Blender") ### just for functions to work LOL
    check274.set_active(check274tf)
    check274.connect("clicked", showdevelop)
    
    customblenderbox.pack_start(check274, False)
    
    
    def edit_custompath(w):
        
        path = w.get_text()
        
        global custompath
        custompath = path
        
        pathsdata = tuple(open("custompaths.data", "r"))
        
        tmp = []
        
        for i in pathsdata:
            tmp.append(i)
        
        pathsdata = tmp
        
        for x, i in enumerate(pathsdata):
            if i.startswith("Blndrpath: "):
                pathsdata[x] = "Blndrpath: "+custompath
        
        tmp = ""
        for i in pathsdata:
            tmp = tmp + i + "\n"
        
        tmp = tmp[:-1]
        pathsdata = tmp
        
        save = open("custompaths.data", "w")
        save.write(pathsdata)
        save.close()
       
        
    custompathentry = gtk.Entry()
    custompathentry.connect("changed", edit_custompath)
    customblenderbox.pack_start(custompathentry)
    custompathentry.set_tooltip_text("Custom Blender Path")
    custompathentry.set_text(custompath)
    
    def on_openb(widget):
        widget.set_sensitive(False)
        
        addbuttondialog = gtk.FileChooserDialog("Open..",
                                         None,
                                         gtk.FILE_CHOOSER_ACTION_OPEN,
                                        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                         gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        addbuttondialog.set_default_response(gtk.RESPONSE_OK)
        
        
        
        
        response = addbuttondialog.run()
        if response == gtk.RESPONSE_OK:
            
            get = addbuttondialog.get_filename()
            custompathentry.set_text(get)
            
        widget.set_sensitive(True)
        addbuttondialog.destroy()
    
    
    chose_blenderfolder = gtk.Button("Path")
    chose_blenderfolder.connect("clicked", on_openb)
    customblenderbox.pack_end(chose_blenderfolder, False)
    chose_blenderfolder.set_tooltip_text("Choose the blender executable file")
    
    
    
    
    
    
    
    
    
    if selectedscene != None:
        try:
            selectedscenebox.pack_start(gtk.Label("Scene: [ "+scenesinfolist[selectedscene][0]+" ]"), False)
            
            #### HERE WILL BE THE SETTINGS AND SHIT
            
            shotsscroll = gtk.ScrolledWindow()
            selectedscenebox.pack_start(shotsscroll)
            
            shotsbox = gtk.VBox(False, 20)
            shotsscroll.add_with_viewport(shotsbox)
            
            
            thelist = sorted(scenesinfolist[selectedscene])
            
            for x, i in enumerate(thelist):
                
                n = str(x)
                
                if i not in [scenesinfolist[selectedscene][0], scenesinfolist[selectedscene][-1]]:
                    
                    com = "frame"+n+" = gtk.Frame('Shot: "+i[0]+"')"
                    exec(com) in locals(), globals()
                    
                    com = "shotsbox.pack_start(frame"+n+", False)"
                    exec(com) in locals(), globals()
                    
                    com = "inframebox"+n+" = gtk.VBox(False)"
                    exec(com) in locals(), globals()
                    
                    com = "frame"+n+".add(inframebox"+n+")"
                    exec(com) in locals(), globals()
                    
                    
                    com = "shotprogress"+n+" = gtk.ProgressBar()"
                    exec(com) in locals(), globals()
                    
                    
                    
                    com = "shotprogress"+n+".set_fraction("+str(float(i[1])/3)+")"
                    exec(com) in locals(), globals()
                    
                    if i[1] == 0:
                        com = "shotprogress"+n+".set_text('Stage: Planning / Scripting')"
                    if i[1] == 1:
                        com = "shotprogress"+n+".set_text('Stage: Story-boarding / Preparing')"
                    if i[1] == 2:
                        com = "shotprogress"+n+".set_text('Stage: Animating / Testing')"
                    if i[1] == 3:
                        com = "shotprogress"+n+".set_text('Stage: Rendering / Finished')"
                    
                    exec(com) in locals(), globals()
                    
                    com = "inframebox"+n+".pack_start(shotprogress"+n+", False)"
                    exec(com) in locals(), globals()
            
            
            
                    com = "inframefolders"+n+" = gtk.HBox(True)"
                    exec(com) in locals(), globals()
                    
                    com = "inframebox"+n+".pack_start(inframefolders"+n+", False)"
                    exec(com) in locals(), globals()
                    
                    
                    def openfolder(w, path):
                        os.system("nautilus "+os.getcwd()+"/rnd/"+scenesinfolist[selectedscene][0]+"/"+path)
                    
                    #shot button
                    
                    com = "shot"+n+" = gtk.Button()"
                    exec(com) in locals(), globals()
                    
                    com = "shotbox"+n+" = gtk.HBox(False)"
                    exec(com) in locals(), globals()
                    
                    com = "shoticon"+n+" = gtk.Image()"
                    exec(com) in locals(), globals()
                    
                    com = "shoticon"+n+".set_from_file('py_data/icons/folder.png')"
                    exec(com) in locals(), globals()
                    
                    com = "shotbox"+n+".pack_start(shoticon"+n+", False)"
                    exec(com) in locals(), globals()
                    
                    com = "shotbox"+n+".pack_start(gtk.Label('.../'))"
                    exec(com) in locals(), globals()
                    
                    com = "shot"+n+".add(shotbox"+n+")"
                    exec(com) in locals(), globals()
                    
                    com = "shot"+n+".connect('clicked', openfolder, '"+i[0]+"' )"
                    exec(com) in locals(), globals()
                    
                    
                    com = "inframefolders"+n+".pack_start(shot"+n+")"
                    exec(com) in locals(), globals()
                    
                    #storyboard button
                    
                    com = "storyboard"+n+" = gtk.Button()"
                    exec(com) in locals(), globals()
                    
                    com = "storyboardbox"+n+" = gtk.HBox(False)"
                    exec(com) in locals(), globals()
                    
                    com = "storyboardicon"+n+" = gtk.Image()"
                    exec(com) in locals(), globals()
                    
                    com = "storyboardicon"+n+".set_from_file('py_data/icons/folder.png')"
                    exec(com) in locals(), globals()
                    
                    com = "storyboardbox"+n+".pack_start(storyboardicon"+n+", False)"
                    exec(com) in locals(), globals()
                    
                    com = "storyboardbox"+n+".pack_start(gtk.Label('.../storyboard'))"
                    exec(com) in locals(), globals()
                    
                    com = "storyboard"+n+".add(storyboardbox"+n+")"
                    exec(com) in locals(), globals()
                    
                    com = "storyboard"+n+".connect('clicked', openfolder, '"+i[0]+"/storyboard' )"
                    exec(com) in locals(), globals()
                    
                    
                    com = "inframefolders"+n+".pack_start(storyboard"+n+")"
                    exec(com) in locals(), globals()
                    
                    #opengl button
                    
                    com = "opengl"+n+" = gtk.Button()"
                    exec(com) in locals(), globals()
                    
                    com = "openglbox"+n+" = gtk.HBox(False)"
                    exec(com) in locals(), globals()
                    
                    com = "openglicon"+n+" = gtk.Image()"
                    exec(com) in locals(), globals()
                    
                    com = "openglicon"+n+".set_from_file('py_data/icons/folder.png')"
                    exec(com) in locals(), globals()
                    
                    com = "openglbox"+n+".pack_start(openglicon"+n+", False)"
                    exec(com) in locals(), globals()
                    
                    com = "openglbox"+n+".pack_start(gtk.Label('.../opengl'))"
                    exec(com) in locals(), globals()
                    
                    com = "opengl"+n+".add(openglbox"+n+")"
                    exec(com) in locals(), globals()
                    
                    com = "opengl"+n+".connect('clicked', openfolder, '"+i[0]+"/opengl' )"
                    exec(com) in locals(), globals()
                    
                    
                    com = "inframefolders"+n+".pack_start(opengl"+n+")"
                    exec(com) in locals(), globals()
                    
                    #rendered button
                    
                    com = "rendered"+n+" = gtk.Button()"
                    exec(com) in locals(), globals()
                    
                    com = "renderedbox"+n+" = gtk.HBox(False)"
                    exec(com) in locals(), globals()
                    
                    com = "renderedicon"+n+" = gtk.Image()"
                    exec(com) in locals(), globals()
                    
                    com = "renderedicon"+n+".set_from_file('py_data/icons/folder.png')"
                    exec(com) in locals(), globals()
                    
                    com = "renderedbox"+n+".pack_start(renderedicon"+n+", False)"
                    exec(com) in locals(), globals()
                    
                    com = "renderedbox"+n+".pack_start(gtk.Label('.../rendered'))"
                    exec(com) in locals(), globals()
                    
                    com = "rendered"+n+".add(renderedbox"+n+")"
                    exec(com) in locals(), globals()
                    
                    com = "rendered"+n+".connect('clicked', openfolder, '"+i[0]+"/rendered' )"
                    exec(com) in locals(), globals()
                    
                    
                    com = "inframefolders"+n+".pack_start(rendered"+n+")"
                    exec(com) in locals(), globals()
                    
                    
                    
                    blendfileofthescene = []
                    for h in os.listdir(os.getcwd()+"/rnd/"+scenesinfolist[selectedscene][0]+"/"+i[0]):
                        
                        if h.endswith(".blend"):
                            blendfileofthescene.append(h)
                    
                    if len(blendfileofthescene) == 0:
                        blendfileofthescene = [False]
                    
                    
                    for m, h in enumerate(blendfileofthescene):
                        k = str(m)
                        
                        
                        if h != False:
                            com = "filebutton"+n+"_"+k+" = gtk.Button('"+h+"')"
                            exec(com) in locals(), globals()
                            
                            com = "filebutton"+n+"_"+k+".props.relief = gtk.RELIEF_NONE"
                            exec(com) in locals(), globals()
                            
                            com = "filebutton"+n+"_"+k+".set_use_underline(False)"
                            exec(com) in locals(), globals()
                            
                            com = "inframebox"+n+".pack_start(filebutton"+n+"_"+k+")"
                            exec(com) in locals(), globals()
                            
                            def openinblender(w, path):
                                
                                print "path", path
                                
                                if check274tf == False:
                                    os.system("xdg-open "+path)
                                    
                                if check274tf == True:
                                    sysopen(""+custompath+" "+path)
                            
                            path = os.getcwd()+"/rnd/"+scenesinfolist[selectedscene][0]+"/"+i[0]+"/"+h
                            com = "filebutton"+n+"_"+k+".connect('clicked', openinblender, '"+path+"')"
                            exec(com) in locals(), globals()
                                                                        
                        else:
                            com = "filebutton"+n+"_"+k+" = gtk.Button('Generate: "+scenesinfolist[selectedscene][0]+"_"+i[0]+".blend')"
                            exec(com) in locals(), globals()
                            
                            com = "filebutton"+n+"_"+k+".props.relief = gtk.RELIEF_NONE"
                            exec(com) in locals(), globals()
                            
                            com = "filebutton"+n+"_"+k+".set_use_underline(False)"
                            exec(com) in locals(), globals()
                            
                            
                            
                            path = os.getcwd()+"/rnd/"+scenesinfolist[selectedscene][0]+"/"+i[0]+"/"+scenesinfolist[selectedscene][0]+"_"+i[0]+".blend"
                            com = "filebutton"+n+"_"+k+".connect('clicked', generateblend, '"+path+"')"
                            exec(com) in locals(), globals()
                            
                            com = "inframebox"+n+".pack_start(filebutton"+n+"_"+k+")"
                            exec(com) in locals(), globals()
            
            
            
                        
            addingshots = gtk.HBox(False)
            
            shotsbox.pack_start(gtk.HSeparator(), False)
            shotsbox.pack_start(addingshots, False)
            
            
            
            addingshots.pack_start(gtk.Label("  New shot:"), False)
            
            shotnameentry = gtk.Entry()
            shotnameentry.set_text("The_New_Shot_Name")
            
            addingshots.pack_start(shotnameentry)
            
            def addnewshot(w, path):
                
                path = path+shotnameentry.get_text().replace(" ", "_")
                
                if not os.path.exists(path):
                    try:
                        os.mkdir(path)
                        os.mkdir(path+"/storyboard")
                        os.mkdir(path+"/opengl")
                        os.mkdir(path+"/rendered")
                        
                        Refresher()
                        
                    except:
                        print "WELL FAILED TO CREATE THE SHOT"
            
            path = os.getcwd()+"/rnd/"+scenesinfolist[selectedscene][0]+"/"
            newshotbutton = gtk.Button("Add New Shot")
            newshotbutton.connect("clicked",addnewshot, path)
            shotnameentry.connect("activate",addnewshot, path)
            addingshots.pack_end(newshotbutton, False)
            
            
            shotsbox.pack_start(gtk.HSeparator(), False)
    
            
        except Exception, expection:
            selectedscenebox.pack_start(gtk.Label("ERROR:\n"+str(expection)), False)    
            raise
    
        
    else:
        selectedscenebox.pack_start(gtk.Label("No scene selected"), False)
    
    



    
#checklistwin = None
checklistpos = None
checkbox = None
checklistwin = None

def thechecklist(widget):
    
    
    try:
        checklistwin.destroy()
    except:
        pass
    
    print "checklist window"
    
    global checklistwin
    global checklistpos
    global checkscroll
    
    checklistwin = gtk.Window()
    if curfile != " ":
        
        checklistwin.set_title("Check List of ASSET: "+curfile)
    else:
        checklistwin.set_title("Project Checklist")
    checklistwin.set_default_size(650, 500)
    checklistwin.connect("destroy", lambda w: Refresher())
    
    checkscroll = gtk.ScrolledWindow()
    checklistwin.add(checkscroll)
    checkscroll.set_vadjustment(checklistpos)
    
    check_updatable(True)
    
    checklistwin.show_all()

for i in range(0, 2048):
    
    com = "newindentname_"+str(i)+" = None"
    exec(com)
startdate = None
enddate  = None
tmp = ""
def checkListOperations(widget, com, pos):
    
    
    global tmp
    
    if curfile != " ":
        checkfile = tuple(open(os.getcwd()+"/dev/"+cfplease+"/"+curfile+"/asset.progress", "r"))
    else:
        checkfile = tuple(open("project.progress", "r"))
    
    checktext = []
    for i in checkfile:
        checktext.append(i)
    
    if curfile != " ":
        savefile = open(os.getcwd()+"/dev/"+cfplease+"/"+curfile+"/asset.progress", "w")
    else:
        savefile = open("project.progress", "w")
    
    if com == "date":
        print startdate.get_text()
        for x, i in enumerate(checktext):
            if i[:4] == "STR ":
                checktext[x] = "STR "+startdate.get_text()+"\n"
            if i[:4] == "FIN ":
                checktext[x] = "FIN "+enddate.get_text()+"\n"
    
    if com == "check":
        if checktext[pos][:4] in ["[ ] ", "[X] "]:
            checktext[pos] = "[V] "+checktext[pos][4:]
        elif checktext[pos][:4] == "[V] ":
            checktext[pos] = "[ ] "+checktext[pos][4:]
        elif checktext[pos][:8] in ["    [ ] ", "    [X] "]:
            checktext[pos] = "    [V] "+checktext[pos][8:]
        elif checktext[pos][:8] == "    [V] ":
            checktext[pos] = "    [ ] "+checktext[pos][8:]
    
    if com == "cancel":
        if checktext[pos][:4] in ["[ ] ", "[V] "]:
            checktext[pos] = "[X] "+checktext[pos][4:]
        elif checktext[pos][:4] == "[X] ":
            checktext[pos] = "[ ] "+checktext[pos][4:]
        elif checktext[pos][:8] in ["    [ ] ", "    [V] "]:
            checktext[pos] = "    [X] "+checktext[pos][8:]
        elif checktext[pos][:8] == "    [X] ":
            checktext[pos] = "    [ ] "+checktext[pos][8:]
    
    if com == "up":
        try:
            
            tmp = checktext[pos]
            del checktext[pos]
            checktext.insert(pos-1, tmp)
        except:
            pass
    
    if com == "down":
        try:
            
            tmp = checktext[pos]
            del checktext[pos]
            checktext.insert(pos+1, tmp)
        except:
            pass
    
    if com == "delete":
        del checktext[pos]
    
    if com == "newsub":
        tmp = "    [ ] "
        command = 'tmp = tmp+newindentname_'+str(pos)+'.get_text()+"\\n"'
        com = "print newindentname_"+str(pos)+".get_text()"
        
        exec(com) in globals(), locals()
        
            
        try:
            exec(command) in globals()
            checktext.insert(pos, tmp)
            
        except:
            raise
    if com == "newmain":
        tmp = "[ ] "
        tmp = tmp+newindentname.get_text()+"\n"
        checktext.append(tmp)
        
        
        
            
        
    
    
#    for i in range(0, 26):
#        com = "print i, newindentname_"+str(i)+".get_text()"
#        try:
#            exec(com) in globals(), locals()
#        except:
#            print i, "Cant"
#    com = "print newindentname_"+str(pos)+".get_text()"
#        
#    exec(com) in globals(), locals()
    
    
    
    
    
    for i in checktext:
        savefile.write(i)
    savefile.close()
    
    
    ### REFRESHING CHECKLIST
    global checkbox
    global checklistpos
    global checklistwin
    
    checklistpos = checkscroll.get_vadjustment()
    
    checkbox.destroy()
    check_updatable(True)
    
    
    checklistwin.show_all()
newindentname = None

def check_updatable(widget):
    
    global checklistwin
    global checklistpos
    global checkbox
    global newindentname
    
    
    checkbox = gtk.VBox(False, 5)
    checkscroll.add_with_viewport(checkbox)
    
    
    for i in range(0, 2048):
        
        command = "global newindentname_"+str(i)
        exec (command) in globals(), locals()
        #print command
    
    # READING FILE
    
    if curfile != " ":
        checkfile = tuple(open(os.getcwd()+"/dev/"+cfplease+"/"+curfile+"/asset.progress", "r"))
    else:
        checkfile = tuple(open("project.progress", "r"))
    # DATES
    # format to use DAY/MONTH/YEAR
    
    DATESBOX = gtk.HBox(False, 5)
    checkbox.pack_start(DATESBOX)
    
    rawToday = datetime.date.today()
    print rawToday
    
    
    today = gtk.Label("⌚ Now: "+str(rawToday)[-2:]+"/"+str(rawToday)[5:7]+"/"+str(rawToday)[:4]+" Start:")
    DATESBOX.pack_start(today)
    
    
    global startdate
    startdate = gtk.Entry()
    for i in checkfile:
        if i[:4] == "STR ":
            startdate.set_text(i[4:][:-1])
    if startdate.get_text() == "00/00/0000":
        startdate.set_text(str(rawToday)[-2:]+"/"+str(rawToday)[5:7]+"/"+str(rawToday)[:4])
    DATESBOX.pack_start(startdate)
    startdate.connect("activate", checkListOperations, "date", True)
    
    endlabel = gtk.Label("End:")
    DATESBOX.pack_start(endlabel)
    
    global enddate
    enddate = gtk.Entry()
    for i in checkfile:
        if i[:4] == "FIN ":
            enddate.set_text(i[4:][:-1])
    if enddate.get_text() == "00/00/0000":
        enddate.set_text(str(rawToday)[-2:]+"/"+str(rawToday)[5:7]+"/"+str(rawToday)[:4])
    DATESBOX.pack_start(enddate)
    enddate.connect("activate", checkListOperations, "date", True)
    
    enddatebutton = gtk.Button("Save")
    DATESBOX.pack_start(enddatebutton)
    enddatebutton.connect("clicked", checkListOperations, "date", True)
    
    # Checklist him self
    
    checktext = []
    
    for i in checkfile:
        checktext.append(i)
    
    #making all of them equal sized
    
    longest = 0
    
    for i in checktext:
        if len(i) > longest and i[:4] in ["[ ] ","[V] ","[X] ","    "]:
            longest = len(i)
    
    
    for ind, i in enumerate(checktext):
        spaces = ""
        if len(i) < longest:
            for b in range(longest-len(i)):
                if i[:4] != "    ": 
                    spaces = spaces + " "
                else:
                    spaces = spaces + " "
            checktext[ind] = i[:-1]+spaces+"\n"
            
        print i
    
    checkitem = 0
    noindentcount = 0
    donemainsnumbers = []
    
    
    for i in checktext:
        
        if i[:4] in ["[ ] ","[V] ","[X] ", "FIN "]:
            #print i
            
            index = "_"+str(checkitem)
        
            if noindentcount != 0:
                globals()["addindentbox%s" % index] = gtk.HBox(False, 5)
                
                add_progress = "checkbox.pack_start(addindentbox_"+str(checkitem)+")"
                exec (add_progress) in globals(), locals()
                
                #make some sapce
                
                globals()["somespace%s" % index] = gtk.Label("")
                
                add_progress = "addindentbox_"+str(checkitem)+".pack_start(somespace_"+str(checkitem)+")"
                exec (add_progress) in globals(), locals()
                
                
                makenew = "newindentname"+index+" = gtk.Entry()"
                #makenew = "newindentname"+index+" = '"+index+"'"
                exec (makenew) in globals()
                #com = "print 'HERE'+newindentname"+index
                #exec(com) in globals()
                
                
                makenew = "newindentname"+index+".set_text('New Sub-task')"
                exec (makenew) in globals()
                globals()["newindentname%s" % index].connect("activate", checkListOperations, "newsub", checkitem)
                
                add_progress = "addindentbox_"+str(checkitem)+".pack_start(newindentname_"+str(checkitem)+")"
                exec (add_progress) in globals(), locals()
                # newsub
                globals()["newindentbutton%s" % index] = gtk.Button("Make New Sub-task")
                globals()["newindentbutton%s" % index].connect("clicked", checkListOperations, "newsub", checkitem)
                add_progress = "addindentbox_"+str(checkitem)+".pack_start(newindentbutton_"+str(checkitem)+")"
                exec (add_progress) in globals(), locals()
        
        if i[:4] in ["[ ] ","[V] ","[X] "]:
            #print i
            donemainsnumbers.append(checkitem)
            
            index = "_"+str(checkitem)
            
            
                
            
            noindentcount = noindentcount + 1
            
            
            
            
            globals()["checkbox%s" % index] = gtk.HBox(False, 5)
            
            add_progress = "checkbox.pack_start(checkbox_"+str(checkitem)+")"
            exec (add_progress) in globals(), locals()
            
            taskname = ""
            if i[:4] == "[ ] ":
                taskname = "☐ "+i[4:]
            elif i[:4] == "[V] ":
                taskname = "☑ "+i[4:]
            elif i[:4] == "[X] ":
                taskname = "☒ "+i[4:]
            
            globals()["progress%s" % index] = gtk.ProgressBar()
            globals()["progress%s" % index].set_text(taskname[:-1])
            
            add_progress = "checkbox_"+str(checkitem)+".pack_start(progress_"+str(checkitem)+")"
            exec (add_progress) in globals(), locals()
            
            #☐☑☒
            #↑↓
            
            
            
            if i[:4] in ["[ ] ", "[X] "]:
                globals()["checkbutton%s" % index] = gtk.Button("☑")
            else:
                globals()["checkbutton%s" % index] = gtk.Button("☐")
            globals()["checkbutton%s" % index].connect("clicked", checkListOperations, "check", checkitem)
            
            add_progress = "checkbox_"+str(checkitem)+".pack_start(checkbutton_"+str(checkitem)+")"
            exec (add_progress) in globals(), locals()
            
            
            if i[:4] in ["[ ] ", "[V] "]:
                globals()["cancelbutton%s" % index] = gtk.Button("☒")
            else:
                globals()["cancelbutton%s" % index] = gtk.Button("☐")
            
            add_progress = "checkbox_"+str(checkitem)+".pack_start(cancelbutton_"+str(checkitem)+")"
            exec (add_progress) in globals(), locals()
            globals()["cancelbutton%s" % index].connect("clicked", checkListOperations, "cancel", checkitem)
            
            
            globals()["upbutton%s" % index] = gtk.Button("↑")
            globals()["upbutton%s" % index].connect("clicked", checkListOperations, "up", checkitem)
            add_progress = "checkbox_"+str(checkitem)+".pack_start(upbutton_"+str(checkitem)+")"
            exec (add_progress) in globals(), locals()
            
            globals()["downbutton%s" % index] = gtk.Button("↓")
            globals()["downbutton%s" % index].connect("clicked", checkListOperations, "down", checkitem)
            add_progress = "checkbox_"+str(checkitem)+".pack_start(downbutton_"+str(checkitem)+")"
            exec (add_progress) in globals(), locals()
            
            
            globals()["deletebutton%s" % index] = gtk.Button("Delete")
            globals()["deletebutton%s" % index].connect("clicked", checkListOperations, "delete", checkitem)
            
            add_progress = "checkbox_"+str(checkitem)+".pack_start(deletebutton_"+str(checkitem)+")"
            exec (add_progress) in globals(), locals()
            
            
            
            
            
            
            
        elif i[:8] in ["    [ ] ","    [V] ","    [X] "]:
            #print i
            index = "_"+str(checkitem)
            globals()["checkbox%s" % index] = gtk.HBox(False)
            
            add_progress = "checkbox.pack_start(checkbox_"+str(checkitem)+")"
            exec (add_progress) in globals(), locals()
            
            taskname = ""
            if i[:8] == "    [ ] ":
                taskname = "    ☐ "+i[8:]
            elif i[:8] == "    [V] ":
                taskname = "    ☑ "+i[8:]
            elif i[:8] == "    [X] ":
                taskname = "    ☒ "+i[8:]
            
            
            globals()["progress%s" % index] = gtk.Label(taskname[:-1])
            
            
            commmand = "progress_"+str(checkitem)+".modify_font(pango.FontDescription('Ubuntu Mono'))"
            exec (commmand) in globals(), locals()
            
            add_progress = "checkbox_"+str(checkitem)+".pack_start(progress_"+str(checkitem)+")"
            exec (add_progress) in globals(), locals()
            
            
            
            #☐☑☒
            
            if i[:8] in ["    [ ] ", "    [X] "]:
                globals()["checkbutton%s" % index] = gtk.Button("☑")
            else:
                globals()["checkbutton%s" % index] = gtk.Button("☐")
            
            globals()["checkbutton%s" % index].connect("clicked", checkListOperations, "check", checkitem)
            
            add_progress = "checkbox_"+str(checkitem)+".pack_start(checkbutton_"+str(checkitem)+")"
            exec (add_progress) in globals(), locals()
            
            
            if i[:8] in ["    [ ] ", "    [V] "]:
                globals()["cancelbutton%s" % index] = gtk.Button("☒")
            else:
                globals()["cancelbutton%s" % index] = gtk.Button("☐")
                
            add_progress = "checkbox_"+str(checkitem)+".pack_start(cancelbutton_"+str(checkitem)+")"
            exec (add_progress) in globals(), locals()
            
            globals()["cancelbutton%s" % index].connect("clicked", checkListOperations, "cancel", checkitem)
            
            
            globals()["upbutton%s" % index] = gtk.Button("↑")
            globals()["upbutton%s" % index].connect("clicked", checkListOperations, "up", checkitem)
            add_progress = "checkbox_"+str(checkitem)+".pack_start(upbutton_"+str(checkitem)+")"
            exec (add_progress) in globals(), locals()
            
            globals()["downbutton%s" % index] = gtk.Button("↓")
            globals()["downbutton%s" % index].connect("clicked", checkListOperations, "down", checkitem)
            add_progress = "checkbox_"+str(checkitem)+".pack_start(downbutton_"+str(checkitem)+")"
            exec (add_progress) in globals(), locals()
            
            globals()["deletebutton%s" % index] = gtk.Button("Delete")
            globals()["deletebutton%s" % index].connect("clicked", checkListOperations, "delete", checkitem)
            add_progress = "checkbox_"+str(checkitem)+".pack_start(deletebutton_"+str(checkitem)+")"
            exec (add_progress) in globals(), locals()
            
            checkbox.pack_start(gtk.HSeparator(), False) # VISUAL LINE AT EVERY ENTRY
            
            
        checkitem = checkitem + 1
    print "CHECKITEM = "+str(checkitem)
    print donemainsnumbers
    for x, i in enumerate(checkfile):
        
        index = "_"+str(x)
        
        if x in donemainsnumbers:
            if i[:4] in ["[V] ", "[X] "]:
                
                
                
                globals()["progress%s" % index].set_fraction(1)
                
            elif i[:4] == "[ ] ":
                print " ___ "
                print x
                print "----"
                
                ALL = 0.0
                DON = 0.0
                
                try:
                    for b in range((x+1), donemainsnumbers[(donemainsnumbers.index(x)+1)]):
                        
                        
                        
                        for n, z in enumerate(checkfile):
                            
                            if n == b:
                                ALL = ALL + 1
                                if z[:8] in ["    [V] ", "    [X] "]:
                                    DON = DON + 1
                    print "ALL = "+str(ALL)
                    print "DON = "+str(DON)
                    try:
                        globals()["progress%s" % index].set_fraction((DON/ALL))
                    except:
                        globals()["progress%s" % index].set_fraction(0)
                except:
                    for b in range((x+1), len(checkfile)):
                        
                        
                        
                        for n, z in enumerate(checkfile):
                            
                            if n == b:
                                ALL = ALL + 1
                                if z[:8] in ["    [V] ", "    [X] "]:
                                    DON = DON + 1
                    print "ALL = "+str(ALL)
                    print "DON = "+str(DON)
                    try:
                        globals()["progress%s" % index].set_fraction((DON/ALL))
                    except:
                        globals()["progress%s" % index].set_fraction(0)
                
                
    newtaskmainbox = gtk.HBox(False, 5)
    checkbox.pack_start(newtaskmainbox)
    
    
    newindentname = gtk.Entry()
    newindentname.set_text("New Task")
    newtaskmainbox.pack_start(newindentname)
    newindentname.connect("activate",checkListOperations , "newmain", True)
    
    newtaskmainbutton = gtk.Button("Make New Task")
    newtaskmainbox.pack_start(newtaskmainbutton)
    newtaskmainbutton.connect("clicked",checkListOperations , "newmain", True)
    #checkListOperations(True, True, True)

def projectchecklist(widget):
    
    global curfile
    curfile = " "
    
    Refresher()
    
    thechecklist(True)


welcome_window()



gtk.main()
    
