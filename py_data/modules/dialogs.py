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
import fileformats
from subprocess import *
import odt_export

tbox = gtk.VBox()

def rendersettings(pf, blend):

    
    dialog = gtk.Dialog("Render Settings", None, 0, (gtk.STOCK_EXECUTE,  gtk.RESPONSE_APPLY, 
                                               gtk.STOCK_CANCEL, gtk.RESPONSE_CLOSE))
    box = dialog.get_child()
    
    # scroller for the text editor
    textscroll = gtk.ScrolledWindow()
    textscroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
    textscroll.set_size_request(300, 100)
    textscroll.set_shadow_type(gtk.SHADOW_NONE)
    
    # text editor
    textview = gtk.TextView()
    textview.set_editable(False)
    #textcolors
    textview.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#5c5c5c"))
    textview.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FFF"))
    fontdesc = pango.FontDescription("Sawasdee")
    textview.modify_font(fontdesc)
    
    textscroll.add_with_viewport(textview)
    
    
    textbuffer = textview.get_buffer()
    
    textbuffer.set_text("""   Blender-Organizer
    Render requirements:

        ✓ Check your resolution and
    frame rate setting inside the file.

        ✓ If you use Drivers or Scripts
    for animation. Check the
    "Auto Run Python Scripts" in 
    User Preferances >> File
        
        ✓ This renderer will ignore
    a file format and render directory
    set up inside the blend file.
    But all the file outputs with in
    compositor will work as intented.
        
        ✓ It will render only into
    single images output to be able
    to pause rendering in between frames.
    And restore crashed blender.
    
    """)
    
    print "FODLER FILE", pf+"/"+blend
    
    box.pack_start(textscroll, False)
    
    
    
    
    
    
    
    
    
    
    # BLEND FILE ICON
    
    
    
    
    bldfileinfobox = gtk.HBox(False)
    
    
    def openblend(W=False):
        
        
        os.system("xdg-open "+pf+"/"+blend)
    
    
    blendfileicon = gtk.Image()
    blendfileicon.set_from_file(thumbnailer.blenderthumb(pf+"/"+blend, 100,100))
    
    
    openfilebutton = gtk.Button()
    openfilebutton.add(blendfileicon)
    openfilebutton.connect("clicked", openblend)
    
    openfilebutton.set_tooltip_text("Open The Blendfile\n\n(for infile settings)\n\nDon't forget to save!")
    
    bldfileinfobox.pack_start(openfilebutton, False)
    
    
    bldinfo = gtk.VBox(False)
    box.pack_start(bldfileinfobox, False)
    bldfileinfobox.pack_start(bldinfo)
    
    bldinfo.pack_start(gtk.Label(blend), False)
    
    
    
    
    
    
    #####  GETTING STArT END FRAME  #### POPEN ######
    
    
    
    
    
    
    #parsing checkstring
    
    fromsaved = False
    try:
        fromsaved = open(pf+"/"+blend[:blend.rfind("/")+1]+"extra/"+blend[blend.rfind("/")+1:]+".rnd", "r")
        fromsaved = fromsaved.read()
    except:
        
        pass
    
    
    START = 1.0
    END = 250.0
    FORMAT = "JPEG"
    FOLDER = "/"+blend[:blend.rfind("/")+1]+"storyboard"
    
    if fromsaved:
        
        for line in fromsaved.split("\n"): 
            if line.startswith("START = "):
                
                START = float(line[line.find("= ")+1:])
            
            if line.startswith("END = "):
                
                END = float(line[line.find("= ")+1:])
        
            if line.startswith("FORMAT = "):
                
                FORMAT = str(line[line.find("= ")+1:]).strip()
            
            if line.startswith("FOLDER = "):
                
                FOLDER = str(line[line.find("= ")+1:]).strip()
        
    def fromblend(w=False):
        
        
        # SHOWING WATCH CURSOR
        
        w.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        while gtk.events_pending():
            gtk.main_iteration()
        
        
        #### NEXT FEW LINES MAKES SENSE, TRUST ME
        # blender -b test.blend -P bltest.py
        
        cblndr = ""
                                        
        try:
            bv = open(self.pf+"/py_data/blenderver.data", "r")
            bv = bv.read().split("\n")
            
            print "bv", bv
            
            if int(bv[0]) > 0:
                cblndr = bv[int(bv[0])]+"/"
        except:
            pass
        
        
        checkframes = Popen([cblndr+"blender", "-b", pf+"/"+blend , "-P", pf+"/py_data/modules/get_start_end_frame.py"],stdout=PIPE, universal_newlines=True)

        checkframes.wait()
        checkstring = checkframes.stdout.read()
        
        
        for line in checkstring.split("\n"):
            if line.startswith("START = "):
                
                START = float(line[line.find("= ")+1:])
                startframe.set_value(START)
            if line.startswith("END = "):
                
                END = float(line[line.find("= ")+1:])
                endframe.set_value(END)
            
            
        
        
        # SHOWING BACK THE NORMAL ARROW
        
        w.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.ARROW))
        while gtk.events_pending():
            gtk.main_iteration()
      
    
    bldinfo.pack_start(gtk.HSeparator(), False)
    
    framesbox = gtk.HBox(False)
    bldinfo.pack_start(framesbox, False)
    
    
    
    framesbox.pack_start(gtk.Label("Start "))
    
    
    
    
      
        
    # GETTING VALUE IS AS SIMPLE AS THIS
    # int(widget.get_value())

    
    def framechangesend(w):
        
        if startframe.get_value() > endframe.get_value():
            startframe.set_value(endframe.get_value())
        
    def framechangesstart(w):
        
        if startframe.get_value() > endframe.get_value():
            endframe.set_value(startframe.get_value())   
            
            
        
    
    startadj = gtk.Adjustment(1.0, 0.0, 9999.0, 1.0, 5.0, 0.0)
    startframe = gtk.SpinButton(startadj, 0, 0)
    startframe.set_value(START)
    startframe.set_wrap(True)
    startframe.connect("changed", framechangesstart)
    framesbox.pack_start(startframe, False)
    
    framesbox.pack_start(gtk.Label(" End "))
    
    endadj = gtk.Adjustment(1.0, 0.0, 9999.0, 1.0, 5.0, 0.0)
    endframe = gtk.SpinButton(endadj, 0, 0)
    endframe.set_value(END)
    endframe.set_wrap(True)
    endframe.connect("changed", framechangesend)
    framesbox.pack_start(endframe, False)
    
    
    fromblendbutton = gtk.Button()
    fromblendbutton.props.relief = gtk.RELIEF_NONE
    fromblendbutton.connect("clicked",fromblend)
    fromblendicon = gtk.Image()
    fromblendicon.set_from_file(pf+"/py_data/icons/blender.png")
    fromblendbutton.add(fromblendicon)
    fromblendbutton.set_tooltip_text("Get Start and End frames\nfrom the blend file.")
    framesbox.pack_start(fromblendbutton, False)
    
    
    
    
    
    bldinfo.pack_start(gtk.HSeparator(), False)
    
    
    
    
    
    ### FILE FORMAT ###
    
    formats = ["JPEG", "PNG", "EXR", "HDR"]
    
    formatsbox = gtk.HBox()
    bldinfo.pack_start(formatsbox, False)
    
    
    formats_selector = gtk.combo_box_new_text()
    for n, i in enumerate(formats):
        formats_selector.append_text(i)
     
    for n, i in enumerate(formats):
        if i == FORMAT:
            formats_selector.set_active(n)
    
    
    
    formatsbox.pack_start(gtk.Label("Format "), False)
    formatsbox.pack_start(formats_selector)
    
    bldinfo.pack_start(gtk.HSeparator(), False)
    
    
    
    
    
    
    
    ### DIRECTORY ####
    
    
    
    directories = ["storyboard" , "opengl", "test_rnd", "rendered", "Custom"]
    
    dirbox = gtk.HBox()
    bldinfo.pack_start(dirbox, False)
    
    direntry = gtk.Entry()
    def outputdir(w):
        
        if w.get_active() == 4:
            
            
            getdir.set_sensitive(True)
            getdir.grab_focus()
            
        else:
            
            getdir.set_sensitive(False)
            
            direntry.set_text("/"+blend[:blend.rfind("/")+1]+directories[w.get_active()])
    
    
    
    dirselector = gtk.combo_box_new_text()
    for i in directories:
        dirselector.append_text(i)
    dirselector.connect("changed", outputdir)
    
    
    dirbox.pack_start(gtk.Label("Folder "), False)
    dirbox.pack_start(dirselector)
    
    direntrybox = gtk.HBox(False)
    
    
    direntry = gtk.Entry()
    direntry.set_text(FOLDER)
    direntry.set_has_frame(False)
    direntrybox.pack_start(direntry, True)
    direntry.set_editable(False)
    
    
    #Get Custom dir buton
    
    
    def getthedir(w):
        
        w.set_sensitive(False)
        
        # FILE CHOOSER
        box.set_sensitive(False)
        addbuttondialog = gtk.FileChooserDialog("CHOOSE RENDER OUTPUT",
                                         None,
                                         gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                                        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                         gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        addbuttondialog.set_default_response(gtk.RESPONSE_OK)
        addbuttondialog.set_current_folder(blend[:blend.rfind("/")])
        
        
        
        response = addbuttondialog.run()
        if response == gtk.RESPONSE_OK:
            
            get = addbuttondialog.get_filename()
            
            if pf in get:
                direntry.set_text(get.replace(pf, ""))
            
            
            
        box.set_sensitive(True)    
        
        addbuttondialog.destroy() 
        
        
        
        w.set_sensitive(True)
    
    getdir = gtk.Button()
    getdir.connect("clicked", getthedir)
    getdir.props.relief = gtk.RELIEF_NONE
    getdiricon = gtk.Image()
    getdiricon.set_from_file(pf+"/py_data/icons/folder.png")
    getdir.add(getdiricon)
    direntrybox.pack_end(getdir, False)
    
    if FOLDER[FOLDER.rfind("/")+1:] in directories:
        for n, i in enumerate(directories):
            if i == FOLDER[FOLDER.rfind("/")+1:]:
                dirselector.set_active(n)
                getdir.set_sensitive(False)
    else:
        dirselector.set_active(4)
        getdir.set_sensitive(True)
    
    
    
    box.pack_start(direntrybox, False)
    
    
    ## NEW AUTOMATIC SWITCH SYSTEM FOR GPU/CPU AT RENDERING
    def useCPUGPUFUNC(w=False):
        scalebox.set_sensitive(w.get_active())
        uselist.set_sensitive(not w.get_active())
        uselist.set_active(False)
        
    useCPUGPU = gtk.CheckButton("CPU/GPU Split")
    useCPUGPU.connect("clicked", useCPUGPUFUNC)
    box.pack_start(useCPUGPU, False)
    
    scalebox = gtk.HBox(False)
    box.pack_start(scalebox, False)    
    
    def scalevaluechange(w):
        v = w.get_value()
        scalenum.set_value(v)
        scale.set_value(v)
       
        
        
    scaleadj = gtk.Adjustment(1.0, 0.0, 100.0, 1.0, 5.0, 0.0)
    scalenum = gtk.SpinButton(scaleadj, 0, 0)
    scalenum.set_value(50)
    scalenum.set_wrap(True)
    scalenum.connect("value-changed", scalevaluechange)
    scalebox.pack_start(scalenum, False)
    
    scalebox.pack_start(gtk.Label("% : CPU"), False)
    
    scale = gtk.HScale()
    scale.set_draw_value(False	)
    scale.set_range(0, 100)
    scale.set_increments(1, 10)
    scale.set_digits(0)
    scale.set_value(50)
    scale.set_size_request(160, 35)
    scale.connect("value-changed", scalevaluechange)
    scalebox.pack_start(scale)
    scalebox.set_sensitive(False)
    
    scalebox.pack_end(gtk.Label(" GPU"), False)
    
    
    
    
    clearfolder = gtk.CheckButton("Delete Frames Before Rendering")
    clearfolder.set_tooltip_text("""
If enabled this will delete all
frames in selected range. Before
rendering to ensure they are
re-rendered.

WARNING!!! Carefully while using
custom folder. It might delete
files you need that happened to
have names such as 0001.png,
0002.png, 0003.png etc...

If not enabled. Renderer will
skip all the frames that are already
in the folder.

""")
    box.pack_start(clearfolder, False)
    
    
    box.pack_start(gtk.HSeparator(), False)
    
    
    
    
    
    ##### RENDER LISTS #####
    
    
    def rlist_sensitive(w):
        
        useCPUGPU.set_sensitive(not w.get_active())
        useCPUGPU.set_active(False)
        
        if w.get_active():
            
            rlistscroll.set_sensitive(True)
            newrlist.set_sensitive(True)
        else:
            rlistscroll.set_sensitive(False)
            newrlist.set_sensitive(False)
    
    uselist = gtk.CheckButton("Use Render List")
    uselist.connect("clicked", rlist_sensitive)
    box.pack_start(uselist, False)
    
    
    
    rlistscroll = gtk.ScrolledWindow()
    rlistscroll.set_sensitive(False) 
    rlistscroll.set_size_request(300, 100)
    
    box.pack_start(rlistscroll, True)
    
    
    
    # rlistbox
    
    
    global tbox
    tbox = gtk.VBox()
    
    rlistscroll.add_with_viewport(tbox)
    
    def loadrlist():
        
        
        global tbox
        tbox.destroy()
        
        
         
        tbox = gtk.VBox(False)
        rlistscroll.add_with_viewport(tbox)
        
        
        
        
        
        #getting the list:
        
        globals()["rdbuttons"] = []
        global rdbuttons
        
        for n, i in enumerate(sorted(os.listdir(pf+"/py_data/rnd_seq"))): 
            
            
            
            
            
            thisbutton = []
            
            
            # THE RADIO BUTTON IT SELF
            if n == 0:
                thisbutton.append(gtk.RadioButton(None, i))
            else:
                thisbutton.append(gtk.RadioButton(rdbuttons[0][0], i))
            
            # THE DELETE ICON
            
            
            def deleterlist(w, name):
                
                
                

                os.remove(pf+"/py_data/rnd_seq/"+name)

                loadrlist()
            
            
            
            deleteicon = gtk.Image()
            deleteicon.set_from_file(pf+"/py_data/icons/delete.png")
            deletebutton = gtk.Button()
            deletebutton.props.relief = gtk.RELIEF_NONE
            deletebutton.add(deleteicon)
            deletebutton.connect("clicked", deleterlist, i)
            
            thisbutton.append(deletebutton)
            
            
            
            rdbuttons.append(thisbutton)
            
            bbox = gtk.HBox()
            
            bbox.pack_start(rdbuttons[n][0], False)
            bbox.pack_end(rdbuttons[n][1], False)
            tbox.pack_start(bbox, False)
            tbox.pack_start(gtk.HSeparator(), False)
            
            
            
        
        tbox.show_all()
    
    
    loadrlist()
    
    
    def makerlist(w):
        
        name = newrlistname.get_text()
        
        while name in os.listdir(pf+"/py_data/rnd_seq"):
            
            name = name+"_copy"
        
        nf = open(pf+"/py_data/rnd_seq/"+name, "w")
        nf.close()
        
        
        
        
        
        
        loadrlist()
        
    
    
    newrlist = gtk.HBox(False)
    newrlist.set_sensitive(False)
    
    box.pack_start(newrlist, False)
    
    
    newrlistname = gtk.Entry()
    newrlistname.connect("activate", makerlist)
    newrlistname.set_text("New_List_Name")
    newrlist.pack_start(newrlistname)
    
    
    
    newrlistplus = gtk.Image()
    newrlistplus.set_from_file(pf+"/py_data/icons/plus.png")
    newrlistbutton = gtk.Button()
    newrlistbutton.props.relief = gtk.RELIEF_NONE
    newrlistbutton.add(newrlistplus)
    newrlistbutton.connect("clicked", makerlist)
    
    newrlist.pack_end(newrlistbutton, False)
    
    ### ONLY MAKE THE FILE ###
    
    onlyset = gtk.CheckButton("Only settings (No Render)")
    onlyset.set_tooltip_text("Do not start rendering. Only edit the settings data.")
    box.pack_start(onlyset, False)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    box.show_all()
    r = dialog.run()
    
    if r == gtk.RESPONSE_APPLY:
        
        
        try:
            getold = open(pf+"/"+blend[:blend.rfind("/")+1]+"extra/"+blend[blend.rfind("/")+1:]+".rnd", "r")
            getold = getold.read().split("\n")
        except:
            
            getold = ""
                
        setting = open(pf+"/"+blend[:blend.rfind("/")+1]+"extra/"+blend[blend.rfind("/")+1:]+".rnd", "w")
        
        setting.write("START = "+str(int(startframe.get_value())))
        setting.write("\nEND = "+str(int(endframe.get_value())))
        setting.write("\nFORMAT = "+str(formats[formats_selector.get_active()]))
        setting.write("\nFOLDER = "+str(direntry.get_text())+"\n")
        
        for i in getold[4:]:
            setting.write(i+"\n")
    
    
    
    
    
    
    
        setting.close()
        
        #IF SPLIT CPU / GPU
        
        if useCPUGPU.get_active():
            dialog.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
            while gtk.events_pending():
                gtk.main_iteration()
            
            ref = open(pf+"/"+blend, "r")
            ref = ref.read()
            cpuF = open(pf+"/"+blend[:blend.rfind(".")]+"_CPU.blend", "w")
            gpuF = open(pf+"/"+blend[:blend.rfind(".")]+"_GPU.blend", "w")
            cpuF.write(ref)
            cpuF.close()
            gpuF.write(ref)
            gpuF.close()
            
            cblndr = ""
                                        
            try:
                bv = open(self.pf+"/py_data/blenderver.data", "r")
                bv = bv.read().split("\n")
                
                print "bv", bv
                
                if int(bv[0]) > 0:
                    cblndr = bv[int(bv[0])]+"/"
            except:
                pass
            
            
            
            CPUchange = Popen([cblndr+"blender", "-b", pf+"/"+blend[:blend.rfind(".")]+"_CPU.blend" , "-P", pf+"/py_data/modules/setfilecpu.py"],stdout=PIPE, universal_newlines=True)
            GPUchange = Popen([cblndr+"blender", "-b", pf+"/"+blend[:blend.rfind(".")]+"_GPU.blend" , "-P", pf+"/py_data/modules/setfilegpu.py"],stdout=PIPE, universal_newlines=True)
            CPUchange.wait()
            GPUchange.wait()
            
            
            cpuexists = False
            try:
                cpu_test = open(pf+"/py_data/rnd_seq/CPU_auto_generated", "r")
                if blend[:blend.rfind(".")]+"_CPU.blend" in cpu_test.read().split("\n"):
                    cpuexists = True
            except:
                pass
            if not cpuexists:
                cpu_list = open(pf+"/py_data/rnd_seq/CPU_auto_generated", "ab")
                cpu_list.write(blend[:blend.rfind(".")]+"_CPU.blend\n")
                cpu_list.close()
            gpuexists = False
            try:
                gpu_test = open(pf+"/py_data/rnd_seq/GPU_auto_generated", "r")
                if blend[:blend.rfind(".")]+"_GPU.blend" in gpu_test.read().split("\n"):
                    gpuexists = True
            except:
                pass
            if not gpuexists:
                gpu_list = open(pf+"/py_data/rnd_seq/GPU_auto_generated", "ab")
                gpu_list.write(blend[:blend.rfind(".")]+"_GPU.blend\n")
                gpu_list.close()
                
            
            # FOR CPU
            
            SV = scale.get_value()
            
            between = endframe.get_value() - startframe.get_value()
            
            v = float(SV) / 100
            df = int(between*v + startframe.get_value())
            
            
           
            
            cpufn = blend[:blend.rfind(".")]+"_CPU.blend"
            gpufn = blend[:blend.rfind(".")]+"_GPU.blend"
            
            
            try:
                getold = open(pf+"/"+cpufn[:cpufn.rfind("/")+1]+"extra/"+cpufn[cpufn.rfind("/")+1:]+".rnd", "r")
                getold = getold.read().split("\n")
            except:
                
                getold = ""
                    
            setting = open(pf+"/"+cpufn[:cpufn.rfind("/")+1]+"extra/"+cpufn[cpufn.rfind("/")+1:]+".rnd", "w")
            
            setting.write("START = "+str(int(startframe.get_value())))
            setting.write("\nEND = "+str(df))
            setting.write("\nFORMAT = "+str(formats[formats_selector.get_active()]))
            setting.write("\nFOLDER = "+str(direntry.get_text())+"\n")
            
            for i in getold[4:]:
                setting.write(i+"\n")
        
            setting.close()
            
            #GPU FILE SETTINGS
            
            try:
                getold = open(pf+"/"+gpufn[:gpufn.rfind("/")+1]+"extra/"+gpufn[gpufn.rfind("/")+1:]+".rnd", "r")
                getold = getold.read().split("\n")
            except:
                
                getold = ""
                    
            setting = open(pf+"/"+gpufn[:gpufn.rfind("/")+1]+"extra/"+gpufn[gpufn.rfind("/")+1:]+".rnd", "w")
            
            setting.write("START = "+str(df+1))
            setting.write("\nEND = "+str(int(endframe.get_value())))
            setting.write("\nFORMAT = "+str(formats[formats_selector.get_active()]))
            setting.write("\nFOLDER = "+str(direntry.get_text())+"\n")
            
            for i in getold[4:]:
                setting.write(i+"\n")
        
            setting.close()
            if not onlyset.get_active():
                P = Popen(["python", pf+"/py_data/modules/render.py", pf+"/"+cpufn], universal_newlines=True)
                P = Popen(["python", pf+"/py_data/modules/render.py", pf+"/"+gpufn], universal_newlines=True)
            
        # IF CLEAR RENDERS
        if clearfolder.get_active():
            
            for frame in range(int(startframe.get_value()), int(endframe.get_value())+1 ):
                
                try:
                    os.remove(pf+FOLDER+"/"+quick.getfileoutput(frame, FORMAT))
                    print "FRAME REMOVED : ", quick.getfileoutput(frame, FORMAT)
                except:
                    pass
        
        
        
        
        
        
        
        if not useCPUGPU.get_active():
            ### IF NOT USING RENDER LISTS
            if uselist.get_active():
                
                print"SAVING DETECTED USING A LITS"
                
                for i in rdbuttons:
                    
                    if i[0].get_active():
                        
                        rlistIS = i[0].get_label() #GETTING THE NAME OF THE RLIST FILE
                        
                        
                        addtofile = open(pf+"/py_data/rnd_seq/"+rlistIS, "ab")
                        addtofile.write(blend+"\n")
                        addtofile.close()
                        
                if not onlyset.get_active():
                    P = Popen(["python", pf+"/py_data/modules/render.py", pf+"/py_data/rnd_seq/"+rlistIS], universal_newlines=True)    
            
            else:
                if not onlyset.get_active():
                    P = Popen(["python", pf+"/py_data/modules/render.py", pf+"/"+blend], universal_newlines=True)              
                            
        
        
        
        
        
    dialog.destroy()
    
    



def PickName(NN):
    
    dialog = gtk.Dialog("Pick A Name", None, 0, (gtk.STOCK_OK,  gtk.RESPONSE_APPLY, 
                                               gtk.STOCK_CANCEL, gtk.RESPONSE_CLOSE))
        
        
                                
    box = dialog.get_child()
    
    
    nm = gtk.HBox(False)
    box.pack_start(nm, False)
    
    nm.pack_start(gtk.Label("  Name:  "), False)
    
    ne = gtk.Entry()
    nm.pack_start(ne)
    ne.grab_focus()
    
    ne.set_text(NN)
    
    
    
    
    
    ret = ""
    
    box.show_all()
    r = dialog.run()
    
    if r == gtk.RESPONSE_APPLY:
        ret = ne.get_text()
    dialog.destroy()
    
    return ret


def GetDate(y, m, d):   
    
    dialog = gtk.Dialog("Pick A Date...", None, 0, (gtk.STOCK_OK,  gtk.RESPONSE_APPLY, 
                                               gtk.STOCK_CANCEL, gtk.RESPONSE_CLOSE))
        
    
        
    
    
                                
    box = dialog.get_child()
    
    c = gtk.Calendar()
    box.pack_start(c)
    
    c.select_month(m, y)
    c.select_day(d)
    
    
    ret = (y, m, d)
    
    box.show_all()
    r = dialog.run()
    if r == gtk.RESPONSE_APPLY:
        ret = c.get_date()
    
    
    dialog.destroy()
    
    return ret


def choose_shot_type():
    
    dialog = gtk.Dialog("Type of Shot?", None, 0, (gtk.STOCK_OK,  gtk.RESPONSE_APPLY, 
                                               gtk.STOCK_CANCEL, gtk.RESPONSE_CLOSE))
        
    
        
    
    
                                
    box = dialog.get_child()
    
    types = ["shot", "shot_anim", "shot_vfx"]
    words = ["Normal", "Animated", "Visual FX"]
    
    buttons = []
    
    for i in words: 
        if i == "Normal":
            buttons.append(gtk.RadioButton(None, i))
        else:
            buttons.append(gtk.RadioButton(buttons[0], i))
    
    for i in buttons:   
        
        box.pack_start(i, False)
    
    
    ret = ""
    
    box.show_all()
    r = dialog.run()
    if r == gtk.RESPONSE_APPLY:
        
        for n, i in enumerate(buttons):
                
            if i.get_active():
                print types[n]
                ret = types[n]
                
    
    
    dialog.destroy()
    
    return ret

class AddAsset:
    def __init__(self, pf, CUR):
        
        
        self.pf = pf
        self.CUR = CUR
        
        
        
        # making a dialog instead of the window to make it run while the script
        # is executing
        dialog = gtk.Dialog("Add Asset", None, 0, (gtk.STOCK_ADD,  gtk.RESPONSE_APPLY, 
                                               gtk.STOCK_CANCEL, gtk.RESPONSE_CLOSE))
        
        
                                
        box = dialog.get_child() # getting the box
        
        
        # folderchooser
        
        fc = gtk.HBox(False)
        box.pack_start(fc, False)
        
        #little folder icon
        foldericon = gtk.Image()
        foldericon.set_from_file(self.pf+"/py_data/icons/folder.png")
        fc.pack_start(foldericon, False)
        
        #chooser of the folder
        # 4 options: chr, obj, veh, loc
                
        
        fldr = gtk.combo_box_new_text()
        fldr.append_text("chr")
        fldr.append_text("veh")
        fldr.append_text("obj")
        fldr.append_text("loc")
        
        if self.CUR == "chr":
            fldr.set_active(0)
        elif self.CUR == "veh":
            fldr.set_active(1)
        elif self.CUR == "obj":
            fldr.set_active(2)
        elif self.CUR == "loc":
            fldr.set_active(3)
        
        fc.pack_start(fldr)
        
        
        # namechooser
        
        nm = gtk.HBox(False)
        box.pack_start(nm, False)
        
        nm.pack_start(gtk.Label("  Name:  "), False)
        
        ne = gtk.Entry()
        nm.pack_start(ne)
        ne.grab_focus()
        
        
        
        
        
        
        
        
        box.show_all()
        r = dialog.run()
        
        if r == gtk.RESPONSE_APPLY:
        
            ne.set_text(ne.get_text().replace("/","_").replace(" ", "_").replace('"',"_").replace("(","_").replace(")","_").replace("'","_").replace("[","_").replace("]","_").replace("{","_").replace("}","_")   )
        
            os.mkdir(self.pf+"/dev/"+fldr.get_active_text()+"/"+ne.get_text())
        
        self.name = ne.get_text()
        dialog.destroy()
        
        
    
    def add(self):
        return self.name


class editPreview:
    
    def __init__(self, ifol, box):
        
        
        
        # FILE CHOOSER
        box.set_sensitive(False)
        addbuttondialog = gtk.FileChooserDialog("CHOOSE NEW BANNER IMAGE",
                                         None,
                                         gtk.FILE_CHOOSER_ACTION_OPEN,
                                        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                         gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        addbuttondialog.set_default_response(gtk.RESPONSE_OK)
        addbuttondialog.set_current_folder(ifol)
        
        
        
        response = addbuttondialog.run()
        if response == gtk.RESPONSE_OK:
            
            get = addbuttondialog.get_filename()
            
            
            # OPENING AND COPEING
            
            if get.lower().endswith(".jpg") or get.lower().endswith(".png") and ifol+"/renders/Preview.jpg" not in get:
                source = open(get, "r")
                
                to = open(ifol+"/renders/Preview.jpg", "w")
                to.write(source.read())
                to.close()
            
        box.set_sensitive(True)    
        
        addbuttondialog.destroy()    





def marker(ID, FILE):
    
    dialog = gtk.Dialog("Rename marker", None, 0, (gtk.STOCK_OK,  gtk.RESPONSE_APPLY, 
                                               gtk.STOCK_CANCEL, gtk.RESPONSE_CLOSE))
        
    box = dialog.get_child() # getting the box
    
    namebox = gtk.HBox(False)
    box.pack_start(namebox, False)
    
    nameentry = gtk.Entry()
    nameentry.set_text(FILE.markers[ID][1])
    
    namebox.pack_start(nameentry)
    
    box.show_all()
    r = dialog.run()
    if r == gtk.RESPONSE_APPLY:
        FILE.markers[ID][1] = nameentry.get_text()
        
    
    dialog.destroy()
    
##### A CLASS TO WORK WITH EVENT IN THE STORY_EDITOR
class event:
    
    def __init__(self, name, text, LIST, IND): 
    
        self.name = name
        self.text = text
        self.LIST = LIST
        self.IND  = IND
    
    
    def view_script(self, linkchainpath):
        
        
        
        
        
        dialog = gtk.Dialog("VIEW SCRIPT", None, 0, ("Export to ODT", 250, gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE))
        
        box = dialog.get_child() # getting the box
        
        
        
        
        
        
        
        
        # scroller for the text editor
        textscroll = gtk.ScrolledWindow()
        textscroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        textscroll.set_size_request(500, 500)
        textscroll.set_shadow_type(gtk.SHADOW_NONE)
        
        # text editor
        textview = gtk.TextView()
        textview.set_wrap_mode(gtk.WRAP_WORD)
        textview.set_editable(False)
        #textcolors
        textview.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#c6c6c6"))
        textview.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse("#424242"))
        fontdesc = pango.FontDescription("FreeMono Bold 15")
        textview.modify_font(fontdesc)
        
        textscroll.add_with_viewport(textview)
        
        
        textbuffer = textview.get_buffer()
        
        
        
        
        try:
            
            self.second_tag = textbuffer.create_tag("Second", paragraph_background="#424242")
            self.frase_tag = textbuffer.create_tag("frase_comment",justification=gtk.JUSTIFY_CENTER, left_margin=150, right_margin=150, foreground="#323232")
            self.frasefirst_tag = textbuffer.create_tag("frasefirst_comment",justification=gtk.JUSTIFY_CENTER, font="FreeMono Bold 17", left_margin=150, right_margin=150)
        except:
            pass
        
        
        ## MAKING THE TEXT ##
        
        scnDATA = self.LIST.get_scenes_data()
        
        
        
        
        second = False
        
        for link in linkchainpath[:-1]:
            
            for i in scnDATA[link[1][0]]:
                if i[1] == link[1][1]:
            
                
                    scenetext = i[3]
                    
                    #CLEARING THE SCENETEXT FROM <shot>
                    for H in range(scenetext.count("<shot>")):
                        
                        rmvname = scenetext[scenetext.find("<shot>")+6:]
                        rmvname = rmvname[rmvname.find('"'):rmvname.replace('"', " ", 1).find('"')+1]
                        scenetext = scenetext.replace("<shot>",  "" , 1)
                        scenetext = scenetext.replace(rmvname,   "")
                        scenetext = scenetext.replace("</shot>", "" ,1)
                        
                    
                    
                    
                    # GETTING INTO THE BUFFER
                    
                    textbuffer.insert(textbuffer.get_end_iter(), "\n"+scenetext+"\n")
                    textbuffer.insert_with_tags(textbuffer.get_end_iter(), "\n", self.second_tag)
                    
                    
                    #if second:
                    #    textbuffer.insert_with_tags(textbuffer.get_end_iter(), scenetext, self.second_tag)
                    #    second = False
                    #else:
                    #    textbuffer.insert(textbuffer.get_end_iter(), scenetext)
                    #    second = True
        
        # Mark images
        
        pixbufs = [] #[ ["path", pixbuf] , ...]
        
        text = textbuffer.get_text(textbuffer.get_start_iter(), textbuffer.get_end_iter())+"\nPS - [Done in Blender-Organizer software Written by J.Y.Amihud]"
        export_text = text
        EXFR = [] #FRASE SPECKER NAME LOCATIONS LIST
        EXSP = [] #FRASES THEM SELFS LOCATIONS
        EXIMG = [] #IMAGES
        
        
        
        # FRASES
        
        if " - [" in text and "]" in text:
            
            t = text
            t = t.replace("[image]", "(image)")
            t = t.replace("[/image]", "(/image)")
            
            
            for i in range(text.count(" - [")):
                
                d = t.find(" - [")   
                pt = t[:d]
                textbuffer.apply_tag(self.frasefirst_tag, textbuffer.get_iter_at_offset(pt.rfind("\n")), textbuffer.get_iter_at_offset(d))
                
                #add frase locations to the EXFR
                EXFR.append([pt.rfind("\n"), d, "name"])
                
                
                d2 = t.find("]")+1
                print d, d2, "\n\n"
                
                phrase = t[d+4:d2-1]
                
                t = t.replace(" - [", " - -", 1)
                
                
                t = t.replace("]", "-", 1)
                textbuffer.delete(textbuffer.get_iter_at_offset(d), textbuffer.get_iter_at_offset(d2))
                textbuffer.insert_with_tags(textbuffer.get_iter_at_offset(d), "   \n"+phrase+"\n", self.frase_tag)
                
                #add sceach locations to the EXSP
                EXSP.append([d, d2, "talk"])
                
                #y = '"'
                #t = text
                #d = 0

                #for i in range( text.count(y)/2 ):
                    #d = t.find(y)
                    #d1 = d
                    #d = t.replace(y, ".", 1).find(y)+1
                    #t = t.replace(y, ".", 1)
                    #t = t.replace(y, ".", 1)
                    #d2 = d
                    
                    #textbuffer.apply_tag_by_name("GREEN", textbuffer.get_iter_at_offset(d1), textbuffer.get_iter_at_offset(d2))
            
        
        
        if "[image]" in text and "[/image]" in text:
            
            ttx = text
            
            for i in range(text.count("[image]")):
                
                if "[/image]" in ttx[ttx.find("[image]"):]:
                    
                    path = ttx[ttx.find("[image]")+7:ttx.find("[/image]")]
                    #print path, ttx.find("[image]"), ttx.find("[/image]"),  "####################################### PATH #################################"
                    
                    #add sceach locations to the EXSP
                    EXIMG.append([ttx.find("[image]")-1, ttx.find("[image]")-1, ["image", os.getcwd()+path.replace(os.getcwd(), "")]])


                    
                    notfound = True
                    for p in pixbufs:
                        if path in p:
                            notfound = False
                    
                    
                    
                    if notfound:
                        try:
                            pixbufs.append([path, gtk.gdk.pixbuf_new_from_file(os.getcwd()+path)])
                        except:
                            try:
                                pixbufs.append([path, gtk.gdk.pixbuf_new_from_file(path)])
                            except:
                                pixbufs.append([path, gtk.gdk.pixbuf_new_from_file(os.getcwd()+"/py_data/icons/pic_big.png")])
                    for p in pixbufs:
                        if path in p:
                    
                            textbuffer.insert_pixbuf(textbuffer.get_iter_at_offset(ttx.find("[image]")-1), p[1])
                    
                    ttx = ttx.replace("[image]", " (image)", 1)
                    ttx = ttx.replace("[/image]", "(/image)", 1)
        
         ############# EXPORTING ODT content.xml FILE TO TMP


        #EXFR names
        #EXSP talks
        #EXIMG images
        #export_text

        reference = open("py_data/new_file/odt.reference")
        ref = reference.read().split("[INSERT]")


        MAIN = sorted(EXFR+EXSP+EXIMG)



        OUTPUT = ref[0]
        imagei = 0
        prev = 0
        for i in MAIN:

            s, e, t = i

            if t != "talk":
                text = export_text[prev:s].replace("&", "and")
                text = text.replace("\n", '\n</text:p><text:p text:style-name="Normal">\n')

                OUTPUT = OUTPUT + '\n<text:p text:style-name="Normal">\n'+text+"\n</text:p>\n"

            if t == "name":

                OUTPUT = OUTPUT + '\n<text:p text:style-name="Speacker">\n'+export_text[s:e].upper()+"\n</text:p>\n"

            elif t == "talk":

                frase = export_text[s+4:e-1]
                frase = frase.replace("\n", '\n</text:p><text:p text:style-name="Speach">\n')

                OUTPUT = OUTPUT + '\n<text:p text:style-name="Speach">\n'+frase+"\n</text:p>\n"

            elif t[0] == "image":   

                print i
                imagei = imagei+1

                OUTPUT = OUTPUT + '''<draw:frame draw:style-name="fr1" draw:name="Image'''+str(imagei)+'''" text:anchor-type="as-char" svg:y="0.0972in" svg:width="2.3362in" svg:height="1.4583in" draw:z-index="0">
<draw:image xlink:href="'''

                OUTPUT = OUTPUT + t[1]
                OUTPUT = OUTPUT + '''" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/>
</draw:frame>'''

            prev = e
        OUTPUT = OUTPUT + export_text[e:]

        OUTPUT = OUTPUT + ref[1]


        save = open("/tmp/content.xml", "w")
        save.write(OUTPUT)
        save.close()
        
        box.pack_start(textscroll)
        
        
        
        
        
        box.show_all()
        r = dialog.run()
        if r == 250:
            odt_export.export()
        dialog.destroy()
       
    def edit(self):
        
        dialog = gtk.Dialog("Edit Event", None, 0, (gtk.STOCK_OK,  gtk.RESPONSE_APPLY, 
                                               gtk.STOCK_CANCEL, gtk.RESPONSE_CLOSE))
        
        box = dialog.get_child() # getting the box
        
        namebox = gtk.HBox(False)
        box.pack_start(namebox, False)
        
        namebox.pack_start(gtk.Label(" Event Name: "), False)
        
        nameentry = gtk.Entry()
        nameentry.set_text(self.name)
        
        namebox.pack_start(nameentry)
        
        
        # SMALL TOOLBAR 
        
        toolbox = gtk.HBox(False)
        box.pack_start(toolbox, False)
        
        
        def mark_now(w=False, com="None"): 
            
            s, e = textbuffer.get_selection_bounds()
            
            
            print s, e
            
            scnname = '"'+com+' Name"'
            
            s = s.get_offset()
            
            textbuffer.insert(e, "</"+com+">")
            
            
            si = textbuffer.get_iter_at_offset(s)
            
            textbuffer.insert(si, "<"+com+">"+scnname)
            
            
            si = textbuffer.get_iter_at_offset(s+len(com)+3)
            ei = textbuffer.get_iter_at_offset(s+len(com)+12)
            if com == "scene":  
                ei = textbuffer.get_iter_at_offset(s+len(com)+13)
            
            
            textbuffer.select_range(si, ei)
            
            textview.grab_focus()
            
        
        def insertimage(w=False):
            
            # FILE CHOOSER
            
            addbuttondialog = gtk.FileChooserDialog("CHOOSE INSERTING IMAGE",
                                             None,
                                             gtk.FILE_CHOOSER_ACTION_OPEN,
                                            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                             gtk.STOCK_OPEN, gtk.RESPONSE_OK))
            addbuttondialog.set_default_response(gtk.RESPONSE_OK)
            addbuttondialog.set_current_folder(os.getcwd())
            
            
            
            response = addbuttondialog.run()
            if response == gtk.RESPONSE_OK:
                
                u = addbuttondialog.get_filename()
                
                imageNOT = True
                for i in fileformats.images:
                    print u.lower(), i, u[-3:]
                    if u.lower().endswith(i):
                        imageNOT = False
                        
                        # FOUND THE IMAGE
                        
                        if os.getcwd() in u:
                            u = u.replace(os.getcwd(), "")
                        
                        textbuffer.insert_at_cursor("[image]"+u+"[/image]")
                        
                        si = textbuffer.get_iter_at_offset(textbuffer.get_iter_at_mark(textbuffer.get_insert()).get_offset()-len("<image>"+u+"</image>"))
                        ei = textbuffer.get_iter_at_offset(textbuffer.get_iter_at_mark(textbuffer.get_insert()).get_offset())
                        
                        
                        textbuffer.select_range(si, ei)
            
                        textview.grab_focus()
                
            addbuttondialog.destroy() 
            
        # mark scene
        
        markscenebutton = gtk.Button()
        markscenebutton.props.relief = gtk.RELIEF_NONE
        markscenebox = gtk.HBox(False)
        marksceneicon = gtk.Image()
        marksceneicon.set_from_file("py_data/icons/scene_editor.png")
        markscenebox.pack_start(marksceneicon, False)
        markscenebox.pack_start(gtk.Label("Mark Scene"))
        markscenebutton.add(markscenebox)
        toolbox.pack_start(markscenebutton, False)
        markscenebutton.connect("clicked", mark_now, "scene")
        
        # mark shot
        
        markshotbutton = gtk.Button()
        markshotbutton.props.relief = gtk.RELIEF_NONE
        markshotbox = gtk.HBox(False)
        markshoticon = gtk.Image()
        markshoticon.set_from_file("py_data/icons/render_big.png")
        markshotbox.pack_start(markshoticon, False)
        markshotbox.pack_start(gtk.Label("Mark Shot"))
        markshotbutton.add(markshotbox)
        toolbox.pack_start(markshotbutton, False)
        markshotbutton.connect("clicked", mark_now, "shot")
        
        # new img
        
        insertimagebutton = gtk.Button()
        insertimagebutton.props.relief = gtk.RELIEF_NONE
        insertimagebox = gtk.HBox(False)
        insertimageicon = gtk.Image()
        insertimageicon.set_from_file("py_data/icons/new_img.png")
        insertimagebox.pack_start(insertimageicon, False)
        insertimagebox.pack_start(gtk.Label("Insert Image"))
        insertimagebutton.add(insertimagebox)
        toolbox.pack_start(insertimagebutton, False)
        insertimagebutton.connect("clicked", insertimage)
        
        
        
        
        # scroller for the text editor
        textscroll = gtk.ScrolledWindow()
        textscroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        textscroll.set_size_request(500, 500)
        textscroll.set_shadow_type(gtk.SHADOW_NONE)
        
        # text editor
        textview = gtk.TextView()
        #textcolors
        textview.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#5c5c5c"))
        textview.modify_base(gtk.STATE_SELECTED, gtk.gdk.color_parse("#2c2c2c"))
        textview.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FFF"))
        fontdesc = pango.FontDescription("Monospace")
        textview.modify_font(fontdesc)
        textview.set_wrap_mode(gtk.WRAP_WORD)
        
        def treeview_changed(widget, thatsecondone):
            
            
            # THIS CODE IS PURE MAGIC... DOWN YOU DARE TOUCHING IT
        
            adj = textscroll.get_vadjustment()
            newval = (adj.upper - adj.page_size)
            oldval = self.adj
            value = adj.value + (newval-oldval) 
            adj.set_value(    value  )
            self.adj = newval
            
            
            
        self.adj = 0.0
        textview.connect("size-allocate", treeview_changed)
        textscroll.add_with_viewport(textview)
        
        box.pack_start(textscroll)
        
        
        # TEXT IT SELF
        
        textbuffer = textview.get_buffer()
        textbuffer.connect("changed", markup)
        textbuffer.set_text(self.text)
        
        
        
        
        
        
        
        
        
        
        
        box.show_all()
        r = dialog.run()
        if r == gtk.RESPONSE_APPLY:
            IND = self.IND
            self.LIST.events[IND][3] = nameentry.get_text()
            self.LIST.events[IND][4] = textbuffer.get_text(textbuffer.get_start_iter(), textbuffer.get_end_iter())
        
        
        
        
        
        
        
        dialog.destroy() 
        
        
    def add_scene(self):        
        
        dialog = gtk.Dialog("SELECT YOUR SCENE and PRESS OK", None, 0, (gtk.STOCK_OK,  gtk.RESPONSE_APPLY, 
                                               gtk.STOCK_CANCEL, gtk.RESPONSE_CLOSE))
        
        box = dialog.get_child() # getting the box
        
        # SCENE ID NAME
        
        
        snbox = gtk.HBox(False)
        snicon = gtk.Image()
        snicon.set_from_file("py_data/icons/scn_asset_done.png")
        snbox.pack_start(snicon, False)
        
        snbox.pack_start(gtk.Label(" Scene Title : "), False)
        
        snentry = gtk.Entry()
        
        
        
         
        
        
        snentry.set_text("SCENE")
        snbox.pack_start(snentry)
        
        
        box.pack_start(snbox)
        
        # DESCTRIPTION
        
        des = gtk.Entry()
        des.set_text("INT. SOMEWHERE. SOMEWHEN. IN SOME WHETHER.")
        #box.pack_start(des)
        
        
        
        # scroller for the text editor
        textscroll = gtk.ScrolledWindow()
        textscroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        textscroll.set_size_request(500, 500)
        textscroll.set_shadow_type(gtk.SHADOW_NONE)
        
        # text editor
        textview = gtk.TextView()
        textview.set_editable(False)
        #textcolors
        textview.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#5c5c5c"))
        textview.modify_base(gtk.STATE_SELECTED, gtk.gdk.color_parse("#db3c16"))
        textview.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FFF"))
        fontdesc = pango.FontDescription("Monospace")
        textview.modify_font(fontdesc)
        textview.set_wrap_mode(gtk.WRAP_WORD)
        def treeview_changed(widget, thatsecondone):
            
            adj = textscroll.get_vadjustment()
            adj.set_value( adj.upper - adj.page_size )
        
        
        textview.connect("size-allocate", treeview_changed)
        textscroll.add_with_viewport(textview)
        
        box.pack_start(textscroll)
        
        
        # TEXT IT SELF
        
        textbuffer = textview.get_buffer()
        textbuffer.connect("changed", markup)
        textbuffer.set_text(self.text)
        textbuffer.select_range(textbuffer.get_start_iter(), textbuffer.get_end_iter())
        
        
        
        
        box.show_all()
        r = dialog.run()
        
        if r == gtk.RESPONSE_APPLY:
        
            
            IND = self.IND
            LIST = self.LIST
            
            s, e = textbuffer.get_selection_bounds()
            
            
            checktext = textbuffer.get_text(s,e)
            
            plustos = 0
            if "</scene>" in checktext:
                plustos = checktext.find("</scene>")+len("</scene>")
            
            
            
            
            
            
            
            s = s.get_offset()+plustos
            
            scnname = snentry.get_text()
            
            #LOOKING FOR THE SCENE NAME
            for i in self.LIST.get_scenes_data():
                
                for b in i:
                    
                    if b[1] == scnname:
                        scnname = scnname+"_ANOTHER"
            
                
            
            scnname = '"'+scnname+'"'#+"\n"+des.get_text()+"\n"
            
            
            textbuffer.insert(e, "\n</scene>\n")
            
            s = textbuffer.get_iter_at_offset(s)
            
            textbuffer.insert(s, "\n<scene>\n"+scnname+"\n")
            
            
            self.LIST.events[IND][4] = textbuffer.get_text(textbuffer.get_start_iter(), textbuffer.get_end_iter())
            
        
        dialog.destroy()
    
    def add_shot(self):        
        
        dialog = gtk.Dialog("SELECT YOUR SHOT and PRESS OK", None, 0, (gtk.STOCK_OK,  gtk.RESPONSE_APPLY, 
                                               gtk.STOCK_CANCEL, gtk.RESPONSE_CLOSE))
        
        box = dialog.get_child() # getting the box
        
        # SCENE ID NAME
        
        
        snbox = gtk.HBox(False)
        snicon = gtk.Image()
        snicon.set_from_file("py_data/icons/scn_asset_done.png")
        snbox.pack_start(snicon, False)
        
        snbox.pack_start(gtk.Label(" Shot Title : "), False)
        
        snentry = gtk.Entry()
        
        
        
         
        
        
        snentry.set_text("SHOT")
        snbox.pack_start(snentry)
        
        
        box.pack_start(snbox)
        
        
        
        
        # scroller for the text editor
        textscroll = gtk.ScrolledWindow()
        textscroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        textscroll.set_size_request(500, 500)
        textscroll.set_shadow_type(gtk.SHADOW_NONE)
        
        # text editor
        textview = gtk.TextView()
        textview.set_editable(False)
        #textcolors
        textview.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#5c5c5c"))
        textview.modify_base(gtk.STATE_SELECTED, gtk.gdk.color_parse("#8888FF"))
        
        
        textview.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FFF"))
        fontdesc = pango.FontDescription("Monospace")
        textview.modify_font(fontdesc)
        textview.set_wrap_mode(gtk.WRAP_WORD)
        def treeview_changed(widget, thatsecondone):
            
            adj = textscroll.get_vadjustment()
            adj.set_value( adj.upper - adj.page_size )
        
        
        textview.connect("size-allocate", treeview_changed)
        textscroll.add_with_viewport(textview)
        
        box.pack_start(textscroll)
        
        
        # TEXT IT SELF
        
        textbuffer = textview.get_buffer()
        textbuffer.connect("changed", markup)
        textbuffer.set_text(self.text)
        textbuffer.select_range(textbuffer.get_start_iter(), textbuffer.get_end_iter())
        
        
        
        
        box.show_all()
        r = dialog.run()
        
        if r == gtk.RESPONSE_APPLY:
        
            
            IND = self.IND
            LIST = self.LIST
            
            s, e = textbuffer.get_selection_bounds()
            
            
            checktext = textbuffer.get_text(s,e)
            
            plustos = 0
            if "</shot>" in checktext:
                plustos = checktext.find("</shot>")+len("</shot>")
            
            
            
            
            
            
            
            s = s.get_offset()+plustos
            
            scnname = snentry.get_text()
            
            
            
                
            
            scnname = '"'+scnname+'"'
            
            
            textbuffer.insert(e, "</shot>")
            
            s = textbuffer.get_iter_at_offset(s)
            
            textbuffer.insert(s, "<shot>"+scnname)
            
            
            self.LIST.events[IND][4] = textbuffer.get_text(textbuffer.get_start_iter(), textbuffer.get_end_iter())
            
        
        dialog.destroy()

