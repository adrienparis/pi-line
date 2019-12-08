import maya.cmds as cmds
from pymel.all import *

from .UC import UserControl
from core.user import User

class VersionUC(UserControl):
    def create(self):
        self.layout = cmds.formLayout('VersionUC', parent=self.parentLay)
        
        self.plop = cmds.columnLayout( adjustableColumn=True )
        self.rc = cmds.radioCollection(parent=self.layout)
        user = User()
        # 1:mod     2:rig   3:surf
        self.cat = (user.profil == "MODELER") * 1 + (user.profil == "RIGGER") * 2 + (user.profil == "ANIMATOR") * 2 + (user.profil == "SURFACER") * 3
        cmds.radioButton( parent=self.plop, label='mod', align='left', onc=Callback(self.runEvent, "changeRadioButton", 1), sl=(self.cat==1))
        cmds.radioButton( parent=self.plop, label='rig', align='center', onc=Callback(self.runEvent, "changeRadioButton", 2), sl=(self.cat==2))
        cmds.radioButton( parent=self.plop, label='surf', align='right', onc=Callback(self.runEvent, "changeRadioButton", 3), sl=(self.cat==3))
        cmds.radioButton( parent=self.plop, label='All', align='right', onc=Callback(self.runEvent, "changeRadioButton", 4), sl=(self.cat==4))
        self.eventHandler("changeRadioButton", self.changeCategory)
        self.runEvent("changeRadioButton", self.cat)
        
    def changeCategory(self, cat):
        self.cat = cat
        self.runEvent("changeItem", self.cat)

