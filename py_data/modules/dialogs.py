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
