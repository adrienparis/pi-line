import os

from .path import Path

class Item():
    _path = ""
    def __init__(self, name, parent):
        self.name = name
        self.parent = None
        self.childrens = []
        self.path = None
        self.setRelativePath()
        self.setParent(parent)
        self.onServer = False
        self.onLocal = False
        #optional
        self.image = ""
        self.author = ""
        self.date = ""
        
    def setRelativePath(self):
        self.relativePath = os.path.join(self._path, self.name)

    def addChildren(self, child):
        self.childrens.append(child)
        child.parent = self

    def removeChildren(self, child):
        self.childrens.remove(child)
        child.parent = None

    def setParent(self, parent):
        if parent is None:
            return
        if self.parent is not None:
            self.parent.removeChildren(self)
        parent.addChildren(self)
        self.path = self.parent.path

    def getAbsolutePath(self):
        if self.parent is not None:
            return os.path.join(self.parent.getAbsolutePath(), self.relativePath)
        return self.relativePath