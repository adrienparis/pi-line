import maya.cmds as cmds
from pymel.all import *

from .UC import *

class TileUC(UserControl):

    baseColor = [0.4,0.4,0.4]
    selectedColor = [0.32,0.52,0.65]
    selected = False
    function = None
    style = 'iconAndTextVertical'

    def __init__(self, asset, parent, sizeImage=100):
        UserControl.__init__(self, parent)
        self.asset = asset
        self.sizeImage = sizeImage
        self.name = asset.name + "Tile" + self.name

    def create(self):
        self.layout = cmds.formLayout(parent=self.parentLay, h=30)
        self.btnLay = cmds.iconTextButton(self.asset.name + "Tile", parent=self.layout, style=self.style, image1=self.asset.image,
                            label=self.asset.name, w=self.sizeImage, h=self.sizeImage, sic=True, c=Callback(self.clickCommand), bgc=self.selectedColor, ebg=self.selected)
        img = "denied"
        if self.asset.state == 0:        
            img = "check"
        if self.asset.state == 1:        
            img = "download"
        if self.asset.state == 2:        
            img = "upload"


        self.iconLay = cmds.image(parent=self.layout, image=getIcon(img), bgc=hexToRGB(0x1d1d1d))
        cmds.formLayout(self.layout, edit=True,
                        attachForm=[(self.btnLay, "top", 2), (self.btnLay, "bottom", 2), (self.btnLay, "left", 2), (self.btnLay, "right", 2), 
                                    (self.iconLay, "top", 5), (self.iconLay, "right", 5)],
                        attachNone=[(self.iconLay, "left"), (self.iconLay, "bottom")])

    def selection(self, b):
        self.selected = b
        cmds.iconTextButton(self.btnLay, e=True, ebg=self.selected)

    def clickCommand(self):
        self.mods = cmds.getModifiers()
        self.runEvent("click", self, self.mods)
