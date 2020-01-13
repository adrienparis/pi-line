import math

import maya.cmds as cmds
from pymel.all import *

from .UC import *

import log
from core.asset import *
from core.shot import *
from core.version import *

from .chooseStepUC import ChooseStepUC
from .newElemUC import NewVersion
from .defineProjectUC import *
from .detailUC import *
from .sceneExplorerUC import *
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
        self.lastSelected = []
        self.versSelected = []
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

    def load(self):
        
        # self.layout = cmds.formLayout('cupboardUC', parent=self.parentLay, bgc=hexToRGB(0x444444))

        self.scrLay = cmds.scrollLayout( "cupBoardScrollLayout", parent=self.layout,
                                        horizontalScrollBarThickness=160,
                                        verticalScrollBarThickness=16,
                                        childResizable=True,
                                        cr=True)
        self.horizontalFrame = cmds.formLayout('horizontalFrame', parent=self.scrLay, vis=True)
        self.verticalFrame = cmds.formLayout('verticalFrame', parent=self.scrLay, vis=True, h=1000)

        self.views = {}

        #initialize the differents userControls and stock them in a dictionnary
        self.views["project"] = ProjectUC(self.horizontalFrame)
        self.views["explorer"] = SceneExplorerUC(self.horizontalFrame)
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
        self.views["project"].eventHandler("refreshBtn", self.refreshAll)
        self.views["explorer"].eventHandler("changeItem", self.changeSelection)
        self.views["explorer"].eventHandler("changeTab", self.changeTabScene)
        self.views["explorer"].eventHandler("newElem", self.commandNewElem)
        self.views["version"].eventHandler("changeItem", self.changeVersion)
        self.views["sync"].eventHandler("download", self.commandDownload)
        self.views["sync"].eventHandler("delete", None)
        self.views["import"].eventHandler("open", self.commandOpen)
        self.views["import"].eventHandler("saveVersion", self.commandSaveVersion)
        self.views["import"].eventHandler("publish", self.commandPublish)
        self.views["import"].eventHandler("importRaw", None)
        self.views["import"].eventHandler("importRef", None)
        self.views["import"].eventHandler("importProxy", None)
        
        #load all the interfaces

        for key, view in self.views.items():
            view.load()
        self.changeTabScene("Assets")

        self.scrLay = cmds.scrollLayout( self.scrLay, e=True, rc=Callback(self.resizeView))
        cmds.formLayout(self.layout, edit=True,
                        attachForm=[(self.scrLay, 'top', -2),(self.scrLay, 'bottom', -2),(self.scrLay, 'left', -2), (self.scrLay, 'right', -2)])

        
        # self.views["version"].reload()
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

        for key, view in self.views.items():
            view.setParent(self.horizontalFrame)

        af = []
        ap = []
        ac = []
        an = [] 
        for key, view in self.views.items():
            af += view.pins.form
            ap += view.pins.position
            ac += view.pins.controller
            an += view.pins.none

        cmds.formLayout(self.verticalFrame, edit=True, vis=False)
        cmds.formLayout(self.horizontalFrame, edit=True, vis=True,
                        attachForm=af,
                        attachPosition=ap,
                        attachControl=ac,
                        attachNone=an)

    def setViewToVertical(self):
        if len(self.views) == 0:
            return
        self.views["project"].attach(top=Attach.FORM, bottom=(Attach.NONE), left=Attach.FORM, right=Attach.FORM, margin=(5,5,2,5))
        self.views["explorer"].attach(top=(Attach.CTRL, self.views["project"]), bottom=(Attach.POS, 55), left=Attach.FORM, right=Attach.FORM, margin=(5,5,2,5))
        self.views["detail"].attach(top=(Attach.CTRL, self.views["explorer"]), bottom=Attach.NONE, left=Attach.FORM, right=Attach.FORM, margin=(5,5,2,5))
        self.views["version"].attach(top=(Attach.CTRL, self.views["detail"]),bottom=(Attach.POS, 80), left=Attach.FORM, right=Attach.FORM, margin=(5,5,2,5))
        self.views["sync"].attach(top=(Attach.CTRL, self.views["version"]), bottom=Attach.NONE, left=Attach.FORM, right=Attach.FORM, margin=(5,5,2,5))
        self.views["versInfo"].attach(top=(Attach.CTRL, self.views["sync"]), bottom=Attach.NONE, left=Attach.FORM, right=Attach.FORM, margin=(5,5,2,5))
        self.views["wip"].attach(top=(Attach.CTRL, self.views["versInfo"]), bottom=Attach.NONE, left=Attach.FORM, right=Attach.FORM, margin=(5,5,2,5))
        self.views["import"].attach(top=(Attach.CTRL, self.views["wip"]), bottom=Attach.NONE, left=Attach.FORM, right=Attach.FORM, margin=(5,5,2,5))


        for key, view in self.views.items():
            view.setParent(self.verticalFrame)

        af = []
        ap = []
        ac = []
        an = [] 
        for key, view in self.views.items():
            af += view.pins.form
            ap += view.pins.position
            ac += view.pins.controller
            an += view.pins.none
        cmds.formLayout(self.horizontalFrame, edit=True, vis=False)
        cmds.formLayout(self.verticalFrame, edit=True, vis=True,
                        attachForm=af,
                        attachPosition=ap,
                        attachControl=ac,
                        attachNone=an)

    def commandProjectOption(self):
        pass

    def commandNewElem(self, name, cat):
        print(name, cat)

    def refreshAll(self):

        # if self.project is None:
        #     return
        # self.project.fetchAll()
        # self.project.setProject()
        # self.views["explorer"].setProject(self.project)
        # self.views["explorer"].refresh()
        self.refresh()

    def refresh(self):
        for key, view in self.views.items():
            view.refresh()


    def changeProject(self, p):
        if p == None:
            log.error("the project was not found")
            # cmds.error("Project do not exist")

            return
        self.project = p
        self.project.fetchAll()
        
        pathProject = os.path.join(self.project.path.local, self.project.name, "3_work", "maya")
        print(pathProject)
        if not os.path.isdir(pathProject):
            log.warning("Project folder not found")
        else:
            cmds.workspace(pathProject, o=True)
            cmds.workspace(dir=pathProject)

        self.views["explorer"].setProject(p)
        self.views["explorer"].refresh()
        # self.views["explorer"].reload()
        print(p.name)
        print(User().lastProj)
        User().lastProj = p.name
        User().prefs["lastProj"] = p.name
        print(User().lastProj)
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        User().writePrefs()

    def changeSelection(self, selection):
        log.debug(selection)
        self.lastSelected = self.selected
        self.selected = [selection[0]]
        if len(selection) == 1:
            self.views["detail"].changeScene(selection[0])
            self.views["version"].changeScene(selection[0])
            
            print(selection[0].__class__.__name__)

            if len(self.lastSelected) == 0 or self.selected[0].__class__ is not self.lastSelected[0].__class__:
                # if selection[0].__class__.__name__ == Asset.__name__:
                #     print("======Asset======")
                #     self.views["version"].changeStepBox(Asset._steps)
                # if selection[0].__class__.__name__ == Shot.__name__:
                #     print("======Shot=======")
                self.views["version"].changeStepBox(selection[0]._steps)
                    # self.views["version"].changeStepBox(["previs", "anim", "light"])

        self.views["detail"].refresh()
        self.views["version"].refresh()

    def changeVersion(self, selection):
        log.debug(selection)
        if len(selection) == 1:
            self.versSelected = [selection[0]]

    def changeTabScene(self, tab):
        return
        if tab == "Assets":
            self.views["version"].changeStepBox(Asset._steps)
        if tab == "Shots":
            # self.views["version"].changeStepBox(["previs", "anim", "light"])
            self.views["version"].changeStepBox(Shot._steps)

    def commandDownload(self):
        if len(self.selected) > 0 and len(self.versSelected) > 0:
            log.debug(self.versSelected[0].step)
            self.views["version"].refresh()

            self.versSelected[0].download()
            # if self.step == 4:
            #     self.selected[0].download()
            #     self.selected[0].state = 0
            # else:
            #     self.selected[0].downloadStep(self.step)
            #     self.selected[0].state = 2
        self.views["explorer"].refresh()
        #TODO remove the line below
        # self.views["explorer"].reload()
        self.views["detail"].changeScene(None)
        self.views["version"].changeScene(None)
        self.views["version"].loadTree()
        self.views["detail"].refresh()

    def commandOpen(self):
        if len(self.selected) > 0 and len(self.versSelected) > 0:
            v = self.versSelected[0]
            wip = v.getLastWip()
            if wip is not None:
                wipPath = os.path.join(v.path.local, v.getAbsolutePath(),"wip", wip)
                print(wipPath)
                if os.path.isfile(wipPath):
                    cmds.file( wipPath, o=True, f=True )
                    return
            pubPath = os.path.join(v.path.local, v.getAbsolutePath(), v.fileName + ".ma")
            print(pubPath)
            if os.path.isfile(pubPath):
                cmds.file( pubPath, o=True, f=True)
                return
            

    def commandPublish(self):
        if len(self.selected) > 0 and len(self.versSelected) > 0:
            log.debug("publish version " + str(self.versSelected[0].date))
            self.versSelected[0].publish()
            self.versSelected[0].setCurrent()
            self.versSelected[0].upload()
            self.views["version"].loadTree()
        pass

    def commandSaveVersion(self):
        if len(self.selected) > 0:
            log.debug("creating a new version")
            
            # self.nvWin = WindowUC("New version")
            # self.nvWin.ih = 100
            # self.nvWin.iw = 200
            # self.nvWin.load()

            newVersUC = NewVersion(self.selected[0])
            newVersUC.name = "New version"
            newVersUC.load()
            newVersUC.attach(top=Attach.FORM, bottom=Attach.FORM, left=Attach.FORM, right=Attach.FORM, margin=0)
            newVersUC.eventHandler("close", self.closeNewVersionWin)
            # self.nvWin.applyAttach()
            self.refresh()

            # self.selected[0].makeNewVersion(Scene._steps[1])
            self.selected[0].makeNewVersion(self.selected[0]._steps[1])
        pass
    
    def closeNewVersionWin(self):
        self.nvWin.close()

    def attachViewTo(self, layout, parent):
        cmds.formLayout(layout, e=True, parent=self.views[parent].layout)
        cmds.formLayout(self.views[parent], edit=True,
                        attachForm=[(layout, 'top', 5),(layout, 'bottom', 5),(layout, 'left', 5), (layout, 'right', 5)])


log.info("Cupboard Loaded")