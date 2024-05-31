import os.path
import subprocess
from os.path import exists

def open_(path, pyfile, parent):
    if exists(path) & exists(pyfile) & ('toolbag' in path):
        subprocess.run([path, pyfile])
    else:
        parent.showOpenErrorDialog()
