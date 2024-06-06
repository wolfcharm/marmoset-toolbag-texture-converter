import os.path
import subprocess
from os.path import exists
from PyQt6.QtWidgets import QWidget
import StaticVariables
import StoredSettings
import Debugger

bakerRecipe = ''

class RunParameters:
    albedoTexturePath: str
    metallicTexturePath: str
    roughnessTexturePath: str
    metallicChannel: str
    roughnessChannel: str
    savePath: str
    resolution: str

def Open(parameters: RunParameters, parent: QWidget):
    marmosetPath = StoredSettings.Settings.marmosetPath
    if exists(marmosetPath) & exists(StaticVariables.pyfile) & ('toolbag' in marmosetPath):
        if (not parameters.albedoTexturePath) or (not parameters.metallicTexturePath) or (not parameters.roughnessTexturePath):
            parent.texturesSetErrorDialog()
            Debugger.debugger_print('[Opener] Some textures are null')
            return

        PrepareRecipe(parameters.albedoTexturePath, parameters.metallicTexturePath, parameters.metallicChannel,
                      parameters.roughnessTexturePath, parameters.roughnessChannel, parameters.savePath,
                      parameters.resolution, StaticVariables.bakerMesh)
        subprocess.run([marmosetPath, StaticVariables.pyfile, bakerRecipe])
        RemoveRecipe()
    else:
        parent.showOpenErrorDialog()

def PrepareRecipe(*args: str):
    recipeFile = open(StaticVariables.defaultRecipeFile, "a+")
    recipeFile.truncate(0)

    for arg in args:
        if '.' in arg:  # weak check
            recipeFile.write(GetAbsolutePath(arg)+'\n')
        else:
            recipeFile.write(arg + '\n')

    recipeFile.close()
    global bakerRecipe
    bakerRecipe = os.path.abspath(StaticVariables.defaultRecipeFile)

def RemoveRecipe():
    os.remove(bakerRecipe)

def GetAbsolutePath(path):
    return os.path.abspath(path)

if __name__ == '__main__':

    PrepareRecipe('C:/Users/ichen/Desktop/wolf 100x100.png', '1str', 0, '1str', 0)
    file = open('data/.bakerRecipe', 'r')
    albedoTexturePath = file.readline().rstrip('\n')
    metallicTexturePath = file.readline().rstrip('\n')
    metallicChannel = file.readline().rstrip('\n')
    roughnessTexturePath = file.readline().rstrip('\n')
    roughnessChannel = file.readline().rstrip('\n')
    file.close()


