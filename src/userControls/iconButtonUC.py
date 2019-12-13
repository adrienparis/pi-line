import maya.cmds as cmds

import log
from .UC import *

class IconButtonUC(UserControl):
    def __init__(self):
        UserControl.__init__(self)
    def load(self):
        self.button = cmds.iconTextButton('btnSetServerPath', parent=self.layout, style='iconOnly', image1=getIcon("folder"), label='Switch view', w=22, h=22, sic=True, bgc=[0.45,0.45,0.45])

