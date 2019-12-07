import maya.cmds as cmds

from .UC import *

class WindowUC(UserControl):

    """ Create a floatable workspace that act like a window but can be plug inside maya interface"""

    def __init__(self, name):
        """
        :name: Name of the window
        """
        UserControl.__init__(self, None)
        self.name = name
        self.iw = 400
        self.ih = 600
    
    def load(self):
        if cmds.workspaceControl(self.name, exists=1):
            cmds.deleteUI(self.name)
        self.window = cmds.workspaceControl(self.name, retain=False, iw=self.iw, ih=self.ih, floating=True)
        self.layout = cmds.formLayout(self.name + "Layout", parent=self.window)
    
    def close(self):
        if cmds.workspaceControl(self.name, exists=1):
            cmds.deleteUI(self.name)

