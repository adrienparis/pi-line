import os
import sys
from shutil import copytree, ignore_patterns, rmtree

current_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
sys.path.append(current_path)

def fetchVersion(path):
    version = [0,0,1,0]
    filename = os.path.join(current_path, "version")
    if not os.path.isfile(filename):
        print("Version was not found")
    else:
        with open(filename, "r") as fp:
            for line in fp:
                version = line.replace("\n", "").split(".")
    return version


def writeVersion(path, version):
    filename = os.path.join(current_path, "version")
    if not os.path.isfile(filename):
        print("Version was not found")
    f = open(os.path.join(current_path, "version"), "rw+")
    f.write(version[0] + "." + version[1] + "." + version[2] + "." + version[3])
    f.write('testAssetManager;tam;Q:/promo002/casiers/a.paris/ateliers;S:/projects;\n')
    f.write('Amenti;amenti;Q:/promo002/projects;S:/projects;\n')
    f.write('Nasterea;nas;Q:/promo002/projects;S:/projects;\n')
    f.close()

v = fetchVersion(current_path)
v[2] += 1
writeVersion(current_path, v)

pathDest = "Q:/partage/library/Maya scripts/general/Pi-Line"

if os.path.exists(pathDest):
    print("delete old " + pathDest)
    rmtree(pathDest, ignore_errors=True)
    print("deleted")

copytree(current_path, pathDest, ignore=ignore_patterns('*.pyc', '.git', '.vscode', '.gitignore', 'uploader.py'))

time.sleep(10)