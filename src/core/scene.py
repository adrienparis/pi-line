import os
from copy import copy

import log

from .user import User
from .item import Item, copyTree
from .version import Version

class Scene(Item):
    _path = os.path.join("3_work", "maya", "scenes")
    _steps = []
    _type = ""

    def __init__(self, name, cat, project=None):
        self.category = cat
        Item.__init__(self, name, project)
        # super(Item, self).__init__(name, project)
        # super(Scene, self).__init__(name, project)
        self.relativePath = os.path.join(self._path, cat, name)
        self.versions = []
        self.fileName = self.parent.diminutive + "_" + self.name

    def setRelativePath(self):
        self.relativePath = os.path.join(self._path, self.category, self.name)

    # #TODO fill the info.pil with date/img etc
    # #TODO copy the server version to a saved version
    # def Publish(self):
    #     self.createVersion()
    #     pass
    # def Download(self):
    #     pass

    # def createVersion(self):
    #     #copy old published version on server to version folder on server
    #     #copy old published version on server to version folder on local
    #     #copy wip folder on local to version folder on local
    #     #copy last wip to asset root, rename it to a publish name
    #     #copy 
    #     pass

    def addVersion(self, version):
        self.versions.append(version)




    def getLastVersion(self):
        '''return the last version'''
        if len(self.versions) == 0:
            return None
        self.versions.sort(key=lambda x: x.name, reverse=True)
        log.debug("last version", self.versions[0].name)
        for v in self.versions:
            log.debug("\tall versions", v.name)
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
        log.debug(os.path.join(self.path.local, self.getAbsolutePath()))
        log.debug(self.relativePath)
        for s in self._steps:
            log.info("create folder " + self.getAbsolutePath() + s)
            p = os.path.join(self.path.local, self.getAbsolutePath(), s, Version._path)
            log.debug(p)
            if not os.path.isdir(p):
                os.makedirs(p)
            #and inside create folder versions, and wip only for local
        pass

    def makeNewVersion(self, step):
        v = Version(self, step)
        v.make()
        self.versions.append(v)
    
    def makeVersionFromPublish(self):
        #TODO !!!!!!!
        for s in self._steps:
            v = Version(self, s)
            v.infoName = "BACKUP - " + s
            v.author = User().name
            v.writeInfo()
            v.make()
            self.versions.append(v)
            src = os.path.join(self.path.server, self.getAbsolutePath(), s)
            dst = os.path.join(self.path.server, self.getAbsolutePath(),
                                s, v._path, v.name)
            copyTree(src, dst)

    def fetchVersions(self):
        self.versions = []
        for s in self._steps:

            lp = os.path.join(self.path.local, self.getAbsolutePath(), s, Version._path)
            sp = os.path.join(self.path.server, self.getAbsolutePath(), s, Version._path)
            if os.path.isdir(lp):
                # print(s + " step in " + self.name + " local")
                for n in os.listdir(lp):
                    v = Version(self, s, n)
                    v.onLocal = True
                    self.versions.append(v)
                    v.readInfo()
                    # print(v.onLocal, v.onServer)
            # else:
            #     print("no " + s + " step in " + self.name + " local")

            if os.path.isdir(sp):
                # print(s + " step in " + self.name + " Server")
                for n in os.listdir(sp):
                    v = next((x for x in self.versions if x.name == n and x.step == s), None)
                    # print(v.name)
                    if v is None:
                        v = Version(self, s, n)
                        self.versions.append(v)
                    v.onServer = True
                    v.readInfo()
                    # print(v.onLocal, v.onServer)
            # else:
            #     print("no " + s + " step of " + self.name + " in server")
        # print(self.versions)
        # for v in self.versions:
            # print(v.onLocal, v.onServer)