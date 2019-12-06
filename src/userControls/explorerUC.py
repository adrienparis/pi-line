import maya.cmds as cmds
from pymel.all import *
from UC import *
from assetTileUC import *
from assetTreeUC import *
from treeUC import *

class ExplorerUC(UserControl):

    def __init__(self, parent):
        UserControl.__init__(self, parent)
        self.project = None
        self.assets = None
        self.tabs = ""
    def assetDisplay(self, parent, a):    
        layout = cmds.formLayout('Assets', parent=parent, numberOfDivisions=100)
        
        current_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
        ativ = AssetTileUC(layout) #AssetTilesView(layout) # cmds.formLayout('assetViewSwitchTile', parent=layout, numberOfDivisions=100, bgc=[0.2,0.2,0.2])

        ativ.setAsset(a)
        ativ.create()
        ativ.eventHandler("changeTile", self.runEvent, "changeItem")
        # atrv = AssetTreeUC(layout)
        atrv = TreeUC(layout)
        for c in a.categories:
            p = atrv.addFolder(c.name, c)
            for asset in c.assets:
                atrv.addItem(asset.name, asset, parent=p, image="check", info="Yesterday")
        atrv.eventHandler("changeSelection", self.runEvent, "changeItem")

        atrv.load()
        # atrv.create()
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
        self.layout = cmds.formLayout('ExplorerUC', parent=self.parentLay, numberOfDivisions=100, bgc=hexToRGB(0x5d5d5d))
        
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

print("ExplorerUC Loaded")