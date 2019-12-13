import maya.cmds as cmds

from .UC import *

class DetailUC(UserControl):
    scene = None
    def __init__(self, parent):
        UserControl.__init__(self, parent)
        # self.bgc = 0x0000ff
    def load(self):
        self.name = cmds.text('name', label='Empty', font="boldLabelFont", align="left", rs=False, ann="char")
        self.shotUses = cmds.text('shotUses', label='Apparition :  shots', align="left")
        cmds.formLayout(self.layout, e=True, attachForm=[(self.name, 'top', 0), (self.name, 'left', 0), (self.name, 'right', 0), (self.shotUses, 'left', 0), (self.shotUses, 'right', 0)], attachControl=[(self.shotUses, 'top', 0, self.name)])
    def changeScene(self, scene):
        self.scene = scene
    
    def refresh(self):
        if self.scene == None:
            return
        cmds.text(self.name, e=True, label=self.scene.name.capitalize() , ann=self.scene.category)
        cmds.text(self.shotUses, e=True, label="Apparition : " + str(self.scene.shotUses) + " shots")
