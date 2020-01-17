import maya.cmds as cmds

import log
from .UC import *
from .buttonsUC import *

class newItemUC(UserControl):
    def __init__(self, title):
        UserControl.__init__(self, None)
        self.name = title
        self.initWidth = 200
        self.initHeight = 50

    def load(self):
        lab = TextLabelUC(self, text="Name : ")
        self.field = TextFieldUC(self)
        butOK = TextButtonUC(self, text="OK")
        butCan = TextButtonUC(self, text="Cancel")
        butOK.eventHandler("click", self.click, True)
        butCan.eventHandler("click", self.click, False)
        lab.attach(top=Attach.FORM, bottom=Attach.NONE, left=Attach.FORM, right=Attach.NONE, margin=5)
        self.field.attach(top=(Attach.CTRL, lab), bottom=Attach.NONE, left=Attach.FORM, right=Attach.FORM, margin=5)
        butOK.attach(top=Attach.NONE, bottom=Attach.FORM, left=Attach.NONE, right=Attach.FORM, margin=5)
        butCan.attach(top=Attach.NONE, bottom=Attach.FORM, left=Attach.NONE, right=(Attach.CTRL, butOK), margin=5)
        
        for c in self.childrens:
            print(c.__class__.__name__)
            c.load()
        if len(self.childrens) == 0:
            return
        af = []
        ap = []
        ac = []
        an = []

        for ch in self.childrens:
            af += ch.pins.form
            ap += ch.pins.position
            ac += ch.pins.controller
            an += ch.pins.none
        print(af)
        print(ap)
        print(ac)
        print(an)

    def click(self, button):
        if button:
            self.runEvent("clickOK", self.field.text)
        self.killSelf()

class newVersionUC(UserControl):
    def load(self):
        TextButtonUC(self, text="New")
        TextButtonUC(self, text="Cancel")
