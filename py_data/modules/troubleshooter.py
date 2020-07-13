# -*- coding: utf-8 -*-
import os

def shoot(ER):
    
    #cls for clearing the screen
    def cls():
        
        os.system("clear")
    
    cls()
    
    print "\033[1;40m                                                                 "
    print "\033[1;40m               BLENDER-ORGANIZER TROUBLE-SHOOTER                 "
    print "\033[1;40m                                                                 "
    print "\033[1;40m  \033[1;36m      Blender-Organizer is just a python script. And in       \033[1;40m "
    print "\033[1;40m  \033[1;36m      order to run it, particular python modules have to      \033[1;40m "
    print "\033[1;40m  \033[1;36m      be installed. And since you see this message some       \033[1;40m "
    print "\033[1;40m  \033[1;36m      of them are still missing from your system.             \033[1;40m "
    
    print "\033[1;40m  \033[1;36m                                                              \033[1;40m "
    
    v = ""
    
    # ▫☐❓⬜⮿⇨⇩→↓⏵⏷
    
    if ER == 1:
        print "\033[1;m\033[1;40m  ⏷ BASIC MODULES                                                "
        print "\033[1;m\033[1;40m       ⮿ os            \033[1;36m? Folders, files, system things           "
        print "\033[1;m\033[1;40m       ⮿ socket        \033[1;36m? Network things                          "
        print "\033[1;m\033[1;40m       ⮿ urllib2       \033[1;36m? Network things                          "
        print "\033[1;m\033[1;40m       ⮿ datetime      \033[1;36m? Date and time calculations              "
        print "\033[1;m\033[1;40m  ⏵ GTK MODULES                                                  "
        print "\033[1;m\033[1;40m  ⏵ IMAGE MODULES                                                "
        print "\033[1;40m  \033[1;36m                                                              \033[1;40m "
        print "\033[1;40m  \033[1;36m    Those modules usually go with python by default it's      \033[1;40m "
        print "\033[1;40m  \033[1;36m    safe to assume that you have a broken version of python.  \033[1;40m "
        print "\033[1;40m  \033[1;36m                                                              \033[1;40m "
        print "\033[1;40m  \033[1;36m    Try reinstalling python2:      On linux debian systems:   \033[1;40m "
        print "\033[1;m\033[1;40m   sudo apt-get remove python2   \033[1;36m? Un-Installs python2           "
        print "\033[1;m\033[1;40m   sudo apt-get install python2  \033[1;36m? Installs new python2          "
        print "\033[1;40m  \033[1;36m                                                              \033[1;40m "
        
        
    elif ER == 2:
        print "\033[1;m\033[1;40m  ⏵ BASIC MODULES                                                "
        print "\033[1;m\033[1;40m  ⏷ GTK MODULES                                                  "
        print "\033[1;m\033[1;40m       ⮿ gtk           \033[1;36m? Windows, Buttons, UI                    "
        print "\033[1;m\033[1;40m       ⮿ pango         \033[1;36m? Text in the UI                          "
        print "\033[1;m\033[1;40m       ⮿ cairo         \033[1;36m? Custom UI elements                      "
        print "\033[1;m\033[1;40m       ⮿ glib          \033[1;36m? Time offsets for UI elements            "
        print "\033[1;m\033[1;40m  ⏵ IMAGE MODULES                                                "
        print "\033[1;40m  \033[1;36m                                                              \033[1;40m "
        print "\033[1;40m  \033[1;36m    Those modules usually the hardest to get right. They      \033[1;40m "
        print "\033[1;40m  \033[1;36m    are for UI development. And most people don't do it.      \033[1;40m "
        print "\033[1;40m  \033[1;36m                                                              \033[1;40m "
        print "\033[1;40m  \033[1;36m    On Linux there are couple of way you can try:             \033[1;40m "
        print "\033[1;m\033[1;40m   sudo apt-get install python-gtk2-dev   \033[1;36m? Maybe will do it.    "
        print "\033[1;m\033[1;40m   sudo apt-get install build-essential gnome-devel  \033[1;36m? If not.   "
        print "\033[1;40m  \033[1;36m                                                              \033[1;40m "
    
    else:
        print "\033[1;m\033[1;40m  ⏵ BASIC MODULES                                                "
        print "\033[1;m\033[1;40m  ⏵ GTK MODULES                                                  "
        print "\033[1;m\033[1;40m  ⏷ IMAGE MODULES                                                "
        print "\033[1;m\033[1;40m       ⮿ PIL           \033[1;36m? Image manipulation                      "
        print "\033[1;m\033[1;40m       ⮿ Image         \033[1;36m? Same if PIL don't exist.                "
        print "\033[1;40m  \033[1;36m                                                              \033[1;40m "
        print "\033[1;40m  \033[1;36m    Those modules usually installed using python PIP          \033[1;40m "
        print "\033[1;40m  \033[1;36m    only with recent addoption of python3. Python PIP is      \033[1;40m "
        print "\033[1;40m  \033[1;36m    not easy to install for python2.                          \033[1;40m "
        print "\033[1;40m  \033[1;36m                                                              \033[1;40m "
        print "\033[1;40m  \033[1;36m    First let's see if PIP is installed:                      \033[1;40m "
        print "\033[1;m\033[1;40m   pip install pillow   \033[1;36m? Installs the Image modules.            "
        print "\033[1;40m  \033[1;36m   If PIP is not installed you can try installing it normally:\033[1;40m "
        print "\033[1;m\033[1;40m   sudo apt-get install python-pip \033[1;36m? Will work on some systems   "
        print "\033[1;40m  \033[1;36m   For newer systems there is solution from bootstrap.pypa.io:\033[1;40m "
        print "\033[1;m\033[1;40m   curl https://bootstrap.pypa.io/get-pip.py --output get-pip.py "
        print "\033[1;m\033[1;40m   sudo python2 get-pip.py             \033[1;36m? Get & Run their script  "
    
    print "\033[1;40m                                                                 \033[1;m"
    
    exit()