import maya.cmds as cmds
from pymel.all import *

import log

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

    def load(self):
        self.btnLay = cmds.iconTextButton(self.asset.name + "Tile", parent=self.layout, style=self.style, image1=getIcon(self.asset.image),
                            label=self.asset.name, w=self.sizeImage, h=self.sizeImage, sic=True, c=Callback(self.clickCommand), bgc=hexToRGB(self.color.highlight), ebg=self.selected)
        img = "denied"
        v = self.asset.getLastVersion()
        for x in self.asset.versions:
            log.debug(x.name + " " + x.fileName)
        if v is not None:
            log.debug(v.parent.name, v.name, v.onLocal, v.onServer, v.fileName)
            if v.onServer and v.onLocal:
                img = "check"
            elif v.onServer and not v.onLocal:
                img = "download"
            elif not v.onServer and v.onLocal:
                img = "upload"
        else:
            img = "new"

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
