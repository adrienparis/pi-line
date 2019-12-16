import os
import sys
from imp import reload
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, "")
sys.path.append(path)
path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)
import user
import core
import main

import userControls as UC

t = UC.TreeUC(None)
t.load()
main.mainUI()