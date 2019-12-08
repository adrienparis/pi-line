import os
from copy import copy

from .item import Item

class Scene(Item):
    _path = os.path.join("3_work", "maya", "scenes")
    _step = []

    def __init__(self, name, cat, project):
        Item.__init__(self, name, project)

        self.relativePath = os.path.join(self.relativePath, Scene._path, cat, name)
        self.category = cat
        self.versions = []

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

    def newVersion(self):
        pass

    def getVersionBy(self, steps):
        l = []
        self.versions.sort(key=lambda x: x.date, reverse=False)
        if type(steps) == tuple:
            l = [x for x in self.versions if x.step in steps]
        elif type(steps) == str:
            l = [x for x in self.versions if x.step == steps]
        
        return l

    def getWips(self):
        pass

    def getLastWip(self):
        pass

    #TODO create on both server and local
    def new(self):
        for s in self.step:
            print("create folder " + s)
            #and inside create folder versions, and wip only for local
        pass