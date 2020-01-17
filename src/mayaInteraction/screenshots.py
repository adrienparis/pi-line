import os
import maya.cmds as cmds

def screenShot(self, wireframe=False):

    #import ref cyclo
    cycloPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "cyclo", "cyclo_surf_scaled.ma")
    cmds.file( "S:/a.paris/Tools/Pi-Line/cyclo/cyclo_surf_scaled.ma", r=True, type="mayaAscii", ignoreVersion=True, gl=True, mergeNamespacesOnClash=False, namespace="cyclo", options="v=0;")

    # get size
    cmds.select(cl=True)
    if cmds.objExists('geoSet'):
        cmds.select( "geoSet", r=True, ne=True)
        cmds.selectKey(clear=True)
        cmds.pickWalk(d="up")
        bb = [0, 0, 0, 0, 0, 0]
        selection = cmds.ls(sl=1)
        for sel in selection:
            obj_raw = cmds.xform(sel, q=1, bb=1)
            bb = [min(bb[0], obj_raw[0]), min(bb[1], obj_raw[1]), min(bb[2], obj_raw[2]), max(bb[3], obj_raw[3]), max(bb[4], obj_raw[4]), max(bb[5], obj_raw[5])]
        size = [bb[3] - bb[0], bb[4] - bb[1], bb[5] - bb[2]]
        dim = max(size[0], max(size[1], size[2])) * 1.25
        print(dim)
    else:
        print("c'est pas bien")
    # change scale tile name
    n = 1
    s = ("1 tile\n" + format(n, ",").replace(",", " ") + " unit" + "s" * (n > 1)).encode("hex")
    sh = ' '.join(a+b for a,b in zip(s[::2], s[1::2]))
    cmds.setAttr('scaleText.textInput', sh, type='string')
    #cmds.setAttr('cyclo_surf_scaled:scaleText.textInput', sh, type='string')

    # scale set
    cmds.setAttr('lookdev_set.scale', 1, 1, 1)
    # scale camera
    cmds.setAttr('lookdev_camera.scale', 1, 1, 1)
    # scale texture
    cmds.setAttr('checkerUV.repeatUV', 20, 20)
    # set wireframe texture
    if wireframe:
        cmds.select(cl=True)
        if cmds.objExists('geoSet'):
            cmds.select( "geoSet", r=True, ne=True)
            cmds.selectKey(clear=True)
            cmds.pickWalk(d="up")
            cmds.sets(e=True, forceElement="rsMaterial6SG")
    #TODO screenshot
    if wireframe:
        cmds.undo() 
    cmds.select(cl=True)
    # take screenshot
    # take render screenshot

    #cmds.render()
    #cmds.render("camera_rendu", x=768, y=576 )

    # rotate set to side
    cmds.setAttr('lookdev_set.rotateY', 90)

    cmds.setAttr("defaultRenderGlobals.imageFormat", 8)
    cmds.setAttr("defaultRenderGlobals.renderer", "redshift", type="string")
    cmds.playblast(st=1, et=1, v=0, orn=False, fmt="image", wh=(128, 128), f=r"S:\a.paris\Works\Atelier\2018\tenoriaum\3_work\maya\images\tmp\plop.png")
    cmds.render("camera_rendu", x=768, y=576 )



    cmds.displaySmoothness( du=0, dv=0, pw=4, ps=1, po=1)

    cmds.displaySmoothness( du=3, dv=3, pw=16, ps=4, po=3)
    cmds.setWireframeOnShadedOption("modelPanel4")
    cmds.DisplayShadedAndTextured()

def getBB():
    cmds.select(cl=True)
    if cmds.objExists('geoSet'):
        cmds.select( "geoSet", r=True, ne=True)
        cmds.selectKey(clear=True)
        cmds.pickWalk(d="up")
        bb = [0, 0, 0, 0, 0, 0]
        selection = cmds.ls(sl=1)
        for sel in selection:
            obj_raw = cmds.xform(sel, q=1, bb=1)
            bb = [min(bb[0], obj_raw[0]), min(bb[1], obj_raw[1]), min(bb[2], obj_raw[2]), max(bb[3], obj_raw[3]), max(bb[4], obj_raw[4]), max(bb[5], obj_raw[5])]
        return bb
        size = [bb[3] - bb[0], bb[4] - bb[1], bb[5] - bb[2]]
        dim = max(size[0], max(size[1], size[2])) * 1.25
        return dim
    return None

def getDimGeoSet():
    bb = getBB()
    dim = [bb[3] - bb[0], bb[4] - bb[1], bb[5] - bb[2]]
    return dim

def getCenterGeoSet():
    bb = getBB()
    if bb == None:
        return [0,0,0]
    dim = [bb[3] - bb[0], bb[4] - bb[1], bb[5] - bb[2]]
    center = [dim[0] / 2 + bb[0], dim[1] / 2 + bb[1], dim[2] / 2 + bb[2]]
    return center


def screenShot(name, path, size=(1024,1024)):
    cmds.setAttr("defaultRenderGlobals.imageFormat", 8)
    cmds.playblast(st=1, et=1, v=0, orn=False, fmt="image", p=100, wh=size, f=os.path.join(path, name))

def selectGeoSet():
    cmds.select(cl=True)
    if cmds.objExists('geoSet'):
        cmds.select( "geoSet", r=True, ne=True)
        cmds.selectKey(clear=True)
        cmds.pickWalk(d="up")

def zoomToGeoSet():
    selectGeoSet
    cmds.viewFit()

def orthographicTurnScreenShot(name, path):
    curCam = cmds.lookThru( q=True )
    camName = cmds.camera(o=True)[0]
    grp = cmds.group(n="rotator", em=True )
    cmds.group( camName, parent="rotator")
    cmds.lookThru(camName)
    zoomToGeoSet()
    center = getCenterGeoSet()
    cmds.setAttr(grp + ".translateX", center[0])
    cmds.setAttr(grp + ".translateY", center[1])
    cmds.setAttr(grp + ".translateZ", center[2])
    cmds.setAttr(camName + ".translateX", 0)
    cmds.setAttr(camName + ".translateY", 0)
    cmds.setAttr(camName + ".translateZ", 1000)
    selectGeoSet()
    cmds.displaySmoothness( du=3, dv=3, pw=16, ps=4, po=3)
    cmds.select(cl=True)
    screenShot(name + "_front", path)
    cmds.setAttr(grp + ".rotateY", 45)
    screenShot(name + "_quarter", path)
    cmds.setAttr(grp + ".rotateY", 90)
    screenShot(name + "_side", path)
    cmds.lookThru(curCam)
    cmds.delete(camName)
    cmds.delete(grp)
    for s in ["front", "quarter", "side"]:
        original = os.path.join(path, name + "_" + s + ".0001.jpg")
        output =  os.path.join(path, name + "_" + s + ".jpg")
        try:
            os.rename(original, output)
        except WindowsError:
            os.remove(output)
            os.rename(original, output)