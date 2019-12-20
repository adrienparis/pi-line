import os
import sys
import getpass
import stat
import ctypes
import shutil
from distutils.dir_util import copy_tree
from shutil import copytree, ignore_patterns
import maya.cmds as cmds
from imp import reload
current_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
sys.path.append(current_path)
u = getpass.getuser()


pathTools = os.path.join("S:/", ".Tools")
pathPiLine = os.path.join(pathTools, "Pi-Line")
pathSrcs = os.path.join(pathPiLine, "src")
pathLogo = os.path.join(pathPiLine, "logo")

pathUser = os.path.join("C:/","Users", u, "Documents", "Pi-Line").replace('\\', '/')


def fetchVersion(path):
    version = []
    filename = os.path.join(path, "version")
    if not os.path.isfile(filename):
        print("Version was not found")
    else:
        with open(filename, "r") as fp:
            for line in fp:
                version = line.replace("\n", "").split(".")
    return version

def download(path):
    print "|--> Downloading files...",
    current_path = path

    if not os.path.exists(current_path):
        cmds.error("no file on the server")


    if not os.path.exists(pathTools):
        os.makedirs(pathTools)
        ctypes.windll.kernel32.SetFileAttributesW(pathTools, 0x02)
    if os.path.exists(pathPiLine):
        if not os.access(pathPiLine, os.W_OK):
            print("give acces write")
            os.chmod(pathPiLine, stat.S_IWUSR)
        # print("delete old " + pathPiLine)
        shutil.rmtree(pathPiLine, ignore_errors=True)
        # print("deleted")
        
    # print(current_path, pathPiLine)
    copytree(current_path, pathPiLine, ignore=ignore_patterns('*.pyc', '.git', '.vscode', 'Template', '.gitignore'))
    # copy_tree(current_path, pathPiLine)
    print("\r|--> Files downloaded          ")




def writePrefsFiles():
    print "|--> Write preferences'files...",
    f = open(os.path.join(pathUser, "preferences.pil"), "w+")
    f.write('lastProj = ""\n')
    f.write('profil = "MODELER"\n')
    f.write('tester = "3"\n')
    f.close()

    f = open(os.path.join(pathUser, "projects.pil"), "w+")
    f.write('golem;go;Q:/promo002/casiers/a.paris/ateliers;S:/projects;\n')
    f.write('testAssetManager;tam;Q:/promo002/casiers/a.paris/ateliers;S:/projects;\n')
    f.write('Amenti;amenti;Q:/promo002/projects;S:/projects;\n')
    f.write('Nasterea;nas;Q:/promo002/projects;S:/projects;\n')
    f.close()
    print("\r|--> Preferences' files written  ")

def createButtons(pathPiLine, current_path):
    print "|--> Creating buttons...",

    cmdImport = 'import sys;sys.path.append(\"' + pathSrcs + '\");' + "import main;" + "import core;" + "import userControls;"
    cmdReload = "reload(main);" + "reload(core);" + "reload(userControls);"

    cmds.shelfButton(rpt=True, i1=pathPiLine + "/logo/pi-line.png", l="Pi-Line", p="Custom", c=cmdImport + "main.mainUI()", dcc=cmdImport + cmdReload)
    # cmds.shelfButton(rpt=True, i1=instalPath + "/logo/pi-line.png", l="Pi-Line", p="Custom", dcc=shrtImportStr + "AMui.start()", c="print(\"Not implemented yet\")")
    # cmds.shelfButton(rpt=True, i1=instalPath + "/logo/reload.png", l="Reload", p="Custom", c=delStr + importStr)
    cmds.shelfButton(rpt=True, i1=pathPiLine + "/logo/install.png", l="Install", p="Custom", c="import sys;sys.path.append(\"" + current_path + "\");import installer; installer.download(\"" + current_path + "\")")
    print("\r|--> Buttons created     ")


print("=================INSTALL PI-LINE=================")


versionLocal = fetchVersion(pathPiLine)
versionServer = fetchVersion(current_path)
# if versionLocal == [] or versionLocal != versionServer:
download(current_path)
if versionLocal == []:
    writePrefsFiles()
    createButtons(pathPiLine, current_path)
print("==============INSTALLATION COMPLETED==============")
