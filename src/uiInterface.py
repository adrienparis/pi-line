import os
from pymel.all import *
import maya.cmds as cmds

# import userControls
from userControls import *

import asset as astPL
from project import *

class Attach():
    NONE = 0
    FORM = 1
    POS = 2
    CTRL = 3

def getIcon(icon):
    img = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo", icon + ".png")
    if os.path.isfile(img):
        return img
    img = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo",  "noPicture.png")
    if os.path.isfile(img):
        return img

def hexToRGB(h):
    rgb = []
    rgb.append((round(h / 0x10000) % 0x100) / 0x100)
    rgb.append((round(h / 0x100) % 0x100) / 0x100)
    rgb.append(float(h % 0x100) / 0x100)
    return rgb

# class userControl():
#     def __init__(self, parent):
#         self.parent = parent
#         self.command = {}
#         self.name = "UC"
#     def create(self):
#         self.layout = cmds.formLayout(parent=self.parent, bgc=hexToRGB(0xa00000), h=30)
#         print("create userControl : " + self.__class__.__name__)
#         print("/!\\ Not implemented")
#     @staticmethod
#     def sideToValue(side):
#         if side == "top" : return 0
#         if side == "bottom" : return 1
#         if side == "left" : return 2
#         if side == "right" : return 3


#     def visibility(self, vis):
#         cmds.formLayout(self.layout, e=True, vis=vis)
#     # Attach.NONE, Attach.FORM, (Attach.POS, pos), (Attach.CTRL, ctrl), margin
#     def attach(self, margin=(0), **kwargs):

#         #check if margin is (0), (0,0) or (0,0,0,0)
#         side = [0,0,0,0]
#         if type(margin) is int:
#             side = [margin, margin, margin, margin]
#         if type(margin) is tuple and len(margin) == 2:
#             side = [margin[0], margin[0], margin[1], margin[1]]
#         if type(margin) is tuple and len(margin) == 4:
#             side = [margin[0], margin[1], margin[2], margin[3]]

#         self.an = []
#         self.af = []
#         self.ap = []
#         self.ac = []

#         for key, value in kwargs.items():
#             if type(value) is int:
#                 if value == Attach.NONE:
#                     self.an.append((self.layout, key))
#                 if value == Attach.FORM:
#                     self.af.append((self.layout, key, side[userControl.sideToValue(str(key))]))
#             elif type(value) is tuple and len(value) == 2:
#                 if value[0] == Attach.POS:
#                     self.ap.append((self.layout, key, side[userControl.sideToValue(str(key))], value[1]))
#                 if value[0] == Attach.CTRL:
#                     if type(value[1]) is str:
#                         self.ac.append((self.layout, key, side[userControl.sideToValue(str(key))], value[1]))
#                     elif isinstance(value[1], userControl):
#                         self.ac.append((self.layout, key, side[userControl.sideToValue(str(key))], value[1].layout))

#     def setParent(self, parent):
#         cmds.formLayout(self.layout, edit=True, parent=parent)

#     def reload(self):
#         print("reload " + self.__class__.__name__)
#         print("/!\\ Not implemented")
#     def refresh(self):
#         print("refresh " + self.__class__.__name__)
#         print("/!\\ Not implemented")
#     def eventHandler(self, event, c, *args):
#         if not event in self.command:
#             self.command[event] = []
#         self.command[event].append((c, args))
#     def runEvent(self, event, *args):
#         if not event in self.command:
#             return
#         for c in self.command[event]:
#             if c[0] is None:
#                 # cmds.error("Event \"" + event + "\" call a function not implemented yet -WIP-")
#                 print("Event \"" + event + "\" call a function not implemented yet -WIP-")
#                 continue
#             a = c[1] + args
#             c[0](*a)

#     def __str__():
#         return self.layout

class iconButtonUC(userControl):
    def __init__(self):
        userControl.__init__(self)
        self.button = cmds.iconTextButton('btnSetServerPath', parent=self.layout, style='iconOnly', image1=getIcon("folder"), label='Switch view', w=22, h=22, sic=True, bgc=[0.45,0.45,0.45])


