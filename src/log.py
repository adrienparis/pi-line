import sys
try:
    import maya.cmds as cmds
except:
    print("no maya")

DEBUG = False


def info(*args):
    if len(args) >= 1:
        if len(args) >= 2:
            print("(i) - " + args[0] + " -> " + str(args[1:]))
        else:
            print("(i) - " + args[0])

def debug(*args):
    if not DEBUG:
        return
    if len(args) >= 1:
        if len(args) >= 2:
            print("[D] - " + args[0] + " -> " + str(args[1:]))
        else:
            print("[D] - " + args[0])


def warning(*args):
    if len(args) >= 1:
        if "maya" in sys.modules:
            cmds.warning(args)
        else:
            if len(args) >= 2:
                print("/!\\ - " + args[0] + " -> " + str(args[1:]))
            else:
                print("/!\\ - " + args[0])

def error(*args):
    if len(args) >= 1:
        if "maya" in sys.modules:
            cmds.error(args)
        else:
            if len(args) >= 2:
                print("(X) - " + args[0] + " -> " + str(args[1:]))
            else:
                print("(X) - " + args[0])

