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


# add       ->   ajouter l'element au enfants
# new       ->   
# fetch     ->   recupere les donnees selon les dossier
# write     ->   enregistre les informations dans les .pil
# read      ->   recupere les info dans les .pil
# make      ->   construire les fichier
# load      ->   charger l'interface
# refresh   ->   mettre a jour l'interface par rapport au donnee et recharger les elements changer de l'interface



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

def mainUI():
    

    # current_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
    # path = core.Path(os.path.join( current_path, "serverFileProject"),  os.path.join(current_path, "localFileProject"))
    # # path = core.Path("D:/creative seed/pi-line/src/test/serverFileProject")
    # proj = core.Project("anubis", path)
    # print(proj.path.local)
    # proj.makeServerFolderTree()
    # proj.makeCategory("char")
    # a = core.Asset("bob", "char", proj)
    # proj.addAssetToCategory(a, "char")
    # a = core.Asset("didier", "char", proj)
    # proj.addAssetToCategory(a, "char")

    # la = proj.getAssetsByCategory("char")
    # print(la)

    projects = core.Project.fetchProjects()
    print(projects)
    if len(projects) >= 1:
        p = projects[0]
        print(p.path.local)
        p.addCategory("char")
        a = core.asset.Asset("bob", "chars", p)
        a.make()
        p.addAssetToCategory(a, a.category)
        # a.makeNewVersion(core.Asset._steps[1])
        a.fetchVersions()
        vers = a.getVersionBy("mod")
        vers[0].fetchWips()
        print(vers[0].wips)
        vers[0].publish()
        vers[0].setCurrent()
        vers[0].upload()
        for v in vers:
            print(v.parent.name, v.name, v.onServer, v.onLocal)
        
#S:\a.paris\projects\Cesaristochat\3_work\maya\scenes\char\bob\mod\versions   
#S:/a.paris/projects\Cesaristochat\3_work\maya\scenes\char\bob\versions\20191209163707

    # win = UC.WindowUC(u"Pi-Line")
    # win.load()

    # cpBrd = UC.CupboardUC(win)
    # cpBrd.load()
    # cpBrd.attach(top=UC.Attach.FORM, bottom=UC.Attach.FORM, left=UC.Attach.FORM, right=UC.Attach.FORM, margin=0)

    # win.applyAttach()


print(u"=====Start pi-Line=====")
# print("Merci pilou <3")
mainUI()
