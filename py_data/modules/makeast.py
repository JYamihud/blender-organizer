import bpy
import os
print("\n\n\n\n\n\n======= NOW THIS IS THE AST MAKER ======")


#preparing the data for the linking
blendpath =  bpy.data.filepath
folder = blendpath[:blendpath.rfind("/")]
pf = folder[:folder.rfind("/dev/")]
cur = folder[folder.rfind("/")-3:][:3]
blendfilename = folder[folder.rfind("/")+1:]+".blend"
destination = pf+"/ast/"+cur+"/"+blendfilename


#gettin the data into the console for testing
print("BLENDPATH : ", blendpath)
print("FOLDER : ", folder)
print("PROJECT FOLDER : ", pf)
print("CUR : ", cur)
print("BLENDNAME : ", blendfilename)
print("DESTINATION : ", destination)



bpy.ops.wm.save_as_mainfile(filepath=destination)













print("======= THE END OF AST MAKER ======\n\n\n\n\n\n")

