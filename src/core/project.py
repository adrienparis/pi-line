import os
import datetime
import getpass
import ctypes
import maya.cmds as cmds

import log

from .user import User

from .path import Path
from .item import Item
from .asset import Asset
from .shot import Shot


class Role(object):
    def __init__(self):

        #Jobs
        self.jobs = {}
        self.jobs["owners"] = []
        self.jobs["writers"] = []
        self.jobs["mainProductionManagers"] = []
        self.jobs["imageProductionManagers"] = []
        self.jobs["animationProductionManagers"] = []
        self.jobs["conceptArtists"] = []
        self.jobs["storyboarders"] = []
        self.jobs["imageReferants"] = []
        self.jobs["animReferants"] = []
        self.jobs["modellers"] = []
        self.jobs["surfacers"] = []
        self.jobs["riggers"] = []
        self.jobs["animators"] = []
        #always autorised
        self.jobs["devs"] = ["a.paris"]

        #Autorisations
        self.autorisations = {}
        self.autorisations["manageAutorisation"] = ["owners"]
        self.autorisations["BackupProject"] = ["all"]
        self.autorisations["manageVersion"] = ["owners", "mainProductionManagers", "imageProductionManagers", "animationProductionManagers"]
        self.autorisations["openFileExplorer"] = ["mainProductionManagers", "imageProductionManagers", "surfacers"]
        self.autorisations["createNewAssetsCategories"] = ["mainProductionManagers", "imageProductionManagers", "conceptArtists"]
        self.autorisations["createNewSequences"] = ["mainProductionManagers", "animationProductionManagers", "storyboarders"]
        self.autorisations["createNewAssets"] = ["mainProductionManagers", "imageProductionManagers", "imageReferants", "conceptArtists"]
        self.autorisations["createNewShots"] = ["mainProductionManagers", "animationProductionManagers", "animReferants", "storyboarders"]
        self.autorisations["deleteAssetsCategories"] = ["mainProductionManagers", "imageProductionManagers", "conceptArtists"]
        self.autorisations["deleteSequences"] = ["mainProductionManagers", "animationProductionManagers", "storyboarders"]
        self.autorisations["deleteAssets"] = ["mainProductionManagers", "imageProductionManagers", "imageReferants", "conceptArtists"]
        self.autorisations["deleteShots"] = ["mainProductionManagers", "animationProductionManagers", "animReferants", "storyboarders"]

    def isUsernameIsAutorised(self, username, autorisation):
        # if username == "a.paris":
        #     return True
        if username in self.jobs["devs"]:
            log.debug("autorized " + username + " to " + autorisation + " because he is a dev")
            return True
        jobs = self.autorisations[autorisation]

        if "all" in jobs:
            log.debug("autorized " + username + " to " + autorisation + " because everyone as acces")
            return True
        for job in jobs:
            if username in self.jobs[job]:
                log.debug("autorized " + username + " to " + autorisation + " because he is a " + job)
                return True
        return False

    def isUsernameIsInAJob(self, username, job):
        if username in self.job:
            return True
        return False

    
    def writeInfo(self, path):
        log.debug(os.path.join(path, "roles.pil"))
        if not os.path.isdir(path):
            log.warning(".pil folder not found")
        with open(os.path.join(path, "roles.pil"), "w+") as fp:
            for key, item in self.jobs.items():
                l = key + "="
                for i in item:
                    l += i + ";"
                fp.write(l + "\n")

    def readInfo(self, path):
        info = os.path.join(path, "roles.pil")
        if not os.path.isfile(info):
            log.warning("can't open roles'file", info)
            return
        data = {}
        with open(info) as fp:
            for line in fp:
                k, v = line.replace("\n", "").split("=")
                array = v.split(";")
                log.debug("line : ", k, array)
                self.jobs[k] = array
        

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
        self.roles = Role()

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
        self.assets = {}
        relativePath = os.path.join(self.relativePath, Asset._path)
        lp = os.path.join(self.path.local, relativePath)
        sp = os.path.join(self.path.server, relativePath)

        log.debug("local  asset [" + lp + "]")
        log.debug("server asset [" + sp + "]")
        if not os.path.isdir(lp):
            log.warning("[" + lp + "] local assets'folder not found")
        else:
            for c in os.listdir(lp):
                cat = os.path.join(lp, c)
                if not os.path.isdir(cat):
                    continue
                self.addCategory(c)
                for n in os.listdir(cat):
                    nPath = os.path.join(cat, n)
                    if not os.path.isdir(nPath):
                        continue
                    a = Asset(n, c, self)
                    self.assets[c].append(a)
                    a.onLocal = True
                    a.fetchVersions()

        if not os.path.isdir(sp):
            log.warning("[" + sp + "] server assets'folder not found")
        else:
            for c in os.listdir(sp):
                cat = os.path.join(sp, c)
                if not os.path.isdir(cat):
                    continue
                self.addCategory(c)
                for n in os.listdir(cat):
                    nPath = os.path.join(cat, n)
                    if not os.path.isdir(nPath):
                        continue
                    a = Asset(n, c, self)
                    s = next((x for x in self.assets[c] if x.name == a.name and x.category == a.category), None)
                    if s is None:
                        self.assets[c].append(a)
                    else:
                        a = s
                    a.onServer = True
                    a.fetchVersions()

    def fetchShots(self):
        self.shots = {}
        relativePath = os.path.join(self.relativePath, Shot._path)
        lp = os.path.join(self.path.local, relativePath)
        sp = os.path.join(self.path.server, relativePath)
        log.debug("local  shot  [" + lp + "]")
        log.debug("server shot  [" + sp + "]")

        if not os.path.isdir(lp):
            log.warning("[" + lp + "] local assets'folder not found")
        else:
            for c in os.listdir(lp):
                cat = os.path.join(lp, c)
                if not os.path.isdir(cat):
                    continue
                self.addSequence(c)
                for n in os.listdir(cat):
                    nPath = os.path.join(cat, n)
                    if not os.path.isdir(nPath):
                        continue
                    a = Shot(n, c, self)
                    self.shots[c].append(a)
                    a.onLocal = True

        if not os.path.isdir(sp):
            log.warning("[" + sp + "] server shots'folder not found")
        else:
            for c in os.listdir(sp):
                cat = os.path.join(sp, c)
                if not os.path.isdir(cat):
                    continue
                self.addSequence(c)
                for n in os.listdir(cat):
                    nPath = os.path.join(cat, n)
                    if not os.path.isdir(nPath):
                        continue
                    a = Shot(n, c, self)
                    s = next((x for x in self.shots[c] if x.name == a.name and x.category == a.category), None)
                    if s is None:
                        self.shots[c].append(a)
                    else:
                        a = s
                    a.onServer = True


    def makeCategory(self, name):
        if name in self.assets:
            log.warning("Category already exist")
            return
        self.assets[name] = []
        p = os.path.join(self.path.server, self.name, "3_work", "maya", "scenes", "assets", name)
        log.debug("create " + p)
        if not os.path.isdir(p):
            os.mkdir(p)
        if not self.onLocal:
            return
        p = os.path.join(self.path.local, self.name, "3_work", "maya", "scenes", "assets", name)
        log.debug("create " + p)
        if not os.path.isdir(p):
            os.mkdir(p)
        #TODO make dir on server and on local
        return

    def makeSequence(self, name):
        if name in self.shots:
            log.warning("Sequence already exist")
            return False
        self.shots[name] = []
        p = os.path.join(self.path.server, self.name, "3_work", "maya", "shots", name)
        os.mkdir(p)
        p = os.path.join(self.path.local, self.name, "3_work", "maya", "shots", name)
        os.mkdir(p)
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

    def copyAllPublishToNewVersion(self):
        self.fetchAll()
        for c, scenes in self.assets.items():
            for s in scenes:
                s.makeVersionFromPublish()
                print(s.name)
        for c, scenes in self.shots.items():
            for s in scenes:
                s.makeVersionFromPublish()
                print(s.name)

    def fetchAll(self):
        self.fetchAssets()
        self.fetchShots()

    #TODO Find an other way
    def setProject(self):
        p = os.path.join(self.path.local, self.name, "3_work", "maya")
        if not os.path.isdir(p):
            log.warning("Project folder not found")
            return
        
        # cmds.workspace(p, o=True)
        # cmds.workspace(dir=p)

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

        self.roles.writeInfo(path)

        ctypes.windll.kernel32.SetFileAttributesW(path, 0x02)

    def readInfo(self):
        path = os.path.join(self.path.server, self.name, ".pil")
        if not os.path.isdir(path):
            return
        info = os.path.join(path, "project.pil")
        data = {}
        log.debug("start reading project infos")
        if not os.path.isfile(info):
            return
        with open(info) as fp:
            for line in fp:
                log.debug("line : ", line)
                k, v = line.replace("\n", "").split("=")
                data[k] = v
        
        self.diminutive = data["dim"]
        self.date = datetime.datetime.strptime( data["date"], '%Y-%m-%d %H:%M:%S.%f')
        self.author = data["author"]

        log.debug("start reading roles infos")
        self.roles.readInfo(path)
        log.debug("stop reading roles infos")

    def writeProjectInPrefs(self):
        user = User()
        if not os.path.isdir(user.prefPath):
            os.mkdir(user.prefPath)
        filepath = os.path.join(user.prefPath, "projects.pil")
        with open(filepath,"a") as f:
            s = ""
            for w in (self.name, self.diminutive, self.path.server, self.path.local):
                s += str(w) + ";"
            f.write(s + "\n")

    @staticmethod
    def writeAllProjectsInPrefs(projects):
        user = User()
        if not os.path.isdir(user.prefPath):
            os.mkdir(user.prefPath)
        filepath = os.path.join(user.prefPath, "projects.pil")
        os.remove(filepath)

        for p in projects:
            p.writeProjectInPrefs()


    # [name, diminutive, pathServer, pathLocal]
    @staticmethod
    def fetchProjects():
        log.info("fetch projects")
        ps = []

        user = User()


        filepath = os.path.join(user.prefPath, "projects.pil")
        if not os.path.isfile(filepath):
            log.warning("Saved projects file not found")
            return ps
        with open(filepath) as fp:
            for line in fp:
                # l = ast.literal_eval(line.replace("\\", "/"))
                l = line.split("\n")[0].split(";")
                # l.pop()
                print(line)
                print(l)
                if len(l) >= 3:
                    p = Project(l[0], Path(l[2]))
                    p.diminutive = l[1]
                    if len(l) >= 4:
                        log.debug(l[3])
                        p.path.local = l[3]
                    p.readInfo()
                    ps.append(p)
                    log.debug("fetch project", ps)
        log.debug("fetch project", ps)
        return ps

    @staticmethod
    def _makeFolderTree(tree, path, deep=0):
        name = ""
        for f in tree:
            if type(f) == str or type(f) == unicode:
                name = f
                if os.path.exists(os.path.join(path, name)):
                    log.warning("\t" + name + ' :  already exists')
                elif not os.path.exists(path):
                    log.warning("\t" + path + ' : does not exist')
                else:
                    os.mkdir(os.path.join(path, name))
            else:
                Project._makeFolderTree(f, path + "/" + name, deep + 1)

    def getAvailableNewAssetCategories(self):
        pass
    def getNextSequence(self):
        pass