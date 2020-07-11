import bpy
import os

#preparing the data for the linking
blendpath =  bpy.data.filepath
folder = blendpath[:blendpath.rfind("/")]
pf = folder[:folder.rfind("/rnd/")]



#gettin the data into the console for testing
print("BLENDPATH : ", blendpath)
print("FOLDER : ", folder)
print("PROJECT FOLDER : ", pf)

if os.path.exists(folder+"/extra/autolink.data"):
    print("FOUND AUTOLINK.DATA YEY :)")
    
    
    #READING FROM extra/autolink.data
    
    df = open(folder+"/extra/autolink.data" , "r")
    df = df.read()
    
    movey = -5
    movex = 0
    
    # TRYING TO GET INFO ABOUT WHAT TO LINK
    for line in df.split("\n"):
        if line.startswith("Link : "):
            
            item = line[7:]
            print("\nLINKING ITEM : "+item)
            
            
            itemsdf = pf+item+"/autolink.data"
            
            #TRYING TO GET ITEM'S AUTOLINK.DATA
            if os.path.exists(itemsdf):
                print("FOUND "+item+"'S AUTOLINK.DATA :)")
                
                #READING ITEM'S AUTOLINK.DATA
                idf = open(itemsdf, "r")
                idf = idf.read()
                
                linkdata = [] #THESE COLLECTIONS WILL BE LINKED
                proxydata = [] # THESE OBJECTS TO MAKE PROXY
                
                for iline in idf.split("\n"):
                    if iline.startswith("Link : "):
                        linkdata.append(iline[7:])
                    elif iline.startswith("Proxy : "):
                        proxydata.append(iline[8:])
                
                print("LINKDATA ", linkdata)
                print("PROXYDATA ", proxydata)
                
                
                astblend = pf+"/ast/"+item[5:]+".blend"
                print("AST BLEND : "+astblend)
                
                #TRYING TO LOCATE THE AST BLEND FILE
                if os.path.exists(astblend):
                    print("YAY FOUND THE BLENDFILE :)")
                
                    
                    for collection in linkdata:
                        
                        
                        
                        movey = movey + 5
                        if movey > 25:
                            movey = 0
                            movex = movex + 5
                        
                        
                        print("ATTEMPTING TO LINK : "+collection)
                        try:
                            with bpy.data.libraries.load(astblend, link=True) as (data_from, data_to):
                                data_to.collections = [c for c in data_from.collections if c == collection]
                            
                            for new_coll in data_to.collections:
                                
                                print("TRYING LINKING ", new_coll.name)
                                
                                try:
                                    if new_coll.name:
                                        instance = bpy.data.objects.new(new_coll.name, None)
                                        instance.instance_type = 'COLLECTION'
                                        instance.instance_collection = new_coll
                                        bpy.context.scene.collection.objects.link(instance)
                                        if not item[5:].startswith("loc"):
                                            bpy.data.objects[collection].location[1] = movey
                                            bpy.data.objects[collection].location[0] = movex
                                        
                                        for proxymake in proxydata:
                                            
                                            print("TRYING PROXING ", proxymake)
                                            
                                            try:
                                                
                                                ob = bpy.context.scene.objects[new_coll.name]
                                                ob.select_set(True)
                                                bpy.context.view_layer.objects.active = ob
                                                bpy.ops.object.proxy_make(object=proxymake)
                                            except Exception as e:
                                                print("PROXY FAILED ", proxymake)
                                                print(e, "ERROR IN PROXY")
                                        #if len(proxymake) > 0:
                                        #    bpy.data.objects[collection].hide_select = True
                                        
                                        bpy.ops.wm.save_mainfile()
                                except Exception as e:
                                    print(e, "ERROR IN LINING")
                        except Exception as e:
                            print(e, "ERROR IN GENERAL")
                                
                                
                else:
                    print("NO BLENDFILE DOEN'T EXIST :(")
            
            
            else:
                print("NO "+item+"'S AUTOLINK.DATA :(")
    
    


else:
    print("NO AUTOLINK.DATA SORRY :(")    
