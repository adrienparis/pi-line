def formLayout(*args, **kwargs):
    print("formLayout" + str(kwargs))
    return "formLayout"

def workspaceControl(*args, **kwargs):
    print("workspaceControl" + str(kwargs))
    return "workspaceControl"

def deleteUI(*args, **kwargs):
    print("deleteUI" + str(kwargs))
    return "deleteUI"

def scrollLayout(*args, **kwargs):
    
    for key, value in kwargs.items():
        if key is "q":
            return 0
    print("scrollLayout" + str(kwargs))
    return "scrollLayout"

def optionMenu(*args, **kwargs):
    print("optionMenu" + str(kwargs))
    return "optionMenu"

def menuItem(*args, **kwargs):
    print("menuItem" + str(kwargs))
    return "menuItem"

def iconTextButton(*args, **kwargs):
    print("iconTextButton" + str(kwargs))
    return "iconTextButton"

def tabLayout(*args, **kwargs):
    print("tabLayout" + str(kwargs))
    return "tabLayout"

def text(*args, **kwargs):
    print("text" + str(kwargs))
    return "text"

def columnLayout(*args, **kwargs):
    print("columnLayout" + str(kwargs))
    return "columnLayout"

def radioCollection(*args, **kwargs):
    print("radioCollection" + str(kwargs))
    return "radioCollection"

def radioButton(*args, **kwargs):
    print("radioButton" + str(kwargs))
    return "radioButton"

def button(*args, **kwargs):
    print("button" + str(kwargs))
    return "button"

def warning(*args, **kwargs):
    print("warning" + str(kwargs))
    return "warning"

def error(*args, **kwargs):
    print("error" + str(kwargs))
    return "error"