class tileUC(userControl):

    baseColor = [0.4,0.4,0.4]
    selectedColor = [0.32,0.52,0.65]
    selected = False
    function = None
    style = 'iconAndTextVertical'

    def __init__(self, asset, parent, sizeImage=100):
        userControl.__init__(self, parent)
        self.asset = asset
        self.sizeImage = sizeImage
        self.name = asset.name + "Tile" + self.name

    def create(self):
        self.layout = cmds.formLayout(parent=self.parent, h=30)
        self.btnLay = cmds.iconTextButton(self.asset.name + "Tile", parent=self.layout, style=self.style, image1=self.asset.image,
                            label=self.asset.name, w=self.sizeImage, h=self.sizeImage, sic=True, c=Callback(self.clickCommand), bgc=self.selectedColor, ebg=self.selected)
        img = "denied"
        if self.asset.state == 0:        
            img = "check"
        if self.asset.state == 1:        
            img = "download"
        if self.asset.state == 2:        
            img = "upload"


        self.iconLay = cmds.image(parent=self.layout, h=15, w=15, image=getIcon(img), bgc=hexToRGB(0x1d1d1d))
        cmds.formLayout(self.layout, edit=True,
                        attachForm=[(self.btnLay, "top", 2), (self.btnLay, "bottom", 2), (self.btnLay, "left", 2), (self.btnLay, "right", 2), 
                                    (self.iconLay, "top", 5), (self.iconLay, "right", 5)],
                        attachNone=[(self.iconLay, "left"), (self.iconLay, "bottom")])

    def selection(self, b):
        self.selected = b
        cmds.iconTextButton(self.btnLay, e=True, ebg=self.selected)

    def clickCommand(self):
        self.mods = cmds.getModifiers()
        self.runEvent("click", self, self.mods)

class assetTileUC(userControl):
    styleIcon = 'iconAndTextVertical'
    sizeImage = 100

    def __init__(self, parent):
        userControl.__init__(self, parent)
        #must be an array of categorie, or a class that encompass all the categories
        self.project = None
        self.assets = None
        self.selected = []

    def setProject(self, project):
        self.project = project
        self.assets = self.project.assets

    def clickCommand(self, tile, mods):
        for t in self.selected:
            if (mods != 1 or tile.asset.category.name != t.asset.category.name):
                t.selection(False)
        if mods != 1:
            self.selected = []
        if mods <= 1:
            if tile.selected:
                tile.selection(False)
                self.selected.remove(tile)
            else:
                tile.selection(True)
                self.selected.append(tile)
        self.runEvent("changeTile", self.selected)

    def newAssetCommand(self, c):
        print("Create New Asset")
        print(c.name)
    
        result = cmds.promptDialog(
                        title='New Asset - ' + c.name,
                        message='Enter name:',
                        button=['OK', 'Cancel'],
                        defaultButton='OK',
                        cancelButton='Cancel',
                        dismissString='Cancel')
        if result != 'OK': return
        name = cmds.promptDialog(query=True, text=True)
        a = astPL.Asset(c, name)
        a.create(c.path)
        a.fetchAssetData()
        c.assets.append(a)
        self.reload()

    def resizeTilesView(self, c):
        h = cmds.scrollLayout(self.shelf[c][0], q=True, h=True)
        w = cmds.scrollLayout(self.shelf[c][0], q=True, w=True)
        size = math.trunc((w - 4) / self.sizeImage)
        if size == 0:
            return

        nbChild = cmds.gridLayout(self.shelf[c][1], q=True, nch=True )
        rows = max((nbChild - 1) / size + 1, 1)
        if h < rows * self.sizeImage:
            size = math.trunc((w - 16) / self.sizeImage)
            if size == 0:
                return

            nbChild = cmds.gridLayout(self.shelf[c][1], q=True, nch=True )
            rows = max((nbChild - 1) / size + 1, 1)

        cmds.gridLayout(self.shelf[c][1], e=True, numberOfColumns=size )
        cmds.gridLayout(self.shelf[c][1], e=True, numberOfRows= rows )


    def setAsset(self, assets):
        #TODO check if it's an Assets class
        self.assets = assets

    def create(self):
        self.layout = cmds.formLayout('AssetTileUC', parent=self.parent)

        
        self.tabs = cmds.tabLayout('Categories', snt=True, parent=self.layout)
        cmds.tabLayout(self.tabs, e=True, ntc='AMui.newTabAsset("{0}")'.format(self.tabs))
        
        self.shelf = {}

        # print(self.assets.serverPath)
        self.reload()
        cmds.formLayout(self.layout, edit=True, attachForm=[(self.tabs, 'top', 0),(self.tabs, 'bottom', 0),(self.tabs, 'left', 0), (self.tabs, 'right', 0)])
        return self.layout

    def reload(self):        
        for s in list(self.shelf.values()):
            print(s[0])
            cmds.deleteUI(s[0])


        for c in self.assets.categories:
            scrollLayout = cmds.scrollLayout( c.name, parent=self.tabs,
                                        horizontalScrollBarThickness=160,
                                        verticalScrollBarThickness=16,
                                        cr=True)
            assetColumn = cmds.gridLayout(c.name + "Grid", numberOfColumns=3, cr=False, ag=True, cellWidthHeight=(self.sizeImage, self.sizeImage))
            self.shelf[c] = [scrollLayout, assetColumn]
            cmds.scrollLayout(self.shelf[c][0], e=True, rc=Callback(self.resizeTilesView, c))
            
            current_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
            newTiles = cmds.iconTextButton(c.name + "NewTile", parent=self.shelf[c][1], style=self.styleIcon, image1=getIcon("add"),
                                label="New Asset", w=self.sizeImage, h=self.sizeImage, sic=True, c=Callback(self.newAssetCommand, c) )
            for a in c.assets:
                t = tileUC(a, self.shelf[c][1], self.sizeImage)
                t.eventHandler("click", self.clickCommand)
                t.create()

