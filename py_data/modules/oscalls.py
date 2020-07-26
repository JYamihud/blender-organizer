# -*- coding: utf-8 -*-

# THIS FILE HANDLES THINGS TO MAKE
# BLENDER-ORGANIZER WORK ON MORE THEN JUST LINUX
# IK IT'S NOT THE HAPPIEST FEATURE
# BUT WHAT CAN YA DO...

import os
import platform

ostype = platform.system()

def Open(arg):
    
    # For Linux
    if ostype == "Linux":
        os.system("xdg-open "+arg)
    else:
        os.system("start "+arg)
