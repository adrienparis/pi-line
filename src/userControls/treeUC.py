from pymel.all import *
import maya.cmds as cmds

import log
from .UC import *
from .lineUC import *

class TreeUC(UserControl):
    class _item():
        def __init__(self, name, elem, image=None, info=""):
            self.name = name
            self.elem = elem
            self.image = image
            self.info = info
            self.deep = 0
            self.parent = None
            self.line = None
            self.selected = False
            
        def setParent(self, parent):
            if self.parent is not None:
                self.parent.removeChildren(self)
            parent.addChildren(self)


    class _folder(_item):
        def __init__(self, name, elem):
            TreeUC._item.__init__(self, name, elem)
            self.childrens = []
            self.image = "arrowBottom"
            self.isDeployed = True
            self.area = None

        def deploying(self, val):
            self.isDeployed = val
            if val:
                self.image = "arrowBottom"
            else:
                self.image = "arrowRight"
            self.line.icon = self.image
            self.line.refresh()
            cmds.formLayout(self.area, e=True, vis=self.isDeployed)

        def deployingAll(self, val):
            self.deploying(val)
            for f in self.childrens:
                if f.__class__ is TreeUC._folder:
                    TreeUC._folder.deployingAll(f, val)


        def addChildren(self, child):
            self.childrens.append(child)
            child.parent = self

        def removeChildren(self, child):
            self.childrens.remove(child)
            child.parent = None
        
        def getAllParent(self):
            if self.parent is None:
                return "/"
            return self.getAllParent() + "/" + self.name

    
    def __init__(self, parent, multiSelect=True):
        UserControl.__init__(self, parent)
        self.name = "Tree" + self.name
        self.root = TreeUC._folder(".", None)
        self.folders = {}
        self.items = {}
        self.selecteds = []
        self.multiSelect = multiSelect
        # self.layout = ""
        self.scrlLay = ""

    
    def _loadFolder(self, fold, parent):
        elems = []
        layout = cmds.formLayout(fold.name + "_layout", parent=parent, bgc=hexToRGB(0x202020 * (fold.deep % 2) + self.color.background), vis=(fold.isDeployed or fold.deep < 1))
        for elem in fold.childrens:
            elem.line = LineUC(layout, elem.name, info=elem.info, icon=elem.image)
            elem.line.load()
            elems.append(elem.line.layout)
            # l.attach(top=(Attach.CTRL, pl), bottom=Attach.NONE, left=(Attach.POS, 15), right=Attach.FORM)
            if elem.__class__ is TreeUC._folder:
                elems.append(self._loadFolder(elem, layout))
                elem.area = elems[-1]
                elem.line.eventHandler("click", self._clickFolder, elem)
            else:
                elem.line.eventHandler("click", self._clickItem, elem)

        af = []
        an = []
        ac = []
        ap = []

        last = None
        for e in elems:
            if last is None:
                af.append((e, "top", 0))
            else:
                ac.append((e, "top", 0, last))
            an.append((e, "bottom"))
            if fold is self.root:
                af.append((e, "left", 0))
            else:
                ap.append((e, "left", 0, 5))
            af.append((e, 'right', 0))
            last = e

        cmds.formLayout(layout, edit=True, attachForm=af,
                                            attachPosition=ap,
                                            attachControl=ac,
                                            attachNone=an)
        return layout

    def load(self):
        # if not cmds.formLayout(self.layout, q=True, ex=True):
        #     self.layout = cmds.formLayout(parent=self.parentLay)
        

        if cmds.scrollLayout(self.scrlLay, q=True, ex=True):
            cmds.deleteUI(self.scrlLay)
        self.scrlLay = cmds.scrollLayout(parent=self.layout, childResizable=True)
        t = self._loadFolder(self.root, self.scrlLay)
        
        cmds.formLayout(self.layout, edit=True, attachForm=[(self.scrlLay, 'top', -2),(self.scrlLay, 'bottom', -2),(self.scrlLay, 'left', -2), (self.scrlLay, 'right', -2)])

    def _clickFolder(self, folder, line, mod):
        if mod == 0:
            folder.deploying(not folder.isDeployed)
        elif mod == 1:
            folder.deployingAll(not folder.isDeployed)


    def _clickItem(self, item, line, mod):
        
        for t in self.selecteds:
            if (mod != 1 or item.parent != t.parent or not self.multiSelect):
                t.line.selection(False)
        if mod != 1:
            self.selecteds = []
        if mod <= 1:
            if line.selected:
                line.selection(False)
                self.selecteds.remove(item)
            else:
                line.selection(True)
                self.selecteds.append(item)
        selection = [x.elem for x in self.selecteds if x.line.selected]
        self.runEvent("changeSelection", selection)

    def deleteAllItemsFolders(self):
        self.folders = {}
        self.items = {}
        self.root = TreeUC._folder(".", None)

    def addFolder(self, name, elem, parent=None):
        f = TreeUC._folder(name, elem)

        if parent is None:
            f.setParent(self.root)
            f.deep = 1
        else:
            f.setParent(parent)
            f.deep = f.parent.deep + 1
        self.folders[elem] = f
        return f
    
    def addItem(self, name, elem, parent=None, image=None, info=""):
        i = TreeUC._item(name, elem, image=image, info=info)

        if parent is None:
            i.setParent(self.root)
        else:
            i.setParent(parent)
            i.deep = i.parent.deep + 1
        self.items[elem] = i
        return i
        
    def select(self, selection, value):
        '''display the lines in selection as selected in the tree
        selection: the lines to be select
        value: True to select
        '''
        pass