import os.path
import subprocess
from os.path import exists
from PyQt6.QtWidgets import QWidget
import StaticVariables
import StoredSettings
import Debugger

bakerRecipe = ''

class RunParameters(object):
    def __init__(self):
        self._albedoTexturePath: str = ''
        self._metallicTexturePath: str = ''
        self._roughnessTexturePath: str = ''
        self._metallicChannel: str = ''
        self._roughnessChannel: str = ''
        self._saveName: str = ''
        self._savePath: str = ''
        self._bakeSamples: str = ''
        self._bakeResolution: str = ''

    @property
    def albedoTexturePath(self):
        return str(self._albedoTexturePath)

    @albedoTexturePath.setter
    def albedoTexturePath(self, value):
        self._albedoTexturePath = str(value)

    @property
    def metallicTexturePath(self):
        return str(self._metallicTexturePath)

    @metallicTexturePath.setter
    def metallicTexturePath(self, value):
        self._metallicTexturePath = str(value)

    @property
    def roughnessTexturePath(self):
        return str(self._roughnessTexturePath)

    @roughnessTexturePath.setter
    def roughnessTexturePath(self, value):
        self._roughnessTexturePath = str(value)

    @property
    def metallicChannel(self):
        return str(self._metallicChannel)

    @metallicChannel.setter
    def metallicChannel(self, value):
        self._metallicChannel = str(value)

    @property
    def roughnessChannel(self):
        return str(self._roughnessChannel)

    @roughnessChannel.setter
    def roughnessChannel(self, value):
        self._roughnessChannel = str(value)

    @property
    def savePath(self):
        return str(self._savePath)

    @savePath.setter
    def savePath(self, value):
        self._savePath = str(value)

    @property
    def bakeResolution(self):
        return str(self._bakeResolution)

    @bakeResolution.setter
    def bakeResolution(self, value):
        self._bakeResolution = str(value)

    @property
    def bakeSamples(self):
        return str(self._bakeSamples)

    @bakeSamples.setter
    def bakeSamples(self, value):
        self._bakeSamples = str(value)

    @property
    def saveName(self):
        return str(self._saveName)

    @saveName.setter
    def saveName(self, value):
        self._saveName = str(value)

    def validate(self):
        members = vars(self)
        for key, value in members.items():
            if value == '':
                return False, key
        return True, None


def Open(parameters: RunParameters, parent: QWidget):
    marmosetPath = StoredSettings.Settings.marmosetPath
    if exists(marmosetPath) & exists(StaticVariables.pyfile) & ('toolbag' in marmosetPath):
        if (not parameters.albedoTexturePath) or (not parameters.metallicTexturePath) or (not parameters.roughnessTexturePath):
            parent.texturesSetErrorDialog()
            Debugger.debugger_print('[Opener] Some textures are null')
            return

        valid, param = parameters.validate()
        if not valid:
            parent.saveParametersErrorDialog(param)
            Debugger.debugger_print('[Opener] Some textures are null')
            return

        PrepareRecipe(parameters.albedoTexturePath, parameters.metallicTexturePath, parameters.metallicChannel,
                      parameters.roughnessTexturePath, parameters.roughnessChannel, parameters.savePath, parameters.saveName,
                      parameters.bakeSamples, parameters.bakeResolution, StaticVariables.bakerMesh)

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


