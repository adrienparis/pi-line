import maya.cmds as cmds
from pymel.all import *

from .UC import *
from .treeUC import TreeUC
from .checkBoxGrpUC import CheckBoxGrpUC
from core.user import User
from core.scene import Scene
from core.asset import Asset
from core.shot import Shot

class VersionUC(UserControl):

    def __init__(self, parent):
        UserControl.__init__(self, parent)
        self.bgc = 0x202020
        self.scene = None
        self.versions = []

    def load(self):
        if self.layout is None or not cmds.formLayout(self.layout, q=True, exists=True):
            self.layout = cmds.formLayout('VersionUC', parent=self.parentLay)
        
        if self.scene is not None:
            self.stepLay = CheckBoxGrpUC(self)
            steps = self.scene._steps[:]

            for step in self.scene._steps:
                self.stepLay.addItem(step)

            self.stepLay.load()
            self.stepLay.eventHandler("changeState", self.chkBxChange)

            self.listVersion = TreeUC(self)
            self.listVersion.load()
            self.listVersion.eventHandler("changeSelection", self._changeSelectedVersions)

            self.scene.fetchVersions()

            self.loadTree()
            # self.listVersion.refresh()
            # self.rc = cmds.radioCollection(parent=self.layout)

            # user = User()
            # 1:mod     2:rig   3:surf
            # self.cat = (user.profil == "MODELER") * 1 + (user.profil == "RIGGER") * 2 + (user.profil == "ANIMATOR") * 2 + (user.profil == "SURFACER") * 3
            # cmds.radioButton( parent=self.plop, label='mod', align='left', onc=Callback(self.runEvent, "changeRadioButton", 1), sl=(self.cat==1))
            # cmds.radioButton( parent=self.plop, label='rig', align='center', onc=Callback(self.runEvent, "changeRadioButton", 2), sl=(self.cat==2))
            # cmds.radioButton( parent=self.plop, label='surf', align='right', onc=Callback(self.runEvent, "changeRadioButton", 3), sl=(self.cat==3))
            # cmds.radioButton( parent=self.plop, label='All', align='right', onc=Callback(self.runEvent, "changeRadioButton", 4), sl=(self.cat==4))
            # self.eventHandler("changeRadioButton", self.changeCategory)
            # self.runEvent("changeRadioButton", self.cat)
            self.stepLay.attach(top=Attach.FORM, bottom=Attach.NONE, left=Attach.FORM, right=Attach.FORM, margin=5)
            self.listVersion.attach(top=(Attach.CTRL, self.stepLay), bottom=Attach.FORM, left=Attach.FORM, right=Attach.FORM, margin=5)

        self.applyAttach()
    
    def loadTree(self):
        self.listVersion.deleteAllItemsFolders()
        for v in self.versions:
            if v.infoName is not None:
                name = v.infoName
            else:
                name = v.fileName
            image = "denied"
            if v.onServer and v.onLocal:
                image = "check"
            elif not v.onServer and v.onLocal:
                image = "upload"
            elif v.onServer and not v.onLocal:
                image = "download"

            self.listVersion.addItem(name, v, image=image, info=v.date)
            print(name, v, image, v.date)
        self.listVersion.load()


    def chkBxChange(self, chkBxs):
        print(chkBxs)
        l = [x for x in chkBxs if chkBxs[x]]
        self.versions = self.scene.getVersionBy(l)
        print(len(self.versions))
        self.loadTree()

    def _changeSelectedVersions(self, selection):
        self.runEvent("changeItem", selection)

    def changeScene(self, scene):
        self.scene = scene
