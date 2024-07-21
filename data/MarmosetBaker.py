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
        self.get_baker_recipe()

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

    def get_baker_recipe(self):
        file = open(sys.argv[1], 'r')
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

recipe = Recipe()

baker = mset.BakerObject()
baker.name = 'Marmoset Baker Executable'

hiMat = mset.Material('High')
hiMat.albedo.setField('Albedo Map', recipe.albedoTexturePath)
hiMat.albedo.getField("Albedo Map").sRGB = True

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

modelHi = mset.importModel(recipe.bakerMesh)
modelHi.name = 'Quad_hi'
modelLow = modelHi.duplicate('Quad_low')

baker.outputSamples = int(recipe.samples)
baker.outputPath = recipe.outputPath
baker.outputWidth = int(recipe.resolution)
baker.outputHeight = int(recipe.resolution)
baker.addGroup('Bake Group')
baker.getMap("Normals").enabled = False
baker.getMap("Albedo").enabled = True
baker.getMap("Specular").enabled = True
baker.getMap("Gloss").enabled = True

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


