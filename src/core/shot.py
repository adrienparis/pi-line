import os

from scene import *

class Shot(Scene):
    _path = os.path.join(Scene._path,"shots")
    _imagePath = os.path.join(Scene._path,"shots")
    _step = ["animation", "previz", "rendering", "sfx"]

    def __init__(self, name, seq, project):
        Scene.__init__(self, name, seq, project)
