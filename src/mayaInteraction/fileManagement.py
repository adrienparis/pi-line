import os
import maya.cmds as cmds

def isCurrentSceneIs(path):
    cur = cmds.file(q=True, sn=True)
    print(cur)
    print(path)
    path = path.replace("\\", "/")
    if cur == path:
        return True
    return False

def open(path):
    cmds.file(path, o=True, f=True)