import maya.cmds as cmds
from pymel.all import Callback
import os

import log
from .UC import *
from .defineProjectUC import DefineProjectUC
from .windowUC import WindowUC

from core.user import User
from core.asset import Asset as astPL
from core.project import Project

class ProjectUC(UserControl):
    projects = []

    def __init__(self, parent):
        # UserControl.__init__(self, parent)
        self.projects = Project.fetchProjects()
        self.eventHandler("optionBtn", self.option)
        # self.bgc = 0x00ff00
        super(ProjectUC, self).__init__(parent=parent)

    def load(self):
        # print("loading project UC")
        # self.layout = cmds.formLayout('ProjectUC', parent=self.parentLay)
        current_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
        
        self.menu = cmds.optionMenu('droplist', parent=self.layout, w=20, cc=Callback(self.changeProject), bgc=hexToRGB(0x5d5d5d))
        self.projectsLabel = []
        self.projectsLabel.append(cmds.menuItem( "projEmpty", label='-' ))
        for i, p in enumerate(self.projects):
            self.projectsLabel.append(cmds.menuItem( "projName_" + str(i) ,label=p.name ))

        self.optionBtn = cmds.iconTextButton('optionBtn', parent=self.layout, style='iconOnly', image1=getIcon("gear"), label='Option', w=22, h=22, sic=True, bgc=hexToRGB(0x5d5d5d),
                                              c=Callback(self.runEvent, "optionBtn"))
        self.refreshBtn = cmds.iconTextButton('refreshBtn', parent=self.layout, style='iconOnly', image1=getIcon("refresh"), label='Option', w=22, h=22, sic=True, bgc=hexToRGB(0x5d5d5d),
                                              c=Callback(self.runEvent, "refreshBtn"))
        cmds.formLayout(self.layout, edit=True,
                        attachForm=[(self.menu, 'top', 0), (self.menu, 'left', 0), (self.optionBtn, 'top', 0), (self.optionBtn, 'right', 0), (self.refreshBtn, 'top', 0)],
                        attachControl=[(self.menu, 'right', 5, self.refreshBtn), (self.refreshBtn, 'right', 5, self.optionBtn)],
                        attachNone=[(self.menu, 'bottom'), (self.optionBtn, 'bottom'), (self.refreshBtn, 'bottom'), (self.refreshBtn, 'left')])

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
        self.dpWin = WindowUC("Project Manager")
        self.dpWin.ih = 200
        self.dpWin.iw = 400
        self.dpWin.load()

        pUC = DefineProjectUC(self.dpWin)
        pUC.load()
        pUC.attach(top=Attach.FORM, bottom=Attach.FORM, left=Attach.FORM, right=Attach.FORM, margin=0)
        pUC.eventHandler("close", self.closeOptionWin)
        self.dpWin.applyAttach()
        self.refresh()

    def closeOptionWin(self):
        self.dpWin.close()
    
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
            attachControl=[(self.menu, 'right', 5, self.refreshBtn)],
            attachNone=[(self.menu, 'bottom')])

        self.projectsLabel *= 0
