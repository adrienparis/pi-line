import maya.cmds as cmds
from pymel.all import *
from .UC import *
from tileUC import TileUC

class TilesViewUC(UserControl):
    
    _styleIcon = 'iconAndTextVertical'
    _sizeImage = 100
    class _item():
        def __init__(self, name, elem, image=None, icon=None, info=""):
            self.name = name
            self.elem = elem
            self.image = image
            self.icon = icon
            self.info = info
            self.parent = None
            self.tile = None
            self.selected = False
            
        def setParent(self, parent):
            if self.parent is not None:
                self.parent.removeChildren(self)
            parent.addChildren(self)

    class _folder(_item):
        def __init__(self, name, elem):
            TilesViewUC._item.__init__(self, name, elem)
            self.childrens = []
            # self.image = "arrowBottom"
            # self.isDeployed = True
            self.area = None

        # def deploying(self, val):
        #     self.isDeployed = val
        #     if val:
        #         self.image = "arrowBottom"
        #     else:
        #         self.image = "arrowRight"
        #     self.line.icon = self.image
        #     self.line.refresh()
        #     cmds.formLayout(self.area, e=True, vis=self.isDeployed)

        # def deployingAll(self, val):
        #     self.deploying(val)
        #     for f in self.childrens:
        #         if f.__class__ is TilesViewUC._folder:
        #             TilesViewUC._folder.deployingAll(f, val)


        def addChildren(self, child):
            self.childrens.append(child)
            child.parent = self

        def removeChildren(self, child):
            self.childrens.remove(child)
            child.parent = None
        
        def getAllParent(self):
            if self.parent is None:
                return "/"
            return self.getAllParent() + "/" + self.name

    def __init__(self, parent, multiSelect=True):
        UserControl.__init__(self, parent)
        #must be an array of categorie, or a class that encompass all the categories
        self.name = "TilesView" + self.name
        self.folders = {}
        self.items = {}
        self.selecteds = []
        self.multiSelect = multiSelect
        # self.layout = ""
        self.scrlLay = ""

    def load(self):
        pass

    def _clickItem(self, item, tile, mod):
        
        for t in self.selecteds:
            if (mod != 1 or item.parent != t.parent or not self.multiSelect):
                t.tile.selection(False)
        if mod != 1:
            self.selecteds = []
        if mod <= 1:
            if tile.selected:
                tile.selection(False)
                self.selecteds.remove(item)
            else:
                tile.selection(True)
                self.selecteds.append(item)
        selection = [x.elem for x in self.selecteds if x.tile.selected]
        self.runEvent("changeSelection", selection)

    # def newAssetCommand(self, c):
    #     print("badly implemented")
    #     return
    #     print("Create New Asset")
    #     print(c.name)
    
    #     result = cmds.promptDialog(
    #                     title='New Asset - ' + c.name,
    #                     message='Enter name:',
    #                     button=['OK', 'Cancel'],
    #                     defaultButton='OK',
    #                     cancelButton='Cancel',
    #                     dismissString='Cancel')
    #     if result != 'OK': return
    #     name = cmds.promptDialog(query=True, text=True)
    #     a = astPL.Asset(c, name)
    #     a.create(c.path)
    #     a.fetchAssetData()
    #     c.assets.append(a)
    #     self.reload()

    def resizeTilesView(self, c):
        h = cmds.scrollLayout(self.shelf[c][0], q=True, h=True)
        w = cmds.scrollLayout(self.shelf[c][0], q=True, w=True)
        size = math.trunc((w - 4) / self._sizeImage)
        if size == 0:
            return

        nbChild = cmds.gridLayout(self.shelf[c][1], q=True, nch=True )
        rows = max((nbChild - 1) / size + 1, 1)
        if h < rows * self._sizeImage:
            size = math.trunc((w - 16) / self._sizeImage)
            if size == 0:
                return

            nbChild = cmds.gridLayout(self.shelf[c][1], q=True, nch=True )
            rows = max((nbChild - 1) / size + 1, 1)

        cmds.gridLayout(self.shelf[c][1], e=True, numberOfColumns=size )
        cmds.gridLayout(self.shelf[c][1], e=True, numberOfRows= rows )


    # def setAsset(self, assets):
    #     #TODO check if it's an Assets class
    #     self.assets = assets

    def load(self):
        # if self.layout is None or not cmds.formLayout(self.layout, q=True, exists=True):
        #     self.layout = cmds.formLayout(parent=self.parentLay)
        # self.layout = cmds.formLayout('AssetTileUC', parent=self.parentLay)

        
        self.tabs = cmds.tabLayout('Categories', snt=True, parent=self.layout)
        cmds.tabLayout(self.tabs, e=True, ntc=Callback(self.runEvent("newCategorie")))
        
        self.shelf = {}

        # print(self.assets.serverPath)
        self.reload()
        cmds.formLayout(self.layout, edit=True, attachForm=[(self.tabs, 'top', 0),(self.tabs, 'bottom', 0),(self.tabs, 'left', 0), (self.tabs, 'right', 0)])
        return self.layout

    def reload(self):        
        for s in list(self.shelf.values()):
            print(s[0])
            cmds.deleteUI(s[0])


        for c in self.assets.assets.keys():
            print(c)
            scrollLayout = cmds.scrollLayout( c, parent=self.tabs,
                                        horizontalScrollBarThickness=160,
                                        verticalScrollBarThickness=16,
                                        cr=True)
            assetColumn = cmds.gridLayout(c + "Grid", numberOfColumns=3, cr=False, ag=True, cellWidthHeight=(self._sizeImage, self._sizeImage))
            self.shelf[c] = [scrollLayout, assetColumn]
            cmds.scrollLayout(self.shelf[c][0], e=True, rc=Callback(self.resizeTilesView, c))
            
            current_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
            newTiles = cmds.iconTextButton(c + "NewTile", parent=self.shelf[c][1], style=self._styleIcon, image1=getIcon("add"),
                                label="New Asset", w=self._sizeImage, h=self._sizeImage, sic=True, c=Callback(self.runEvent, "newAsset", c) )
            for a in self.assets.assets[c]:
                t = TileUC(a, self.shelf[c][1], self._sizeImage)
                t.eventHandler("click", self.clickCommand)
                t.create()
