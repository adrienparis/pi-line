import maya.cmds as cmds
from pymel.all import *

import log
from .UC import *
from .treeUC import TreeUC
from core.user import User

class CheckBoxGrpUC(UserControl):

    def __init__(self, parent):
        UserControl.__init__(self, parent)
        self.items = {}

    def load(self):
        if self.layout is None or not cmds.formLayout(self.layout, q=True, exists=True):
            self.layout = cmds.formLayout(parent=self.parentLay)
        log.debug(self.parentLay)
        for i in self.items:
            if "box" in self.items[i] and cmds.checkBox(self.items[i]["box"], q=True, exist=True):
                cmds.deleteUI(lay)

        af = []
        ac = []
        an = []
        prev = None
        for i in self.items:
            c = cmds.checkBox( parent=self.layout, label=i, value=self.items[i]["value"], onc=Callback(self._changeState, True, i), ofc=Callback(self._changeState, False, i))
            self.items[i]["box"] = c
            af.append((c, "top", 5))
            an.append((c, "bottom"))
            an.append((c, "right"))
            if prev is None:
                af.append((c, "left", 5))
            else:
                ac.append((c, "left", 5, prev))
            prev = c
        cmds.formLayout(self.layout, e=True, af=af, an=an, ac=ac)



        pass

    def clearItems(self):
        for i in self.items:
            if "box" in self.items[i]:
                log.debug("delete " + self.items[i]["box"])
                cmds.deleteUI(self.items[i]["box"], ctl=True)
        self.items.clear()
        pass

    def addItem(self, item, value=False):
        self.items[item] = {}
        self.items[item]["value"] = value

    def modifyItem(self, item, value):
        self.items[item]["value"] = value

    def refresh(self):
        if self.layout is None or not cmds.formLayout(self.layout, q=True, exists=True):
            return
        for i in self.items:
            cmds.checkBox(self.items[i]["box"], e=True, label=i, value=self.items[i]["value"])

    def getListValue(self):
        l = {}
        for i in self.items:
            l[i] = self.items[i]["value"]
        return l
    
    def _changeState(self, value, elem):
        self.items[elem]["value"] = value
        self.runEvent("changeState", self.getListValue())
