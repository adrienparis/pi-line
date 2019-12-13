
import log

from .UC import UserControl
from .lineUC import LineUC

class AssetTreeUC(UserControl):
    pass
    def __init__(self, parent):
        UserControl.__init__(self, parent)
        self.name = "assetTree" + self.name

    def load(self):
        # self.layout = cmds.formLayout(self.name, parent=self.parentLay, bgc=hexToRGB(0x505050))
        cat = ["char", "set", "props", "modules"]
        ast = ["plop", "plip", "plap"]
        pl = None
        for c in cat:
            l = LineUC(self.layout, c, "arrowRight")
            l.load()
            if pl is not None:
                l.attach(top=(Attach.CTRL, pl), bottom=Attach.NONE, left=Attach.FORM, right=Attach.FORM)
            else:
                l.attach(top=Attach.FORM, bottom=Attach.NONE, left=Attach.FORM, right=Attach.FORM)
            pl = l
            for a in ast:
                l = LineUC(self.layout, a, "check")
                l.load()
                if pl is not None:
                    l.attach(top=(Attach.CTRL, pl), bottom=Attach.NONE, left=(Attach.POS, 15), right=Attach.FORM)
                else:
                    l.attach(top=Attach.FORM, bottom=Attach.NONE, left=(Attach.POS, 15), right=Attach.FORM)
                pl = l




log.info("AssetTreeUC Loaded")

