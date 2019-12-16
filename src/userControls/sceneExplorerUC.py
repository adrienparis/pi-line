import maya.cmds as cmds

import log
from .UC import *
from .explorerUC import ExplorerUC
from core.asset import Asset

class SceneExplorerUC(UserControl):

    def __init__(self, parent):
        UserControl.__init__(self, parent)
        self.project = None
        self.tabs = ""


    def setProject(self, project):
        self.project = project

    def refreshProjectTree(self):
        plop = 0
        if self.project is not None:
            self.explorerAssets.deleteAllItemsFolders()
            for c in self.project.assets.keys():
                p = self.explorerAssets.addFolder(c, c)
                self.explorerAssets.addFolder("Test" + str(plop), "test", parent=p)
                plop += 1
                for asset in self.project.assets[c]:
                    v = asset.getLastVersion()
                    ico = self.getStateIcon(v)
                    self.explorerAssets.addItem(asset.name, asset, parent=p, icon=ico)

    def getStateIcon(self, v):
        ico = "denied"
        if v is not None:
            if v.onServer and v.onLocal:
                ico = "check"
            elif v.onServer and not v.onLocal:
                ico = "download"
            elif not v.onServer and v.onLocal:
                ico = "upload"
        else:
            ico = "new"
        return ico
        
    def load(self):

        self.tabs = cmds.tabLayout('SceneFold', parent=self.layout, sc=Callback(self.changeTab))

        self.tabAssets = cmds.formLayout('Assets', numberOfDivisions=100, parent=self.tabs)
        self.tabShots = cmds.formLayout('Shots', numberOfDivisions=100, parent=self.tabs)


        self.explorerAssets = ExplorerUC(self.tabAssets)
        self.explorerShots = ExplorerUC(self.tabShots)

        self.explorerAssets.attach(top=Attach.FORM, bottom=Attach.FORM, left=Attach.FORM, right=Attach.FORM)
        self.explorerShots.attach(top=Attach.FORM, bottom=Attach.FORM, left=Attach.FORM, right=Attach.FORM)

        self.explorerAssets.color.background = 0xa5c957
        self.explorerShots.color.background = 0xa5c957


        self.refreshProjectTree()
        self.explorerAssets.eventHandler("changeSelection", self.runEvent, "changeItem")





        self.explorerAssets.load()
        self.explorerShots.load()

        cmds.formLayout(self.tabAssets, e=True, attachForm=self.explorerAssets.pins.form)
        cmds.formLayout(self.tabShots, e=True, attachForm=self.explorerShots.pins.form)

        cmds.formLayout(self.layout, e=True, 
                        attachForm=[(self.tabs, 'top', 0),(self.tabs, 'bottom', 0),(self.tabs, 'left', 0), (self.tabs, 'right', 0)])
        self.changeTab()

    def refresh(self):
        self.refreshProjectTree()
        self.explorerAssets.refresh()
        self.explorerShots.refresh()

    def changeTab(self):
        tabSel = cmds.tabLayout(self.tabs, q=True, st=True)
        self.runEvent("changeTab", tabSel)


log.info("SceneExplorerUC Loaded")