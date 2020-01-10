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
        self.tileView.visibility(not self.dispTile)
        self.treeView.visibility(self.dispTile)

    def load(self):



        self.treeView = TreeUC(self)
        self.tileView = TilesViewUC(self)
        self.switchdisp = switchBtn(self, imageOn="list", imageOff="tiles", label="Switch view")
        self.switchSelect = switchBtn(self, imageOn="selectAll", imageOff="deselectAll", label="Deselect all", labelOn="select all")
   
        self.treeView.importBrows(self)
        self.tileView.importBrows(self)
        self.treeView.addable = self.addable
        self.tileView.addable = self.addable
        log.debug("addable", self.tileView.addable)


        self.treeView.load()
        self.tileView.load()
        self.switchdisp.load()
        self.switchSelect.load()



        self.switchdisp.eventHandler("switch", self.switchView)
        self.treeView.eventHandler("newElem", self.newElem)
        self.tileView.eventHandler("newElem", self.newElem)

        self.treeView.eventHandler("changeSelection", self.changeSelection, "treeView")
        self.tileView.eventHandler("changeSelection", self.changeSelection, "tileView")

        self.switchdisp.attach(top=Attach.FORM, bottom=Attach.NONE, left=Attach.FORM, right=Attach.NONE, margin=5)
        self.switchSelect.attach(top=Attach.FORM, bottom=Attach.NONE, left=(Attach.CTRL, self.switchdisp), right=Attach.NONE, margin=5)
        self.treeView.attach(top=(Attach.CTRL, self.switchdisp), bottom=Attach.FORM, left=Attach.FORM, right=Attach.FORM, margin=5)
        self.tileView.attach(top=(Attach.CTRL, self.switchdisp), bottom=Attach.FORM, left=Attach.FORM, right=Attach.FORM, margin=5)






        self.switchdisp.switchTo(False)


    def refresh(self):
        self.treeView.addable = self.addable
        self.tileView.addable = self.addable
        self.treeView.importBrows(self)
        self.tileView.importBrows(self)
        self.treeView.reload()
        self.tileView.reload()
        self.tileView.load()

    def changeSelection(self, view, selection):
        sel = [x.elem for x in selection if x.selected]
        self.runEvent("changeSelection", sel)

    # def changeTab(self):
    #     tabSel = cmds.tabLayout(self.tabs, q=True, st=True)
    #     self.runEvent("changeTab", tabSel)

    def newElem(self, elem):
        # print(elem)
        self.runEvent("newElem", elem)

    def newScene(self, cat, sceneName):
        a = Asset(sceneName, cat, self.project)
        a.make()
        self.project.addAssetToCategory(a, a.category)

     
log.info("ExplorerUC Loaded")