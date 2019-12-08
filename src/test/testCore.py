import os
import sys
from imp import reload
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, "")
sys.path.append(path)
path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)
import user
import core

import userControls as UC


# add       ->   ajouter l'élément au enfants
# new       ->   
# fetch     ->   recupere les données 
# write     ->   enregistre les informations dans les .pil
# read      ->   recupere les info dans les .pil
# make      ->   construire les fichier
# load      ->   charger l'interface
# refresh   ->   mettre a jour l'interface par rapport au donnée et recharger les éléments changer de l'interface



# define a project name, dim, server path, local etc
# create tree folders in server
# copy tree folder in local
# fetch all assets
# fetch all shots
# create a new asset categorie
# create a new seq
# create a new asset
# create a new shot
# create a new mod version of an asset
# create a new rig version from the mod version
# publish it 



#download
#publish
#
unicode = str

def mainUI():
    

    path = core.Path("D:/creative seed/pi-line/src/test/serverFileProject", "D:/creative seed/pi-line/src/test/localFileProject")
    # path = core.Path("D:/creative seed/pi-line/src/test/serverFileProject")
    proj = core.Project("anubis", path)
    print(proj.path.local)
    proj.makeServerFolderTree()
    proj.makeCategory("char")
    a = core.Asset("bob", "char", proj)
    proj.addAssetToCategory(a, "char")
    a = core.Asset("didier", "char", proj)
    proj.addAssetToCategory(a, "char")

    la = proj.getAssetsByCategory("char")
    print(la)

    win = UC.WindowUC(u"Pi-Line")
    win.load()

    cpBrd = UC.CupboardUC(win)
    cpBrd.create()
    cpBrd.attach(top=UC.Attach.FORM, bottom=UC.Attach.FORM, left=UC.Attach.FORM, right=UC.Attach.FORM, margin=0)

    win.applyAttach()


print(u"=====Start pi-Line=====")
# print("Merci pilou <3")
mainUI()
