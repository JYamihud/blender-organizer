# -*- coding: utf-8 -*-
import os
import random
def shoot(ER):
    
    #cls for clearing the screen
    def cls():
        
        os.system("clear")
    
    page = "Intoduction"
    options = ["telegram", "details", "ideas", "fix", "exit", "ignore"]
    cls()
    
    rndchar = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890"
    fixpass = ""
    for l in range(20):
        fixpass = fixpass + random.choice(rndchar)
        
    options.append(fixpass)
                                                                     
    
    while True:
        
        print "\033[1;40m                                                                 "
        print "\033[1;40m               BLENDER-ORGANIZER TROUBLE-SHOOTER                 "
        print "\033[1;40m                                                                 "
            
        
        if page not in options:
        
            
            print "\033[1;40m  \033[1;36m   Blender-Organizer is a small program developed             \033[1;40m "
            print "\033[1;40m  \033[1;36m   mostly by one dude for free. If you see this message       \033[1;40m "
            print "\033[1;40m  \033[1;36m   probably Blender-Organizer had found an error or a         \033[1;40m "
            print "\033[1;40m  \033[1;36m   missing module. This page will help you to resolve it.     \033[1;40m "
            print "\033[1;40m  \033[1;36m                                                              \033[1;40m "
            
            print "\033[1;m\033[1;40m              OPTIONS (TYPE OPTION AND PRESS ENTER)              "
            print "\033[1;m\033[1;40m    telegram\033[1;36m   Opens Telegram group.                             "
            print "\033[1;m\033[1;40m    details \033[1;36m   Prints out the problem found.                     "
            print "\033[1;m\033[1;40m    ideas   \033[1;36m   Prints out possible solutions.                    "
            print "\033[1;m\033[1;40m    fix     \033[1;36m   Try to fix everything automatically.              "
            print "\033[1;m\033[1;40m    ignore  \033[1;36m   Ignore the error and try running anyway.          "
            
            print "\033[1;m\033[1;40m    exit    \033[1;36m   Exit Blender-Organizer Trouble-Shooter.           "
            print "\033[1;40m  \033[1;36m If the OPTION is misspelled it will return you back to here. \033[1;40m "
            print "\033[1;40m  \033[1;36m                                                              \033[1;40m "
            print "\033[1;40m  \033[1;36m Just Press ENTER to go to details.                           \033[1;40m "
        
        elif page == "exit":
            
            print "\033[1;40m  \033[1;36m                           BYE BYE                            \033[1;40m "
            print "\033[1;40m                                                                 \033[1;m"
            exit()
        
        elif page == "ignore":
            
            print "\033[1;40m  \033[1;36m                           IGNORING                           \033[1;40m "
            print "\033[1;40m                                                                 \033[1;m"
            break      
            
        elif page == "telegram":
                
            print "\033[1;40m  \033[1;36m   On our Telegram group you can talk to the developers       \033[1;40m "
            print "\033[1;40m  \033[1;36m   and users in order to fix issues. Here is the link.        \033[1;40m "
            print "\033[1;40m  \033[1;36m                                                              \033[1;40m "
            print "\033[1;m\033[1;40m                https://t.me/blenderorganizer                   \033[1;40m "
            print "\033[1;40m  \033[1;36m                                                              \033[1;40m "
            print "\033[1;40m  \033[1;36m Just Press ENTER to exit.                                    \033[1;40m "
        
        elif page == "details":
            
            if ER == 0:  #WINDOWS
            
                print "\033[1;m\033[1;40m                  ERROR code [0] WINDOWS                        \033[1;40m "
                print "\033[1;40m  \033[1;36m   Blender-Organizer is sensing presents of evil.             \033[1;40m "
                print "\033[1;40m  \033[1;36m   It seems like you are running it on Microsoft Windows.     \033[1;40m "
                print "\033[1;40m  \033[1;36m                                                              \033[1;40m "
                print "\033[1;m\033[1;40m                  blender-organizer.py line 78                  \033[1;40m "
                
                print "\033[1;40m  \033[1;36m  platform\033[1;m\033[1;40m Microsoft Windows.                                 \033[1;40m "
                
                print "\033[1;40m                                                                 \033[1;m"       
                print "\033[1;40m  \033[1;36m Just Press ENTER to go to ideas.                             \033[1;40m "
            
            elif ER == 1:  #BAISC MODULES
                
                print "\033[1;m\033[1;40m                  ERROR code [1] BASIC MODULES                  \033[1;40m "
                print "\033[1;40m  \033[1;36m   Seems like your python installation is not full, or        \033[1;40m "
                print "\033[1;40m  \033[1;36m   corrupted. Because some basic modules are missing from it. \033[1;40m "
                print "\033[1;40m  \033[1;36m                                                              \033[1;40m "
                print "\033[1;m\033[1;40m                  blender-organizer.py line 32                  \033[1;40m "
                
                print "\033[1;40m  \033[1;36m   import \033[1;m\033[1;40mos                                                  \033[1;40m "
                print "\033[1;40m  \033[1;36m   import \033[1;m\033[1;40msocket                                              \033[1;40m "
                print "\033[1;40m  \033[1;36m   import \033[1;m\033[1;40mdatetime                                            \033[1;40m "
                print "\033[1;40m  \033[1;36m   import \033[1;m\033[1;40murllib2                                             \033[1;40m "
                print "\033[1;40m  \033[1;36m   import \033[1;m\033[1;40msubprocess                                          \033[1;40m "
                print "\033[1;40m  \033[1;36m   import \033[1;m\033[1;40mplatform                                            \033[1;40m "
                print "\033[1;40m                                                                 \033[1;m"   
                print "\033[1;40m  \033[1;36mOne of these modules is failed to import. Therefor the error. \033[1;40m "      
                print "\033[1;40m                                                                 \033[1;m"       
                print "\033[1;40m  \033[1;36m Just Press ENTER to go to ideas.                             \033[1;40m "
            
            elif ER == 2: #GTK MODULES
                
                print "\033[1;m\033[1;40m                  ERROR code [2] GTK MODULES                    \033[1;40m "
                print "\033[1;40m  \033[1;36m   Seems like you are missing GTK modules for python2.        \033[1;40m "
                print "\033[1;40m  \033[1;36m   This modules make drawing of UI possible.                  \033[1;40m "
                print "\033[1;40m  \033[1;36m                                                              \033[1;40m "
                print "\033[1;m\033[1;40m                  blender-organizer.py line 50                  \033[1;40m "
                
                print "\033[1;40m  \033[1;36m   import \033[1;m\033[1;40mgtk                                                 \033[1;40m "
                print "\033[1;40m  \033[1;36m   import \033[1;m\033[1;40mpango                                               \033[1;40m "
                print "\033[1;40m  \033[1;36m   import \033[1;m\033[1;40mcairo                                               \033[1;40m "
                print "\033[1;40m  \033[1;36m   import \033[1;m\033[1;40mglib                                                \033[1;40m "
                print "\033[1;40m                                                                 \033[1;m"   
                print "\033[1;40m  \033[1;36mOne of these modules is failed to import. Therefor the error. \033[1;40m "      
                print "\033[1;40m                                                                 \033[1;m"       
                print "\033[1;40m  \033[1;36m Just Press ENTER to go to ideas.                             \033[1;40m "
            
            elif ER == 3: #IMAGE MODULES
                
                print "\033[1;m\033[1;40m                  ERROR code [3] IMAGE MODULES                  \033[1;40m "
                print "\033[1;40m  \033[1;36m   Seems like you are missing IMAGE manipulation modules.     \033[1;40m "
                print "\033[1;40m  \033[1;36m   These modules make thumbnails and othe image manipulations.\033[1;40m "
                print "\033[1;40m  \033[1;36m                                                              \033[1;40m "
                print "\033[1;m\033[1;40m                  blender-organizer.py line 66                  \033[1;40m "
                
                print "\033[1;40m  \033[1;36m   import \033[1;m\033[1;40mImage                                               \033[1;40m "
                print "\033[1;40m  \033[1;36m   import \033[1;m\033[1;40mPIL             (\033[1;40m\033[1;35mfrom \033[1;m\033[1;40mPIL \033[1;40m\033[1;36mimport \033[1;m\033[1;40mImage)             \033[1;40m "
                
                print "\033[1;40m                                                                 \033[1;m"   
                print "\033[1;40m  \033[1;36mBoth of these modules failed to import. Therefor the error.   \033[1;40m " 
                print "\033[1;40m  \033[1;36mOnly one should import to work. They are identical.           \033[1;40m "      
                print "\033[1;40m                                                                 \033[1;m"       
                print "\033[1;40m  \033[1;36m Just Press ENTER to go to ideas.                             \033[1;40m "
            
            elif ER == 4: #DATETIME LANGUAGE
                
                print "\033[1;m\033[1;40m                  ERROR code [4] DATETIME LANGUAGE BUG          \033[1;40m "
                print "\033[1;40m  \033[1;36m   There is a bug in the Date calculation module datetime.    \033[1;40m "
                print "\033[1;40m  \033[1;36m   It outputs a mistake when the system language is set to    \033[1;40m "
                print "\033[1;40m  \033[1;36m   something strange.                                         \033[1;40m "
                print "\033[1;40m  \033[1;36m                                                              \033[1;40m "
                print "\033[1;m\033[1;40m                  /py_data/modules/analytic.py line 197         \033[1;40m "
                print "\033[1;40m  \033[1;36m Just Press ENTER to go to ideas.                             \033[1;40m "
            
        elif page == "ideas":
            
            if ER == 0:  #WINDOWS
                print "\033[1;40m  \033[1;36m   There are a few things you can try to combat this issue.   \033[1;40m "
                print "\033[1;40m  \033[1;36m                                                              \033[1;40m "
                print "\033[1;m\033[1;40m        1     Delete WINDOWS and install LINUX.(Recommended)    \033[1;40m "
                print "\033[1;40m  \033[1;36m   Windows operating system is closed source and doesn't      \033[1;40m "
                print "\033[1;40m  \033[1;36m   support any freedom. Also Blender-Organizer was not        \033[1;40m "
                print "\033[1;40m  \033[1;36m   designed to work on Windows even if you can run it. So     \033[1;40m "
                print "\033[1;40m  \033[1;36m   the best solution will be to wipe the computer from it     \033[1;40m "
                print "\033[1;40m  \033[1;36m   and install a Linux distro of your choise. Linux mint?     \033[1;40m "
                print "\033[1;m\033[1;40m                    https://linuxmint.com/                      \033[1;40m "
                print "\033[1;40m  \033[1;36m                                                              \033[1;40m "
                print "\033[1;m\033[1;40m        2     Ignore and continue (Not Recommended)             \033[1;40m "
                print "\033[1;40m  \033[1;36m   Even tho Windows does not respect your 4 essential freedoms\033[1;40m "
                print "\033[1;40m  \033[1;36m   we do. As a FOSS (Free And Open Source) project we have to \033[1;40m "
                print "\033[1;40m  \033[1;36m   respect user freedoms to run, study, modify and destribute \033[1;40m "
                print "\033[1;40m  \033[1;36m   software. So type ignore and press enter.                  \033[1;40m "
                print "\033[1;m\033[1;40m                      http://www.gnu.org/                       \033[1;40m "
                print "\033[1;40m  \033[1;36m                                                              \033[1;40m "
                print "\033[1;40m  \033[1;36m Just Press ENTER to go to fix.                               \033[1;40m "
            
            elif ER == 1:  #BAISC MODULES
                print "\033[1;40m  \033[1;36m   There are a few things you can try to combat this issue.   \033[1;40m "
                print "\033[1;40m  \033[1;36m                                                              \033[1;40m "
                print "\033[1;m\033[1;40m        1     Check for the correct python version              \033[1;40m "
                print "\033[1;40m  \033[1;36m   Most new systems have Python3 as the default python.       \033[1;40m "
                print "\033[1;40m  \033[1;36m   The only problem is that Blender-Organizer is written on   \033[1;40m "
                print "\033[1;40m  \033[1;36m   Python2. And while some code will work in both. It's not   \033[1;40m "
                print "\033[1;40m  \033[1;36m   nearly all of the code. Try typing instead of python       \033[1;40m "
                print "\033[1;m\033[1;40m                python2 blender-organizer.py                    \033[1;40m "
                print "\033[1;40m  \033[1;36m                                                              \033[1;40m "
                print "\033[1;m\033[1;40m        2     Fixing bad python installation.                   \033[1;40m "
                print "\033[1;40m  \033[1;36m   If you are running in in python2 already. And the issue    \033[1;40m "
                print "\033[1;40m  \033[1;36m   persists, try reinstall the python by deleting it and      \033[1;40m "
                print "\033[1;40m  \033[1;36m   installing it again.                                       \033[1;40m "
                print "\033[1;40m  \033[1;36m                APT-GET EXAMPLE COMMANDS:                     \033[1;40m "
                print "\033[1;m\033[1;40m                sudo apt-get remove python2                     \033[1;40m "
                print "\033[1;m\033[1;40m                sudo apt-get install python2                    \033[1;40m "
                print "\033[1;40m  \033[1;36m Just Press ENTER to go to fix.                               \033[1;40m "
        
            elif ER == 2:  #GTK
                print "\033[1;40m  \033[1;36m   There are a few things you can try to install GTK modules. \033[1;40m "
                print "\033[1;40m  \033[1;36m                                                              \033[1;40m "
                print "\033[1;m\033[1;40m        1  By trying to install gnome development tools.        \033[1;40m "
                print "\033[1;40m  \033[1;36m                 APT-GET EXAMPLE COMMAND:                     \033[1;40m "
                print "\033[1;m\033[1;40m        sudo apt-get install build-essential gnome-devel        \033[1;40m "
                
                
                print "\033[1;40m  \033[1;36m                                                              \033[1;40m "
                print "\033[1;m\033[1;40m        2  By Adding repository and installing GTK directly.    \033[1;40m "
                print "\033[1;40m  \033[1;36m                APT-GET EXAMPLE COMMANDS:                     \033[1;40m "
                print "\033[1;m\033[1;40m         sudo add-apt-repository ppa:nrbrtx/python2-stuff       \033[1;40m "
                print "\033[1;m\033[1;40m                      sudo apt-get update                       \033[1;40m "
                print "\033[1;m\033[1;40m              sudo apt-get install python-gtk2                  \033[1;40m "
                print "\033[1;40m  \033[1;36m Just Press ENTER to go to fix.                               \033[1;40m "
            
            elif ER == 3:  #PIL
                print "\033[1;40m  \033[1;36m   There is a process for installing PIL modules.             \033[1;40m "
                print "\033[1;40m  \033[1;36m                                                              \033[1;40m "
                print "\033[1;m\033[1;40m        1  You need to have python PIP installed.               \033[1;40m "
                print "\033[1;40m  \033[1;36m   If you don't have it you need to install it either by      \033[1;40m "
                print "\033[1;40m  \033[1;36m                 APT-GET EXAMPLE COMMAND:                     \033[1;40m "
                print "\033[1;m\033[1;40m                 sudo apt-get install python-pip                \033[1;40m "
                print "\033[1;40m  \033[1;36m   And if your systen is new and python-pip is hard to        \033[1;40m "
                print "\033[1;40m  \033[1;36m   install officially. There is another way I found.          \033[1;40m "
                print "\033[1;40m  \033[1;36m                     EXAMPLE COMMANDS:                        \033[1;40m "
                print "\033[1;m\033[1;40m  curl https://bootstrap.pypa.io/get-pip.py --output get-pip.py \033[1;40m "
                print "\033[1;m\033[1;40m                  sudo python2 get-pip.py                       \033[1;40m "
                
                print "\033[1;40m  \033[1;36m                                                              \033[1;40m "
                print "\033[1;m\033[1;40m        2  Install PIL using python PIP.                        \033[1;40m "
                print "\033[1;40m  \033[1;36m                     EXAMPLE COMMAND:                         \033[1;40m "
                print "\033[1;m\033[1;40m                      pip install pillow                        \033[1;40m "
                
                print "\033[1;40m  \033[1;36m Just Press ENTER to go to fix.                               \033[1;40m "
            
            elif ER == 4:  #LANGUAGE
                print "\033[1;40m  \033[1;36m   At the moment there only one way to fix this issue.        \033[1;40m "
                print "\033[1;40m  \033[1;36m                                                              \033[1;40m "
                print "\033[1;m\033[1;40m        To change system language to English.                   \033[1;40m "
                print "\033[1;40m  \033[1;36m   You can do this in the system setting.                     \033[1;40m "
                
                print "\033[1;40m  \033[1;36m Just Press ENTER to go to fix.                               \033[1;40m "
            
        elif page == "fix":
            
            print "\033[1;40m  \033[1;36m   Blender-organizer can try to resolve the issue by it self. \033[1;40m "
            print "\033[1;40m  \033[1;31m   But since it's going to access the SUDO it's not too safe. \033[1;40m "
            print "\033[1;40m  \033[1;31m   Commands it's about to execute can be found in a file      \033[1;40m "
            print "\033[1;40m  \033[1;31m   /pydata/modules/troubleshooter.py . Please check it for    \033[1;40m "
            print "\033[1;40m  \033[1;31m   your system's safety. Or execute those comands by yourself.\033[1;40m "
            print "\033[1;40m  \033[1;36m                                                              \033[1;40m "
            print "\033[1;40m  \033[1;36m                     THE COMMANDS ARE:                        \033[1;40m "
            
            if ER == 0:  #WINDOWS
            
                
                print "\033[1;m\033[1;40m                    https://linuxmint.com/                      \033[1;40m "
            
            elif ER == 1:  #BAISC MODULES
            
                print "\033[1;m\033[1;40m                sudo apt-get remove python2                     \033[1;40m "
                print "\033[1;m\033[1;40m                sudo apt-get install python2                    \033[1;40m "
            
            elif ER == 2:  #GTK
            
                print "\033[1;m\033[1;40m        sudo apt-get install build-essential gnome-devel        \033[1;40m "
                print "\033[1;m\033[1;40m         sudo add-apt-repository ppa:nrbrtx/python2-stuff       \033[1;40m "
                print "\033[1;m\033[1;40m                      sudo apt-get update                       \033[1;40m "
                print "\033[1;m\033[1;40m              sudo apt-get install python-gtk2                  \033[1;40m "
                
            elif ER == 3:  #PIL
            
                print "\033[1;m\033[1;40m                 sudo apt-get install python-pip                \033[1;40m "
                print "\033[1;m\033[1;40m  curl https://bootstrap.pypa.io/get-pip.py --output get-pip.py \033[1;40m "
                print "\033[1;m\033[1;40m                  sudo python2 get-pip.py                       \033[1;40m "
                print "\033[1;m\033[1;40m                      pip install pillow                        \033[1;40m "
            
            elif ER == 4:  #LANGUAGE
            
                print "\033[1;m\033[1;40m                     gnome-control-center                       \033[1;40m "
                
            
            #gnome-control-center
                
            print "\033[1;40m  \033[1;36m                                                              \033[1;40m "    
            print "\033[1;40m  \033[1;31m   NOTE! These commands are for Debian / Ubuntu type distros. \033[1;40m "
            print "\033[1;40m  \033[1;36m   If you are on a different disto. Please better contact us. \033[1;40m "
            print "\033[1;40m  \033[1;36m                                                              \033[1;40m "
            print "\033[1;40m  \033[1;36m  To activate the automatic fix. Type in the following capcha.\033[1;40m "
            print "\033[1;40m  \033[1;31m                      "+fixpass+"                    \033[1;40m "
            print "\033[1;40m  \033[1;36m Just Press ENTER to go to telegram.                          \033[1;40m "
        
        elif page == fixpass:
            print "\033[1;40m  \033[1;31m   STARTTING THE AUTOMATIC FIX...                             \033[1;40m "
            if ER == 0:  #WINDOWS
                print "\033[1;40m  \033[1;31m                      EXECUTING!!!                            \033[1;40m "
                print "\033[1;m\033[1;40m                    https://linuxmint.com/                      \033[1;40m "
                print "\033[1;40m                                                                 \033[1;m"
                import oscalls
                oscalls.Open("https://linuxmint.com/")
            
            elif ER == 1:  #BAISC MODULES
                print "\033[1;40m  \033[1;31m                      EXECUTING!!!                            \033[1;40m "
                print "\033[1;m\033[1;40m                sudo apt-get remove python2                     \033[1;40m "
                print "\033[1;40m                                                                 \033[1;m"
                os.system("sudo apt-get remove python2")
                
                print "\033[1;40m  \033[1;31m                      EXECUTING!!!                            \033[1;40m "
                print "\033[1;m\033[1;40m                sudo apt-get install python2                    \033[1;40m "
                print "\033[1;40m                                                                 \033[1;m"
                os.system("sudo apt-get install python2")
            
            elif ER == 2:  #GTK MODULES
                print "\033[1;40m  \033[1;31m                      EXECUTING!!!                            \033[1;40m "
                print "\033[1;m\033[1;40m        sudo apt-get install build-essential gnome-devel        \033[1;40m "
                print "\033[1;40m                                                                 \033[1;m"
                os.system("sudo apt-get install build-essential gnome-devel")
                
                print "\033[1;40m  \033[1;31m                      EXECUTING!!!                            \033[1;40m "
                print "\033[1;m\033[1;40m         sudo add-apt-repository ppa:nrbrtx/python2-stuff       \033[1;40m "
                print "\033[1;40m                                                                 \033[1;m"
                os.system("sudo add-apt-repository ppa:nrbrtx/python2-stuff")
                
                print "\033[1;40m  \033[1;31m                      EXECUTING!!!                            \033[1;40m "
                print "\033[1;m\033[1;40m                      sudo apt-get update                       \033[1;40m "
                print "\033[1;40m                                                                 \033[1;m"
                os.system("sudo apt-get update")
                
                print "\033[1;40m  \033[1;31m                      EXECUTING!!!                            \033[1;40m "
                print "\033[1;m\033[1;40m              sudo apt-get install python-gtk2                  \033[1;40m "
                print "\033[1;40m                                                                 \033[1;m"
                os.system("sudo apt-get install python-gtk2")
            
            elif ER == 3:  #PIL
                print "\033[1;40m  \033[1;31m                      EXECUTING!!!                            \033[1;40m "
                print "\033[1;m\033[1;40m                 sudo apt-get install python-pip                \033[1;40m "
                print "\033[1;40m                                                                 \033[1;m"
                os.system("sudo apt-get install python-pip")
                
                print "\033[1;40m  \033[1;31m                      EXECUTING!!!                            \033[1;40m "
                print "\033[1;m\033[1;40m  curl https://bootstrap.pypa.io/get-pip.py --output get-pip.py \033[1;40m "
                print "\033[1;40m                                                                 \033[1;m"
                os.system("curl https://bootstrap.pypa.io/get-pip.py --output get-pip.py")
                
                print "\033[1;40m  \033[1;31m                      EXECUTING!!!                            \033[1;40m "
                print "\033[1;m\033[1;40m                  sudo python2 get-pip.py                       \033[1;40m "
                print "\033[1;40m                                                                 \033[1;m"
                os.system("sudo python2 get-pip.py")
                
                print "\033[1;40m  \033[1;31m                      EXECUTING!!!                            \033[1;40m "
                print "\033[1;m\033[1;40m                      pip install pillow                        \033[1;40m "
                print "\033[1;40m                                                                 \033[1;m"
                os.system("pip install pillow")
            
            elif ER == 4:  #LANGUGE
                print "\033[1;40m  \033[1;31m                      EXECUTING!!!                            \033[1;40m "
                print "\033[1;m\033[1;40m                     gnome-control-center                       \033[1;40m "
                print "\033[1;40m                                                                 \033[1;m"
                os.system("gnome-control-center")
            
            print "\033[1;40m  \033[1;31m   FINISHED THE AUTOMATIC FIX...                              \033[1;40m "
              
        print "\033[1;40m                                                                 \033[1;m"
        
        pp = page
        
        page = raw_input("OPTION: ")
        
        # MAKING IT AUTOMATICALLY GO WHERE NEEDED
        
        if page == "":
            if pp not in options:
                page = "details"
            elif pp == "details":
                page = "ideas"
            elif pp == "ideas":
                page = "fix"
            elif pp == "fix" or pp == fixpass:
                page = "telegram"
            elif pp == "telegram":
                page = "exit"
        cls()
    
