import os
import subprocess
from os.path import exists

from PyQt6.QtWidgets import QWidget

import Debugger
import StaticVariables
import StoredSettings

bakerRecipe = ''

class RunParameters(object):
    def __init__(self):
        self._pipeline: str = ''
        self._saveName: str = ''
        self._savePath: str = ''
        self._albedoTexturePath: str = ''
        self._metallicTexturePath: str = ''
        self._roughnessTexturePath: str = ''
        self._metallicChannel: str = ''
        self._roughnessChannel: str = ''
        self._specularTexturePath: str = ''
        self._glossTexturePath: str = ''
        self._glossChannel: str = ''
        self._bakeSamples: str = ''
        self._bakeResolution: str = ''

    @property
    def pipeline(self):
        return str(self._pipeline)

    @pipeline.setter
    def pipeline(self, value):
        self._pipeline = str(value)

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
    def specTexturePath(self):
        return str(self._specularTexturePath)

    @specTexturePath.setter
    def specTexturePath(self, value):
        self._specularTexturePath = str(value)

    @property
    def glossTexturePath(self):
        return str(self._glossTexturePath)

    @glossTexturePath.setter
    def glossTexturePath(self, value):
        self._glossTexturePath = str(value)

    @property
    def glossChannel(self):
        return str(self._glossChannel)

    @glossChannel.setter
    def glossChannel(self, value):
        self._glossChannel = str(value)

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
            if value == '' or value[0] == '.':
                return False, key
        return True, None

def Open(parameters: RunParameters, parent: QWidget):
    marmosetPath = StaticVariables.resource_path(StoredSettings.Settings.marmosetPath)
    if exists(marmosetPath) & exists(StaticVariables.pyfile) & ('toolbag' in marmosetPath):

        if parameters.pipeline == '0':
            valid, param = parameters.validate()
            if not valid:
                if param == '_specularTexturePath' or param == '_glossTexturePath':
                    pass
                else:
                    parent.saveParametersErrorDialog(param)
                    Debugger.debugger_print(f'[Opener] Some textures are null: {param}')
                    return

            PrepareRecipe(parameters.pipeline, parameters.albedoTexturePath, parameters.metallicTexturePath,
                          parameters.metallicChannel, parameters.roughnessTexturePath, parameters.roughnessChannel,
                          parameters.specTexturePath, parameters.glossTexturePath, parameters.glossChannel,
                          parameters.savePath, parameters.saveName, parameters.bakeSamples, parameters.bakeResolution,
                          StaticVariables.bakerMesh, StoredSettings.Settings.marmoset_doBake,
                          StoredSettings.Settings.marmoset_quitAfterBake)

        if parameters.pipeline == '1':
            valid, param = parameters.validate()
            if not valid:
                if param == '_metallicTexturePath' or param == '_roughnessTexturePath':
                    pass
                else:
                    parent.saveParametersErrorDialog(param)
                    Debugger.debugger_print(f'[Opener] Some textures are null: {param}')
                    return
            PrepareRecipe(parameters.pipeline, parameters.albedoTexturePath, parameters.metallicTexturePath,
                          parameters.metallicChannel, parameters.roughnessTexturePath, parameters.roughnessChannel,
                          parameters.specTexturePath, parameters.glossTexturePath, parameters.glossChannel,
                          parameters.savePath, parameters.saveName, parameters.bakeSamples, parameters.bakeResolution,
                          StaticVariables.bakerMesh, StoredSettings.Settings.marmoset_doBake,
                          StoredSettings.Settings.marmoset_quitAfterBake)

        subprocess.run([marmosetPath, StaticVariables.pyfile, bakerRecipe])
        RemoveRecipe()
    else:
        parent.showOpenErrorDialog()

def PrepareRecipe(*args: str):
    recipeFile = open(StaticVariables.defaultRecipeFile, "a+")
    recipeFile.truncate(0)

    for arg in args:
        path = GetAbsolutePath(arg)
        if path is None:
            recipeFile.close()
            os.remove(os.path.abspath(StaticVariables.defaultRecipeFile))
            raise NotImplementedError('Bad path given to OS')
        recipeFile.write(path+'\n')

    recipeFile.close()
    global bakerRecipe
    bakerRecipe = os.path.abspath(StaticVariables.defaultRecipeFile)

def RemoveRecipe():
    os.remove(bakerRecipe)

def GetAbsolutePath(path):
    try:
        if (path == '') or (path[0] == '.') or ('.' not in path) or (not os.path.isfile(path)):
            return path
        return os.path.abspath(path)
    except:
        return None


if __name__ == '__main__':

    PrepareRecipe('C:/Users/ichen/Desktop/wolf 100x100.png', '1str', '1str')
    file = open('data/.bakerRecipe', 'r')
    albedoTexturePath = file.readline().rstrip('\n')
    metallicTexturePath = file.readline().rstrip('\n')
    metallicChannel = file.readline().rstrip('\n')
    roughnessTexturePath = file.readline().rstrip('\n')
    roughnessChannel = file.readline().rstrip('\n')
    file.close()


