# -*- coding: utf-8 -*-

# system
import os
import zipfile

#
import gtk

def export():
    
    chosefolder = gtk.FileChooserDialog("CHOOSE FOLDER CONTAINING BLENDER",
                                     None,
                                     gtk.FILE_CHOOSER_ACTION_SAVE,
                                    (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                     gtk.STOCK_OPEN, gtk.RESPONSE_OK))
    
    
    
    
    response = chosefolder.run()
    if response == gtk.RESPONSE_OK:
        
        get = chosefolder.get_filename()
        
        
    
    
        ########################## EXPORT IT SELF ##############################
        
        
        
        print "LAUNCHING THE ZIPFILE AND EXTRACTING THE REFERENCE ODT"
        
        print os.getcwd()+"/py_data/new_file/empty.odt"
        if os.path.exists(os.getcwd()+"/py_data/new_file/empty.odt"):
            
            try:
                os.system("rm -rf /tmp/odt_export")
            except:
                raise
            os.mkdir("/tmp/odt_export")
            
            print "EXPORTING..."
            
            ref = zipfile.ZipFile(os.getcwd()+"/py_data/new_file/empty.odt", "r")
            ref.extractall("/tmp/odt_export")
            ref.close()
        
            print "EXPORTED!!!"
    
            print "CHANGING THE FILE content.xml"
            
            os.remove("/tmp/odt_export/content.xml")
            
            reffile = open("/tmp/content.xml", "r")
            destfile = open("/tmp/odt_export/content.xml", "w")
            destfile.write(reffile.read())
            destfile.close()
            
            print "CHANGING COMPLITE"
            
            
            # FOLLOWING CODE I GOT FROM INTERNET #
            
            def zip_odt(src, dst):
                zf = zipfile.ZipFile("%s.odt" % (dst), "w", zipfile.ZIP_DEFLATED) #changed file extension
                abs_src = os.path.abspath(src)
                for dirname, subdirs, files in os.walk(src):
                    for filename in files:
                        absname = os.path.abspath(os.path.join(dirname, filename))
                        arcname = absname[len(abs_src) + 1:]
                        print 'zipping %s as %s' % (os.path.join(dirname, filename),
                                                    arcname)
                        zf.write(absname, arcname)
                zf.close()
            
            zip_odt("/tmp/odt_export", get)

            
            print "DONE... FILE HAD BEEN SAVED"
            
            
    
    
    chosefolder.destroy()
