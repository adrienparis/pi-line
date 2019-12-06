import os
import math

import maya.cmds as cmds
from pymel.all import *
import assetManager as am
# import uiInterface as piUi
import asset as ast
import plUser as usr

import userControls as UC

def AssetTreeView(parent):
    layout = cmds.formLayout('AssetTreeView', parent=parent)

    control = cmds.treeView( parent = layout, adr = False, ams = True, pc=[1, clickAsset], nb=1 )

    cmds.formLayout(layout,e=True, attachForm=[ (control,'top', 2),
                                                (control,'left', 2), 
                                                (control,'bottom', 2), 
                                                (control,'right', 2)])
    assets = getAssetsNames()
    if assets == False:
        print("No assets founds")
        return layout


    for categorie in sorted(assets, key=unicode.lower):
        cmds.treeView( control, e=True, addItem = (categorie, ""))
        for item in assets[categorie]:
            cmds.treeView( control, e=True, addItem = (item, categorie))
    # cmds.treeView(control,edit=True,pressCommand=[(1,pressTreeCallBack),(2,pressTreeCallBack),(3,pressTreeCallBack)])
    cmds.treeView(control,edit=True,selectCommand=selectTreeCallBack)


    # cmds.treeView( control, edit=True, removeAll = True )
    return layout

def switchAssetView(*args):
    buttonTree = args[0].split(", ")[0]
    buttonTile = args[0].split(", ")[1]
    atrv = args[0].split(", ")[2]
    ativ = args[0].split(", ")[3]
    switch = cmds.layout(ativ, q=True, vis=True)

    cmds.layout(ativ, e=True, vis=not switch)
    cmds.layout(atrv, e=True, vis=switch)
    cmds.iconTextButton(buttonTile, e=True, vis=not switch)
    cmds.iconTextButton(buttonTree, e=True, vis=switch)


def menuBarLayout(parent):
    layout = cmds.menuBarLayout('MenuBar', parent=parent, bgc=UC.hexToRGB(0x5285a6))
    cmds.menu( label='File' )
    cmds.menuItem( label='New' )
    cmds.menuItem( label='Open' )
    cmds.menuItem( label='Close' )
    return layout


def mainUI():
    sizeImage = 100

    # plWindow = cmds.workspaceControl(u"Pi-Line", retain=False, iw=400, ih=600, floating=True)


    # mainForm = cmds.formLayout('MainForm', numberOfDivisions=100)
    
    # menuBarLay = menuBarLayout(mainForm)
    # cmds.setParent(mainForm)

    win = UC.WindowUC(u"Pi-Line")
    win.load()

    cpBrd = UC.CupboardUC(win)
    cpBrd.create()
    cpBrd.attach(top=UC.Attach.FORM, bottom=UC.Attach.FORM, left=UC.Attach.FORM, right=UC.Attach.FORM, margin=0)

    win.applyAttach()

    # secForm = cmds.formLayout('secForm', numberOfDivisions=100)
    # secForm = cpBrd.layout
    # cmds.formLayout( mainForm, edit=True,
    #                 attachForm=[(menuBarLay, 'top', 0), (menuBarLay, 'left', 0), (menuBarLay, 'right', 0), (cpBrd.layout, 'left', 0), (cpBrd.layout, 'right', 0), (cpBrd.layout, 'bottom', 0)],
    #                 attachControl=[(cpBrd.layout, 'top', 0, menuBarLay)],
    #                 attachNone=[(menuBarLay, 'bottom')])

def start():
    print(u"=====Start pi-Line=====")
    # print("Merci pilou <3")
    if cmds.workspaceControl(u"Pi-Line", exists=1):
        cmds.deleteUI(u"Pi-Line")
    mainUI()

if __name__ == "__main__":
    if cmds.workspaceControl(u"Pi-Line", exists=1):
        cmds.deleteUI(u"Pi-Line")
    # execute only if run as a script
    start()
if __name__ == "ui":
    print("rentre dans ui si name == ui")
    if cmds.workspaceControl(u"Pi-Line", exists=1):
        cmds.deleteUI(u"Pi-Line")

print("AMui Loaded")