def markup(textbuffer):
    
    try:
        textbuffer.create_tag("YELLOW", foreground="#e47649", font="Monospace Bold")
        textbuffer.create_tag("BLUE", foreground="#8888FF", font="Monospace Bold")
        textbuffer.create_tag("GREEN", foreground="#55AA55", font="Monospace Bold")
        textbuffer.create_tag("GREY", foreground="#999", font="Monospace Italic")
        
    except:
        pass
    
    
    textbuffer.remove_all_tags(textbuffer.get_start_iter(), textbuffer.get_end_iter())
    text = textbuffer.get_text(textbuffer.get_start_iter(), textbuffer.get_end_iter())
    
    YELLOW = ["<scene>", "</scene>"]
    BLUE   = ["<shot>", "</shot>"]
    GREY   = ["[image]", "[/image]"]
    
    
    grey = []
    for l in [[YELLOW, "YELLOW"], [BLUE, "BLUE"], [GREY, "GREY"]]:
        for y in l[0]:
        
            if y in text:
                
                t = text
                d = 0
                
                for i in range( text.count(y) ):
                    
                    d = t.find(y)
                    d1 = d
                    d = d+len(y)
                    t = t.replace(y, "."*len(y), 1)
                    d2 = d
                    
                    
                    
                    textbuffer.apply_tag_by_name(l[1], textbuffer.get_iter_at_offset(d1), textbuffer.get_iter_at_offset(d2))
                    
                    try:
                        if l[1] == "GREY":
                            grey.append(d1)
                            print grey, "THE GREY"
                        
                            textbuffer.apply_tag_by_name(l[1], textbuffer.get_iter_at_offset(grey[-2]), textbuffer.get_iter_at_offset(grey[-1]))
                    except:
                        
                        
                        
                        print "FULL TEXT WAS NOT POSSIBLE TO DO"
     
    if '"' in text:
        y = '"'
        t = text
        d = 0
        
        for i in range( text.count(y)/2 ):
            d = t.find(y)
            d1 = d
            d = t.replace(y, ".", 1).find(y)+1
            t = t.replace(y, ".", 1)
            t = t.replace(y, ".", 1)
            d2 = d
            
            textbuffer.apply_tag_by_name("GREEN", textbuffer.get_iter_at_offset(d1), textbuffer.get_iter_at_offset(d2))
            
                        
    
    
    
    
    
    
