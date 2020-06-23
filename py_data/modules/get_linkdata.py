import bpy


from bpy import data as D
from bpy import context as C
from mathutils import *
from math import *
print("LOADING THE DATA... WAIT FOR IT")
try:
    for i in bpy.data.collections: #getting all the collections
        for b in i.all_objects: #getting all the obejects in the collection
            print( ">>>", i.name, "<==" ,b.name) #output to the pipe Collection <== Suzanne
            #                                                  Collection <== Camera
    print ("VERSION = SUCCESS")
except:
    pass
