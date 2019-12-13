import maya.cmds as cmds
from pymel.all import *

import log
from .UC import *

class ImportUC(UserControl):
    def load(self):
        # self.layout = cmds.formLayout('ImportUC', parent=self.parentLay, w=130)
        self.pubLay = cmds.formLayout('pubLay', parent=self.layout, bgc=hexToRGB(0x373737))
        self.impLay = cmds.formLayout('impLay', parent=self.layout, bgc=hexToRGB(0x373737))
        self.publishBtn = cmds.button(parent=self.pubLay, label="Publish", c=Callback(self.runEvent, "publish"), bgc=hexToRGB(0x5d5d5d))
        self.OpenBtn = cmds.button(parent=self.pubLay, label="Open", c=Callback(self.runEvent, "open"), bgc=hexToRGB(0x5d5d5d))
        self.SaVeBtn = cmds.button(parent=self.pubLay, label="Save Version", c=Callback(self.runEvent, "saveVersion"), bgc=hexToRGB(0x5d5d5d))
        self.impRawBtn = cmds.button(parent=self.impLay, label="Import", c=Callback(self.runEvent, "importRaw"), bgc=hexToRGB(0x5d5d5d))
        self.impRefBtn = cmds.button(parent=self.impLay, label="Ref", c=Callback(self.runEvent, "importRef"), bgc=hexToRGB(0x5d5d5d))
        self.impProBtn = cmds.button(parent=self.impLay, label="Proxy", c=Callback(self.runEvent, "importProxy"), bgc=hexToRGB(0x5d5d5d))
        cmds.formLayout(self.pubLay, e=True,
                        attachForm=[(self.publishBtn, 'top', 4), (self.publishBtn, 'bottom', 4), (self.publishBtn, 'right', 4),
                                    (self.OpenBtn, 'top', 4), (self.OpenBtn, 'bottom', 4), (self.OpenBtn, 'left', 4),
                                    (self.SaVeBtn, 'top', 4), (self.SaVeBtn, 'bottom', 4)],
                        attachPosition=[(self.publishBtn, 'left', 2, 69), (self.OpenBtn, 'right', 2, 25),
                                        (self.SaVeBtn, 'left', 2, 25), (self.SaVeBtn, 'right', 2, 69)])
        cmds.formLayout(self.impLay, e=True,
                        attachForm=[(self.impRawBtn, 'top', 4), (self.impRawBtn, 'bottom', 4), (self.impRawBtn, 'left', 4),
                                    (self.impRefBtn, 'top', 4), (self.impRefBtn, 'bottom', 4),
                                    (self.impProBtn, 'top', 4), (self.impProBtn, 'bottom', 4), (self.impProBtn, 'right', 4)],
                        attachPosition=[(self.impProBtn, 'left', 2, 66), (self.impRawBtn, 'right', 2, 40), 
                                    (self.impRefBtn, 'right', 2, 66), (self.impRefBtn, 'left', 2, 40)])



        cmds.formLayout(self.layout, e=True,
                        attachForm=[
                                    (self.pubLay, 'bottom', 5),  (self.pubLay, 'left', 5), (self.pubLay, 'right', 5),
                                    (self.impLay, 'top', 5), (self.impLay, 'left', 5), (self.impLay, 'right', 5)],
                        attachControl=[(self.impLay, 'bottom', 5, self.pubLay)],
                        attachNone=[(self.pubLay, 'top')])
