import maya.cmds as cmds

import log
from .UC import *
from .buttonsUC import *
from .treeUC import *
from .tilesViewUC import *
from core.asset import Asset

class ExplorerUC(UserControl):

    def __init__(self, parent):
        UserControl.__init__(self, parent)
        self.dispTile = True
        self.treeView = None
        self.tileView = None
        
    def switchAssetView(self):
        self.dispTile = not self.dispTile
        # switch = cmds.layout(self.ativ.layout, q=True, vis=True)

        self.tileView.visibility(self.dispTile)
        self.treeView.visibility(not self.dispTile)
        # cmds.layout(self.ativ.layout, e=True, vis=self.dispTile)
        # cmds.layout(self.atrv.layout, e=True, vis=not self.dispTileswitch)
        cmds.iconTextButton(self.buttonTile, e=True, vis=self.dispTile)
        cmds.iconTextButton(self.buttonTree, e=True, vis=not self.dispTile)

    def assetDisplay(self, parent, a):    
        layout = cmds.formLayout('Assets', parent=parent, numberOfDivisions=100)
        
        current_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
        ativ = AssetTileUC(layout) #AssetTilesView(layout) # cmds.formLayout('assetViewSwitchTile', parent=layout, numberOfDivisions=100, bgc=[0.2,0.2,0.2])

        ativ.eventHandler("newScene", self.newScene)

        ativ.setAsset(a)
        ativ.eventHandler("changeTile", self.runEvent, "changeItem")
        # atrv = AssetTreeUC(layout)
        ativ = tilesViewUc(self)
        atrv = TreeUC(self)
        for c in a.assets.keys():
            p = atrv.addFolder(c, None)
            for asset in a.assets[c]:
                
                img = "denied"
                v = asset.getLastVersion()
                if v is not None:
                    if v.onServer and v.onLocal:
                        img = "check"
                    elif v.onServer and not v.onLocal:
                        img = "download"
                    elif not v.onServer and v.onLocal:
                        img = "upload"
                else:
                    img = "new"

                atrv.addItem(asset.name, asset, parent=p, image=img)
        atrv.eventHandler("changeSelection", self.runEvent, "changeItem")


        atrv.load()
        ativ.load()
        assetViewSwitchTree = cmds.iconTextButton('assetViewSwitchTree', parent=layout, style='iconOnly', image1=getIcon("list"), label='Switch view', w=22, h=22, sic=True, bgc=[0.45,0.45,0.45])
        assetViewSwitchTile = cmds.iconTextButton('assetViewSwitchTile', parent=layout, style='iconOnly', image1=getIcon("tiles"), label='Switch view', w=22, h=22, sic=True, bgc=[0.45,0.45,0.45])
        cmds.iconTextButton(assetViewSwitchTile, e=True, c=Callback(self.switchAssetView), vis=False)
        cmds.iconTextButton(assetViewSwitchTree, e=True, c=Callback(self.switchAssetView), vis=True)
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

    def load(self):



        self.treeView = TreeUC(self)
        self.tileView = TilesViewUC(self)
        self.switchdisp = switchBtn(self, imageOn="list", imageOff="tiles", label="Switch view")
        self.switchSelect = switchBtn(self, imageOn="selectAll", imageOff="deselectAll", label="Deselect all", labelOn="select all")

        # self.switchTree = cmds.iconTextButton(parent=self.layout, style='iconOnly', image1=getIcon("list"), label='Switch view', w=22, h=22, sic=True, bgc=hexToRGB(self.color.button))
        # self.switchTile = cmds.iconTextButton(parent=self.layout, style='iconOnly', image1=getIcon("tiles"), label='Switch view', w=22, h=22, sic=True, bgc=hexToRGB(self.color.button))
        # self.switchSelAll = cmds.iconTextButton(parent=self.layout, style='iconOnly', image1=getIcon("deselectAll"), label='Deselect all', w=22, h=22, sic=True, bgc=hexToRGB(self.color.button))
        # self.switchDeselAll = cmds.iconTextButton(parent=self.layout, style='iconOnly', image1=getIcon("selectAll"), label='Select all', w=22, h=22, sic=True, bgc=hexToRGB(self.color.button))
        
        self.treeView.load()
        self.tileView.load()
        self.switchdisp.load()
        self.switchSelect.load()




        self.switchdisp.attach(top=Attach.FORM, bottom=Attach.NONE, left=Attach.FORM, right=Attach.NONE, margin=5)
        self.switchSelect.attach(top=Attach.FORM, bottom=Attach.NONE, left=(Attach.CTRL, self.switchdisp), right=Attach.NONE, margin=5)
        self.treeView.attach(top=(Attach.CTRL, self.switchdisp), bottom=Attach.FORM, left=Attach.FORM, right=Attach.FORM, margin=5)
        self.tileView.attach(top=(Attach.CTRL, self.switchdisp), bottom=Attach.FORM, left=Attach.FORM, right=Attach.FORM, margin=5)










        return
        if cmds.tabLayout(self.tabs, q=True, ex=True):
            cmds.deleteUI(self.tabs)
        self.tabs = cmds.tabLayout('SceneFold', parent=self.layout, sc=Callback(self.changeTab))

        if self.project is None or self.project.assets is None:
            self.tabAssets = cmds.formLayout('Assets', numberOfDivisions=100, parent=self.tabs)
        else:
            #TODO REPLACE THAT!!!
            self.assetDisplay(self.tabs, self.project)
        self.tabShots = cmds.formLayout('Shots', numberOfDivisions=100, parent=self.tabs)

        cmds.formLayout(self.layout, e=True, 
                        attachForm=[(self.tabs, 'top', 0),(self.tabs, 'bottom', 0),(self.tabs, 'left', 0), (self.tabs, 'right', 0)])
        self.changeTab()

    def changeTab(self):
        tabSel = cmds.tabLayout(self.tabs, q=True, st=True)
        self.runEvent("changeTab", tabSel)

    def newScene(self, cat, sceneName):
        a = Asset(sceneName, cat, self.project)
        a.make()
        self.project.addAssetToCategory(a, a.category)

log.info("ExplorerUC Loaded")