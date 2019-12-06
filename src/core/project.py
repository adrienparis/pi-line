import os
import getpass
# import maya.cmds as cmds
import ast

from item import *
from asset import *
from shot import *

class Project(Item):
    treeTemplate = [["1_preprod"],
                    ["2_ressource"], 
                    ["3_work", 
                        ["maya", 
                            ["scenes", 
                                ["assets"],
                                ["shots"]],
                            ["images",
                                    ["shots"]],
                                        ["sourceimage", ["assets"]]]],
                    ["4_out"]
    ]

    
    assetCategory = ["mod", "rig", "surf"]
    sequence = ["animation", "previz", "rendering", "sfx"]

    def __init__(self, name, path):
        Item.__init__(self, name, None)
        self.path = path
        self.relativePath = self.name
        self.diminutive = ""
        self.assets = []
        self.shots = []

    def getAssetsBy(self, cat):
        l = []
        self.assets.sort(key=lambda x: x.name, reverse=False)
        if type(cat) == tuple:
            l = [x for x in self.assets if x.category in cat]
        elif type(cat) == str:
            l = [x for x in self.assets if x.category == cat]
        print(l)
        return l

    def getShotsBy(self, seq):
        l = []
        print(seq)
        self.shots.sort(key=lambda x: x.name, reverse=False)
        if type(seq) == tuple:
            print("tuple")
            l = [x for x in self.shots if x.category in seq]
        elif type(seq) == str:
            print("str")
            l = [x for x in self.shots if x.category == seq]
        
        return l

    def addAsset(self, asset, cat):
        asset.categorie = cat
        self.assets.append(asset)

    def addShot(self, shot, seq):
        shot.categorie = seq
        self.shots.append(shot)

    def fetchAssets(self):
        relativePath = os.path.join(self.relativePath, Asset._path)
        lp = os.path.join(self.path.local, relativePath)
        sp = os.path.join(self.path.server, relativePath)

        if not os.path.isdir(lp):
            print(lp)
            print("local assets folder not found")
        else:
            for c in os.listdir(lp):
                cat = os.path.join(lp, c)
                if not os.path.isdir(cat):
                    continue
                for n in os.listdir(cat):
                    a = Asset(n, c, self)
                    self.assets.append(a)
                    a.onLocal = True

        if not os.path.isdir(sp):
            print(sp)
            print("server assets folder not found")
        else:
            for c in os.listdir(sp):
                cat = os.path.join(sp, c)
                if not os.path.isdir(cat):
                    continue
                for n in os.listdir(cat):
                    a = Asset(n, c, self)
                    s = next((x for x in self.assets if x.name == a.name and x.category == a.category), None)
                    if s is None:
                        self.assets.append(a)
                    else:
                        a = s
                    a.onServer = True

    def fetchShots(self):
        relativePath = os.path.join(self.relativePath, Shot._path)
        lp = os.path.join(self.path.local, relativePath)
        sp = os.path.join(self.path.server, relativePath)

        if not os.path.isdir(lp):
            print(lp)
            print("local shot folder not found")
        else:
            for c in os.listdir(lp):
                print("\t" + c)
                cat = os.path.join(lp, c)
                if not os.path.isdir(cat):
                    continue
                for n in os.listdir(cat):
                    print("\t\t" + n)
                    a = Shot(n, c, self)
                    self.shots.append(a)
                    a.onLocal = True

        if not os.path.isdir(sp):
            print(sp)
            print("server shot folder not found")
        else:
            for c in os.listdir(sp):
                print("\t" + c)
                cat = os.path.join(sp, c)
                if not os.path.isdir(cat):
                    continue
                for n in os.listdir(cat):
                    print("\t\t" + n)
                    a = Shot(n, c, self)
                    s = next((x for x in self.shots if x.name == a.name and x.category == a.category), None)
                    if s is None:
                        self.shots.append(a)
                    else:
                        a = s
                    a.onServer = True
        
    def create(self):
        pass



    #TODO Create on server and on local
    def newAssetCategory(self, name):
        pass
    #TODO Create on server and on local
    def newSequence(self, name):
        pass


    def fetchAll(self):
        self.fetchAssets()
        self.fetchShots()

    def setProject(self):
        p = os.path.join(self.serverPath, self.name, "3_work", "maya")
        if not os.path.isdir(p):
            cmds.error("Project folder not found")
            return
        
        cmds.workspace(p, o=True)
        cmds.workspace(dir=p)


    def updateInfo(self):
        #TODO look in the project folder if there is the name of the project, if it's there replace it with the new path, if not, add it to te file
        username = getpass.getuser()
        print(username)
        print("C:/Users/" + username + "/Documents/Pi-Line")


    #TODO Create all the folders of the server tree
    def createTreeTemplateLocal(self):
        path = self.localPath
        fold = self.name
        # (path, fold) = os.path.split(self.localPath)
        print(Project.treeTemplate)
        tree = [fold] + Project.treeTemplate
        print("the path")
        print(tree)
        print(path)
        Project.createProjectTree(tree, 0, path)

    def createTreeTemplateServer(self):
        path = self.serverPath
        fold = self.name
        # (path, fold) = os.path.split(self.serverPath)
        print(Project.treeTemplate)
        tree = [fold] + Project.treeTemplate
        print("the path")
        print(tree)
        print(path)
        Project.createProjectTree(tree, 0, path)  

    # [name, diminutive, pathServer, pathLocal]
    @staticmethod
    def fetchProjects(pathProject):
        ps = []

        filepath = os.path.join(pathProject, "projects.pil")
        if not os.path.isfile(filepath):
            print("File path {} does not exist. Exiting...".format(filepath))
        #TODO create a try and catch to avoid a badly written config file
        with open(filepath) as fp:
            for line in fp:
                l = ast.literal_eval(line.replace("\\", "\\\\"))
                if len(l) >= 3:
                    name = l[0]
                    diminutive = l[1]
                    path = Path(server=l[2])
                    if len(l) == 4:
                        path.local = l[3]
                    
                    print(path.server)
                    p = Project(name, path)
                    ps.append(p)
        return ps

    @staticmethod
    def createProjectTree(tree, deep, path):
        name = ""
        print(tree, deep, path)
        for f in tree:
            print(f)
            if type(f) == str or type(f) == unicode:
                print("\t" * deep + f)
                name = f
                print(os.path.join(path, name))
                if os.path.exists(os.path.join(path, name)):
                    print("\t" + name + ' : exists')
                else:
                    os.mkdir(os.path.join(path, name))
            else:
                Project.createProjectTree(f, deep + 1, path + "/" + name)

