import maya.cmds as cmds

import log
from .UC import *
from .buttonsUC import *

class VersInfonUC(UserControl):

    def load(self):
        self.b = TextButtonUC(self, text="screenShot")
        self.b.eventHandler("click", self.runEvent, "clickScreenShot")
