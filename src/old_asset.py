import os
import shutil
import datetime
from distutils.dir_util import copy_tree

import maya.cmds as cmds

class SyncState():
    SYNC = 0
    OUTDATED = 1
    NEW = 2
    ERROR = 3

class Item():
    def __init__(self, name, project):
        self.name = name
        self.project = project
        self.image = ""
        self.comment = ""
        self.state = SyncState.ERROR
    def fetchImage(self):
        imgs = [
                os.path.join(self.project.serverPath, self.name, "thumbnail.png"),
                os.path.join(self.project.localPath, self.name, "thumbnail.png"),
                os.path.join(self.project.serverPath, self.name, "surf", "thumbnail.png"),
                os.path.join(self.project.localPath, self.name, "surf", "thumbnail.png"),
                os.path.join(self.project.serverPath, self.name, "rig", "thumbnail.png"),
                os.path.join(self.project.localPath, self.name, "rig", "thumbnail.png"),
                os.path.join(self.project.serverPath, self.name, "mod", "thumbnail.png"),
                os.path.join(self.project.localPath, self.name, "mod", "thumbnail.png")
        ]
        current_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
        self.image = os.path.join(current_path,"logo", "noPicture.png")
        for img in imgs:
            if os.path.exists(img):
                self.image = img
                break
        #TODO look in ref folder


class Version(Item):

    def __init__(self, name):
        Item.__init__(self, name)
        self.date = datetime.datetime.now()
    
    def saveVersionLocal(self):
        pass
    def saveVersionServer(self):
        pass
    def removeLocal(self):
        pass
    def downloadToLocal(self):
        pass

class Step():
    def __init__(self):
        pass

class Scene(Item):

    def __init__(self, category, name):
        Item.__init__(self, name)
        self.category = category
        self.shotUses = 0
    def createTreeLocal(self):
        pass
    def createTreeServer(self):
        pass



class Category():

    catPath =  os.path.join("3_work", "maya", "scenes", "assets")

    def __init__(self, name, project):
        self.name = name
        self.project = project
        self.fetchAllAssets()

    def fetchAllAssets(self):
        self.assets = []

        astServ = []
        astLocl = []


        sp = os.path.join(self.project.serverPath, self.project.name, self.catPath, self.name)
        if not os.path.isdir(sp):
            print(self.name + " folder not found")
            print(sp)
        else:
            for n in os.listdir(sp):
                asset = Asset(self, n)
                asset.fetchAssetData()
                asset.state = SyncState.OUTDATED
                astServ.append(asset)
                self.assets.append(asset)
        
        lp = os.path.join(self.project.localPath, self.project.name, self.catPath, self.name)
        if not os.path.isdir(lp):
            print(self.name + " folder not found")
            print(lp)
        else:
            for n in os.listdir(lp):
                asset = Asset(self, n)
                asset.fetchAssetData()
                astLocl.append(asset)

                s = next((x for x in self.assets if x.name == asset.name), None)
                # TODO set the state of the Asset based on the date
                if s is None:
                    asset.state = SyncState.NEW
                    self.assets.append(asset)
                else:
                    s.state = SyncState.SYNC

        return self.assets

    # take array of category
    def fetchAllCategories(path, categories):
        c = []

        for folder in os.listdir(path):
            if not os.path.isdir(folder):
                print(folder + " is a file")
                continue
            
            
            assets[folder] = []
            for asset in os.listdir(path + folder + "/"):
                assets[folder].append(asset)

    def listElem(self):
        for a in self.assets:
            print(a.name, a.category)


