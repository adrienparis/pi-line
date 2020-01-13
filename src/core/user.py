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
            self.readPrefs()
            self.assignPrefs()
            self.profil = None
            self.lastProj = None
            #0=alpha 1=beta 2=releaseCandidate 3=release
            self.tester = 3
        
        def readPrefs(self):
            filepath = os.path.join(self.prefPath, "preferences.pil")
            if not os.path.isfile(filepath):
                log.warning("user's preference file does not exist")
                return
            with open(filepath) as fp:
                for line in fp:
                    key = line.split('=', 1)[0].replace(" ", "")
                    if len(line.split('=', 1)) == 2:
                        value = line.split('=', 1)[1].strip()
                    self.prefs[key] = value
        
        def writePrefs(self):
            filepath = os.path.join(self.prefPath, "preferences.pil")
            print("%\\%\\%\\%\\%\\%\\%\\%\\%\\%\\%\\%\\%\\%\\%\\%\\%\\%\\%\\")
            print(filepath)
            with open(filepath, "w+") as fp:
                for k,v in self.prefs.items():
                    if v is not None:
                        fp.write(k + "=" + str(v) + "\n")

                # if self.lastProj is not None:
                #     fp.write("lastProj=" + self.lastProj + "\n")
                #     print(self.lastProj)
                # if self.profil is not None:
                #     fp.write("profil=" + self.profil + "\n")
                #     print(self.profil)
                fp.close()


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
        return getattr(self.__instance, name)
    def __setattr__(self, name, val):
        return setattr(self.__instance, name, val)