class assetTreeUC(userControl):
    pass



class cupboardUC(userControl):
    colMinSize = 225
    propCol1 = 3
    propCol2 = 2
    propCol3 = 2

    def __init__(self, parent):
        userControl.__init__(self, parent)
        self.project = None
        self.assets = None
        self.selected = []
        self.viewVert = False
        

    # TODO When the width is large enough display 3 columns in horizontal, When it's to small
    # it's display the 3 column inside one column
    def resizeView(self):
        width = cmds.scrollLayout(self.scrLay, q=True, w=True)
        height = cmds.scrollLayout(self.scrLay, q=True, h=True) -5
        sizeCol = math.trunc(width - 16) / 3
        if sizeCol < self.colMinSize:
            small = True
        else:
            small = False
            cmds.formLayout(self.horizontalFrame, e=True, h=height)

        if small is not self.viewVert:
            self.viewVert = small
            if self.viewVert:
                self.setViewToVertical()
            else:
                self.setViewToHorizontal()
        # cmds.gridLayout(self.gridLay, e=True, numberOfColumns=nCol, numberOfRows=nRow, cw=sizeCol)

    def create(self):
        
        self.layout = cmds.formLayout('cupboardUC', parent=self.parent, bgc=hexToRGB(0x444444))

        self.scrLay = cmds.scrollLayout( "cupBoardScrollLayout", parent=self.layout,
                                        horizontalScrollBarThickness=160,
                                        verticalScrollBarThickness=16,
                                        childResizable=True,
                                        cr=True)
        self.horizontalFrame = cmds.formLayout('horizontalFrame', parent=self.scrLay, bgc=hexToRGB(0x3b3b3b), vis=True)
        self.verticalFrame = cmds.formLayout('verticalFrame', parent=self.scrLay, bgc=hexToRGB(0x3b3b3b), vis=True, h=1000)

        self.views = {}

        #initialize the differents userControls and stock them in a dictionnary
        self.views["project"] = ProjectUC(self.horizontalFrame)
        self.views["explorer"] = ExplorerUC(self.horizontalFrame)
        self.views["detail"] = DetailUC(self.horizontalFrame)
        self.views["version"] = VersionUC(self.horizontalFrame)
        self.views["sync"] = SyncUC(self.horizontalFrame)
        self.views["versInfo"] = VersInfonUC(self.horizontalFrame)
        self.views["wip"] = WipUC(self.horizontalFrame)
        self.views["import"] = ImportUC(self.horizontalFrame)
        
        # Attach function to events
        # TODO replace [None] by actual fonction
        self.views["project"].eventHandler("changeProject", self.changeProject)
        self.views["project"].eventHandler("optionBtn", self.commandProjectOption)
        self.views["explorer"].eventHandler("changeItem", self.changeSelection)
        self.views["version"].eventHandler("changeItem", self.changeVersion)
        self.views["sync"].eventHandler("download", self.commandDownload)
        self.views["sync"].eventHandler("delete", None)
        self.views["import"].eventHandler("edit", None)
        self.views["import"].eventHandler("saveVersion", None)
        self.views["import"].eventHandler("publish", None)
        self.views["import"].eventHandler("importRaw", None)
        self.views["import"].eventHandler("importRef", None)
        self.views["import"].eventHandler("importProxy", None)
        
        #Create and load all the interfaces
        self.views["project"].create()
        self.views["explorer"].create()
        self.views["detail"].create()
        self.views["version"].create()
        self.views["sync"].create()
        self.views["versInfo"].create()
        self.views["wip"].create()
        self.views["import"].create()
        self.scrLay = cmds.scrollLayout( self.scrLay, e=True, rc=Callback(self.resizeView))
        cmds.formLayout(self.layout, edit=True,
                        attachForm=[(self.scrLay, 'top', -2),(self.scrLay, 'bottom', -2),(self.scrLay, 'left', -2), (self.scrLay, 'right', -2)])

        
        self.views["project"].setLastProject()
        self.resizeView()

    def setViewToHorizontal(self):
        if len(self.views) == 0:
            return
        col1 = (self.propCol1 * 100) / (self.propCol1 + self.propCol2 + self.propCol3)
        col2 = ((self.propCol1 + self.propCol2) * 100)/ (self.propCol1 + self.propCol2 + self.propCol3)
        self.views["project"].attach(top=Attach.FORM, bottom=(Attach.NONE), left=Attach.FORM, right=(Attach.POS, col1), margin=(5,5,2,5))
        self.views["explorer"].attach(top=(Attach.CTRL, self.views["project"]), bottom=Attach.FORM, left=Attach.FORM, right=(Attach.POS, col1), margin=(5,5,2,5))
        self.views["detail"].attach(top=Attach.FORM, bottom=Attach.NONE, left=(Attach.POS, col1), right=(Attach.POS, col2), margin=5)
        self.views["version"].attach(top=(Attach.CTRL, self.views["detail"]),bottom=(Attach.CTRL, self.views["sync"]), left=(Attach.POS, col1), right=(Attach.POS, col2), margin=5)
        self.views["sync"].attach(top=Attach.NONE, bottom=Attach.FORM, left=(Attach.POS, col1), right=(Attach.POS, col2), margin=5)
        self.views["versInfo"].attach(top=Attach.FORM, bottom=(Attach.CTRL, self.views["wip"]), left=(Attach.POS, col2), right=Attach.FORM, margin=5)
        self.views["wip"].attach(top=Attach.NONE, bottom=(Attach.CTRL, self.views["import"]), left=(Attach.POS, col2), right=Attach.FORM, margin=5)
        self.views["import"].attach(top=Attach.NONE, bottom=Attach.FORM, left=(Attach.POS, col2), right=Attach.FORM, margin=5)

        self.views["project"].setParent(self.horizontalFrame)
        self.views["explorer"].setParent(self.horizontalFrame)
        self.views["detail"].setParent(self.horizontalFrame)
        self.views["version"].setParent(self.horizontalFrame)
        self.views["sync"].setParent(self.horizontalFrame)
        self.views["versInfo"].setParent(self.horizontalFrame)
        self.views["wip"].setParent(self.horizontalFrame)
        self.views["import"].setParent(self.horizontalFrame)

        af = [] + self.views["project"].af + self.views["explorer"].af + self.views["detail"].af + self.views["version"].af + self.views["sync"].af + self.views["versInfo"].af + self.views["wip"].af + self.views["import"].af
        ap = [] + self.views["project"].ap + self.views["explorer"].ap + self.views["detail"].ap + self.views["version"].ap + self.views["sync"].ap + self.views["versInfo"].ap + self.views["wip"].ap + self.views["import"].ap
        ac = [] + self.views["project"].ac + self.views["explorer"].ac + self.views["detail"].ac + self.views["version"].ac + self.views["sync"].ac + self.views["versInfo"].ac + self.views["wip"].ac + self.views["import"].ac
        an = [] + self.views["project"].an + self.views["explorer"].an + self.views["detail"].an + self.views["version"].an + self.views["sync"].an + self.views["versInfo"].an + self.views["wip"].an + self.views["import"].an

        cmds.formLayout(self.verticalFrame, edit=True, vis=False)
        cmds.formLayout(self.horizontalFrame, edit=True, vis=True,
                        attachForm=af,
                        attachPosition=ap,
                        attachControl=ac,
                        attachNone=an)

    def setViewToVertical(self):
        if len(self.views) == 0:
            return
        self.views["project"].attach(top=Attach.FORM, bottom=(Attach.NONE), left=Attach.FORM, right=Attach.FORM, margin=5)
        self.views["explorer"].attach(top=(Attach.CTRL, self.views["project"]), bottom=(Attach.POS, 55), left=Attach.FORM, right=Attach.FORM, margin=5)
        self.views["detail"].attach(top=(Attach.CTRL, self.views["explorer"]), bottom=Attach.NONE, left=Attach.FORM, right=Attach.FORM, margin=5)
        self.views["version"].attach(top=(Attach.CTRL, self.views["detail"]),bottom=(Attach.POS, 80), left=Attach.FORM, right=Attach.FORM, margin=5)
        self.views["sync"].attach(top=(Attach.CTRL, self.views["version"]), bottom=Attach.NONE, left=Attach.FORM, right=Attach.FORM, margin=5)
        self.views["versInfo"].attach(top=(Attach.CTRL, self.views["sync"]), bottom=Attach.NONE, left=Attach.FORM, right=Attach.FORM, margin=5)
        self.views["wip"].attach(top=(Attach.CTRL, self.views["versInfo"]), bottom=Attach.NONE, left=Attach.FORM, right=Attach.FORM, margin=5)
        self.views["import"].attach(top=(Attach.CTRL, self.views["wip"]), bottom=Attach.NONE, left=Attach.FORM, right=Attach.FORM, margin=5)

        self.views["project"].setParent(self.verticalFrame)
        self.views["explorer"].setParent(self.verticalFrame)
        self.views["detail"].setParent(self.verticalFrame)
        self.views["version"].setParent(self.verticalFrame)
        self.views["sync"].setParent(self.verticalFrame)
        self.views["versInfo"].setParent(self.verticalFrame)
        self.views["wip"].setParent(self.verticalFrame)
        self.views["import"].setParent(self.verticalFrame)

        af = [] + self.views["project"].af + self.views["explorer"].af + self.views["detail"].af + self.views["version"].af + self.views["sync"].af + self.views["versInfo"].af + self.views["wip"].af + self.views["import"].af
        ap = [] + self.views["project"].ap + self.views["explorer"].ap + self.views["detail"].ap + self.views["version"].ap + self.views["sync"].ap + self.views["versInfo"].ap + self.views["wip"].ap + self.views["import"].ap
        ac = [] + self.views["project"].ac + self.views["explorer"].ac + self.views["detail"].ac + self.views["version"].ac + self.views["sync"].ac + self.views["versInfo"].ac + self.views["wip"].ac + self.views["import"].ac
        an = [] + self.views["project"].an + self.views["explorer"].an + self.views["detail"].an + self.views["version"].an + self.views["sync"].an + self.views["versInfo"].an + self.views["wip"].an + self.views["import"].an

        cmds.formLayout(self.horizontalFrame, edit=True, vis=False)
        cmds.formLayout(self.verticalFrame, edit=True, vis=True,
                        attachForm=af,
                        attachPosition=ap,
                        attachControl=ac,
                        attachNone=an)

    def commandProjectOption(self):
        pass
        # print("creating tree")
        # if self.project is not None:
        #     self.project.createTreeTemplateLocal()

    def changeProject(self, p):
        if p == None:
            print("the project was not found")
            # cmds.error("Project do not exist")

            return
        self.project = p
        self.project.fetchAll()
        self.project.setProject()
        self.views["explorer"].setProject(p)
        self.views["explorer"].reload()

    def changeSelection(self, tiles):
        if len(tiles) == 1:
            self.selected = [tiles[0].asset]
            self.views["detail"].changeAsset(tiles[0].asset)
            self.views["detail"].refresh()

    def changeVersion(self, s):
        self.step = s

    def commandDownload(self):
        if len(self.selected) > 0:
            if self.step == 4:
                self.selected[0].download()
                self.selected[0].state = 0
            else:
                self.selected[0].downloadStep(self.step)
                self.selected[0].state = 2
        self.views["explorer"].refresh()
        #TODO remove the line below
        self.views["explorer"].reload()


    def attachViewTo(self, layout, parent):
        print("attach " + layout + " to " + self.views[parent].layout)
        cmds.formLayout(layout, e=True, parent=self.views[parent].layout)
        cmds.formLayout(self.views[parent], edit=True,
                        attachForm=[(layout, 'top', 5),(layout, 'bottom', 5),(layout, 'left', 5), (layout, 'right', 5)])


    def reload(self):
        self.colProj.reload()
    def refresh(self):
        self.colProj.reload()