class Asset():

    def __init__(self, category, name):
        self.category = category
        self.name = name
        self.image = "S:/a.paris/Works/Atelier/chara/lefuneste/03_work/maya/images/endSnapshot.jpg"
        self.comment = ""
        self.shotUses = 0
        self.state = SyncState.ERROR


    def create(self, path):
        rootDir = os.path.join(path, self.name)
        if os.path.exists(rootDir):
            print("The asset [" + self.name + '] already exists')
            return
        os.mkdir(rootDir)
        steps = ["mod", "rig", "surf"]
        for s in steps:
            dir = os.path.join(rootDir,s)
            if not os.path.exists(dir):
                os.mkdir(dir)
            wipDir = os.path.join(dir,"wip")
            if not os.path.exists(wipDir):
                os.mkdir(wipDir)

    def fetchAssetData(self):
        self.fetchImage()
        #TODO get comment, date last version, author, time work on, etc


    def fetchImage(self):
        imgs = [
                os.path.join(self.category.project.serverPath, self.name, "thumbnail.png"),
                os.path.join(self.category.project.localPath, self.name, "thumbnail.png"),
                os.path.join(self.category.project.serverPath, self.name, "surf", "thumbnail.png"),
                os.path.join(self.category.project.localPath, self.name, "surf", "thumbnail.png"),
                os.path.join(self.category.project.serverPath, self.name, "rig", "thumbnail.png"),
                os.path.join(self.category.project.localPath, self.name, "rig", "thumbnail.png"),
                os.path.join(self.category.project.serverPath, self.name, "mod", "thumbnail.png"),
                os.path.join(self.category.project.localPath, self.name, "mod", "thumbnail.png")
        ]
        current_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
        self.image = current_path + "/logo/noPicture.png"
        for img in imgs:
            if os.path.exists(img):
                self.image = img
                break
        #TODO look in ref folder

    def setImage(self, newImg):
        img = os.path.join(path, self.name, "thumbnail.png")
        shutil.copyfile(newImg, img)


    #TODO download the publish version of mod/rig/surf from the server to local
    #and later [download lasts] wich download the latest version of each mod/surf/rig
    def download(self):
        p =  os.path.join(self.category.project.name, "3_work", "maya", "scenes", "assets", self.category.name)
        steps = ["mod", "rig", "surf"]
        for step in steps:
            name = self.category.project.diminutive + "_" + self.name + "_" + step + ".ma"

            s = os.path.join( self.category.project.serverPath, p, self.name, step, "").replace('\\', '/')
            l = os.path.join( self.category.project.localPath, p, self.name, step, "").replace('\\', '/')
            print("copy : \n\t" + s + "\nTo : \n\t" + l)
            
            if not os.path.exists(l):
                os.makedirs(l)
            if not os.path.exists(s):
                print("no file in the server")
                continue
            src_files = os.listdir(s)
            for file_name in src_files:
                full_file_name = os.path.join(s, file_name)
                if os.path.isfile(full_file_name):
                    shutil.copy(full_file_name, l)

    def downloadStep(self, stepInt):
        p =  os.path.join(self.category.project.name, "3_work", "maya", "scenes", "assets", self.category.name)
        step = (stepInt == 1) * "mod" + (stepInt == 2) * "rig" + (stepInt == 3) * "surf"
        name = self.category.project.diminutive + "_" + self.name + "_" + step + ".ma"

        s = os.path.join( self.category.project.serverPath, p, self.name, step, "").replace('\\', '/')
        l = os.path.join( self.category.project.localPath, p, self.name, step, "").replace('\\', '/')
        print("copy : \n\t" + s + "\nTo : \n\t" + l)
        
        if not os.path.exists(l):
            os.makedirs(l)
        if not os.path.exists(s):
            print("no file in the server")
            return
        src_files = os.listdir(s)
        for file_name in src_files:
            full_file_name = os.path.join(s, file_name)
            if os.path.isfile(full_file_name):
                shutil.copy(full_file_name, l)


    #TODO delete the local version of the asset
    def removeLocal(self):
        pass

    #import 
    def importHard(self):
        pass
    def importProxy(self):
        pass
    def importRef(self):
        pass

    #TODO Open the last wip, if does not exist copy the publish in the wip folder rename it *.0001 and open it
    def open(self, stepInt):
        p =  os.path.join(self.category.project.name, "3_work", "maya", "scenes", "assets", self.category.name)
        step = (stepInt == 1) * "mod" + (stepInt == 2) * "rig" + (stepInt == 3) * "surf"
        name = self.category.project.diminutive + "_" + self.name + "_" + step + ".ma"
        l = os.path.join( self.category.project.localPath, p, self.name, step, "").replace('\\', '/')
    
    #TODO save the current file as the last wip of the selected asset
    def saveVersion(self, stepInt):
        p = os.path.join(self.category.project.name, "3_work", "maya", "scenes", "assets", self.category.name)
        step = (stepInt == 1) * "mod" + (stepInt == 2) * "rig" + (stepInt == 3) * "surf"
        name = self.category.project.diminutive + "_" + self.name + "_" + step + ".ma"
        l = os.path.join( self.category.project.localPath, p, self.name, step, "").replace('\\', '/')


    #TODO Copy the last wip file to the root dir of the mod/rig/surf, replacing the last one, 
    # create a folder "datetime" in the version folder
    # create info of the asset in the info.pil
    # And copy the version folder and the publish version to the Server
    # for al the type of assets execpte the set, create proxy, and obj lowpoly, and highpoly
    def publish(self, stepInt):
        p =  os.path.join(self.category.project.name, "3_work", "maya", "scenes", "assets", self.category.name)
        step = (stepInt == 1) * "mod" + (stepInt == 2) * "rig" + (stepInt == 3) * "surf"
        name = self.category.project.diminutive + "_" + self.name + "_" + step + ".ma"

        s = os.path.join( self.category.project.serverPath, p, self.name, step, "").replace('\\', '/')
        l = os.path.join( self.category.project.localPath, p, self.name, step, "").replace('\\', '/')
        print("copy : \n\t" + s + "\nTo : \n\t" + l)
        
        if not os.path.exists(s):
            os.makedirs(s)
        if not os.path.exists(l):
            print("no file in the server")
            return
        src_files = os.listdir(l)
        for file_name in src_files:
            full_file_name = os.path.join(l, file_name)
            if os.path.isfile(full_file_name):
                shutil.copy(full_file_name, s)