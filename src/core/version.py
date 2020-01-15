import os
import datetime
from distutils.dir_util import copy_tree
import shutil

import mayaInteraction.screenshots as ScreenShots
import mayaInteraction.fileManagement as FileManagement

from .item import Item

class Version(Item):
    _path = "versions"
    def __init__(self, scene, step, name=None):
        self.step = step
        if name is None:
            self.name = name=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        else:
            self.name = name
        Item.__init__(self, name, scene)
        self.date = datetime.datetime.strptime(self.name, '%Y%m%d%H%M%S')
        # print("init version", self.date)
        self.fileName = self.parent.fileName + "_" + self.step
        self.infoName = None
        self.wips = []

    def setRelativePath(self):
        self.relativePath = os.path.join(self.step, self._path, self.name)
        
    def make(self):
        '''Create folder of the current version on local named by the current date.
        it also creates a wip folder and an empty project'''

        path = os.path.join(self.path.server, self.parent.getAbsolutePath(),
                            self.step, Version._path, self.name)
        os.makedirs(path)
    
    def makeNewWIP(self):
        path = os.path.join(self.path.local, self.parent.getAbsolutePath(),
                            self.step, Version._path, self.name)
        wipPath = os.path.join(path, "wip")
        print(path)
        os.makedirs(wipPath)
        name = self.fileName + ".001" + ".ma"
        # TODO make wips too
        templateFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, "empty.ma")
        self.onLocal = True
        shutil.copy(templateFile, os.path.join(wipPath, name))

    def download(self):
        print("downloading " + self.name)
        if not(self.onServer and not self.onLocal):
            print("Already on local")
            return
        loc = os.path.join(self.path.local, self.parent.getAbsolutePath(), self.step, Version._path, self.name)
        ser = os.path.join(self.path.server, self.parent.getAbsolutePath(), self.step, Version._path, self.name)
        print(loc)
        print(ser)
        copy_tree(ser, loc)
        self.onLocal = True

        print(self.name + " downloaded")

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
        #BAD IDEA
        #TODO REPLACE THAT!! do not copy all and deleting after! only copy what's needed
        shutil.rmtree(newSerWip)
        self.onServer = True
        print("all worked")

    def deleteLocal(self):
        print("delete Local -> not implemented")
        self.onLocal = False
        pass

    def setCurrent(self):
        '''copy the publish of the version to the local scene'''
        pubPath = os.path.join( self.path.local, self.parent.getAbsolutePath(), self.step)
        verPath = os.path.join( self.path.local, self.getAbsolutePath())
        wipPath = os.path.join( verPath, "wip")
        print("copy \n\t" + verPath + "\n to \n\t" + pubPath)

        f = os.listdir(verPath)
        for name in f:
            fullName = os.path.join(verPath, name)
            if os.path.isfile(fullName):
                shutil.copy(fullName, pubPath)


        # shutil.copytree(verPath, pubPath, ignore=shutil.ignore_patterns("./wip"))
        print("copied")
        # copy_tree(verPath, pubPath)
        #TODO BAD IDEA!!!! find a way to copy the folder WITHOUT copying the wip path
        # shutil.rmtree(wipPath)

    def fetchWips(self):
        path = os.path.join(self.path.local, self.parent.getAbsolutePath(),
                            self.step, Version._path, self.name, "wip")
        if not os.path.isdir(path):
            self.wips = []
            return
        self.wips = os.listdir(path)
        self.wips.sort(key=lambda x: x, reverse=True)

    def getLastWip(self):
        '''return the last wip'''
        self.fetchWips()
        if len(self.wips) == 0:
            return None
        return self.wips[0]
    
    def publish(self):
        '''export low poly obj, export high poly obj, export proxy, export .ma in the version folder'''

        #TODO Check if the selected file is open in maya

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

    
    def readInfo(self):
        path = os.path.join(self.getRoot().path.server, self.getRoot().name, ".pil")
        if not os.path.isdir(path):
            return
        info = os.path.join(path, self.fileName + "_" + self.name + ".pil")
        if not os.path.isfile(info):
            return
        data = {}
        with open(info) as fp:
            for line in fp:
                k, v = line.replace("\n", "").split("=")
                data[k] = v
        
        self.date = datetime.datetime.strptime( data["date"], '%Y-%m-%d %H:%M:%S.%f')
        self.author = data["author"]
        self.name = data["name"]
        self.fileName = data["fileName"]
        self.infoName = data["infoName"]
        

        img = os.path.join(path, self.fileName + "_" + self.name + ".png")
        if os.path.isfile(img):
            self.image = img


    def writeInfo(self):
        path = os.path.join(self.getRoot().path.server, self.getRoot().name, ".pil")
        if not os.path.isdir(path):
            os.mkdir(path)
        info = os.path.join(path, self.fileName + "_" + self.name + ".pil")
        with open(info, "w+") as fp:
            fp.write("name=" + self.name + "\n")
            fp.write("fileName=" + self.fileName + "\n")
            fp.write("infoName=" + self.infoName + "\n")
            fp.write("author=" + self.author + "\n")
            fp.write("date=" + datetime.datetime.strftime(self.date, '%Y-%m-%d %H:%M:%S.%f') + "\n")

    def takeScreenshots(self):
        path = os.path.join(self.getRoot().path.server, self.getRoot().name, ".pil")
        if not os.path.isdir(path):
            os.mkdir(path)
            
        filePath = os.path.join(self.path.local, self.parent.getAbsolutePath(),
                            self.step, Version._path, self.name, self.fileName + ".ma")
        if not FileManagement.isCurrentSceneIs(filePath):
            print(filePath + " is not currently open")
            # fileManagement.open(filePath)
            return
        name = self.fileName + "_" + self.name
        ScreenShots.orthographicTurnScreenShot(name, path)

        