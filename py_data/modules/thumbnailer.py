try: 
    import Image
except:
    from PIL import Image
import os
def thumbnail(im, x=200, y=200, pf=False):
    
    try:
        thrumb = Image.open(im)
    except:
        thrumb = Image.open(os.getcwd()+"/py_data/icons/pic_big.png")
    size = x, y
    thrumb.thumbnail(size, Image.NEAREST)
    if not pf:
        thrumb.save("py_data/tmp.png", "PNG")
        return(os.getcwd()+"/py_data/tmp.png")
    else:
        thrumb.save(pf+"/py_data/tmp.png", "PNG")
        return(pf+"/py_data/tmp.png")
    
def videothumb(im, s=200, y=200):
    IF = os.system("totem-video-thumbnailer -s "+str(s)+" "+im+" "+os.getcwd()+"/py_data/tmp.png")
    
    if IF:
        return(os.getcwd()+"/py_data/icons/empy_video.png")
    
    return(os.getcwd()+"/py_data/tmp.png") 
    
    
def blenderthumb(im, x=200, y=200):
    
    
    cblndr = ""
    
    try:
        bv = open(os.getcwd()+"/py_data/blenderver.data", "r")
        bv = bv.read().split("\n")
        
        print "bv", bv
        
        if int(bv[0]) > 0:
            cblndr = "python3 "+bv[int(bv[0])]+"/"
    except:
        pass
        
    
    

    IF = os.system(cblndr+"blender-thumbnailer.py "+im+" "+os.getcwd()+"/py_data/tmp.png")
    
    thrumb = Image.open(os.getcwd()+"/py_data/tmp.png")
    size = x, y
    thrumb.thumbnail(size, Image.NEAREST)
    thrumb.save("py_data/tmp.png", "PNG")
    
    if IF:
        return(os.getcwd()+"/py_data/icons/blendfile_big.png")
    
    
    return(os.getcwd()+"/py_data/tmp.png") 



