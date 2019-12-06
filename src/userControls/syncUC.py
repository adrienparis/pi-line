import maya.cmds as cmds
from pymel.all import *
from UC import *

class SyncUC(UserControl):
    def create(self):
        self.layout = cmds.formLayout('syncUC', parent=self.parentLay, w=200)
        self.downloadButton = cmds.button(label="Download", parent=self.layout, c=Callback(self.runEvent, "download"), bgc=hexToRGB(0x5d5d5d))
        self.deleteButton = cmds.button(label="Delete", parent=self.layout, c=Callback(self.runEvent, "delete"), bgc=hexToRGB(0x5d5d5d))
        cmds.formLayout(self.layout, e=True, attachForm=[(self.downloadButton, 'top', 5), (self.downloadButton, 'bottom', 5),  (self.downloadButton, 'left', 5),
                                                         (self.deleteButton, 'top', 5), (self.deleteButton, 'bottom', 5), (self.deleteButton, 'right', 5)],
                                             attachPosition=[(self.deleteButton, 'left', 5, 50), (self.downloadButton, 'right', 5, 50)])
