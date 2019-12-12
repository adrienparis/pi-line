import os
import sys
from shutil import copytree, ignore_patterns, rmtree

current_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
sys.path.append(current_path)

pathDest = "Q:/partage/library/Maya scripts/general/Pi-Line"

if os.path.exists(pathDest):
    print("delete old " + pathDest)
    rmtree(pathDest, ignore_errors=True)
    print("deleted")

copytree(current_path, pathDest, ignore=ignore_patterns('*.pyc', '.git', '.vscode', '.gitignore', 'uploader.py'))

time.sleep(10)