class ProjectUC(userControl):
    projects = []

    def __init__(self, parent):
        userControl.__init__(self, parent)
        self.projects = Project.fetchProjects()
        self.eventHandler("optionBtn", self.option)
    def create(self):
        self.layout = cmds.formLayout('ProjectUC', parent=self.parent)
        current_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
        
        self.menu = cmds.optionMenu('droplist', parent=self.layout, w=20, cc=Callback(self.changeProject), bgc=hexToRGB(0x5d5d5d))
        self.projectsLabel = []
        self.projectsLabel.append(cmds.menuItem( "projEmpty", label='-' ))
        for i, p in enumerate(self.projects):
            self.projectsLabel.append(cmds.menuItem( "projName_" + str(i) ,label=p.name ))

        self.optionBtn = cmds.iconTextButton('optionBtn', parent=self.layout, style='iconOnly', image1=getIcon("gear"), label='Option', w=22, h=22, sic=True, bgc=hexToRGB(0x5d5d5d),
                                              c=Callback(self.runEvent, "optionBtn"))
        cmds.formLayout(self.layout, edit=True,
                        attachForm=[(self.menu, 'top', 0), (self.menu, 'left', 0), (self.optionBtn, 'top', 0), (self.optionBtn, 'right', 0)],
                        attachControl=[(self.menu, 'right', 5, self.optionBtn)],
                        attachNone=[(self.menu, 'bottom')])
    def changeProject(self, *args):
        v = cmds.optionMenu(self.menu, q=True, v=True)
        p = next((x for x in self.projects if x.name == v), None)
        self.runEvent("changeProject", p)

    def setLastProject(self):
        u = User()
        sel = 1
        if "lastProj" in u.prefs:
            for i, p in enumerate(self.projects):
                if p.name == u.prefs["lastProj"]:
                    sel = i + 2
                    break
        cmds.optionMenu(self.menu, e=True, sl=sel)
        if sel != 1:
            self.runEvent("changeProject", p)
    
    def option(self):
        pUC = defineProjectUC()
        pUC.create()
        self.refresh()
    
    def refresh(self):
        self.projects = Project.fetchProjects()
        cmds.deleteUI(self.menu)
        self.menu = cmds.optionMenu('droplist', parent=self.layout, w=20, cc=Callback(self.changeProject), bgc=hexToRGB(0x5d5d5d))
        self.projectsLabel = []
        self.projectsLabel.append(cmds.menuItem( "projEmpty", label='-' ))
        for i, p in enumerate(self.projects):
            self.projectsLabel.append(cmds.menuItem( "projName_" + str(i) ,label=p.name ))
        cmds.formLayout(self.layout, edit=True,
            attachForm=[(self.menu, 'top', 0), (self.menu, 'left', 0)],
            attachControl=[(self.menu, 'right', 5, self.optionBtn)],
            attachNone=[(self.menu, 'bottom')])

        self.projectsLabel *= 0

