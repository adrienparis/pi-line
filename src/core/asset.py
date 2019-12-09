import os

from .scene import Scene

class Asset(Scene):
    _path = os.path.join(Scene._path, "assets")
    _srcimagePath = os.path.join(Scene._path,"assets")
    _steps = ["mod", "rig", "surf"]

    def __init__(self, name, cat, project):
        Scene.__init__(self, name, cat, project)
        self.shotUses = 0
        self.setRelativePath()
