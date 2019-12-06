import os
import sys
from imp import reload
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir)
print(path)
sys.path.append(path)
import plUser as user
import core


u = user.User()
print(u.name)