class ExplorerUC(userControl):

    def __init__(self, parent):
        userControl.__init__(self, parent)
        self.project = None
        self.assets = None
        self.tabs = ""
    def assetDisplay(self, parent, a):    
        layout = cmds.formLayout('Assets', parent=parent, numberOfDivisions=100)
        
        current_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
        ativ = assetTileUC(layout) #AssetTilesView(layout) # cmds.formLayout('assetViewSwitchTile', parent=layout, numberOfDivisions=100, bgc=[0.2,0.2,0.2])

        ativ.setAsset(a)
        ativ.create()
        ativ.eventHandler("changeTile", self.runEvent, "changeItem")
        atrv = assetTreeUC(layout)
        atrv.create()
        assetViewSwitchTree = cmds.iconTextButton('assetViewSwitchTree', parent=layout, style='iconOnly', image1=getIcon("list"), label='Switch view', w=22, h=22, sic=True, bgc=[0.45,0.45,0.45])
        assetViewSwitchTile = cmds.iconTextButton('assetViewSwitchTile', parent=layout, style='iconOnly', image1=getIcon("tiles"), label='Switch view', w=22, h=22, sic=True, bgc=[0.45,0.45,0.45])
        cmds.iconTextButton(assetViewSwitchTile, e=True, c='AMui.switchAssetView("{0}, {1}, {2}, {3}")'.format(assetViewSwitchTree, assetViewSwitchTile, ativ.layout, atrv.layout), vis=False)
        cmds.iconTextButton(assetViewSwitchTree, e=True, c='AMui.switchAssetView("{0}, {1}, {2}, {3}")'.format(assetViewSwitchTree, assetViewSwitchTile, ativ.layout, atrv.layout), vis=True)
        cmds.layout(ativ.layout, e=True, vis=True)
        cmds.layout(atrv.layout, e=True, vis=False)
        cmds.formLayout( layout, edit=True,
                        attachForm=[(assetViewSwitchTree, 'top', 2), (assetViewSwitchTree, 'right', 2),
                                    (assetViewSwitchTile, 'top', 2), (assetViewSwitchTile, 'right', 2),
                                    (ativ.layout, 'left', -2), (ativ.layout, 'bottom', -2), (ativ.layout, 'right', -2),
                                    (atrv.layout, 'left', -2), (atrv.layout, 'bottom', -2), (atrv.layout, 'right', -2)],
                        attachControl=[(ativ.layout, 'top', 2, assetViewSwitchTree),(atrv.layout, 'top', 2, assetViewSwitchTile)],
                        attachNone=[(assetViewSwitchTree, 'bottom'),(assetViewSwitchTree, 'left'),
                                    (assetViewSwitchTile, 'bottom'),(assetViewSwitchTile, 'left')])


        return layout


    def setProject(self, project):
        self.project = project

    def create(self):
        self.layout = cmds.formLayout('ExplorerUC', parent=self.parent, numberOfDivisions=100, bgc=hexToRGB(0x5d5d5d))
        
        self.reload()

    def reload(self):

        
        if cmds.tabLayout(self.tabs, q=True, ex=True):
            cmds.deleteUI(self.tabs)
        self.tabs = cmds.tabLayout('SceneFold', parent=self.layout)

        if self.project is None or self.project.categories is None:
            self.tabAssets = cmds.formLayout('Assets', numberOfDivisions=100, parent=self.tabs)
        else:
            #TODO REPLACE THAT!!!
            self.assetDisplay(self.tabs, self.project)
        self.tabShots = cmds.formLayout('Shots', numberOfDivisions=100, parent=self.tabs)

        cmds.formLayout(self.layout, e=True, 
                        attachForm=[(self.tabs, 'top', 0),(self.tabs, 'bottom', 0),(self.tabs, 'left', 0), (self.tabs, 'right', 0)])


