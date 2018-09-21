# -*- coding: utf-8 -*-

# THIS IS A REWRITE ATTEMPT OF THE ORGINIZER
# THIS MAY MAKE THE ORGINIZER IT SELF MORE
# ORGINIZED LOL

# COPYRIGHT J.Y.AMIHUD 2018 under CC:BY LINCENCE
# YOU CAN FIND THE LICENCE ONLINE
# BASICALLY IT'S FREE TO USE AND SHARE AND MODIFY
# BUY MY NAME SHOULD BE CREDITED AS (made by J.Y.Amihud)

VERSION = 4.0


### IMPORTING MODULES

try:            # GIVING THE USER ALL NEEDED INFORMATION IF MODULES ARE MISSING
    # system
    import os
    import socket
    # calculational help
    import datetime
    import urllib2
    
    #1.0/0   # TESTER
    
except:
    
    print '''
ERROR !!! SOME OF THE PYTHON'S
MAIN MODULES ARE MISSING

os
socket
datetime
urllib2

to install those better to reinstall
python it self

use:
sudo apt-get remove python2
sudo apt-get install python2'''
    
    raw_input()
    exit()
    
try:  
  
    # graphics interface
    import gtk
    import pango
    import cairo
    import glib
    
    #1.0/0
    
except:
    print '''

ERROR !!! Py-GTK MODULES ARE MISSING

To install Py-GTK module do next commands


sudo apt-get install python-pip
sudo pip install PyGTK



'''
    
    raw_input()
    exit()
    
try:    
    try: 
        import Image
    except:
        from PIL import Image

    #1.0/0
except:
    print '''

ERROR !!! PIL MODULE IS MISSING

To install PIL module do next commands


sudo apt-get install python-pip
sudo pip install PIL



'''

    
    raw_input() #IN CASE THE TERMINAL IS LIKE CMD AND WILL CLOSE AUTOMATICALLY
    
    exit()
    
### IMPORTING OUR EXTENDED MODULES

from py_data.modules import analytics
from py_data.modules import assets
from py_data.modules import story_editor
from py_data.modules import checklist
from py_data.modules import schedule
from py_data.modules import update_window

### FILES FOLDERS MAKE SURE

# py_data bullshit






# others

try:
    os.mkdir(os.getcwd()+"/ast")
    os.mkdir(os.getcwd()+"/ast/chr")
    os.mkdir(os.getcwd()+"/ast/veh")
    os.mkdir(os.getcwd()+"/ast/loc")
    os.mkdir(os.getcwd()+"/ast/obj")
    
    os.mkdir(os.getcwd()+"/dev")
    os.mkdir(os.getcwd()+"/dev/chr")
    os.mkdir(os.getcwd()+"/dev/veh")
    os.mkdir(os.getcwd()+"/dev/loc")
    os.mkdir(os.getcwd()+"/dev/obj")
    
    os.mkdir(os.getcwd()+"/mus")
    os.mkdir(os.getcwd()+"/pln")
    os.mkdir(os.getcwd()+"/rnd")

except:
    pass

### MAIN WINDOW

# Let's Skip the old opening and make a 
# part of the new main window


mainwin = gtk.Window()
mainwin.set_title("Blender Organizer " + str(VERSION))
mainwin.maximize()
mainwin.connect("destroy", lambda w: gtk.main_quit())

mainbox = gtk.VBox(False)
mainwin.add(mainbox)


gtk.window_set_default_icon_from_file("py_data/icon.png")

# Let's make a quick functions panel on the top

toppannelbox = gtk.HBox(False)
mainbox.pack_start(toppannelbox, False)
mainbox.pack_start(gtk.HSeparator(), False)

# open project folder

projectfolder = gtk.Button()
projectfolder.props.relief = gtk.RELIEF_NONE
projectfolbox = gtk.HBox(False)
projectfolico = gtk.Image()
projectfolico.set_from_file("py_data/icons/folder.png")
projectfolbox.pack_start(projectfolico, False)
projectfolbox.pack_start(gtk.Label("  Project"))
projectfolder.add(projectfolbox)
projectfolder.set_tooltip_text("Open the "+os.getcwd())

def openpf(w=None):
    os.system("nautilus "+os.getcwd())
projectfolder.connect("clicked",openpf)

toppannelbox.pack_start(projectfolder, False)


# open rnd folder

