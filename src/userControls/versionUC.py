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
        # if self.stepLay is None:
        self.stepLay = CheckBoxGrpUC(self)
        self.stepLay.heigt = 30
        self.stepLay.width = 30
        # if self.listVersion is None:
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


        self.stepLay.load()
        self.loadTree()

        cmds.formLayout(self.layout, e=True, bgc=hexToRGB(0x808080))

        self.stepLay.attach(top=Attach.FORM, bottom=Attach.NONE, left=Attach.FORM, right=Attach.FORM, margin=5)
        self.listVersion.attach(top=(Attach.CTRL, self.stepLay), bottom=Attach.FORM, left=Attach.FORM, right=Attach.FORM, margin=5)

        # self.applyAttach()
    
    def refresh(self):
        self.listVersion.unload()
        self.loadTree()
        # self.stepLay.reload()

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

    def getStateIcon(self, v):
        ico = "denied"
        print(v.onServer, v.onLocal)
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

    def loadTree(self):
        if self.listVersion is None:
            return
        self.listVersion.deleteAllItemsFolders()

        for v in self.versions:
            if v.infoName is not None:
                name = v.infoName
            else:
                name = v.fileName
            icon = self.getStateIcon(v)

            d = self.displayTimeToSimpleStr(v.date)
            self.listVersion.addItem(name, v, icon=icon, info=d)
        self.listVersion.reload()

    def changeStepBox(self, bxs):

        if self.stepLay is None:
            return
        print(bxs)
        self.stepLay.clearItems()
        for step in bxs:
            self.stepLay.addItem(step)
        self.stepLay.reload()
        print("stepbox change")

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