class DetailUC(userControl):
    asset = None
    def create(self):
        self.layout = cmds.formLayout('detailUC', parent=self.parent)
        self.name = cmds.text('name', label='Empty', font="boldLabelFont", align="left", rs=False, ann="char")
        self.shotUses = cmds.text('shotUses', label='Apparition :  shots', align="left")
        cmds.formLayout(self.layout, e=True, attachForm=[(self.name, 'top', 0), (self.name, 'left', 0), (self.name, 'right', 0), (self.shotUses, 'left', 0), (self.shotUses, 'right', 0)], attachControl=[(self.shotUses, 'top', 0, self.name)])
    def changeAsset(self, asset):
        self.asset = asset
    
    def refresh(self):
        if self.asset == None:
            return
        cmds.text(self.name, e=True, label=self.asset.name.capitalize() , ann=self.asset.category.name)
        cmds.text(self.shotUses, e=True, label="Apparition : " + str(self.asset.shotUses) + " shots")

class VersionUC(userControl):
    def create(self):
        self.layout = cmds.formLayout('VersionUC', parent=self.parent)
        
        self.plop = cmds.columnLayout( adjustableColumn=True )
        self.rc = cmds.radioCollection(parent=self.layout)
        user = User()
        # 1:mod     2:rig   3:surf
        self.cat = (user.profil == "MODELER") * 1 + (user.profil == "RIGGER") * 2 + (user.profil == "ANIMATOR") * 2 + (user.profil == "SURFACER") * 3
        cmds.radioButton( parent=self.plop, label='mod', align='left', onc=Callback(self.runEvent, "changeRadioButton", 1), sl=(self.cat==1))
        cmds.radioButton( parent=self.plop, label='rig', align='center', onc=Callback(self.runEvent, "changeRadioButton", 2), sl=(self.cat==2))
        cmds.radioButton( parent=self.plop, label='surf', align='right', onc=Callback(self.runEvent, "changeRadioButton", 3), sl=(self.cat==3))
        cmds.radioButton( parent=self.plop, label='All', align='right', onc=Callback(self.runEvent, "changeRadioButton", 4), sl=(self.cat==4))
        self.eventHandler("changeRadioButton", self.changeCategory)
        self.runEvent("changeRadioButton", self.cat)
        
    def changeCategory(self, cat):
        self.cat = cat
        self.runEvent("changeItem", self.cat)


