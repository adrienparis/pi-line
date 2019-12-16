import maya.cmds as cmds

import log
from browsing import Browsing
from .UC import *
from .buttonsUC import *
from .treeUC import *
from .tilesViewUC import *
from core.asset import Asset

class ExplorerUC(UserControl, Browsing):

    def __init__(self, parent):
        UserControl.__init__(self, parent)
        Browsing.__init__(self)
        self.dispTile = True
        self.treeView = None
        self.tileView = None
        
    def switchView(self, val):
        self.dispTile = val
        print("tileview is visible" * self.dispTile + "treeview is visible" * (not self.dispTile))
        self.tileView.visibility(not self.dispTile)
        self.treeView.visibility(self.dispTile)

    def load(self):



        self.treeView = TreeUC(self)
        self.tileView = TilesViewUC(self)
        self.switchdisp = switchBtn(self, imageOn="list", imageOff="tiles", label="Switch view")
        self.switchSelect = switchBtn(self, imageOn="selectAll", imageOff="deselectAll", label="Deselect all", labelOn="select all")

        # self.switchTree = cmds.iconTextButton(parent=self.layout, style='iconOnly', image1=getIcon("list"), label='Switch view', w=22, h=22, sic=True, bgc=hexToRGB(self.color.button))
        # self.switchTile = cmds.iconTextButton(parent=self.layout, style='iconOnly', image1=getIcon("tiles"), label='Switch view', w=22, h=22, sic=True, bgc=hexToRGB(self.color.button))
        # self.switchSelAll = cmds.iconTextButton(parent=self.layout, style='iconOnly', image1=getIcon("deselectAll"), label='Deselect all', w=22, h=22, sic=True, bgc=hexToRGB(self.color.button))
        # self.switchDeselAll = cmds.iconTextButton(parent=self.layout, style='iconOnly', image1=getIcon("selectAll"), label='Select all', w=22, h=22, sic=True, bgc=hexToRGB(self.color.button))
        
        self.treeView.importBrows(self)
        self.tileView.importBrows(self)


        self.treeView.load()
        self.tileView.load()
        self.switchdisp.load()
        self.switchSelect.load()



        self.switchdisp.eventHandler("switch", self.switchView)
        self.treeView.eventHandler("newElem", self.newElem)

        self.switchdisp.attach(top=Attach.FORM, bottom=Attach.NONE, left=Attach.FORM, right=Attach.NONE, margin=5)
        self.switchSelect.attach(top=Attach.FORM, bottom=Attach.NONE, left=(Attach.CTRL, self.switchdisp), right=Attach.NONE, margin=5)
        self.treeView.attach(top=(Attach.CTRL, self.switchdisp), bottom=Attach.FORM, left=Attach.FORM, right=Attach.FORM, margin=5)
        self.tileView.attach(top=(Attach.CTRL, self.switchdisp), bottom=Attach.FORM, left=Attach.FORM, right=Attach.FORM, margin=5)






        self.switchdisp.switchTo(False)



        return
        if cmds.tabLayout(self.tabs, q=True, ex=True):
            cmds.deleteUI(self.tabs)
        self.tabs = cmds.tabLayout('SceneFold', parent=self.layout, sc=Callback(self.changeTab))

        if self.project is None or self.project.assets is None:
            self.tabAssets = cmds.formLayout('Assets', numberOfDivisions=100, parent=self.tabs)
        else:
            #TODO REPLACE THAT!!!
            self.assetDisplay(self.tabs, self.project)
        self.tabShots = cmds.formLayout('Shots', numberOfDivisions=100, parent=self.tabs)

        cmds.formLayout(self.layout, e=True, 
                        attachForm=[(self.tabs, 'top', 0),(self.tabs, 'bottom', 0),(self.tabs, 'left', 0), (self.tabs, 'right', 0)])
        self.changeTab()

    def refresh(self):
        self.treeView.importBrows(self)
        self.tileView.importBrows(self)
        self.treeView.reload()
        self.tileView.reload()
        self.tileView.load()


    def changeTab(self):
        tabSel = cmds.tabLayout(self.tabs, q=True, st=True)
        self.runEvent("changeTab", tabSel)

    def newElem(self, elem):
        print(elem)

    def newScene(self, cat, sceneName):
        a = Asset(sceneName, cat, self.project)
        a.make()
        self.project.addAssetToCategory(a, a.category)

     
log.info("ExplorerUC Loaded")