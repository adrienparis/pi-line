import os

from .path import Path

class Item():
    def __init__(self, name, parent):
        self.name = name
        self.parent = None
        self.childrens = []
        if parent is not None:
            self.setParent(parent)
            self.path = self.parent.path
            self.relativePath = os.path.join(self.parent.relativePath)
        else:
            self.path = Path()
            self.relativePath = self.name
        self.onServer = False
        self.onLocal = False
        #optional
        self.image = ""
        self.author = ""
        self.date = ""
        


    def addChildren(self, child):
        self.childrens.append(child)
        child.parent = self

    def removeChildren(self, child):
        self.childrens.remove(child)
        child.parent = None

    def setParent(self, parent):
        if self.parent is not None:
            self.parent.removeChildren(self)
        parent.addChildren(self)