class SyncUC(userControl):
    def create(self):
        self.layout = cmds.formLayout('syncUC', parent=self.parent, w=200)
        self.downloadButton = cmds.button(label="Download", parent=self.layout, c=Callback(self.runEvent, "download"), bgc=hexToRGB(0x5d5d5d))
        self.deleteButton = cmds.button(label="Delete", parent=self.layout, c=Callback(self.runEvent, "delete"), bgc=hexToRGB(0x5d5d5d))
        cmds.formLayout(self.layout, e=True, attachForm=[(self.downloadButton, 'top', 5), (self.downloadButton, 'bottom', 5),  (self.downloadButton, 'left', 5),
                                                         (self.deleteButton, 'top', 5), (self.deleteButton, 'bottom', 5), (self.deleteButton, 'right', 5)],
                                             attachPosition=[(self.deleteButton, 'left', 5, 50), (self.downloadButton, 'right', 5, 50)])

class VersInfonUC(userControl):
    pass

class WipUC(userControl):
    pass

class ImportUC(userControl):
    def create(self):
        self.layout = cmds.formLayout('ImportUC', parent=self.parent, w=130)
        self.pubLay = cmds.formLayout('pubLay', parent=self.layout, bgc=hexToRGB(0x373737))
        self.impLay = cmds.formLayout('impLay', parent=self.layout, bgc=hexToRGB(0x373737))
        self.publishBtn = cmds.button(parent=self.pubLay, label="Publish", c=Callback(self.runEvent, "publish"), bgc=hexToRGB(0x5d5d5d))
        self.OpenBtn = cmds.button(parent=self.pubLay, label="Open", c=Callback(self.runEvent, "open"), bgc=hexToRGB(0x5d5d5d))
        self.SaVeBtn = cmds.button(parent=self.pubLay, label="Save Version", c=Callback(self.runEvent, "saveVersion"), bgc=hexToRGB(0x5d5d5d))
        self.impRawBtn = cmds.button(parent=self.impLay, label="Import", c=Callback(self.runEvent, "importRaw"), bgc=hexToRGB(0x5d5d5d))
        self.impRefBtn = cmds.button(parent=self.impLay, label="Ref", c=Callback(self.runEvent, "importRef"), bgc=hexToRGB(0x5d5d5d))
        self.impProBtn = cmds.button(parent=self.impLay, label="Proxy", c=Callback(self.runEvent, "importProxy"), bgc=hexToRGB(0x5d5d5d))
        cmds.formLayout(self.pubLay, e=True,
                        attachForm=[(self.publishBtn, 'top', 4), (self.publishBtn, 'bottom', 4), (self.publishBtn, 'right', 4),
                                    (self.OpenBtn, 'top', 4), (self.OpenBtn, 'bottom', 4), (self.OpenBtn, 'left', 4),
                                    (self.SaVeBtn, 'top', 4), (self.SaVeBtn, 'bottom', 4)],
                        attachPosition=[(self.publishBtn, 'left', 2, 69), (self.OpenBtn, 'right', 2, 25),
                                        (self.SaVeBtn, 'left', 2, 25), (self.SaVeBtn, 'right', 2, 69)])
        cmds.formLayout(self.impLay, e=True,
                        attachForm=[(self.impRawBtn, 'top', 4), (self.impRawBtn, 'bottom', 4), (self.impRawBtn, 'left', 4),
                                    (self.impRefBtn, 'top', 4), (self.impRefBtn, 'bottom', 4),
                                    (self.impProBtn, 'top', 4), (self.impProBtn, 'bottom', 4), (self.impProBtn, 'right', 4)],
                        attachPosition=[(self.impProBtn, 'left', 2, 66), (self.impRawBtn, 'right', 2, 40), 
                                    (self.impRefBtn, 'right', 2, 66), (self.impRefBtn, 'left', 2, 40)])



        cmds.formLayout(self.layout, e=True,
                        attachForm=[
                                    (self.pubLay, 'bottom', 5),  (self.pubLay, 'left', 5), (self.pubLay, 'right', 5),
                                    (self.impLay, 'top', 5), (self.impLay, 'left', 5), (self.impLay, 'right', 5)],
                        attachControl=[(self.impLay, 'bottom', 5, self.pubLay)],
                        attachNone=[(self.pubLay, 'top')])

