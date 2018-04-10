import os
seq = open(os.getcwd().replace("/py_data", "")+"/py_data/rendersequenccer.data", "r")
seq = seq.read()

for i in seq.split("\n"):
    
    if os.path.exists(i):
        try:
            x = open(i+"renderinfo.data", "r")
            y = open(os.getcwd().replace("/py_data", "")+"/py_data//renderinfo.data", "w")
            y.write(x.read())
            y.close()
            
            os.system("python "+os.getcwd().replace("/py_data", "")+"/py_data/renderer.py")
            
        except:
            pass
