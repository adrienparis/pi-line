import math

import maya.cmds as cmds
from pymel.all import *

from .UC import *

from .defineProjectUC import *
from .detailUC import *
from .explorerUC import *
from .importUC import *
from .projectUC import *
from .syncUC import *
from .versInfonUC import *
from .versionUC import *
from .wipUC import *

class CupboardUC(UserControl):
    colMinSize = 225
    propCol1 = 3
    propCol2 = 2
    propCol3 = 2

    def __init__(self, parent):
        # super(CupboardUC, self).__init__(parent)
        # super().__init__(parent)
        UserControl.__init__(self, parent)
        self.project = None
        self.assets = None
        self.selected = []
        self.viewVert = False
        

    # TODO When the width is large enough display 3 columns in horizontal, When it's to small
    # it's display the 3 column inside one column
    def resizeView(self):
        width = cmds.scrollLayout(self.scrLay, q=True, w=True)
        height = cmds.scrollLayout(self.scrLay, q=True, h=True) -5
        sizeCol = math.trunc(width - 16) / 3
        if sizeCol < self.colMinSize:
            small = True
        else:
            small = False
            cmds.formLayout(self.horizontalFrame, e=True, h=height)

        if small is not self.viewVert:
            self.viewVert = small
            if self.viewVert:
                self.setViewToVertical()
            else:
                self.setViewToHorizontal()
        # cmds.gridLayout(self.gridLay, e=True, numberOfColumns=nCol, numberOfRows=nRow, cw=sizeCol)

    def create(self):
        
        self.layout = cmds.formLayout('cupboardUC', parent=self.parentLay, bgc=hexToRGB(0x444444))

        self.scrLay = cmds.scrollLayout( "cupBoardScrollLayout", parent=self.layout,
                                        horizontalScrollBarThickness=160,
                                        verticalScrollBarThickness=16,
                                        childResizable=True,
                                        cr=True)
        self.horizontalFrame = cmds.formLayout('horizontalFrame', parent=self.scrLay, bgc=hexToRGB(0x3b3b3b), vis=True)
        self.verticalFrame = cmds.formLayout('verticalFrame', parent=self.scrLay, bgc=hexToRGB(0x3b3b3b), vis=True, h=1000)

        self.views = {}

        #initialize the differents userControls and stock them in a dictionnary
        self.views["project"] = ProjectUC(self.horizontalFrame)
        self.views["explorer"] = ExplorerUC(self.horizontalFrame)
        self.views["detail"] = DetailUC(self.horizontalFrame)
        self.views["version"] = VersionUC(self.horizontalFrame)
        self.views["sync"] = SyncUC(self.horizontalFrame)
        self.views["versInfo"] = VersInfonUC(self.horizontalFrame)
        self.views["wip"] = WipUC(self.horizontalFrame)
        self.views["import"] = ImportUC(self.horizontalFrame)
        
        # Attach function to events
        # TODO replace [None] by actual fonction
        self.views["project"].eventHandler("changeProject", self.changeProject)
        self.views["project"].eventHandler("optionBtn", self.commandProjectOption)
        self.views["explorer"].eventHandler("changeItem", self.changeSelection)
        self.views["version"].eventHandler("changeItem", self.changeVersion)
        self.views["sync"].eventHandler("download", self.commandDownload)
        self.views["sync"].eventHandler("delete", None)
        self.views["import"].eventHandler("edit", None)
        self.views["import"].eventHandler("saveVersion", None)
        self.views["import"].eventHandler("publish", None)
        self.views["import"].eventHandler("importRaw", None)
        self.views["import"].eventHandler("importRef", None)
        self.views["import"].eventHandler("importProxy", None)
        
        #Create and load all the interfaces
        for key, view in self.views.items():
            view.create()
        # self.views["project"].create()
        # self.views["explorer"].create()
        # self.views["detail"].create()
        # self.views["version"].create()
        # self.views["sync"].create()
        # self.views["versInfo"].create()
        # self.views["wip"].create()
        # self.views["import"].create()
        self.scrLay = cmds.scrollLayout( self.scrLay, e=True, rc=Callback(self.resizeView))
        cmds.formLayout(self.layout, edit=True,
                        attachForm=[(self.scrLay, 'top', -2),(self.scrLay, 'bottom', -2),(self.scrLay, 'left', -2), (self.scrLay, 'right', -2)])

        
        self.views["project"].setLastProject()
        self.resizeView()

    def setViewToHorizontal(self):
        if len(self.views) == 0:
            return
        col1 = (self.propCol1 * 100) / (self.propCol1 + self.propCol2 + self.propCol3)
        col2 = ((self.propCol1 + self.propCol2) * 100)/ (self.propCol1 + self.propCol2 + self.propCol3)
        

        self.views["project"].attach(top=Attach.FORM, bottom=(Attach.NONE), left=Attach.FORM, right=(Attach.POS, col1), margin=(5,5,2,5))
        self.views["explorer"].attach(top=(Attach.CTRL, self.views["project"]), bottom=Attach.FORM, left=Attach.FORM, right=(Attach.POS, col1), margin=(5,5,2,5))
        self.views["detail"].attach(top=Attach.FORM, bottom=Attach.NONE, left=(Attach.POS, col1), right=(Attach.POS, col2), margin=5)
        self.views["version"].attach(top=(Attach.CTRL, self.views["detail"]),bottom=(Attach.CTRL, self.views["sync"]), left=(Attach.POS, col1), right=(Attach.POS, col2), margin=5)
        self.views["sync"].attach(top=Attach.NONE, bottom=Attach.FORM, left=(Attach.POS, col1), right=(Attach.POS, col2), margin=5)
        self.views["versInfo"].attach(top=Attach.FORM, bottom=(Attach.CTRL, self.views["wip"]), left=(Attach.POS, col2), right=Attach.FORM, margin=5)
        self.views["wip"].attach(top=Attach.NONE, bottom=(Attach.CTRL, self.views["import"]), left=(Attach.POS, col2), right=Attach.FORM, margin=5)
        self.views["import"].attach(top=Attach.NONE, bottom=Attach.FORM, left=(Attach.POS, col2), right=Attach.FORM, margin=5)

        self.views["project"].setParent(self.horizontalFrame)
        self.views["explorer"].setParent(self.horizontalFrame)
        self.views["detail"].setParent(self.horizontalFrame)
        self.views["version"].setParent(self.horizontalFrame)
        self.views["sync"].setParent(self.horizontalFrame)
        self.views["versInfo"].setParent(self.horizontalFrame)
        self.views["wip"].setParent(self.horizontalFrame)
        self.views["import"].setParent(self.horizontalFrame)

        # self.applyAttach()

        af = [] + self.views["project"].af + self.views["explorer"].af + self.views["detail"].af + self.views["version"].af + self.views["sync"].af + self.views["versInfo"].af + self.views["wip"].af + self.views["import"].af
        ap = [] + self.views["project"].ap + self.views["explorer"].ap + self.views["detail"].ap + self.views["version"].ap + self.views["sync"].ap + self.views["versInfo"].ap + self.views["wip"].ap + self.views["import"].ap
        ac = [] + self.views["project"].ac + self.views["explorer"].ac + self.views["detail"].ac + self.views["version"].ac + self.views["sync"].ac + self.views["versInfo"].ac + self.views["wip"].ac + self.views["import"].ac
        an = [] + self.views["project"].an + self.views["explorer"].an + self.views["detail"].an + self.views["version"].an + self.views["sync"].an + self.views["versInfo"].an + self.views["wip"].an + self.views["import"].an

        cmds.formLayout(self.verticalFrame, edit=True, vis=False)
        cmds.formLayout(self.horizontalFrame, edit=True, vis=True,
                        attachForm=af,
                        attachPosition=ap,
                        attachControl=ac,
                        attachNone=an)

    def setViewToVertical(self):
        if len(self.views) == 0:
            return
        self.views["project"].attach(top=Attach.FORM, bottom=(Attach.NONE), left=Attach.FORM, right=Attach.FORM, margin=5)
        self.views["explorer"].attach(top=(Attach.CTRL, self.views["project"]), bottom=(Attach.POS, 55), left=Attach.FORM, right=Attach.FORM, margin=5)
        self.views["detail"].attach(top=(Attach.CTRL, self.views["explorer"]), bottom=Attach.NONE, left=Attach.FORM, right=Attach.FORM, margin=5)
        self.views["version"].attach(top=(Attach.CTRL, self.views["detail"]),bottom=(Attach.POS, 80), left=Attach.FORM, right=Attach.FORM, margin=5)
        self.views["sync"].attach(top=(Attach.CTRL, self.views["version"]), bottom=Attach.NONE, left=Attach.FORM, right=Attach.FORM, margin=5)
        self.views["versInfo"].attach(top=(Attach.CTRL, self.views["sync"]), bottom=Attach.NONE, left=Attach.FORM, right=Attach.FORM, margin=5)
        self.views["wip"].attach(top=(Attach.CTRL, self.views["versInfo"]), bottom=Attach.NONE, left=Attach.FORM, right=Attach.FORM, margin=5)
        self.views["import"].attach(top=(Attach.CTRL, self.views["wip"]), bottom=Attach.NONE, left=Attach.FORM, right=Attach.FORM, margin=5)

        self.views["project"].setParent(self.verticalFrame)
        self.views["explorer"].setParent(self.verticalFrame)
        self.views["detail"].setParent(self.verticalFrame)
        self.views["version"].setParent(self.verticalFrame)
        self.views["sync"].setParent(self.verticalFrame)
        self.views["versInfo"].setParent(self.verticalFrame)
        self.views["wip"].setParent(self.verticalFrame)
        self.views["import"].setParent(self.verticalFrame)

        af = [] + self.views["project"].af + self.views["explorer"].af + self.views["detail"].af + self.views["version"].af + self.views["sync"].af + self.views["versInfo"].af + self.views["wip"].af + self.views["import"].af
        ap = [] + self.views["project"].ap + self.views["explorer"].ap + self.views["detail"].ap + self.views["version"].ap + self.views["sync"].ap + self.views["versInfo"].ap + self.views["wip"].ap + self.views["import"].ap
        ac = [] + self.views["project"].ac + self.views["explorer"].ac + self.views["detail"].ac + self.views["version"].ac + self.views["sync"].ac + self.views["versInfo"].ac + self.views["wip"].ac + self.views["import"].ac
        an = [] + self.views["project"].an + self.views["explorer"].an + self.views["detail"].an + self.views["version"].an + self.views["sync"].an + self.views["versInfo"].an + self.views["wip"].an + self.views["import"].an

        cmds.formLayout(self.horizontalFrame, edit=True, vis=False)
        cmds.formLayout(self.verticalFrame, edit=True, vis=True,
                        attachForm=af,
                        attachPosition=ap,
                        attachControl=ac,
                        attachNone=an)

    def commandProjectOption(self):
        pass
        # print("creating tree")
        # if self.project is not None:
        #     self.project.createTreeTemplateLocal()

    def changeProject(self, p):
        if p == None:
            print("the project was not found")
            # cmds.error("Project do not exist")

            return
        self.project = p
        self.project.fetchAll()
        self.project.setProject()
        self.views["explorer"].setProject(p)
        self.views["explorer"].reload()

    def changeSelection(self, item):
        if len(item) == 1:
            self.selected = [item[0]]
            self.views["detail"].changeAsset(item[0])
            self.views["detail"].refresh()

    def changeVersion(self, s):
        self.step = s

    def commandDownload(self):
        if len(self.selected) > 0:
            if self.step == 4:
                self.selected[0].download()
                self.selected[0].state = 0
            else:
                self.selected[0].downloadStep(self.step)
                self.selected[0].state = 2
        self.views["explorer"].refresh()
        #TODO remove the line below
        self.views["explorer"].reload()


    def attachViewTo(self, layout, parent):
        print("attach " + layout + " to " + self.views[parent].layout)
        cmds.formLayout(layout, e=True, parent=self.views[parent].layout)
        cmds.formLayout(self.views[parent], edit=True,
                        attachForm=[(layout, 'top', 5),(layout, 'bottom', 5),(layout, 'left', 5), (layout, 'right', 5)])


    def reload(self):
        self.colProj.reload()
    def refresh(self):
        self.colProj.reload()

print("Cupboard Loaded")