class defineProjectUC(userControl):
    def __init__(self):

        if cmds.workspaceControl(u"Manage Projects", exists=1):
            cmds.deleteUI(u"Manage Projects")
        
        self.parent = cmds.workspaceControl(u"Manage Projects", retain=False, iw=100, ih=200, floating=True)
        userControl.__init__(self, self.parent)

    def create(self):
        userControl.create(self)
        self.btnSave = cmds.button(parent=self.layout, label="Save & Exit", c=Callback(self.runEvent, "saveExit"), bgc=hexToRGB(0x5d5d5d))
        
        
        self.btnSetServerPath = cmds.iconTextButton('btnSetServerPath', parent=self.layout, style='iconOnly', image1=getIcon("folder"), label='Switch view', w=22, h=22, sic=True, bgc=[0.45,0.45,0.45])
        self.btnServerTree = cmds.iconTextButton('btnServerTree', parent=self.layout, style='iconOnly', image1=getIcon("createFolder"), label='Switch view', w=22, h=22, sic=True, bgc=[0.45,0.45,0.45])
        self.btnSetLocalPath = cmds.iconTextButton('btnSetLocalPath', parent=self.layout, style='iconOnly', image1=getIcon("folder"), label='Switch view', w=22, h=22, sic=True, bgc=[0.45,0.45,0.45])
        self.btnLocalTree = cmds.iconTextButton('btnLocalTree', parent=self.layout, style='iconOnly', image1=getIcon("createFolder"), label='Switch view', w=22, h=22, sic=True, bgc=[0.45,0.45,0.45])



        cmds.formLayout(self.layout, edit=True, attachForm=[(self.btnSetServerPath, 'top', 0),(self.btnSetServerPath, 'bottom', 0),(self.btnSetServerPath, 'left', 0), (self.btnSetServerPath, 'right', 0)])