rndfolder = gtk.Button()
rndfolder.props.relief = gtk.RELIEF_NONE
rndfolbox = gtk.HBox(False)
rndfolico = gtk.Image()
rndfolico.set_from_file("py_data/icons/folder.png")
rndfolbox.pack_start(rndfolico, False)
rndfolbox.pack_start(gtk.Label("  Renders"))
rndfolder.add(rndfolbox)
rndfolder.set_tooltip_text("Open the "+os.getcwd()+"/rnd")

def openpf(w=None):
    os.system("nautilus "+os.getcwd()+"/rnd")
rndfolder.connect("clicked",openpf)

toppannelbox.pack_start(rndfolder, False)
toppannelbox.pack_start(gtk.VSeparator(), False)


#### OLD STYLE ELEMENTS BUTTONS WITH A TWIST

CUR = "stats"

def chgCUR(w=None, cur=CUR):
    
    
    
    
    print cur
    global CUR
    CUR = cur
    drawmainbuttons()
    drawmain()
    
    
    
mainbuttonsbox = gtk.HBox()
toppannelbox.pack_start(mainbuttonsbox, False)

def drawmainbuttons():
    
    
    
    try:
        global mainbuttonsbox
        mainbuttonsbox.destroy()
        print "destroyed"
    except:
        pass
    
    mainbuttonsbox = gtk.HBox()
    
    
    
    
    # scenes

    scender = gtk.Button()
    scender.props.relief = gtk.RELIEF_NONE
    scenbox = gtk.HBox(False)
    scenico = gtk.Image()
    scenico.set_from_file("py_data/icons/scn_asset_undone.png")
    if CUR == "rnd":
        scenico.set_from_file("py_data/icons/scn_asset_done.png")
    scenbox.pack_start(scenico, False)
    scenbox.pack_start(gtk.Label("  Scenes"))
    scender.add(scenbox)
    scender.set_tooltip_text("Manage Scenes")
    scender.connect("clicked",chgCUR, "rnd")
    mainbuttonsbox.pack_start(scender, False)

    # characters

    charder = gtk.Button()
    charder.props.relief = gtk.RELIEF_NONE
    charbox = gtk.HBox(False)
    charico = gtk.Image()
    charico.set_from_file("py_data/icons/chr_asset_undone.png")
    if CUR == "chr":
        charico.set_from_file("py_data/icons/chr_asset_done.png")
    charbox.pack_start(charico, False)
    charbox.pack_start(gtk.Label("  Characters"))
    charder.add(charbox)
    charder.set_tooltip_text("Manage characters")
    charder.connect("clicked",chgCUR, "chr")
    mainbuttonsbox.pack_start(charder, False)
    
    # vehicles
    
    vehider = gtk.Button()
    vehider.props.relief = gtk.RELIEF_NONE
    vehibox = gtk.HBox(False)
    vehiico = gtk.Image()
    vehiico.set_from_file("py_data/icons/veh_asset_undone.png")
    if CUR == "veh":
        vehiico.set_from_file("py_data/icons/veh_asset_done.png")
    vehibox.pack_start(vehiico, False)
    vehibox.pack_start(gtk.Label("  Vehicles"))
    vehider.add(vehibox)
    vehider.set_tooltip_text("Manage Vehicles")
    vehider.connect("clicked",chgCUR, "veh")
    mainbuttonsbox.pack_start(vehider, False)
    
    # locations
    
    locider = gtk.Button()
    locider.props.relief = gtk.RELIEF_NONE
    locibox = gtk.HBox(False)
    lociico = gtk.Image()
    lociico.set_from_file("py_data/icons/loc_asset_undone.png")
    if CUR == "loc":
        lociico.set_from_file("py_data/icons/loc_asset_done.png")
    locibox.pack_start(lociico, False)
    locibox.pack_start(gtk.Label("  Locations"))
    locider.add(locibox)
    locider.set_tooltip_text("Manage locations")
    locider.connect("clicked",chgCUR, "loc")
    mainbuttonsbox.pack_start(locider, False)
    
   
    
    # Objects
    
    objider = gtk.Button()
    objider.props.relief = gtk.RELIEF_NONE
    objibox = gtk.HBox(False)
    objiico = gtk.Image()
    objiico.set_from_file("py_data/icons/obj_asset_undone.png")
    if CUR == "obj":
        objiico.set_from_file("py_data/icons/obj_asset_done.png")
    objibox.pack_start(objiico, False)
    objibox.pack_start(gtk.Label("  Objects"))
    objider.add(objibox)
    objider.set_tooltip_text("Manage objects")
    objider.connect("clicked",chgCUR, "obj")
    mainbuttonsbox.pack_start(objider, False)
    
    
    
    mainbuttonsbox.pack_start(gtk.VSeparator(), False)
    toppannelbox.pack_start(mainbuttonsbox, False)
    
    mainbuttonsbox.show_all()
    
