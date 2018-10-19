import bpy


from bpy import data as D
from bpy import context as C
from mathutils import *
from math import *

bpy.context.scene.cycles.device = 'CPU'
bpy.ops.wm.save_mainfile()

