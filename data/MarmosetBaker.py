import mset
import sys

print('Marmoset Texture Converter run parameters', sys.argv)

class Recipe(object):
    def __init__(self):
        self.pipeline = ''
        self.albedoTexturePath = ''
        self.metallicTexturePath = ''
        self.metallicChannel = ''
        self.roughnessTexturePath = ''
        self.roughnessChannel = ''
        self.specTexturePath = ''
        self.glossTexturePath = ''
        self.glossChannel = ''
        self.outputPath = f' .png'
        self.samples = ''
        self.resolution = ''
        self.bakerMesh = ''
        self.doBake = '1'
        self.quitAfterBake = '1'

    # order. see in Opener.py Open method
    # pipeline
    # albedoTexturePath
    # metallicTexturePath
    # metallicChannel
    # roughnessTexturePath
    # roughnessChannel
    # specTexturePath
    # glossTexturePath
    # glossChannel
    # savePath
    # saveName
    # bakeSamples
    # bakeResolution
    # bakerMesh
    # doBake
    # quitAfterBake

    def get_baker_recipe(self, recipeFile):
        file = open(recipeFile, 'r')
        self.pipeline = file.readline().rstrip('\n')
        self.albedoTexturePath = file.readline().rstrip('\n')
        self.metallicTexturePath = file.readline().rstrip('\n')
        self.metallicChannel = file.readline().rstrip('\n')
        self.roughnessTexturePath = file.readline().rstrip('\n')
        self.roughnessChannel = file.readline().rstrip('\n')
        self.specTexturePath = file.readline().rstrip('\n')
        self.glossTexturePath = file.readline().rstrip('\n')
        self.glossChannel = file.readline().rstrip('\n')
        self.outputPath = file.readline().rstrip('\n')
        saveName = file.readline().rstrip('\n')
        self.outputPath = f'{self.outputPath}{saveName}'
        self.samples = file.readline().rstrip('\n')
        self.resolution = file.readline().rstrip('\n')
        self.bakerMesh = file.readline().rstrip('\n')
        self.doBake = file.readline().rstrip('\n')
        self.quitAfterBake = file.readline().rstrip('\n')
        file.close()

def interpret_channels(index: int) -> [int, bool]:
    if index <= 3:
        return index, False
    if index == 4:  # white
        return 0, False
    if index == 5:  # black
        return 0, False
    if index == 6:  # 1-R
        return 0, True
    if index == 7:  # 1-G
        return 1, True
    if index == 8:  # 1-B
        return 2, True
    if index == 9:  # 1-A
        return 3, True
