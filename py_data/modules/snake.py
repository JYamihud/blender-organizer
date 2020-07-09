    
import gtk
import time
import glib
import random
import os

VERSION = 0.1


# MAIN WINDOW LAYOUT

snakewindow = gtk.Window()
snakewindow.grab_focus()
snakewindow.set_title("THE BITCHY PYTHON")
snakewindow.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#292929"))
snakewindow.set_default_size(500, 500)
snakewindow.set_position(gtk.WIN_POS_CENTER)
snakewindow.connect("destroy", lambda w: gtk.main_quit())

mainbox = gtk.VBox(False)
snakewindow.add(mainbox)

def on_restart(widget):
    pass

count = gtk.Label("Lenght : 2")
mainbox.pack_start(count, False)





# GRAPHICS

pause = True
pixelsize = 20
tickspeed = 100
w, h = 0, 0

spit = False
snake = [[2,1],[1,1]] #,[1,2],[1,3],[1,4]]
food = [5, 5]
direction = "r"



def snake_graphics(widget, event, win):
    
    
    
    
    global pixelsize
    widget.set_size_request(pixelsize*4, pixelsize*4)
    
    global w, h
    w, h = widget.window.get_size()
    xgc = widget.window.new_gc()
    
    mx, my, fx  = widget.window.get_pointer()
    
    winactive = win.is_active()
    
    
    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#1c1c1c"))
    widget.window.draw_rectangle(xgc, True, 0,0,w,h)
    
    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#000000"))
    # frame
    widget.window.draw_rectangle(xgc, False, pixelsize, pixelsize, w-pixelsize*2, h-pixelsize*2)
    
    #inside grid
    
    if pixelsize > 2:
        
        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#2c2c2c"))
        
        for i in range(0,h,pixelsize):
            
            if i > pixelsize and i < h-pixelsize:
                widget.window.draw_line(xgc, pixelsize+1, i, w-pixelsize-1, i)
        for i in range(0,w,pixelsize):
            
            if i > pixelsize and i < w-pixelsize:
                widget.window.draw_line(xgc, i, pixelsize+1, i, h-pixelsize-1)
    
    
    # draw snake
    
    xgc.set_rgb_fg_color(gtk.gdk.color_parse("#E7A153")) #color of the snake
    
    global snake
    global direction
    global pause
    for x, i in enumerate(snake):
        
        sw, sh = i
        
        widget.window.draw_rectangle(xgc, True, sw*pixelsize, sh*pixelsize, pixelsize, pixelsize)
        
        #head move
        
        if pause == False:
        
            if x == 0:
                if direction == "r":
                    snake[x] = [sw+1, sh]
                    pw, ph = sw, sh
                if direction == "l":
                    snake[x] = [sw-1, sh]
                    pw, ph = sw, sh
                if direction == "u":
                    snake[x] = [sw, sh-1]
                    pw, ph = sw, sh
                if direction == "d":
                    snake[x] = [sw, sh+1]
                    pw, ph = sw, sh 
                    
                   
            else:
                snake[x] = pw, ph
                pw, ph = sw, sh
    
    global food
    # groth
    if snake[0] == food:
        
        food = [random.randint(1,w/pixelsize-1), random.randint(1,h/pixelsize-1)]
        snake.append([pw, ph])
        
        global count
        count.set_text("Lenght : "+str(len(snake)))
        
        if food in snake or (food[0], food[1]) in snake:
            food = [random.randint(1,w/pixelsize-5), random.randint(1,h/pixelsize-5)]
    # death
    dead = False
    if (snake[0][0],snake[0][1]) in snake[1:] or snake[0][0] == w/pixelsize or snake[0][1] == h/pixelsize\
    or snake[0][0] == 0 or snake[0][1] == 0:
        
        #snake high score dialogue
        
        # checking if the highscore file exisit
        if "highscores.snake" in os.listdir(os.getcwd()):
            print "Exists already"
        else:
            quickly = open("highscores.snake", "w")
            quickly.close()
        
        #writting a new score
        scoresw = open("highscores.snake", "ab")
        scoresw.write(str(len(snake))+"\n")
        scoresw.close()
        
        #opening all the rest of scores
        scores = tuple(open("highscores.snake", "r"))
        quick = scores
        
        scores = []
        for score in quick:
            try:
                scores.append(int(score))
            except:
                pass
        
        scores = reversed(sorted(scores))
        
        #making a string that will appear in the scores window
        quickly = ""
        for score in scores:
            if str(score)+"\n" not in quickly:
                quickly = quickly + str(score) + "\n"
        scoreslabel = gtk.Label(quickly)
        
        scorew = gtk.Window()
        scorew.set_title("HIGH SCORES")
        scorew.set_size_request(300, 300)
        scorscroller = gtk.ScrolledWindow()
        scorscroller.add_with_viewport(scoreslabel)
        scorew.add(scorscroller)
        
        scorew.show_all()
        
        global count
        count.set_text("Lenght : 2")
        
        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#FF0000"))
        
        
        sw, sh = snake[1]
        widget.window.draw_rectangle(xgc, True, sw*pixelsize, sh*pixelsize, pixelsize, pixelsize)
        
        direction = "r"
        snake = [[2,1],[1,1]]
        dead = True
        
    # draw food
    global spit 
    if not spit:
        spit = True
        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#FF00FF")) #color of the food
    else:
        spit = False
        xgc.set_rgb_fg_color(gtk.gdk.color_parse("#FF0000")) #color of the food
    
    
    sw, sh = food
    widget.window.draw_rectangle(xgc, True, sw*pixelsize, sh*pixelsize, pixelsize, pixelsize)
    
    # restarting
    
    def refresh():
        
        
        
        
            widget.queue_draw()
            
    global tickspeed
    
    
    if dead == False:
        
        
        glib.timeout_add(tickspeed, refresh)
    
    

    
graphics = gtk.DrawingArea()
mainbox.pack_start(graphics)
graphics.connect("expose-event", snake_graphics, snakewindow)


# KEYBORAD SENSORING 

def sens(widget,  key):
    
    global direction
    if key.string == "w" and direction != "d":
        
        direction = "u"
    if key.string == "s" and direction != "u":
        
        direction = "d"
    if key.string == "d" and direction != "l":
        
        direction = "r"
    if key.string == "a" and direction != "r":
        
        direction = "l"
        
    #if key.string == "p" :
    #    global pause
    #    if pause == True:
    #       pause = False
    #    else:
    #        pause = True
    
    if key.string: #####   IF MOUSE CLICKED #####   :
        global pause
        pause = False
    
    
    if key.keyval == 65293:
        print "ENTER PRESSED"
        
        global graphics
        graphics.queue_draw()
    
snakewindow.connect("key-press-event", sens)





# BOTTOM SETTINGS

def pixelset_fun(widget):
    global pixelsize
    pixelsize = int(widget.get_value())

box = gtk.HBox(True)
mainbox.pack_end(box, False)

adj = gtk.Adjustment(0.0, 1.0, 100.0, 1.0, 10.0, 0.0)
pixelset = gtk.HScale(adj)
box.pack_start(pixelset)

pixelset.set_value(pixelsize)
pixelset.connect("value-changed", pixelset_fun)







def speedset_fun(widget):
    global tickspeed
    tickspeed = int(widget.get_value())


adj2 = gtk.Adjustment(0.0, 1.0, 1000.0, 1.0, 10.0, 0.0)
speedset = gtk.HScale(adj2)
box.pack_start(speedset)

speedset.set_value(tickspeed)
speedset.connect("value-changed", speedset_fun)



# GTK MAIN

snakewindow.show_all()
gtk.main()
