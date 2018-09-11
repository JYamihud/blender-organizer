def timestring(tleft):
    print "tleft", tleft
                                                
    valt = str(tleft)+" SEC"
    print valt , "VALT HERE1"
    if tleft > 60 :
        le = tleft
        tleft = tleft / 60
        le = le - (tleft * 60)
        valt = str(tleft)+":"+ str(le)
    
        if tleft > 60 :
            lele = le
            le = tleft
            tleft = tleft / 60
            le = le - (tleft * 60)
            lele = (lele - le)
            if lele < 0:
                lele = lele * -1
            
            valt = str(tleft)+":"+ str(le) + ":" + str(lele) 
    
            if tleft > 24 :
                le = tleft
                tleft = tleft / 24
                le = le - (tleft * 24)
                valt = str(tleft)+" DAYS AND "+ str(le) + " HRS"
    return valt
    
def getnumstr(num):
    
    s = ""
    for i in range(4-len(str(num))):
        s = s + "0"
    
    return s+str(num)

def getfileoutput(num, FORMAT):
    
    s = getnumstr(num)
    
    if FORMAT == "JPEG":
        s = s + ".jpg"
    else:
        s = s + "." + FORMAT.lower()
        
    return s
