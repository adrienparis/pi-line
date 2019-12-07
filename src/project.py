import os
import ctypes
import datetime
import getpass
import maya.cmds as cmds

from plUser import *
from asset import *

class Project():
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
                    ["4_out"],
    ]
    def __init__(self):
        self.name = ""
        self.author = ""
        self.serverPath = ""
        self.localPath = ""
        self.diminutive = ""
        self.categories = []
        self.shots = []
        self.date = datetime.datetime.now()

    def fetchAll(self):
        self.categories = []

        path = os.path.join(self.serverPath, self.name, "3_work", "maya", "scenes", "assets")

        if not os.path.isdir(path):
            print("assets folder not found")
            return

        for folder in os.listdir(path):
            c = Category(folder, self)
            self.categories.append(c)

    def setProject(self):
        p = os.path.join(self.serverPath, self.name, "3_work", "maya")
        if not os.path.isdir(p):
            # cmds.error("Project folder not found")
            return
        
        cmds.workspace(p, o=True)
        cmds.workspace(dir=p)

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
        self.date = datetime.datetime.now()
        path = self.serverPath
        fold = self.name
        # (path, fold) = os.path.split(self.serverPath)
        print(Project.treeTemplate)
        tree = [fold] + Project.treeTemplate
        print("the path")
        print(tree)
        print(path)
        Project.createProjectTree(tree, 0, path)
        self.writeInfoFile()


    def writeInfoFile(self):
        path = os.path.join(self.serverPath, self.name, ".pil")
        if not os.path.isdir(path):
            os.mkdir(path)
        info = open(os.path.join(path, "project.pil"), "w+")
        info.write("name=" + self.name + "\n")
        info.write("dim=" + self.diminutive + "\n")
        info.write("author=" + self.author + "\n")
        info.write("date=" + str(self.date) + "\n")

        ctypes.windll.kernel32.SetFileAttributesW(path, 0x02)

    def fetchProjectInfo(self):
        print("fetching Data")
        path = os.path.join(self.serverPath, self.name, ".pil", "project.pil")
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




    # [name, pathServer, pathLocal]
    @staticmethod
    def fetchProjects():
        ps = []

        user = User()


        filepath = os.path.join(user.prefPath, "projects.pil")
        if not os.path.isfile(filepath):
            print("File path {} does not exist. Exiting...".format(filepath))
        #TODO create a try and catch to avoid a badly written config file
        return ps
        with open(filepath) as fp:
            for line in fp:
                # l = ast.literal_eval(line.replace("\\", "/"))
                l = line.split(";")
                print(l)
                p = Project()
                if len(l) >= 3:
                    p.name = l[0]
                    p.diminutive = l[1]
                    p.serverPath = l[2]
                    if len(l) == 4:
                        p.localPath = l[3]
                    elif len(l) == 3:
                        p.localPath = l[2]
                    p.fetchProjectInfo()
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
    
    @staticmethod
    def saveListProject(projects):
        user = User()
        if not os.path.isdir(user.prefPath):
            os.mkdir(user.prefPath)
        filepath = os.path.join(user.prefPath, "projects.pil")
        print(filepath)
        f = open(filepath,"w+")
        for p in projects:
            line = []
            line.append(p.name)
            line.append(p.diminutive)
            line.append(p.serverPath)
            line.append(p.localPath)
            s = ""
            for w in line:
                s += str(w) + ";"
            f.write(s + "\n")
            print(s)
