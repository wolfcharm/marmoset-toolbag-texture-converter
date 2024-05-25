import os.path
import subprocess
from os.path import exists


def open_(path, pyfile):
    if exists(path) & exists(pyfile):
        subprocess.run([path, pyfile])
