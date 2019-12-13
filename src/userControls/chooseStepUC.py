import datetime

import maya.cmds as cmds
from pymel.all import *

import log
from .UC import *

class ChooseStepUC(UserControl):

    def __init__(self, parent):
        UserControl.__init__(self, parent)
        # self.bgc = 0xa5cc59