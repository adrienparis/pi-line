from os.path import dirname, basename, isfile, join
import glob
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

# print(__all__)

from . import *
# import asset
# import sys
# m = sys.modules.keys()
# for i in m:
#     if i in __all__:
#         print(i)

# for module in __all__:
#     print("reload " + module)
#     reload(module)
# __all__ = ["asset", "item", "path", "project", "scene", "shot", "version"]

# from .user import *
# from .path import *
# from .item import *
# from .version import *
# from .project import *
# from .scene import *
# from .asset import *
# from .shot import *

print("Core reloaded")