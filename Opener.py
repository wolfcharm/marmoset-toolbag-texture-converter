import os.path
import subprocess
from os.path import exists
from PyQt6.QtWidgets import QWidget
import Debugger

bakerRecipe = ''

def Open(path, pyfile, albedoPath: str, metallicPath: str, metallicChannel: int, roughnessPath: str, roughChannel: int, parent: QWidget):
    if exists(path) & exists(pyfile) & ('toolbag' in path):
        if (not albedoPath) or (not metallicPath) or (not roughnessPath):
            parent.texturesSetErrorDialog()
            Debugger.debugger_print('[Opener] Some textures are null')
            return

        PrepareRecipe(albedoPath, metallicPath, metallicChannel, roughnessPath, roughChannel)
        subprocess.run([path, pyfile, bakerRecipe])
        RemoveRecipe()
    else:
        parent.showOpenErrorDialog()

def PrepareRecipe(albedoPath: str, metallicPath: str, metallicChannel: int, roughnessPath: str, roughChannel: int):
    file = open(".bakerRecipe", "a+")
    file.truncate(0)
    file.write(albedoPath+'\n')
    file.write(metallicPath+'\n')
    file.write(str(metallicChannel)+'\n')
    file.write(roughnessPath+'\n')
    file.write(str(roughChannel)+'\n')
    file.close()
    global bakerRecipe
    bakerRecipe = os.path.abspath('data/.bakerRecipe')

def RemoveRecipe():
    os.remove(bakerRecipe)

if __name__ == '__main__':

    PrepareRecipe('C:/Users/ichen/Desktop/wolf 100x100.png', '1str', 0, '1str', 0)
    file = open('data/.bakerRecipe', 'r')
    albedoTexturePath = file.readline().rstrip('\n')
    metallicTexturePath = file.readline().rstrip('\n')
    metallicChannel = file.readline().rstrip('\n')
    roughnessTexturePath = file.readline().rstrip('\n')
    roughnessChannel = file.readline().rstrip('\n')
    file.close()


