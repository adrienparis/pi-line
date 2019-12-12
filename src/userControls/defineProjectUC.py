import maya.cmds as cmds
from pymel.all import *

from .UC import *
from .treeUC import TreeUC

from core.project import Project, Path
from core.user import User




class DefineProjectUC(UserControl):

    class workPathUC(UserControl):
        def __init__(self, parent):
            UserControl.__init__(self, parent)
            self.name = "workpath" + self.name
            self.path = "Q:/"
        def load(self):
            self.layout = cmds.formLayout(self.name, parent=self.parentLay, bgc=hexToRGB(0x5a5a5a))
            self.pathLay = cmds.text(label=self.path, parent=self.layout, bgc=hexToRGB(0x9a9a9a), al="left")
            self.folderBtn = cmds.iconTextButton('folderBtn', parent=self.layout, style='iconOnly', image1=getIcon("folder"), label='Option', w=22, h=22, sic=True, bgc=hexToRGB(0x4a4a4a),
                                              c=Callback(self.selectDir))
            cmds.formLayout(self.layout, e=True, attachForm=[(self.pathLay, "top", 5), (self.pathLay, "bottom", 5), (self.pathLay, "left", 5), (self.folderBtn, "top", 5), (self.folderBtn, "bottom", 5), (self.folderBtn, "right", 5)], 
                                                 attachControl=[(self.pathLay, "right", 5, self.folderBtn)],
                                                 attachNone=[(self.folderBtn, "left")])

        def selectDir(self):
            multipleFilters = "Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)"
            # p = cmds.fileDialog2(fileFilter=multipleFilters, dialogStyle=2, dir="Q:/", fm=3)
            self.path = cmds.fileDialog2(dialogStyle=1, dir=self.path, fm=3)[0]
            self.refresh()
            self.runEvent("changeDir", self.path)

        def refresh(self):
            cmds.text(self.pathLay, e=True, label=self.path)

    class newUC(UserControl):
        def __init__(self, parent):
            UserControl.__init__(self, parent)
            self.name = "new"
            self.projName = ""
            self.projDim = ""
        def load(self):
            self.layout = cmds.formLayout(self.name, parent=self.parentLay, bgc=hexToRGB(0x5a5a5a), h=30, w=10)
            self.labName = cmds.text(parent=self.layout, label="Project name : ")
            self.nameFld = cmds.textField(parent=self.layout, text="", bgc=hexToRGB(0xababab))
            self.labShrtNm = cmds.text(parent=self.layout, label="Short Name : ")
            self.dimFld = cmds.textField(parent=self.layout, text="", bgc=hexToRGB(0xababab))
            self.button = cmds.button(parent=self.layout, label="Create new project", c=Callback(self.createNewProject), bgc=hexToRGB(0x7d7d7d))

            cmds.formLayout(self.layout, e=True, attachForm=[(self.labName, "top", 5), (self.labName, "left", 5),
                                                             (self.nameFld, "top", 5), 
                                                             (self.labShrtNm, "left", 5), 
                                                             (self.nameFld, "right", 5),
                                                             (self.button, "bottom", 5), (self.button, "right", 5)],
                                                 attachControl=[(self.nameFld, "left", 5, self.labName), (self.dimFld, "left", 5, self.labShrtNm), 
                                                                (self.labShrtNm, "top", 10, self.labName), (self.dimFld, "top", 10, self.labName)],
                                                 attachPosition=[(self.dimFld, "right", 5, 40)],
                                                 attachNone=[(self.labName, "right"), (self.labName, "bottom"),
                                                             (self.nameFld, "bottom"),
                                                             (self.labShrtNm, "right"), (self.labShrtNm, "bottom"), 
                                                             (self.dimFld, "bottom"), 
                                                             (self.button, "top"), (self.button, "left")])

        def refresh(self):
            cmds.textField(self.nameFld, e=True, text=self.projName)
            cmds.textField(self.dimFld, e=True, text=self.projDim)

        def createNewProject(self):
            self.projName = cmds.textField(self.nameFld, q=True, text=True)
            self.projDim = cmds.textField(self.dimFld, q=True, text=True)
            
            self.runEvent("create", self.projName, self.projDim)


    class loadUC(UserControl):
        def __init__(self, parent):
            UserControl.__init__(self, parent)
            self.name = "load"
            self.projName = ""
            self.path = ""
            self.projects = []
            self.folderMenuItem = []
            self.layout = ""

        def load(self):
            self.layout = cmds.formLayout(self.name, parent=self.parentLay, bgc=hexToRGB(0x5a5a5a))
            self.button = cmds.button(parent=self.layout, label="Load", c=Callback(self.clickLoad), bgc=hexToRGB(0x5d5d5d))
            self.menu = cmds.optionMenu('droplist', parent=self.layout, w=150, cc=Callback(self.changeFolder), bgc=hexToRGB(0x7d7d7d))
            self.refresh()
            cmds.formLayout(self.layout, e=True, attachForm=[(self.menu, "left", 5), (self.button, "bottom", 5), (self.button, "right", 5)], 
                                                 attachNone=[(self.button, "left"), (self.button, "top"), (self.menu, "bottom"), (self.menu, "right")], 
                                                 attachPosition=[(self.menu, "top", 5, 30), (self.menu, "right", 5, 100)])

        def changePath(self, path):
            self.path = path
            if self.layout != "":
                self.refresh()

        def refresh(self):
            for x in self.folderMenuItem:
                cmds.deleteUI(x)
            self.folderMenuItem = []
            self.folderMenuItem.append(cmds.menuItem(label='-', parent=self.menu ))
            self.listFolder()
            for p in self.projects:
                self.folderMenuItem.append(cmds.menuItem( label=p, parent=self.menu ))
        
        def clickLoad(self):
            self.runEvent("load", self.projName)
            

        def changeFolder(self, *args):
            self.projName = cmds.optionMenu(self.menu, q=True, v=True)

        def listFolder(self):
            if not os.path.isdir(self.path):
                cmds.warning("Server folder not found")
                return
            self.projects = [x for x in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, x, ".pil", "project.pil"))]

    class infoUC(UserControl):
        def __init__(self, parent):
            UserControl.__init__(self, parent)
            self.name = "info"
            self.project = None
        def load(self):
            self.layout = cmds.formLayout(self.name, parent=self.parentLay, bgc=hexToRGB(0x7a7a7a), h=150)
            self.txName = cmds.text(parent=self.layout, label="test Name")
            self.txDim = cmds.text(parent=self.layout, label="test Dim")
            self.txServPath = cmds.text(parent=self.layout, label="test Server Path")
            self.txAuthor = cmds.text(parent=self.layout, label="test Author")
            self.txDate = cmds.text(parent=self.layout, label="test creation Date")

            cmds.formLayout(self.layout, e=True, attachForm=[(self.txName, "left", 10), (self.txName, "top", 10),
                                                             (self.txDim, "left", 10), 
                                                             (self.txServPath, "left", 10), 
                                                             (self.txAuthor, "left", 10), 
                                                             (self.txDate, "left", 10)], 
                                                 attachNone=[(self.txName, "right"), (self.txName, "bottom"),
                                                             (self.txDim, "right"), (self.txDim, "bottom"),
                                                             (self.txServPath, "right"), (self.txServPath, "bottom"),
                                                             (self.txAuthor, "right"), (self.txAuthor, "bottom"),
                                                             (self.txDate, "right"), (self.txDate, "bottom")],
                                                 attachControl=[(self.txDim, "top", 2, self.txName),
                                                                (self.txServPath, "top", 15, self.txDim),
                                                                (self.txAuthor, "top", 10, self.txServPath),
                                                                (self.txDate, "top", 2, self.txAuthor)])

        def setProject(self, project):
            self.project = project
            self.refresh()

        def refresh(self):
            if self.project is None:
                return
            cmds.text(self.txName, e=True, label=self.project.name)
            cmds.text(self.txDim, e=True, label=self.project.diminutive)
            cmds.text(self.txServPath, e=True, label=self.project.path.server)
            cmds.text(self.txAuthor, e=True, label=self.project.author)
            cmds.text(self.txDate, e=True, label=self.project.date)
            

    class localPathUC(UserControl):
        def __init__(self, parent):
            UserControl.__init__(self, parent)
            self.name = "localPath" + self.name
            self.path = "S:/"
        def load(self):
            self.layout = cmds.formLayout(self.name, parent=self.parentLay, bgc=hexToRGB(0x5a5a5a))
            self.pathLay = cmds.text(label=self.path, parent=self.layout, bgc=hexToRGB(0x9a9a9a), al="left")
            self.folderBtn = cmds.iconTextButton('folderBtn', parent=self.layout, style='iconOnly', image1=getIcon("folder"), label='Option', w=22, h=22, sic=True, bgc=hexToRGB(0x4a4a4a),
                                              c=Callback(self.selectDir))
            self.createTreeBtn = cmds.iconTextButton('createTreeBtn', parent=self.layout, style='iconOnly', image1=getIcon("createFolder"), label='Option', w=22, h=22, sic=True, bgc=hexToRGB(0x4a4a4a),
                                              c=Callback(self.createTree))
            cmds.formLayout(self.layout, e=True, attachForm=[(self.pathLay, "top", 5), (self.pathLay, "bottom", 5), (self.pathLay, "left", 5),
                                                             (self.folderBtn, "top", 5), (self.folderBtn, "bottom", 5), (self.folderBtn, "right", 5),
                                                             (self.createTreeBtn, "top", 5), (self.createTreeBtn, "bottom", 5),], 
                                                 attachControl=[(self.pathLay, "right", 5, self.createTreeBtn), (self.createTreeBtn, "right", 5, self.folderBtn)],
                                                 attachNone=[(self.folderBtn, "left"), (self.createTreeBtn, "left")])

        def selectDir(self):
            multipleFilters = "Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)"
            # p = cmds.fileDialog2(fileFilter=multipleFilters, dialogStyle=2, dir="Q:/", fm=3)
            self.path = cmds.fileDialog2(dialogStyle=1, dir=self.path, fm=3)[0]
            self.refresh()
            self.runEvent("changeDir", self.path)
        def createTree(self):
            pass

        def refresh(self):
            cmds.text(self.pathLay, e=True, label=self.path)

    class saveExitUC(UserControl):
        def __init__(self, parent):
            UserControl.__init__(self, parent)
            self.name = "saveExit" + self.name
        def load(self):
            self.layout = cmds.formLayout(self.name, parent=self.parentLay, bgc=hexToRGB(0x5a5a5a))
            self.svBtn = cmds.button(parent=self.layout, label="Save and Exit", c=Callback(self.runEvent, "save"), bgc=hexToRGB(0x7d7d7d))
            self.calBtn = cmds.button(parent=self.layout, label="Cancel", c=Callback(self.runEvent, "cancel"), bgc=hexToRGB(0x7d7d7d))

            cmds.formLayout(self.layout, e=True, attachForm=[(self.svBtn, "top", 5), (self.svBtn, "bottom", 5),
                                                             (self.calBtn, "top", 5), (self.calBtn, "bottom", 5),
                                                             (self.calBtn, "left", 5), (self.svBtn, "right", 5)],
                                                 attachControl=[(self.calBtn, "right", 5, self.svBtn)],
                                                 attachNone=[(self.svBtn, "left")])


    class initializeProjectUC(UserControl):

        def __init__(self, parent):
            UserControl.__init__(self, parent)
            self.name = "initializeProjectUC" + self.name
            self.tabs = ""
            self.edition = True
            self.project = Project("new Project", Path())
        def load(self):
            self.layout = cmds.formLayout(self.name, parent=self.parentLay, bgc=hexToRGB(0x5a5a5a))
            
            self.infoUC = DefineProjectUC.infoUC(self)
            self.pathUC = DefineProjectUC.workPathUC(self)
        
            if cmds.tabLayout(self.tabs, q=True, ex=True):
                cmds.deleteUI(self.tabs)
            self.tabs = cmds.tabLayout('createLoad', parent=self.layout, h=150)
            self.loadTab = DefineProjectUC.loadUC(self.tabs)
            self.newTab = DefineProjectUC.newUC(self.tabs)
            
            self.pathUC.eventHandler("changeDir", self.changeWorkDir)
            self.loadTab.eventHandler("load", self.loadProject)
            self.newTab.eventHandler("create", self.createNewProject)
            
            if self.project is not None:
                self.loadTab.changePath(self.project.path.server)
            else:
                self.loadTab.changePath("")

            self.infoUC.load()
            self.newTab.load()
            self.loadTab.load()
            self.pathUC.load()


            cmds.formLayout(self.layout, e=True, attachForm=[(self.infoUC, "bottom", 0), (self.infoUC, "left", 0), (self.infoUC, "right", 0), (self.infoUC, "left", 0),
                                                             (self.tabs, "bottom", 0), (self.tabs, "left", 0), (self.tabs, "right", 0),
                                                             (self.pathUC.layout, "top", 0), (self.pathUC.layout, "left", 0), (self.pathUC.layout, "right", 0)],
                                                 attachNone=[(self.pathUC.layout, "bottom")],
                                                 attachControl=[((self.tabs, "top", 0, self.pathUC.layout))])
            self.refresh()
        
        def refresh(self):
            cmds.tabLayout(self.tabs, e=True, vis=self.edition)
            cmds.formLayout(self.pathUC.layout, e=True, vis=self.edition)
            cmds.formLayout(self.infoUC.layout, e=True, vis=(not self.edition))
            self.infoUC.setProject(self.project)
            self.infoUC.refresh()

        def setEdition(self, val):
            self.edition = val
            self.refresh()

        def changeWorkDir(self, p):
            self.project.path.server = p
            
            self.loadTab.changePath(self.project.path.server)
            self.loadTab.refresh()

        def loadProject(self, name):
            if len(self.project.path.server) == 0:
                cmds.warning("The working directory is empty")
                return
            if len(name) == 0:
                cmds.warning("Name invalide")
                return
            self.project.name = name
            self.project.readInfo()
            #TODO fetch data of the project
            self.setEdition(False)
            self.runEvent("loadProj", self.project)
        
        def createNewProject(self, name, dim):
            user = User()
            if len(self.project.path.server) == 0:
                cmds.warning("The working directory is empty")
                return
            if len(name) == 0:
                cmds.warning("Name is empty")
                return
            if len(dim) == 0:
                cmds.warning("Short name is empty")
                return
            if len(dim) > len(name):
                cmds.warning("Short name is Longer than name")
                return

            self.project.name = name
            self.project.diminutive = dim
            self.project.author = user.name
            self.project.makeServerFolderTree()
            self.setEdition(False)
            self.runEvent("loadProj", self.project)


        
        def setProj(self, proj):
            if proj is None:
                self.setEdition(True)
                self.project = Project("", Path())
            else:
                self.project = proj
                self.setEdition(False)

    
    def __init__(self, parent):
        UserControl.__init__(self, parent)
        self.name = "DefineProjectUC"
        self.selected = None

    def load(self):
        UserControl.create(self)
        cmds.formLayout(self.layout, e=True, bgc=hexToRGB(0x4a4a4a))

        self.views = {}
        self.views["projects"] = TreeUC(self, multiSelect=False)
        # self.views["workPath"] = DefineProjectUC.workPathUC(self)
        self.views["initInfo"] = DefineProjectUC.initializeProjectUC(self)
        self.views["localPath"] = DefineProjectUC.localPathUC(self)
        self.views["exit"] = DefineProjectUC.saveExitUC(self)

        self.projects = Project.fetchProjects()
        self.views["projects"].addItem("New project", None)
        
        self.projects.sort(key=lambda x: x.name)
        
        for p in self.projects:
            self.views["projects"].addItem(p.name, p)
        self.views["projects"].eventHandler("changeSelection", self.changeSelect)
        self.views["exit"].eventHandler("save", self.saveExit)
        self.views["initInfo"].eventHandler("loadProj", self.loadNewProject)
        self.views["localPath"].eventHandler("changeDir", self.changeLocalDir)


        for key, view in self.views.items():
            view.load()

        # cmds.formLayout(self.views["projects"].layout, e=True, bgc=hexToRGB(0x3a3a3a))
        self.views["projects"].attach(top=Attach.FORM, bottom=Attach.FORM, left=Attach.FORM, right=(Attach.POS, 33), margin=5)
        self.views["initInfo"].attach(top=Attach.FORM, bottom=Attach.NONE, left=(Attach.CTRL, self.views["projects"]), right=Attach.FORM, margin=5)
        self.views["localPath"].attach(top=(Attach.CTRL, self.views["initInfo"]), bottom=Attach.NONE, left=(Attach.CTRL, self.views["projects"]), right=Attach.FORM, margin=(20,5,5,5))
        self.views["exit"].attach(top=Attach.NONE, bottom=Attach.FORM, left=Attach.NONE, right=Attach.FORM, margin=5)


        self.applyAttach()

    def changeSelect(self, p):
        self.selected = p[0]
        self.views["initInfo"].setProj(p[0])
        self.views["localPath"].path = p[0].path.local
        self.views["localPath"].refresh()
 
    def changeLocalDir(self, path):
        if self.selected is None:
            return
        self.selected.path.local = path

    def updateLocalPath(self, p):
        pass

    def loadNewProject(self, project):
        self.projects.append(project)
        self.views["projects"].addItem(project.name, project)
        self.views["projects"].load()

    def saveExit(self):
        Project.writeAllProjectsInPrefs(self.projects)
        self.runEvent("close")