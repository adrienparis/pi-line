import os

from scene import *

class Asset(Scene):
    _path = os.path.join(Scene._path,"assets")
    _srcimagePath = os.path.join(Scene._path,"assets")
    _step = ["mod", "rig", "surf"]

    def __init__(self, name, cat, project):
        Scene.__init__(self, name, cat, project)
