import os
import shutil
import re


path = r"S:\a.paris\Works\Atelier\test\testcopy"
dest = r"S:\a.paris\Works\Atelier\test\testcopy\Dest"


def copyTree(src, dst, exception=[]):
    for f in os.listdir(src):
        fp = os.path.join(src, f)

        if fp.endswith(dst):
            continue

        go = True
        for e in exception:
            e = e.replace("/", "\\")
            print(e)
            print(fp)
            if fp.endswith(e):
                go = False
        if not go:
            continue
        dfp = os.path.join(dst, f)
        if os.path.isfile(fp):
            # print("copy file " + f)
            shutil.copyfile(fp, dfp)
        elif os.path.isdir(fp):
            # print("create folder " + f)
            if not os.path.isdir(dfp):
                os.mkdir(dfp)
            copyTree(fp, dfp, exception=exception)


copyTree(path, dest, exception=["fileA", "/folderB/fileB"])