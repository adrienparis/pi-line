import os
import sys
import getpass
import shutil
import maya.cmds as cmds
from imp import reload
current_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
sys.path.append(current_path)
# import AMui
# reload(AMui)

# copy file destination
# S:/%username%/Tools/Pi-Line/
u = getpass.getuser()

instalPath = os.path.join("S:/", u, "Tools", "Pi-Line", "src").replace('\\', '/')
logoPath =  os.path.join(instalPath, "logo").replace('\\', '/')
userPath = os.path.join("C:/","Users", u, "Documents", "Pi-Line").replace('\\', '/')

if not os.path.exists(instalPath):
    os.makedirs(instalPath)
if not os.path.exists(logoPath):
    os.makedirs(logoPath)
if not os.path.exists(userPath):
    os.makedirs(userPath)
if not os.path.exists(current_path):
    print("no file on the server")

src_files = os.listdir(current_path)
for file_name in src_files:
    full_file_name = os.path.join(current_path, file_name)
    if os.path.isfile(full_file_name):
        print(full_file_name)
        # shutil.copy(full_file_name, instalPath)
src_files = os.listdir(os.path.join(current_path, "logo"))
for file_name in src_files:
    full_file_name = os.path.join(current_path, "logo", file_name)
    if os.path.isfile(full_file_name):
        print(full_file_name)
        # shutil.copy(full_file_name, logoPath)

f = open(os.path.join(userPath, "preferences.pil"), "w+")
f.write('lastProj = ""\n')
f.write('profil = "MODELER"\n')
f.close()

f = open(os.path.join(userPath, "projects.pil"), "w+")
f.write('golem;go;Q:/promo002/casiers/a.paris/ateliers;S:/' + u + '/projects;\n')
f.write('testAssetManager;tam;Q:/promo002/casiers/a.paris/ateliers;S:/' + u + '/projects;\n')
f.write('Amenti;amenti;Q:/promo002/projects;S:/' + u + '/projects;\n')
f.write('Nasterea;nas;Q:/promo002/projects;S:/' + u + '/projects;\n')
f.close()

shrtImportStr = 'import sys;sys.path.append(\"' + instalPath + '\");' + "import AMui;" 
importStr = shrtImportStr + "import assetManager;" + "import asset;" + "import plUser;" + "import project;" + "import userControls;"
delStr ="del AMui;" +  "del assetManager;" + "del asset;" + "del plUser;" + "del project;" + "del userControls;"
cmds.shelfButton(rpt=True, i1=instalPath + "/logo/pi-line.png", l="Pi-Line", p="Custom", dcc=shrtImportStr + "AMui.start()", c="print(\"Not implemented yet\")")
cmds.shelfButton(rpt=True, i1=instalPath + "/logo/reload.png", l="Reload", p="Custom", c=delStr + importStr)
