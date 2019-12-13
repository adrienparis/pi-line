import os
from pymel.all import *
import maya.cmds as cmds


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

class Attach(object):
    NONE = 0
    FORM = 1
    POS = 2
    CTRL = 3

    def __init__(self, parent):
        self.parent = parent
        self.margin = [0,0,0,0]
        self.none = 0
        self.form = 0
        self.position = 0
        self.controller = 0
        self._attachs = {}
        self._an = []
        self._af = []
        self._ap = []
        self._ac = []

    def __getattribute__(self,name):
        if name == 'none' or name == 'form' or name == 'position' or name == 'controller':
            self._createAttach()
            if name == 'none':
                # print("an", self._an)
                return object.__getattribute__(self, "_an")
            elif name == 'form':
                # print("af", self._af)
                return object.__getattribute__(self, "_af")
            elif name == 'position':
                # print("ap", self._ap)
                return object.__getattribute__(self, "_ap")
            elif name == 'controller':
                # print("ac", self._ac)
                return object.__getattribute__(self, "_ac")
        else:
            return object.__getattribute__(self, name)

    @staticmethod
    def __sideToValue(side):
        if side == "top" : return 0
        if side == "bottom" : return 1
        if side == "left" : return 2
        if side == "right" : return 3

    def _createAttach(self):
        self._an = []
        self._af = []
        self._ap = []
        self._ac = []
        for key, value in self._attachs.items():
            if type(value) is int:
                if value == Attach.NONE:
                    self._an.append((self.parent.layout, key))
                if value == Attach.FORM:
                    self._af.append((self.parent.layout, key, self.margin[Attach.__sideToValue(str(key))]))
            elif type(value) is tuple and len(value) == 2:
                if value[0] == Attach.POS:
                    self._ap.append((self.parent.layout, key, self.margin[Attach.__sideToValue(str(key))], value[1]))
                if value[0] == Attach.CTRL:
                    if type(value[1]) is str or type(value[1]) is unicode:
                        self._ac.append((self.parent.layout, key, self.margin[Attach.__sideToValue(str(key))], value[1]))
                    else:
                        try:
                            self._ac.append((self.parent.layout, key, self.margin[Attach.__sideToValue(str(key))], value[1].layout))
                        except AttributeError:
                            print(value[1] + "is not supported")

    def attach(self, margin, attachs):
        #check if margin is (0), (0,0) or (0,0,0,0)
        self.margin = [0,0,0,0]
        if type(margin) is int:
            self.margin = [margin, margin, margin, margin]
        if type(margin) is tuple and len(margin) == 2:
            self.margin = [margin[0], margin[0], margin[1], margin[1]]
        if type(margin) is tuple and len(margin) == 4:
            self.margin = [margin[0], margin[1], margin[2], margin[3]]
        self._attachs = attachs






class UserControl(object):
    """ 
    Creating a userControl
    """

    increment = 0

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
        self.bgc = 0xa00000
        self.width = 30
        self.height = 30
        self.initWidth = 30
        self.initHeight = 30
        self.loaded = False
        self.pins = Attach(self)


    
    def create(self):
        self._load()

    def load(self):
        print("/!\\ Not implemented")

    def _load(self):
        print("loading " + self.__class__.__name__ + "...")
        if not self.loaded:
            print("loading UC")
            if self.parentLay is None:
                print("parent layout doesnot exist")
                if cmds.workspaceControl(self.name, exists=1):
                    print("delete " + self.name)
                    cmds.deleteUI(self.name)
                self.parentLay = cmds.workspaceControl(self.name, retain=False, iw=self.initWidth, ih=self.initHeight, floating=True)
            self.layout = cmds.formLayout(self.__class__.__name__ + str(UserControl.increment) , parent=self.parentLay, bgc=hexToRGB(self.bgc), h=self.height, w=self.width)
            
            print("create layout " + self.__class__.__name__ + str(UserControl.increment))
            UserControl.increment += 1
            self.loaded = True
        else:
            print("Editing UC")
            cmds.formLayout(self.layout, e=True, parent=self.parentLay, bgc=hexToRGB(self.bgc), h=self.height, w=self.width)
        
        object.__getattribute__(self, "load")()
        
        self.applyAttach()


    def refresh(self):
        print("/!\\ Not implemented")

    def _refresh(self):
        print("refresh " + self.__class__.__name__ + "...")
        for c in self.childrens:
            c.refresh()
        object.__getattribute__(self, "refresh")
  
    def _unload(self):
        print("unload " + self.__class__.__name__ + "...")
        self.loaded = False
        for c in self.childrens:
            c.unload()
        if cmds.workspaceControl(self.name, exists=1):
            cmds.deleteUI(self.name)
        object.__getattribute__(self, "unload")

    def unload(self):
        print("/!\\ Not implemented")

    def reload(self):
        self.unload()
        self.load()


    def __getattribute__(self,name):
        # print(object.__getattribute__(self, "__class__").__name__ + "\t get attr : " + name)
        if name == 'load':
            return object.__getattribute__(self, "_load")
        elif name == 'refresh':
            return object.__getattribute__(self, "_refresh")
        elif name == 'unload':
            return object.__getattribute__(self, "_refresh")
        else:
            return object.__getattribute__(self, name)

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
        at = kwargs.items()
        keys = ["top", "bottom", "left", "right"]
        at = { k:v for k,v in at if k in keys }
        self.pins.attach(margin, at)


    def applyAttach(self):
        af = []
        ap = []
        ac = []
        an = []

        for ch in self.childrens:
            af += ch.pins.form
            ap += ch.pins.position
            ac += ch.pins.controller
            an += ch.pins.none

        print("~~~~~~~~~~~attach~~~~~~~~~")
        print(self.__class__.__name__)
        print(af)
        print(ap)
        print(ac)
        print(an)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~")

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