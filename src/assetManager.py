import os
import datetime
# import maya.cmds as cmds

treeTemplate = [["1_preprod"],
                ["2_ressource"], 
                ["3_work", 
                    ["maya", 
                        ["scenes", 
                            ["assets"],
                            ["shots"]],
                        ["images",
                                ["shots"]],
                                    ["sourceimage", ["assets"]]]],
                ["4_out"]
]

def createProjectTree(tree, deep, path):
    name = ""
    print(tree, deep, path)
    for f in tree:
        print(f)
        if type(f) == str or type(f) == unicode:
            print("\t" * deep + f)
            name = f
            print(os.path.join(path, name))
            if os.path.exists(os.path.join(path, name)):
                print("\t" + name + ' : exists')
            else:
                os.mkdir(os.path.join(path, name))
        else:
            createProjectTree(f, deep + 1, path + "/" + name)


def takeScreenshot():
    print('plap')
    # cmds.viewFit()
    
    ws = cmds.workspace(q = True, fullName = True)
    wsp = ws + "/" + "images"
    cmds.sysFile(wsp, makeDir=True)

    # Prepare unique image name for snapshot
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print('plap')
    print(now)
    imageSnapshot = wsp + "/" + "endSnapshot_" + ".jpg"

    # Take a snapshot of the viewport and save to file
    cmds.refresh(cv=True, fe = "jpg", fn = imageSnapshot)
    cmds.saveImage("plop", currentView=True )

# from  Tkinter import *
# import Tkinter, Tkconstants, tkFileDialog
# from Tkinter import FileDialog
# root = Tk()
# root.directory = tkFileDialog.askdirectory()
# dir =  FileDialog.askopenfilename()
# print (root.directory)
# print (dir)

def createTreeTemplate(path):
    (path, fold) = os.path.split(path)
    print(treeTemplate)
    tree = [fold] + treeTemplate
    print("the path")
    print(tree)
    print(path)
    createProjectTree(tree, 0, path)