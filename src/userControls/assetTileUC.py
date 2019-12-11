import maya.cmds as cmds
from pymel.all import *
from .UC import *
from tileUC import TileUC

class AssetTileUC(UserControl):
    styleIcon = 'iconAndTextVertical'
    sizeImage = 100

    def __init__(self, parent):
        UserControl.__init__(self, parent)
        #must be an array of categorie, or a class that encompass all the categories
        self.project = None
        self.assets = None
        self.selected = []

    def setProject(self, project):
        self.project = project
        self.assets = self.project.assets

    def clickCommand(self, tile, mods):
        for t in self.selected:
            if (mods != 1 or tile.asset.category != t.asset.category):
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
        selection = [x.asset for x in self.selected]
        self.runEvent("changeTile", selection)

    def newAssetCommand(self, c):
        print("badly implemented")
        return
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
        self.layout = cmds.formLayout('AssetTileUC', parent=self.parentLay)

        
        self.tabs = cmds.tabLayout('Categories', snt=True, parent=self.layout)
        cmds.tabLayout(self.tabs, e=True, ntc='AMui.newTabAsset("{0}")'.format(self.tabs))
        
        self.shelf = {}

        # print(self.assets.serverPath)
        self.reload()
        cmds.formLayout(self.layout, edit=True, attachForm=[(self.tabs, 'top', 0),(self.tabs, 'bottom', 0),(self.tabs, 'left', 0), (self.tabs, 'right', 0)])
        return self.layout

    def reload(self):        
        for s in list(self.shelf.values()):
            cmds.deleteUI(s[0])


        for c in self.assets.assets.keys():
            scrollLayout = cmds.scrollLayout( c, parent=self.tabs,
                                        horizontalScrollBarThickness=160,
                                        verticalScrollBarThickness=16,
                                        cr=True)
            assetColumn = cmds.gridLayout(c + "Grid", numberOfColumns=3, cr=False, ag=True, cellWidthHeight=(self.sizeImage, self.sizeImage))
            self.shelf[c] = [scrollLayout, assetColumn]
            cmds.scrollLayout(self.shelf[c][0], e=True, rc=Callback(self.resizeTilesView, c))
            
            current_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
            newTiles = cmds.iconTextButton(c + "NewTile", parent=self.shelf[c][1], style=self.styleIcon, image1=getIcon("add"),
                                label="New Asset", w=self.sizeImage, h=self.sizeImage, sic=True, c=Callback(self.newAssetCommand, c) )
            for a in self.assets.assets[c]:
                t = TileUC(a, self.shelf[c][1], self.sizeImage)
                t.eventHandler("click", self.clickCommand)
                t.create()
