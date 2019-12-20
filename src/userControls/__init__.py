import sys
from os.path import dirname, basename, isfile, join
import glob
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

# from . import *

# import importlib

# # i=0
# for name in __all__:
    
#     mod = importlib.import_module(name)
#     importlib.reload(mod)
    # print("reload " + module)
    # reload( __all__[i] )
    # i += 1


# from imp import reload

# __all__ = ["UC", "cupboardUC", "defineProjectUC", "detailUC", "explorerUC", "iconButtonUC", "importUC", "projectUC", "syncUC", "tileUC", "versInfonUC", "versionUC", "windowUC", "wipUC"]

# import log

from UC import *
from buttonsUC import *
from browsing import Browsing
from cupboardUC import CupboardUC
from checkBoxGrpUC import CheckBoxGrpUC
from chooseStepUC import ChooseStepUC
from defineProjectUC import DefineProjectUC
from detailUC import DetailUC
from explorerUC import ExplorerUC
from importUC import ImportUC
from lineUC import LineUC
from newElemUC import NewVersion
from projectUC import ProjectUC
from sceneExplorerUC import SceneExplorerUC
from syncUC import SyncUC
from tileUC import TileUC
from tilesViewUC import TilesViewUC
from treeUC import TreeUC
from versInfonUC import VersInfonUC
from versionUC import VersionUC
from windowUC import WindowUC
from wipUC import WipUC

# reload(UC)
# reload(browsing)
reload(windowUC)
reload(cupboardUC)
reload(checkBoxGrpUC)
reload(chooseStepUC)
reload(explorerUC)
reload(buttonsUC)
reload(defineProjectUC)
reload(detailUC)
reload(importUC)
reload(lineUC)
reload(newElemUC)
reload(projectUC)
reload(sceneExplorerUC)
reload(syncUC)
reload(tileUC)
reload(tilesViewUC)
reload(treeUC)
reload(versInfonUC)
reload(versionUC)
reload(wipUC)
log.info("userControls Loaded")

from UC import *
from buttonsUC import *
from browsing import Browsing
from cupboardUC import CupboardUC
from checkBoxGrpUC import CheckBoxGrpUC
from chooseStepUC import ChooseStepUC
from defineProjectUC import DefineProjectUC
from detailUC import DetailUC
from explorerUC import ExplorerUC
from importUC import ImportUC
from lineUC import LineUC
from projectUC import ProjectUC
from sceneExplorerUC import SceneExplorerUC
from syncUC import SyncUC
from tileUC import TileUC
from tilesViewUC import TilesViewUC
from treeUC import TreeUC
from versInfonUC import VersInfonUC
from versionUC import VersionUC
from windowUC import WindowUC
from wipUC import WipUC
print("UserControl reloaded")