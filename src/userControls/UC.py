import os
from pymel.all import *
import maya.cmds as cmds

class Attach():
    NONE = 0
    FORM = 1
    POS = 2
    CTRL = 3

def getIcon(icon):
    if icon is not None:
        img = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, "logo", icon + ".png")
        if os.path.isfile(img):
            return img
    img = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, "logo",  "noPicture.png")
    if os.path.isfile(img):
        return img

def hexToRGB(hexa):
    """
    :hexa:
    """
    rgb = []
    rgb.append((round(hexa / 0x10000) % 0x100) / 0x100)
    rgb.append((round(hexa / 0x100) % 0x100) / 0x100)
    rgb.append(float(hexa % 0x100) / 0x100)
    return rgb

class UserControl(object):
    """ 
    Creating a userControl
    """

    def __init__(self, parent):
        """Initialize
        
        :parent: str formlayout
        """
        self.parentUC = None
        self.parentLay = None
        self.layout = None
        self.setParent(parent)
        self.childrens = []
        self.command = {}
        self.name = "UC"


    
    def create(self):
        self.layout = cmds.formLayout(parent=self.parentLay, bgc=hexToRGB(0xa00000), h=30, w=30)
        print("create userControl : " + self.__class__.__name__)
        print("/!\\ Not implemented")

    def load(self):
        self.create()
    @staticmethod
    def __sideToValue(side):
        if side == "top" : return 0
        if side == "bottom" : return 1
        if side == "left" : return 2
        if side == "right" : return 3


    def visibility(self, vis):
        """Set the vibility of the UserControl

        :vis: boolean True=Visible False=Invisible
        """
        cmds.formLayout(self.layout, e=True, vis=vis)

    # Attach.NONE, Attach.FORM, (Attach.POS, pos), (Attach.CTRL, ctrl), margin
    def attach(self, margin=(0), **kwargs):
        """Attach the form to his parent

        Use Attach.NONE or Attach.FORM or (Attach.POS, [pos]) or (Attach.CTRL, [ctrl]) where [pos] is an Int and [ctrl] is a UserControl or a layout to the followings arguments

        :top:
        :bottom:
        :left:
        :right:

        :margin: 0 or (0,0) or (0,0,0,0) -> all or (top, bottom) or (top, bottom, left, right)
        """
        #check if margin is (0), (0,0) or (0,0,0,0)
        side = [0,0,0,0]
        if type(margin) is int:
            side = [margin, margin, margin, margin]
        if type(margin) is tuple and len(margin) == 2:
            side = [margin[0], margin[0], margin[1], margin[1]]
        if type(margin) is tuple and len(margin) == 4:
            side = [margin[0], margin[1], margin[2], margin[3]]

        self.an = []
        self.af = []
        self.ap = []
        self.ac = []

        for key, value in kwargs.items():
            if type(value) is int:
                if value == Attach.NONE:
                    self.an.append((self.layout, key))
                if value == Attach.FORM:
                    self.af.append((self.layout, key, side[UserControl.__sideToValue(str(key))]))
            elif type(value) is tuple and len(value) == 2:
                if value[0] == Attach.POS:
                    self.ap.append((self.layout, key, side[UserControl.__sideToValue(str(key))], value[1]))
                if value[0] == Attach.CTRL:
                    if type(value[1]) is str or type(parent) is unicode:
                        self.ac.append((self.layout, key, side[UserControl.__sideToValue(str(key))], value[1]))
                    else:
                        try:
                            self.ac.append((self.layout, key, side[UserControl.__sideToValue(str(key))], value[1].layout))
                        except AttributeError:
                            print(value[1] + "is not supported")

    def applyAttach(self):
        af = []
        ap = []
        ac = []
        an = []

        for ch in self.childrens:
            af += ch.af
            ap += ch.ap
            ac += ch.ac
            an += ch.an

        cmds.formLayout(self.layout, edit=True,
                        attachForm=af,
                        attachPosition=ap,
                        attachControl=ac,
                        attachNone=an)


    def setParent(self, parent):

        if parent is None:
            self.parentLay = parent
            self.parentUC = parent
        elif type(parent) is str or type(parent) is unicode:
            self.parentLay = parent
        else:
            try:
                if self.parentUC is not None:
                    self.parentUC.delChildren(self)
                self.parentUC = parent
                self.parentLay = parent.layout
                self.parentUC.addChildren(self)
            except:
                print(parent + " is unreadable")
        if self.layout is not None and self.parentLay is not None:
            cmds.formLayout(self.layout, edit=True, parent=self.parentLay)


    def addChildren(self, child):
        self.childrens.append(child)
    def delChildren(self, child):
        self.childrens.remove(child)

    def reload(self):
        print("reload " + self.__class__.__name__)
        print("/!\\ Not implemented")
    def refresh(self):
        print("refresh " + self.__class__.__name__)
        print("/!\\ Not implemented")
    def eventHandler(self, event, c, *args):
        if not event in self.command:
            self.command[event] = []
        self.command[event].append((c, args))
    def runEvent(self, event, *args):
        if not event in self.command:
            return
        for c in self.command[event]:
            if c[0] is None:
                # cmds.error("Event \"" + event + "\" call a function not implemented yet -WIP-")
                print("Event \"" + event + "\" call a function not implemented yet -WIP-")
                continue
            a = c[1] + args
            c[0](*a)

    def __str__(self):
        return self.layout

print("UC Loaded")