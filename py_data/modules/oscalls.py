# -*- coding: utf-8 -*-

# THIS FILE HANDLES THINGS TO MAKE
# BLENDER-ORGANIZER WORK ON MORE THEN JUST LINUX
# IK IT'S NOT THE HAPPIEST FEATURE
# BUT WHAT CAN YA DO...

import os
import platform

ostype = platform.system()

def Open(arg):  # XDG-OPEN (start the file in a default software)
    
    # For The Best OS Ever
    if ostype == "Linux":                     #####       ##        ##    ##        ##
        os.system("xdg-open "+arg)          ##      ##    ####      ##    ##        ##
    # For Stinky                           ##             ##  ##    ##    ##        ##
    elif ostype == "Windows":             ##    ####      ##    ##  ##    ##        ##
        os.system("start "+arg)            ##   #  ##     ##     ## ##     ##      ##
    # For Not that Stinky                   ##      ##    ##      ####      ##    ##
    elif ostype == "Darwin":                  #####       ##        ##        ####
        os.system("open "+arg)
        
        
