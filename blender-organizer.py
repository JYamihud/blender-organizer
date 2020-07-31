# -*- coding: utf-8 -*-

# THIS IS A REWRITE ATTEMPT OF THE ORGINIZER
# THIS MAY MAKE THE ORGINIZER IT SELF MORE
# ORGINIZED LOL

# COPYRIGHT J.Y.AMIHUD 2018 under CC:BY LINCENCE
# YOU CAN FIND THE LICENCE ONLINE
# BASICALLY IT'S FREE TO USE AND SHARE AND MODIFY
# BUY MY NAME SHOULD BE CREDITED AS (made by J.Y.Amihud)



# TRYING TO GET VERSION FROM UPDATE FILE



try:
    up = open("update_info.data", "r")
    VERSION = float(up.read().split("\n")[0][len("VERSION "):])
except:
    VERSION = 0.0


savename = open("MAIN_FILE", "w")
savename.write(str(__file__))
savename.close()






### IMPORTING MODULES

ER = 0

try:            # GIVING THE USER ALL NEEDED INFORMATION IF MODULES ARE MISSING
    # system
    import os
    import socket
    # calculational help
    import datetime
    import urllib2
    
    #1.0/0   # TESTER
    
except:
    ER = 1
    from py_data.modules import troubleshooter
    troubleshooter.shoot(ER)
    
    
    
try:  
  
    # graphics interface
    import gtk
    import pango
    import cairo
    import glib
    
    #1.0/0
    
except:
    ER = 2
    from py_data.modules import troubleshooter
    troubleshooter.shoot(ER)
    
    
try:    
    try: 
        import Image
    except:
        from PIL import Image

    #1.0/0
except:
    ER = 3
    from py_data.modules import troubleshooter
    troubleshooter.shoot(ER)

    
    
    
    
### IMPORTING OUR EXTENDED MODULES

from py_data.modules import analytics
from py_data.modules import assets
from py_data.modules import story_editor
from py_data.modules import checklist
from py_data.modules import schedule
from py_data.modules import update_window
from py_data.modules import blendver
from py_data.modules import history
from py_data.modules import oscalls

### FILES FOLDERS MAKE SURE

# py_data bullshit

history.write(os.getcwd(), "/", "[Project Started]")

#make sure schedule.data exists
if os.path.exists(os.getcwd()+"/schedule.data") == False:
    
    s = open(os.getcwd()+"/schedule.data", "w")
    s.close()


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
def buttons1():
    
    globals()["toppannelbox"] = gtk.HBox(False)
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
        oscalls.Open(os.getcwd())
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
        oscalls.Open(os.getcwd()+"/rnd")
    rndfolder.connect("clicked",openpf)

    toppannelbox.pack_start(rndfolder, False)
    toppannelbox.pack_start(gtk.VSeparator(), False)


    #### OLD STYLE ELEMENTS BUTTONS WITH A TWIST

    
        
        
        
    mainbuttonsbox = gtk.HBox()
    toppannelbox.pack_start(mainbuttonsbox, False)
buttons1()
CUR = "stats"

def chgCUR(w=None, cur=CUR):
    
    
    
    print "\033[1;31m ⬥ OPENING "+cur+" :  \033[1;m"
    
    global CUR
    CUR = cur
    drawmainbuttons()
    drawmain()
def drawmainbuttons():
    
    
    
    try:
        global mainbuttonsbox
        mainbuttonsbox.destroy()
        
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
    scenbox.pack_start(gtk.Label("  Story Editor"))
    scender.add(scenbox)
    scender.set_tooltip_text("The Famous Blender-Organizer Story Editor")
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
    charder.set_tooltip_text("Do The People. The Characters. \nThe Humans. The Aliens.\n The Monsters")
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
    vehider.set_tooltip_text("People Should Have Cars. \nIK It's a little bit Hibdy Bi.\nBut I love cars so much, they have to have their own tab")
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
    locider.set_tooltip_text("The Places. The Settings.\nThe Backgrounds. The Cities.\nThe Houses. YOU KNOW.")
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
    objibox.pack_start(gtk.Label("  Other Items"))
    objider.add(objibox)
    objider.set_tooltip_text("All The Other Junk")
    objider.connect("clicked",chgCUR, "obj")
    mainbuttonsbox.pack_start(objider, False)
    
    
    
    
    toppannelbox.pack_start(mainbuttonsbox, False)
    
    mainbuttonsbox.show_all()
    
