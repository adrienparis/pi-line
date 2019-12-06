import os
from os import sys, path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

import core

projects = core.Project.fetchProjects(r"C:\Users\a.paris\Documents\Pi-Line")
print(len(projects))
for p in projects:
    print(p.name)
    p.fetchAssets()
    print("========================")
    l = p.getAssetsBy(("props", "characters"))
    print(len(l))
    for i in l:
        print(i.name, i.category)
    p.fetchShots()
    print("========================")
    l = p.getShotsBy("seq010")
    print(len(l))
    for i in l:
        print(i.name, i.category)
    