import mset
import sys

print('Marmoset Texture Converter run parameters', sys.argv)

class Recipe(object):
    def __init__(self):
        self.albedoTexturePath = ''
        self.metallicTexturePath = ''
        self.metallicChannel = 0
        self.roughnessTexturePath = ''
        self.roughnessChannel = 0
        self.outputPath = f' .png'

        self.get_baker_recipe()

    def get_baker_recipe(self):
        file = open(sys.argv[1], 'r')
        self.albedoTexturePath = file.readline().rstrip('\n')
        self.metallicTexturePath = file.readline().rstrip('\n')
        self.metallicChannel = file.readline().rstrip('\n')
        self.roughnessTexturePath = file.readline().rstrip('\n')
        self.roughnessChannel = file.readline().rstrip('\n')
        self.outputPath = f' .png'
        file.close()


recipe = Recipe()

baker = mset.BakerObject()
baker.name = 'Marmoset Baker Executable'

hiMat = mset.Material('High')
hiMat.albedo.setField('Albedo Map', recipe.albedoTexturePath)
hiMat.albedo.getField("Albedo Map").sRGB = True

#['Metalness Map', 'Channel', 'Metalness', 'Invert']
hiMat.reflectivity.setField('Metalness Map', recipe.metallicTexturePath)
hiMat.reflectivity.setField('Channel', int(recipe.metallicChannel))
hiMat.reflectivity.getField("Metalness Map").sRGB = False

#['Roughness Map', 'Channel', 'Roughness', 'Invert;roughness']
hiMat.microsurface.setField('Roughness Map', recipe.metallicTexturePath)
hiMat.microsurface.setField('Channel', int(recipe.roughnessChannel))
hiMat.microsurface.getField("Roughness Map").sRGB = False
hiMat.microsurface.getFieldNames()

baker.outputSamples = 64
baker.outputPath = recipe.outputPath
baker.outputWidth = 2048
baker.outputHeight = 2048
baker.addGroup('Bake Group')
baker.getMap("Normals").enabled = False
baker.getMap("Albedo (Metal)").enabled = True
baker.getMap("Specular").enabled = True
baker.getMap("Gloss").enabled = True

print(recipe.albedoTexturePath, recipe.metallicTexturePath, recipe.metallicChannel, recipe.roughnessTexturePath,
      recipe.roughnessChannel)

