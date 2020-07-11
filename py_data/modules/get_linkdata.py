import bpy


from bpy import data as D
from bpy import context as C
from mathutils import *
from math import *
print("LOADING THE DATA... WAIT FOR IT")
try:
    for n, i in enumerate(bpy.data.collections): #getting all the collections
        print(i, "Collection")
        foundobj = False
        for nn, b in enumerate(i.objects): #getting all the obejects in the collection
            foundobj = True
            print( ">>>", i.name, "<==" ,b.name) #output to the pipe Collection <== Suzanne
            #                                                  Collection <== Camera
            
            if nn > 100:
                print("BROKEN AFTER", b.name)
                break
        
        if not foundobj:
            print( ">>>", i.name)
            
        #if n > 300:
        #    break
    
    print ("VERSION = SUCCESS")
except:
    print("ERROR")
