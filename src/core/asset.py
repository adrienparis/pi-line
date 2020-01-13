import os

from .scene import Scene

class Asset(Scene):
    _path = os.path.join(Scene._path, "assets")
    _srcimagePath = os.path.join(Scene._path,"assets")
    _steps = ["previs", "mod", "rig", "surf"]

    def __init__(self, name, cat, project):
        Scene.__init__(self, name, cat, project)
        self.shotUses = 0
        self.setRelativePath()

    def make(self):
        Scene.make(self)
        p = os.path.join(self._srcimagePath, self.name)
        if not os.path.isdir(p):
            os.makedirs(p)
            
    def download(self):
        print("downloading " + self.name)
        if not(self.onServer and not self.onLocal):
            print("Already on local")
            return
        loc = os.path.join(self.path.local, self.parent.getAbsolutePath(), self.step, Version._path, self.name)
        ser = os.path.join(self.path.server, self.parent.getAbsolutePath(), self.step, Version._path, self.name)
        print(loc)
        print(ser)
        copy_tree(ser, loc)
        self.onLocal = True

        print(self.name + " downloaded")

# TODO and copy the publish of the version to the server scene
    def upload(self):
        '''rename the self version to actual date 
        copy to server'''
        print("uploading " + self.name)
        if not(not self.onServer and self.onLocal):
            print("Already on server")
            return
        last = os.path.join(self.path.local, self.parent.getAbsolutePath(), self.step, Version._path, self.name)
        print(last)
        self.name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.date = datetime.datetime.now()
        self.setRelativePath()
        newLoc = os.path.join(self.path.local, self.parent.getAbsolutePath(), self.step, Version._path, self.name)
        newSer = os.path.join(self.path.server, self.parent.getAbsolutePath(), self.step, Version._path, self.name)
        newSerWip = os.path.join(newSer, "wip")
        print(newLoc)
        print(newSer)
        shutil.move(last, newLoc)
        os.makedirs(newSer)
        copy_tree(newLoc, newSer)
        #BAD IDEA
        #TODO REPLACE THAT!! do not copy all and deleting after! only copy what's needed
        shutil.rmtree(newSerWip)
        self.onServer = True
        print("all worked")