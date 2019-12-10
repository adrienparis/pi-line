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
        self.date = datetime.datetime.strptime(self.name, '%Y%m%d%H%M%S')
        self.fileName = self.parent.fileName + "_" + self.step
        self.infoName = None
        self.wips = []

    def setRelativePath(self):
        self.relativePath = os.path.join(self.step, self._path, self.name)
        
    def make(self):
        '''Create folder of the current version on local named by the current date.
        it also creates a wip folder and an empty project'''

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

# TODO and copy the publish of the version to the server scene
    def upload(self):
        '''rename the self version to actual date 
        copy to server'''
        print("uploading " + self.name)
        if not(not self.onServer and self.onLocal):
            print("Already on server")
            return
        last = os.path.join(self.path.local, self.parent.getAbsolutePath(), self.step, Version._path, self.name)
        print(last)
        self.name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.date = datetime.datetime.now()
        self.setRelativePath()
        newLoc = os.path.join(self.path.local, self.parent.getAbsolutePath(), self.step, Version._path, self.name)
        newSer = os.path.join(self.path.server, self.parent.getAbsolutePath(), self.step, Version._path, self.name)
        newSerWip = os.path.join(newSer, "wip")
        print(newLoc)
        print(newSer)
        shutil.move(last, newLoc)
        os.makedirs(newSer)
        copy_tree(newLoc, newSer)
        shutil.rmtree(newSerWip)
        self.onServer = True
        print("all worked")

    def deleteLocal(self):
        pass

    def setCurrent(self):
        '''copy the publish of the version to the local scene'''
        pubPath = os.path.join( self.path.local, self.parent.getAbsolutePath(), self.step)
        verPath = os.path.join( self.path.local, self.getAbsolutePath())
        wipPath = os.path.join( pubPath, "wip")
        print("copy \n\t" + verPath + "\n to \n\t" + pubPath)
        copy_tree(verPath, pubPath)
        shutil.rmtree(wipPath)

    def fetchWips(self):
        path = os.path.join(self.path.local, self.parent.getAbsolutePath(),
                            self.step, Version._path, self.name, "wip")
        self.wips = os.listdir(path)
        self.wips.sort(key=lambda x: x, reverse=True)

    def getLastWip(self):
        '''return the last wip'''
        self.fetchWips()
        if len(self.wips) == 0:
            return []
        return self.wips[0]
    
    def publish(self):
        '''export low poly obj, export high poly obj, export proxy, export .ma'''
        wip = self.getLastWip()
        if len(wip) == 0:
            return False
        path = os.path.join(self.path.local, self.parent.getAbsolutePath(),
                            self.step, Version._path, self.name)
        wipPath = os.path.join(path, "wip", wip)
        pubPath = os.path.join(path, self.fileName + ".ma")
        # print("copy \n\t" + wipPath + "\n to \n\t" + pubPath)
        #export .ma
        shutil.copyfile(wipPath, pubPath)
        #export lowpoly obj
        #export highpoly obj
        #export proxy
        return True