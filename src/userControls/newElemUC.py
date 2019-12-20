import datetime

import maya.cmds as cmds
from pymel.all import *

import log
from .UC import *

class NewVersion(UserControl):

    def __init__(self, scene, parent=None):
        UserControl.__init__(self, parent)
        self.scene = scene
        # self.bgc = 0xa5cc59

    def load(self):

        l = ["Cancel"]
        l += sorted(self.scene._steps)
        af = []
        ac = []
        ap = []
        an = []
        col = int(100 / len(l))
        p = 100 - col

        
        prev = cmds.button( parent=self.layout, label=l[0], c=Callback(self._cancel), bgc=[1,0,0])
        an.append((prev, "top"))
        af.append((prev, "bottom", 5))
        an.append((prev, "left"))
        af.append((prev, "right", 5))

        i = 0
        for step in l[1:]:
            c = cmds.button( parent=self.layout, label=step, c=Callback(self._click, step))
            if len(l) > 3:
                if i % 2 == 0:
                    an.append((c, "top"))
                    af.append((c, "bottom", 5))
                else:
                    an.append((c, "top"))
                    ac.append((c, "bottom", 5, prev))
            else:
                an.append((c, "top"))
                af.append((c, "bottom", 5))


            if p == 0:
                af.append((c, "left", 5))
            else:
                ap.append((c, "left", 5, int(p)))
            if prev is None:
                af.append((c, "right", 5))
            else:
                ac.append((c, "right", 5, prev))
            prev = c
            p -= col
            i += 1
        
        print(af)
        print(ac)
        print(ap)
        print(an)
        cmds.formLayout(self.layout, edit=True, attachForm=af, attachControl=ac, attachNone=an, attachPosition=ap)
        


        pass

    def _click(self, step):
        print(step)

    def _cancel(self):
        print("Abort")