drawmainbuttons()

# Analytics

startsider = gtk.Button()
startsider.props.relief = gtk.RELIEF_NONE
startsibox = gtk.HBox(False)
startsiico = gtk.Image()
startsiico.set_from_file("py_data/icons/stats.png")
startsibox.pack_start(startsiico, False)
startsibox.pack_start(gtk.Label("  Analytics"))
startsider.add(startsibox)
startsider.set_tooltip_text("See Analytics")
startsider.connect("clicked",chgCUR, "stats")
toppannelbox.pack_end(startsider, False)

# SYNC

syncider = gtk.Button()
syncider.props.relief = gtk.RELIEF_NONE
syncibox = gtk.HBox(False)
synciico = gtk.Image()
synciico.set_from_file("py_data/icons/sync.png")
syncibox.pack_start(synciico, False)
syncibox.pack_start(gtk.Label("  Synchronize"))
syncider.add(syncibox)
syncider.set_tooltip_text("Synchronize between multiple machines")
syncider.connect("clicked",chgCUR, "sync")
syncider.set_sensitive(False)
toppannelbox.pack_end(syncider, False)

# Update

def start_schedule(w):
    schedule.draw(os.getcwd())

Updateider = gtk.Button()
Updateider.props.relief = gtk.RELIEF_NONE
Updateibox = gtk.HBox(False)
Updateiico = gtk.Image()
Updateiico.set_from_file("py_data/icons/update.png")
Updateibox.pack_start(Updateiico, False)
Updateibox.pack_start(gtk.Label("  Update"))
Updateider.add(Updateibox)
Updateider.set_tooltip_text("Check for updates")
#Updateider.set_sensitive(False)
Updateider.connect("clicked", update_window.main, os.getcwd())


toppannelbox.pack_end(Updateider, False)

# Schedule

#make sure schedule.data exists
if os.path.exists(os.getcwd()+"/schedule.data") == False:
    
    s = open(os.getcwd()+"/schedule.data", "w")
    s.close()

Scheduleider = gtk.Button()
Scheduleider.props.relief = gtk.RELIEF_NONE
Scheduleibox = gtk.HBox(False)
Scheduleiico = gtk.Image()
Scheduleiico.set_from_file("py_data/icons/schedule.png")
Scheduleibox.pack_start(Scheduleiico, False)
Scheduleibox.pack_start(gtk.Label("  Schedule"))
Scheduleider.add(Scheduleibox)
Scheduleider.set_tooltip_text("Edit Scheduling")
Scheduleider.connect("clicked",start_schedule)

#toppannelbox.pack_end(Scheduleider, False)


# checklist

checklistider = gtk.Button()
checklistider.props.relief = gtk.RELIEF_NONE
checklistibox = gtk.HBox(False)
checklistiico = gtk.Image()
checklistiico.set_from_file("py_data/icons/checklist.png")
checklistibox.pack_start(checklistiico, False)
checklistibox.pack_start(gtk.Label("  Checklist"))
checklistider.add(checklistibox)
checklistider.set_tooltip_text("Open Main Checklist")
checklistider.connect("clicked", checklist.checkwindow, os.getcwd(), "Main Checklist", "project.progress")
toppannelbox.pack_end(checklistider, False)



#### DRAWING

drawbox = gtk.VBox(False)

def drawmain(w=None):
    
    
    
    
    global drawbox
    drawbox.destroy()
    
    
    drawbox = gtk.VBox(False)
    mainbox.pack_start(drawbox, True)
    
    if CUR in ["chr","obj","loc","veh"]:
        assets.draw_assets(os.getcwd(), drawbox, mainwin, CUR)
        
    
    if CUR == "stats":
        analytics.draw_analytics(os.getcwd(), drawbox, mainwin)

    mainbox.show_all()
    
    
    if CUR == "rnd":    
    
        story_editor.story(os.getcwd(), drawbox, mainwin)
drawmain()




# show the window
mainwin.show_all()


#run GTK
gtk.main()