def main():
    recipe = Recipe()
    recipe.get_baker_recipe(sys.argv[1])

    baker = mset.BakerObject()
    baker.name = 'Marmoset Baker Executable'

    hiMat = mset.Material()
    hiMat.name = 'High'
    hiMat.albedo.setField('Albedo Map', recipe.albedoTexturePath)
    hiMat.albedo.getField("Albedo Map").sRGB = True

    if recipe.pipeline == '0':
        #['Metalness Map', 'Channel', 'Metalness', 'Invert']
        hiMat.reflectivity.setField('Metalness', 1.0)
        hiMat.reflectivity.setField('Metalness Map', recipe.metallicTexturePath)
        chIndex, invert = interpret_channels(int(recipe.metallicChannel))
        hiMat.reflectivity.setField('Channel', chIndex)
        hiMat.reflectivity.setField('Invert', invert)
        hiMat.reflectivity.getField("Metalness Map").sRGB = False
        #['Roughness Map', 'Channel', 'Roughness', 'Invert;roughness']
        hiMat.microsurface.setField('Roughness', 1.0)
        hiMat.microsurface.setField('Roughness Map', recipe.metallicTexturePath)
        chIndex, invert = interpret_channels(int(recipe.roughnessChannel))
        hiMat.microsurface.setField('Channel', chIndex)
        hiMat.microsurface.setField('Invert;roughness', invert)
        hiMat.microsurface.getField("Roughness Map").sRGB = False
        hiMat.microsurface.getFieldNames()

        # if channel set to 0 or 1
        if int(recipe.metallicChannel) == 4:
            hiMat.reflectivity.setField('Metalness', 1.0)
            hiMat.reflectivity.setField('Metalness Map', '')
            hiMat.reflectivity.setField('Channel', 0)
            hiMat.reflectivity.setField('Invert', False)

        if int(recipe.metallicChannel) == 5:
            hiMat.reflectivity.setField('Metalness', 0.0)
            hiMat.reflectivity.setField('Metalness Map', '')
            hiMat.reflectivity.setField('Channel', 0)
            hiMat.reflectivity.setField('Invert', False)

        if int(recipe.roughnessChannel) == 4:
            hiMat.microsurface.setField('Roughness', 1.0)
            hiMat.microsurface.setField('Roughness Map', '')
            hiMat.microsurface.setField('Channel', chIndex)
            hiMat.microsurface.setField('Invert;roughness', False)

        if int(recipe.roughnessChannel) == 5:
            hiMat.microsurface.setField('Roughness', 0.0)
            hiMat.microsurface.setField('Roughness Map', '')
            hiMat.microsurface.setField('Channel', chIndex)
            hiMat.microsurface.setField('Invert;roughness', False)

        baker.outputSamples = int(recipe.samples)
        baker.outputPath = recipe.outputPath
        baker.outputWidth = int(recipe.resolution)
        baker.outputHeight = int(recipe.resolution)
        baker.addGroup('Bake Group')
        baker.getMap("Normals").enabled = False
        baker.getMap("Albedo").enabled = True
        baker.getMap("Specular").enabled = True
        baker.getMap("Gloss").enabled = True

    elif recipe.pipeline == '1':
        hiMat.setSubroutine('reflectivity', 'Specular')
        hiMat.setSubroutine('microsurface', 'Gloss')
        # ['Specular Map', 'Channel;specular', 'Intensity', 'Color', 'Fresnel', 'Color;fresnel', 'Conserve Energy']
        hiMat.reflectivity.setField('Intensity', 1.0)
        hiMat.reflectivity.setField('Specular Map', recipe.specTexturePath)
        # hiMat.reflectivity.getField("Specular Map").sRGB = False
        # ['Gloss Map', 'Channel', 'Gloss', 'Invert']
        hiMat.microsurface.setField('Gloss', 1.0)
        hiMat.microsurface.setField('Gloss Map', recipe.glossTexturePath)
        chIndex, invert = interpret_channels(int(recipe.glossChannel))
        hiMat.microsurface.setField('Channel', chIndex)
        hiMat.microsurface.setField('Invert', invert)
        hiMat.microsurface.getField("Gloss Map").sRGB = False
        hiMat.microsurface.getFieldNames()

        # if channel set to 0 or 1
        if int(recipe.glossChannel) == 4:
            hiMat.microsurface.setField('Gloss', 1.0)
            hiMat.microsurface.setField('Gloss Map', '')
            hiMat.microsurface.setField('Channel', chIndex)
            hiMat.microsurface.setField('Invert', False)

        if int(recipe.glossChannel) == 5:
            hiMat.microsurface.setField('Gloss', 0.0)
            hiMat.microsurface.setField('Gloss Map', '')
            hiMat.microsurface.setField('Channel', chIndex)
            hiMat.microsurface.setField('Invert', False)

        baker.outputSamples = int(recipe.samples)
        baker.outputPath = recipe.outputPath
        baker.outputWidth = int(recipe.resolution)
        baker.outputHeight = int(recipe.resolution)
        baker.addGroup('Bake Group')
        baker.getMap("Normals").enabled = False
        baker.getMap("Albedo (Metal)").enabled = True
        baker.getMap("Metalness").enabled = True
        baker.getMap("Roughness").enabled = True

    else:
        return

    modelHi = mset.importModel(recipe.bakerMesh)
    modelHi.name = 'Quad_hi'
    modelLow = modelHi.duplicate('Quad_low')

    bakerHigh = baker.findInChildren('High')
    bakerLow = baker.findInChildren('Low')
    modelHi.parent = bakerHigh
    modelLow.parent = bakerLow
    hiMat.assign(modelHi, True)

    print(bool(int(recipe.doBake)), bool(int(recipe.quitAfterBake)))
    if bool(int(recipe.doBake)):
        mset.bakeAll()
        if bool(int(recipe.quitAfterBake)):
            mset.quit()


    #print(recipe.albedoTexturePath, recipe.metallicTexturePath, recipe.metallicChannel, recipe.roughnessTexturePath,
    #      recipe.roughnessChannel, recipe.bakerMesh)
    #print([my_object.name for my_object in bakerGroup[0].getChildren()])
    #print(modelHi.findInChildren('default').material)


if __name__ == '__main__':
    main()
