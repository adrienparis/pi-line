import datetime

import maya.cmds as cmds
from pymel.all import *

import log
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
        # self.bgc = 0x202020
        self.scene = None
        self.versions = []
        self.listVersion = None
        self.stepLay = None
        self.selectSteps = []

    def load(self):
        # if self.layout is None or not cmds.formLayout(self.layout, q=True, exists=True):
        #     self.layout = cmds.formLayout('VersionUC', parent=self.parentLay)
        # print(self.layout)
        if self.stepLay is None:
            self.stepLay = CheckBoxGrpUC(self)
        print(self.stepLay.parentUC)
        self.stepLay.heigt = 30
        self.stepLay.width = 30
        self.stepLay.load()
        if self.listVersion is None:
            self.listVersion = TreeUC(self)
            self.listVersion.addable = False

        if self.scene is not None:
            steps = self.scene._steps[:]
            self.scene.fetchVersions()
        else:
            steps = []

        for step in steps:
            self.stepLay.addItem(step)


        self.stepLay.eventHandler("changeState", self.chkBxChange)
        self.listVersion.eventHandler("changeSelection", self._changeSelectedVersions)


        self.loadTree()

        cmds.formLayout(self.layout, e=True, bgc=hexToRGB(0x808080))

        self.stepLay.attach(top=Attach.FORM, bottom=Attach.NONE, left=Attach.FORM, right=Attach.FORM, margin=5)
        self.listVersion.attach(top=(Attach.CTRL, self.stepLay), bottom=Attach.FORM, left=Attach.FORM, right=Attach.FORM, margin=5)

        self.applyAttach()
    
    def displayTimeToSimpleStr(self, time):

            dLag = datetime.datetime.now() - time
            now = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
            
            p = now - datetime.timedelta(hours = 1)
            if p < time:
                d = str((dLag.seconds//60)%60 ) + "min ago"
            else:
                d = time.strftime('%Hh%M')
            p = p.replace(hour=0)
            if p >= time:
                d = time.strftime('Yesterday - %Hh%M')
            if p - datetime.timedelta(days=1) >= time:
                d = time.strftime('%A - %Hh%M')
            if p - datetime.timedelta(days=6) >= time:
                d = time.strftime('%m/%d - %Hh')
            if p - datetime.timedelta(days=20) >= time:
                d = time.strftime('%Y/%m/%d')
            return d


    def loadTree(self):
        print("load version list")
        # print(self.listVersion)
        if self.listVersion is None:
            return
        self.listVersion.deleteAllItemsFolders()
        print(self.versions)
        for v in self.versions:
            print(v.name)
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

            d = self.displayTimeToSimpleStr(v.date)

            self.listVersion.addItem(name, v, image=image, info=d)
        self.listVersion.load()

    def changeStepBox(self, bxs):

        if self.stepLay is None:
            return
        print(bxs)
        self.stepLay.clearItems()
        for step in bxs:
            self.stepLay.addItem(step)
        self.stepLay.load()
        print("stepbox change")

    def refresh(self):
        if self.listVersion is not None:
            self.listVersion.load()


    def chkBxChange(self, chkBxs):
        self.selectSteps = [x for x in chkBxs if chkBxs[x]]
        if self.scene is None:
            return
        self.versions = self.scene.getVersionBy(self.selectSteps)
        self.loadTree()

    def _changeSelectedVersions(self, selection):
        self.runEvent("changeItem", selection)

    def changeScene(self, scene):
        self.versions = []
        self.scene = scene
        if self.scene is None:
            self.versions = []
        else:    
            self.versions = self.scene.getVersionBy(self.selectSteps)
