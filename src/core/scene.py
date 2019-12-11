import os
from copy import copy

from .item import Item
from .version import Version

class Scene(Item):
    _path = os.path.join("3_work", "maya", "scenes")
    _steps = []

    def __init__(self, name, cat, project=None):
        self.category = cat
        Item.__init__(self, name, project)
        self.relativePath = os.path.join(self._path, cat, name)
        self.versions = []
        self.fileName = self.parent.diminutive + "_" + self.name

    def setRelativePath(self):
        self.relativePath = os.path.join(self._path, self.category, self.name)

    #TODO fill the info.pil with date/img etc
    #TODO copy the server version to a saved version
    def Publish(self):
        self.createVersion()
        pass
    def Download(self):
        pass

    def createVersion(self):
        #copy old published version on server to version folder on server
        #copy old published version on server to version folder on local
        #copy wip folder on local to version folder on local
        #copy last wip to asset root, rename it to a publish name
        #copy 
        pass

    def addVersion(self, version):
        self.versions.append(version)




    def getLastVersion(self):
        '''return the last version'''
        if len(self.versions) == 0:
            return None
        self.versions.sort(key=lambda x: x, reverse=True)
        return self.versions[0]

    def getVersionBy(self, steps):
        l = []
        self.versions.sort(key=lambda x: x.name, reverse=True)
        if type(steps) == tuple or type(steps) == list :
            l = [x for x in self.versions if x.step in steps]
        elif type(steps) == str:
            l = [x for x in self.versions if x.step == steps]
        
        return l

    #TODO create on both server and local
    def make(self):
        print(os.path.join(self.path.local, self.getAbsolutePath()))
        print(self.relativePath)
        for s in self._steps:
            print("create folder " + self.getAbsolutePath() + s)
            p = os.path.join(self.path.local, self.getAbsolutePath(), s, Version._path)
            print(p)
            if not os.path.isdir(p):
                os.makedirs(p)
            #and inside create folder versions, and wip only for local
        pass

    def makeNewVersion(self, step):
        v = Version(self, step)
        v.make()
        self.versions.append(v)
    
    def fetchVersions(self):
        self.versions = []
        for s in self._steps:

            lp = os.path.join(self.path.local, self.getAbsolutePath(), s, Version._path)
            sp = os.path.join(self.path.server, self.getAbsolutePath(), s, Version._path)
            if not os.path.isdir(lp):
                # print("no " + s + " step in " + self.name + " local")
                pass
            else:
                for n in os.listdir(lp):
                    v = Version(self, s, n)
                    v.onLocal = True
                    self.versions.append(v)

            if not os.path.isdir(sp):
                # print("no " + s + " step of " + self.name + " in server")
                pass
            else:
                for n in os.listdir(sp):
                    isOnLoc = next((x for x in self.versions if x.name == n and x.step == s), None)
                    if isOnLoc is None:
                        v = Version(self, s, n)
                        v.onServer = True
                        self.versions.append(v)
                    else:
                        isOnLoc.onServer = True