import os.path
import subprocess
from os.path import exists
from PyQt6.QtWidgets import QWidget

import Debugger


def Open(path, pyfile, albedoPath: str, metallicPath: str, roughnessPath: str, parent: QWidget):
    if exists(path) & exists(pyfile) & ('toolbag' in path):
        if (not albedoPath) or (not metallicPath) or (not roughnessPath):
            parent.texturesSetErrorDialog()
            Debugger.debugger_print('[Opener] Some textures are null')
            return

        subprocess.run([path, pyfile, albedoPath, metallicPath, roughnessPath])
    else:
        parent.showOpenErrorDialog()

# def PrepareRecipe(albedoPath: str, metallicPath: str, roughnessPath: str):
#     with open("bakerRecipe", "a+") as f:
#         f.write(albedoPath+'\n')
#         f.write(metallicPath+'\n')
#         f.write(roughnessPath+'\n')
