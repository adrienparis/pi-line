import os

from .scene import Scene

class Shot(Scene):
    _path = os.path.join(Scene._path,"shots")
    _imagePath = os.path.join(Scene._path,"shots")
    _steps = ["animation", "previz", "rendering", "sfx"]

    def __init__(self, name, seq, project=None):
        Scene.__init__(self, name, seq, project)
