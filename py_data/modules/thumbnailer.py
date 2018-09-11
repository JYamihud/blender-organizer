try: 
    import Image
except:
    from PIL import Image
import os
def thumbnail(im, x=200, y=200, pf=False):
    
    thrumb = Image.open(im)
    size = x, y
    thrumb.thumbnail(size, Image.NEAREST)
    if not pf:
        thrumb.save("py_data/tmp.png", "PNG")
        return(os.getcwd()+"/py_data/tmp.png")
    else:
        thrumb.save(pf+"/py_data/tmp.png", "PNG")
        return(pf+"/py_data/tmp.png")
    
def videothumb(im, s=200, y=200):
    os.system("totem-video-thumbnailer -s "+str(s)+" "+im+" "+os.getcwd()+"/py_data/tmp.png")
    return(os.getcwd()+"/py_data/tmp.png") 
    
    
def blenderthumb(im, x=200, y=200):
    

    os.system("blender-thumbnailer.py "+im+" "+os.getcwd()+"/py_data/tmp.png")
    
    thrumb = Image.open(os.getcwd()+"/py_data/tmp.png")
    size = x, y
    thrumb.thumbnail(size, Image.NEAREST)
    thrumb.save("py_data/tmp.png", "PNG")
    
    
    
    
    return(os.getcwd()+"/py_data/tmp.png") 


