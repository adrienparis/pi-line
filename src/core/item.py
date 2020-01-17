import os
import shutil

import log
from .path import *


def copyTree(src, dst, exception=[]):
    for f in os.listdir(src):
        fp = os.path.join(src, f)

        if fp.endswith(dst):
            continue
        if dst.startswith(fp):
            continue

        go = True
        for e in exception:
            e = e.replace("/", "\\")
            if fp.endswith(e):
                go = False
        if not go:
            continue
        dfp = os.path.join(dst, f)
        if os.path.isfile(fp):
            shutil.copyfile(fp, dfp)
        elif os.path.isdir(fp):
            if not os.path.isdir(dfp):
                os.mkdir(dfp)
            copyTree(fp, dfp, exception=exception)

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
        self.date = None
        
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

    def getRoot(self):
        if self.parent is not None:
            return self.parent.getRoot()
        return self
    
    def fetchSelfBoth(self):
        self.fetchSelfLocal()
        self.fetchSelfServer()
    def fetchSelfLocal(self):
        log.warning("fetch Local -> Not Implemented")
    def fetchSelfServer(self):
        log.warning("fetch Server -> Not Implemented")
        
    def writeInfo(self):
        log.warning("write info -> Not Implemented")

    def readInfo(self):
        log.warning("read info -> Not Implemented")

    def getImage(self):
        if self.image is not None:
            if os.path.isfile(self.image):
                return self.image
        img = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, "logo",  "noPicture.png")
        if os.path.isfile(img):
            return img