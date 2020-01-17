import maya.cmds as cmds

import log
from .UC import *
from .explorerUC import ExplorerUC
from core.asset import Asset
from core.user import User

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
            for c in sorted(self.project.assets.keys()):
                p = self.explorerAssets.addFolder(c, c)
                for asset in self.project.assets[c]:
                    v = asset.getLastVersion()
                    ico = self.getStateIcon(v)
                    self.explorerAssets.addItem(asset.name, asset, parent=p, image=asset.getImage(), icon=ico)
                    print(asset.getImage())
            self.explorerShots.deleteAllItemsFolders()
            for c in sorted(self.project.shots.keys()):
                p = self.explorerShots.addFolder(c, c)
                for shot in self.project.shots[c]:
                    v = shot.getLastVersion()
                    ico = self.getStateIcon(v)
                    self.explorerShots.addItem(shot.name, shot, parent=p, image=shot.getImage(), icon=ico)

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
        self.explorerShots.eventHandler("changeSelection", self.runEvent, "changeItem")
        self.explorerAssets.eventHandler("newElem", self.runEvent, "newElem", "asset")
        self.explorerShots.eventHandler("newElem", self.runEvent, "newElem", "shot")




        # self.explorerAssets.addable = False
        # self.explorerShots.addable = False

        self.explorerAssets.load()
        self.explorerShots.load()
        if self.project is not None:
            self.explorerAssets.addable = self.project.roles.isUsernameIsAutorised(User().name, "createNewAssets")
            self.explorerShots.addable = self.project.roles.isUsernameIsAutorised(User().name, "createNewShots")

        cmds.formLayout(self.tabAssets, e=True, attachForm=self.explorerAssets.pins.form)
        cmds.formLayout(self.tabShots, e=True, attachForm=self.explorerShots.pins.form)

        cmds.formLayout(self.layout, e=True, 
                        attachForm=[(self.tabs, 'top', 0),(self.tabs, 'bottom', 0),(self.tabs, 'left', 0), (self.tabs, 'right', 0)])
        self.changeTab()

    def refresh(self):
        if self.project is not None:
            self.explorerAssets.addable = self.project.roles.isUsernameIsAutorised(User().name, "createNewAssets")
            self.explorerShots.addable = self.project.roles.isUsernameIsAutorised(User().name, "createNewShots")
        self.refreshProjectTree()
        self.explorerAssets.refresh()
        self.explorerShots.refresh()

    def changeTab(self):
        tabSel = cmds.tabLayout(self.tabs, q=True, st=True)
        self.runEvent("changeTab", tabSel)


log.info("SceneExplorerUC Loaded")