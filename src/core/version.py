import os
import datetime
from distutils.dir_util import copy_tree
import shutil

from .item import Item

class Version(Item):
    _path = "versions"
    def __init__(self, scene, step, name=datetime.datetime.now().strftime("%Y%m%d%H%M%S")):
        self.step = step
        Item.__init__(self, name, scene)
        self.fileName = self.parent.parent.diminutive + "_" + self.parent.name + "_" + self.step

    def setRelativePath(self):
        self.relativePath = os.path.join(self.step, self._path, self.name)
# TODO create folder on local named by the current date
    def make(self):

        path = os.path.join(self.path.local, self.parent.getAbsolutePath(),
                            self.step, Version._path, self.name)
        wipPath = os.path.join(path, "wip")
        print(path)
        os.makedirs(wipPath)
        name = self.fileName + ".001" + ".ma"
        # TODO make wips too
        templateFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, "empty.ma")
        print(templateFile)
        print(os.path.join(wipPath, name))
        shutil.copy(templateFile, os.path.join(wipPath, name))

# TODO copy the server version to the local version
# TODO and copy the publish of the version to the local scene
    def download(self):
        pass

# TODO rename the self version to actual date
# TODO copy to server
# TODO and copy the publish of the version to the server scene
    def upload(self):
        if not(not self.onServer and self.onLocal):
            return
        last = os.path.join(self.path.local, self.parent.getAbsolutePath(), self.step, Version._path, self.name)
        print(last)
        self.name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.setRelativePath()
        newLoc = os.path.join(self.path.local, self.parent.getAbsolutePath(), self.step, Version._path, self.name)
        newSer = os.path.join(self.path.server, self.parent.getAbsolutePath(), self.step, Version._path, self.name)
        print(newLoc)
        print(newSer)
        shutil.move(last, newLoc)
        os.makedirs(newSer)
        copy_tree(newLoc, newSer)
        print("all worked")

    def deleteLocal(self):
        pass

# TODO copy the publish of the version to the local scene
    def setCurrent(self):
        pubPath = os.path.join( self.path.local, self.parent.getAbsolutePath(), self.step)
        verPath = os.path.join( self.path.local, self.getAbsolutePath())
        copy_tree(verPath, pubPath)

    def fetchWips(self):
        pass

# TODO return an array of wips
    def getWips(self):
        pass

# TODO return the last wip
    def getLastWip(self):
        pass
