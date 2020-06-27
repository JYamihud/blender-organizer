import bpy


from bpy import data as D
from bpy import context as C
from mathutils import *
from math import *
print("LOADING THE DATA... WAIT FOR IT")
try:
    for n, i in enumerate(bpy.data.collections): #getting all the collections
        for nn, b in enumerate(i.objects): #getting all the obejects in the collection
            print( ">>>", i.name, "<==" ,b.name) #output to the pipe Collection <== Suzanne
            #                                                  Collection <== Camera
            
            if nn > 100:
                break
            
        if n > 100:
            break
    
    print ("VERSION = SUCCESS")
except:
    raise
