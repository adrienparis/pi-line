import maya.cmds as cmds
from pymel.all import *
from UC import *

class DetailUC(UserControl):
    asset = None
    def create(self):
        self.layout = cmds.formLayout('detailUC', parent=self.parentLay)
        self.name = cmds.text('name', label='Empty', font="boldLabelFont", align="left", rs=False, ann="char")
        self.shotUses = cmds.text('shotUses', label='Apparition :  shots', align="left")
        cmds.formLayout(self.layout, e=True, attachForm=[(self.name, 'top', 0), (self.name, 'left', 0), (self.name, 'right', 0), (self.shotUses, 'left', 0), (self.shotUses, 'right', 0)], attachControl=[(self.shotUses, 'top', 0, self.name)])
    def changeAsset(self, asset):
        self.asset = asset
    
    def refresh(self):
        if self.asset == None:
            return
        cmds.text(self.name, e=True, label=self.asset.name.capitalize() , ann=self.asset.category.name)
        cmds.text(self.shotUses, e=True, label="Apparition : " + str(self.asset.shotUses) + " shots")
