def formLayout(*args, **kwargs):
    print("formLayout")
    return "formLayout"

def workspaceControl(*args, **kwargs):
    print("workspaceControl")
    return "workspaceControl"

def deleteUI(*args, **kwargs):
    print("deleteUI")
    return "deleteUI"

def scrollLayout(*args, **kwargs):
    
    for key, value in kwargs.items():
        if key is "q":
            return 0
    print("scrollLayout")
    return "scrollLayout"

def optionMenu(*args, **kwargs):
    print("optionMenu")
    return "optionMenu"

def menuItem(*args, **kwargs):
    print("menuItem")
    return "menuItem"

def iconTextButton(*args, **kwargs):
    print("iconTextButton")
    return "iconTextButton"

def tabLayout(*args, **kwargs):
    print("tabLayout")
    return "tabLayout"

def text(*args, **kwargs):
    print("text")
    return "text"

def columnLayout(*args, **kwargs):
    print("columnLayout")
    return "columnLayout"

def radioCollection(*args, **kwargs):
    print("radioCollection")
    return "radioCollection"

def radioButton(*args, **kwargs):
    print("radioButton")
    return "radioButton"

def button(*args, **kwargs):
    print("button")
    return "button"


