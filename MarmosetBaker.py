import mset
import sys

print('Marmoset Texture Converter run parameters', sys.argv)

albedoTexturePath = sys.argv[1]
metallicTexturePath = sys.argv[2]
roughnessTexturePath = sys.argv[3]

baker = mset.BakerObject()
baker.name = 'Marmoset Baker Executable'

hiMat = mset.Material('High')
hiMat.albedo.setField('Albedo Map', albedoTexturePath)
hiMat.albedo.getField("Albedo Map").sRGB = True

#['Metalness Map', 'Channel', 'Metalness', 'Invert']
hiMat.reflectivity.setField('Metalness Map', metallicTexturePath)
hiMat.reflectivity.getField("Metalness Map").sRGB = False

#['Roughness Map', 'Channel', 'Roughness', 'Invert;roughness']
hiMat.microsurface.setField('Roughness Map', metallicTexturePath)
hiMat.microsurface.getField("Roughness Map").sRGB = False