drawmainbuttons()
def secondarybuttonsOMGWTF():
    toppannelbox.pack_start(gtk.VSeparator(), False)

    # Analytics

    startsider = gtk.Button()
    startsider.props.relief = gtk.RELIEF_NONE
    startsibox = gtk.HBox(False)
    startsiico = gtk.Image()
    startsiico.set_from_file("py_data/icons/stats.png")
    startsibox.pack_start(startsiico, False)
    startsibox.pack_start(gtk.Label("  Analytics"))
    startsider.add(startsibox)
    startsider.set_tooltip_text("Schedules, Analitycs.\nAre you doing by deadline? Ah...?")
    startsider.connect("clicked",chgCUR, "stats")
    toppannelbox.pack_start(startsider, False)
    
    
    
    
    

    # checklist

    checklistider = gtk.Button()
    checklistider.props.relief = gtk.RELIEF_NONE
    checklistibox = gtk.HBox(False)
    checklistiico = gtk.Image()
    checklistiico.set_from_file("py_data/icons/checklist.png")
    checklistibox.pack_start(checklistiico, False)
    checklistibox.pack_start(gtk.Label("  Main Checklist"))
    checklistider.add(checklistibox)
    checklistider.set_tooltip_text("Open Main Checklist")
    checklistider.connect("clicked", checklist.checkwindow, os.getcwd(), "Main Checklist", "project.progress")
    toppannelbox.pack_start(checklistider, False)
    
    
    toppannelbox.pack_start(gtk.VSeparator(), False)
    
    
    
    # Settings AKA blender version ( I'm not going to change names of the buttons and shit)

    blendverb = gtk.Button()
    blendverb.props.relief = gtk.RELIEF_NONE
    blendbox = gtk.HBox(False)
    blendico = gtk.Image()
    blendico.set_from_file("py_data/icons/settings.png")
    blendbox.pack_start(blendico, False)
    blendbox.pack_start(gtk.Label("  Settings"))
    blendverb.add(blendbox)
    blendverb.set_tooltip_text("Blender Versions, And other settings")
    blendverb.connect("clicked",chgCUR, "bldv")
    #blendver.set_sensitive(False)
    toppannelbox.pack_end(blendverb, False)
    
    toppannelbox.pack_end(gtk.VSeparator(), False)
    
    # TELEGRAM
    
    def telegram(w):
        oscalls.Open("https://t.me/blenderorganizer")
        
    
    syncider = gtk.Button()
    syncider.props.relief = gtk.RELIEF_NONE
    syncibox = gtk.HBox(False)
    synciico = gtk.Image()
    synciico.set_from_file("py_data/icons/telegram.png")
    syncibox.pack_start(synciico, False)
    syncibox.pack_start(gtk.Label("  Community Help!"))
    syncider.add(syncibox)
    syncider.set_tooltip_text("Get Help, Request Features, Chat With Developers")
    syncider.connect("clicked",telegram)
    #syncider.set_sensitive(False)
    toppannelbox.pack_end(syncider, False)

    ctut = "Analytics"
    if CUR in ["chr", "veh", "loc", "obj"]:
        ctut = "Items"
    elif CUR == "rnd":
        ctut = "Story Editor"
    
    def tutorials(w):
        
        if CUR in ["chr", "veh", "loc", "obj"]: 
            oscalls.Open("https://youtu.be/wiejIqHS0Vg")
        elif CUR == "rnd":
            oscalls.Open("https://youtu.be/086qRkHCa6c")
        else:
            oscalls.Open("https://youtu.be/ohTgpc-FuXE") # PUT
        
    
    syncider = gtk.Button()
    syncider.props.relief = gtk.RELIEF_NONE
    syncibox = gtk.HBox(False)
    synciico = gtk.Image()
    synciico.set_from_file("py_data/icons/info.png")
    syncibox.pack_start(synciico, False)
    syncibox.pack_start(gtk.Label(ctut+" Help!"))
    syncider.add(syncibox)
    syncider.set_tooltip_text("Watch a tutorial on YouTube\nabout Blender-Organizer's "+ctut)
    syncider.connect("clicked",tutorials)
    #syncider.set_sensitive(False)
    toppannelbox.pack_end(syncider, False)
    
    toppannelbox.pack_end(gtk.VSeparator(), False)

    # SYNC

    #syncider = gtk.Button()
    #syncider.props.relief = gtk.RELIEF_NONE
    #syncibox = gtk.HBox(False)
    #synciico = gtk.Image()
    #synciico.set_from_file("py_data/icons/sync.png")
    #syncibox.pack_start(synciico, False)
    #syncibox.pack_start(gtk.Label("  Synchronize"))
    #syncider.add(syncibox)
    #syncider.set_tooltip_text("Synchronize between multiple machines")
    #syncider.connect("clicked",chgCUR, "sync")
    #syncider.set_sensitive(False)
    #toppannelbox.pack_end(syncider, False)


    # REPORT BUG
    def Reportbug(w=False):
        
        oscalls.Open("https://github.com/JYamihud/blender-organizer/issues")
    Reportbugider = gtk.Button()
    Reportbugider.props.relief = gtk.RELIEF_NONE
    Reportbugibox = gtk.HBox(False)
    Reportbugiico = gtk.Image()
    Reportbugiico.set_from_file("py_data/icons/report_bug.png")
    Reportbugibox.pack_start(Reportbugiico, False)
    Reportbugibox.pack_start(gtk.Label("  Report BUG!"))
    Reportbugider.add(Reportbugibox)
    Reportbugider.set_tooltip_text("Go to report bug page.")
    #Reportbugider.set_sensitive(False)
    Reportbugider.connect("clicked", Reportbug)


    toppannelbox.pack_end(Reportbugider, False)

    # Update



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
    
    toppannelbox.pack_end(gtk.VSeparator(), False)    
    
    


secondarybuttonsOMGWTF()
#### DRAWING

drawbox = gtk.VBox(False)

def drawmain(w=None):
    
    
    
    
    #global drawbox
    #drawbox.destroy()
    global mainbox
    mainbox.destroy()
    mainbox = gtk.VBox(False)
    mainwin.add(mainbox)
    buttons1()
    drawmainbuttons()
    secondarybuttonsOMGWTF()
    
    drawbox = gtk.VBox(False)
    mainbox.pack_start(drawbox, True)
    
    if CUR in ["chr","obj","loc","veh"]:
        assets.draw_assets(os.getcwd(), drawbox, mainwin, CUR,)
        
    
    if CUR == "stats":
        analytics.draw_analytics(os.getcwd(), drawbox, mainwin, mainbox)

    mainbox.show_all()
    
    
    if CUR == "rnd":    
    
        story_editor.story(os.getcwd(), drawbox, mainwin, mainbox)
        
    if CUR == "bldv":
        
        blendver.draw_blendver(os.getcwd(), drawbox, mainwin)
drawmain()




# show the window
mainwin.show_all()


#run GTK
gtk.main()


history.write(os.getcwd(), "/", "[Project Exited]")
print "\033[1;m"
