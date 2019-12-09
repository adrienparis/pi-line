import os
import datetime
import getpass
import maya.cmds as cmds

from .user import User

from .path import Path
from .item import Item
from .asset import Asset
from .shot import Shot

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

    
    assetCategory = ["chars", "props", "sets", "modules", "vehs"]

    def __init__(self, name, path):
        Item.__init__(self, name, None)
        self.path = path
        self.relativePath = self.name
        self.diminutive = ""
        self.assets = {}
        self.assetCategories = [] # Categories ????
        self.shots = {}
        self.sequences = []

    def getAssetsByCategory(self, cat):
        '''Return a list of assets that are a [cat] categories

        cat : name of the category
        '''

        l = []
        if type(cat) == tuple:
            for c in cat:
                l += self.assets[c][:]
        elif type(cat) == str or type(cat) == unicode:
            l = self.assets[cat][:]
        l.sort(key=lambda x: x.name, reverse=False)
        return l

    def getShotsBySequence(self, seq):
        '''Return a list of shots that are in a sequence

        seq : name of the sequence
        '''
        
        l = []
        if type(seq) == tuple:
            for c in seq:
                l += self.shots[c][:]
        elif type(seq) == str or type(seq) == unicode:
            l = self.shots[seq][:]
        l.sort(key=lambda x: x.name, reverse=False)
        return l

    def addAssetToCategory(self, asset, cat):
        '''add an asset to the project

        asset: -asset-
        cat: -str- name of the category
        return bool
        '''

        if not cat in self.assets:
            return False
        asset.categorie = cat
        asset.setParent(self)
        self.assets[cat].append(asset)
        return True

    def addShotToSequence(self, shot, seq):
        '''add a shot to the project

        shot: -shot-
        seq: -str- name of the sequence
        return bool
        '''

        if not seq in self.shots:
            return False
        shot.categorie = seq # bad object attribute name. he should be name sequence
        shot.setParent(self)
        self.shots[seq].append(shot)
        return True

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
                self.addCategory(c)
                for n in os.listdir(cat):
                    a = Asset(n, c, self)
                    print(self.assets)
                    self.assets[c].append(a)
                    a.onLocal = True

        if not os.path.isdir(sp):
            print(sp)
            print("server assets folder not found")
        else:
            for c in os.listdir(sp):
                cat = os.path.join(sp, c)
                if not os.path.isdir(cat):
                    continue
                self.addCategory(c)
                for n in os.listdir(cat):
                    a = Asset(n, c, self)
                    s = next((x for x in self.assets[c] if x.name == a.name and x.category == a.category), None)
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
                self.addSequence(c)
                for n in os.listdir(cat):
                    print("\t\t" + n)
                    a = Shot(n, c, self)
                    self.shots[c].append(a)
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
                self.addSequence(c)
                for n in os.listdir(cat):
                    print("\t\t" + n)
                    a = Shot(n, c, self)
                    s = next((x for x in self.shots[c] if x.name == a.name and x.category == a.category), None)
                    if s is None:
                        self.shots.append(a)
                    else:
                        a = s
                    a.onServer = True


    def makeCategory(self, name):
        if name in self.assets:
            return False
        self.assets[name] = []
        #TODO make dir on server and on local
        return True

    def makeSequence(self, name):
        if name in self.shots:
            return False
        self.shots[name] = []
        #TODO make dir on server and on local
        return True

    def addCategory(self, name):
        if name in self.assets:
            return False
        self.assets[name] = []
        return True

    def addSequence(self, name):
        if name in self.shots:
            return False
        self.shots[name] = []
        return True


    def fetchAll(self):
        self.fetchAssets()
        self.fetchShots()

    def setProject(self):
        p = os.path.join(self.path.server, self.name, "3_work", "maya")
        if not os.path.isdir(p):
            cmds.warning("Project folder not found")
            return
        
        cmds.workspace(p, o=True)
        cmds.workspace(dir=p)


    def updateInfo(self):
        #TODO look in the project folder if there is the name of the project, if it's there replace it with the new path, if not, add it to te file
        username = getpass.getuser()
        print(username)
        print("C:/Users/" + username + "/Documents/Pi-Line")


    #TODO Create/copy all the folders of the local tree
    def makeLocalFolderTree(self):
        tree = [self.name] + Project.treeTemplate
        Project._makeFolderTree(tree, self.path.local)

    def makeServerFolderTree(self):
        tree = [self.name] + Project.treeTemplate
        Project._makeFolderTree(tree, self.path.server)


    def writeInfo(self):
        path = os.path.join(self.path.server, self.name, ".pil")
        if not os.path.isdir(path):
            os.mkdir(path)
        info = open(os.path.join(path, "project.pil"), "w+")
        info.write("name=" + self.name + "\n")
        info.write("dim=" + self.diminutive + "\n")
        info.write("author=" + self.author + "\n")
        info.write("date=" + str(self.date) + "\n")

        ctypes.windll.kernel32.SetFileAttributesW(path, 0x02)

    def readInfo(self):
        print("fetching Data") 
        path = os.path.join(self.path.server, self.name, ".pil", "project.pil")
        print(path)
        if not os.path.isfile(path):
            return
        data = {}
        with open(path) as fp:
            for line in fp:
                k, v = line.replace("\n", "").split("=")
                data[k] = v
        
        print(data)
        self.diminutive = data["dim"]
        self.date = datetime.datetime.strptime( data["date"], '%Y-%m-%d %H:%M:%S.%f')
        self.author = data["author"]

    def writeProjectInPrefs(self):
        user = User()
        if not os.path.isdir(user.prefPath):
            os.mkdir(user.prefPath)
        filepath = os.path.join(user.prefPath, "projects.pil")
        print(filepath)
        with open(filepath,"a") as f:
            s = ""
            for w in (self.name, self.diminutive, self.path.server, self.path.local):
                s += str(w) + ";"
            f.write(s + "\n")
            print(s)

    @staticmethod
    def writeAllProjectsInPrefs(projects):
        user = User()
        if not os.path.isdir(user.prefPath):
            os.mkdir(user.prefPath)
        filepath = os.path.join(user.prefPath, "projects.pil")
        os.remove(filepath)

        for p in projects:
            print(p.name, p.diminutive, p.path.server, p.path.local)
            p.writeProjectInPrefs()


    # [name, diminutive, pathServer, pathLocal]
    @staticmethod
    def fetchProjects():
        ps = []

        user = User()


        filepath = os.path.join(user.prefPath, "projects.pil")
        if not os.path.isfile(filepath):
            print("File path {} does not exist. Exiting...".format(filepath))
            return ps
        with open(filepath) as fp:
            for line in fp:
                # l = ast.literal_eval(line.replace("\\", "/"))
                l = line.split(";")
                l.pop()
                if len(l) >= 3:
                    p = Project(l[0], Path(l[2]))
                    p.diminutive = l[1]
                    print(l)
                    if len(l) == 4:
                        print(l[3])
                        p.path.local = l[3]
                    p.readInfo()
                    ps.append(p)
        return ps

    @staticmethod
    def _makeFolderTree(tree, path, deep=0):
        name = ""
        for f in tree:
            if type(f) == str or type(f) == unicode:
                name = f
                if os.path.exists(os.path.join(path, name)):
                    print("\t" + name + ' : exists')
                elif not os.path.exists(path):
                    print("\t" + path + ' : does not exist')
                else:
                    os.mkdir(os.path.join(path, name))
            else:
                Project._makeFolderTree(f, path + "/" + name, deep + 1)

    def getAvailableNewAssetCategories(self):
        pass
    def getNextSequence(self):
        pass