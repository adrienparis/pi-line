import sys
import os
import getpass
import ast


class User():
    class __user:
        def __init__(self):
            self.name = getpass.getuser()
            self.prefPath = os.path.join("C:/Users", self.name, "Documents", "Pi-Line")
            self.prefs = {}
            self.loadPref()
            self.assignPrefs()
            self.profil = None
            #0=alpha 1=beta 2=releaseCandidate 3=release
            self.tester = 3
            
        def loadPref(self):
            filepath = os.path.join(self.prefPath, "preferences.pil")
            if not os.path.isfile(filepath):
                print("File path {} does not exist. Exiting...".format(filepath))
                return
            #TODO create a try and catch to avoid a badly written config file
            with open(filepath) as fp:
                for line in fp:
                    key = line.split('=', 1)[0].replace(" ", "")
                    if len(line.split('=', 1)) == 2:
                        value = ast.literal_eval(line.split('=', 1)[1].strip())
                    self.prefs[key] = value

        def createPrefFiles(self):
            pass

        def assignPrefs(self):
            #name project
            if "lastProj" in self.prefs:
                self.lastProj = self.prefs["lastProj"]

            # "MODELER" "RIGGER" "ANIMATOR" "SURFACER"
            if "profil" in self.prefs:
                self.profil = self.prefs["profil"]

    __instance = None

    def __init__(self):
        if not User.__instance:
            User.__instance = User.__user()
    def __getattr__(self, name):
        return getattr(User.__instance, name)