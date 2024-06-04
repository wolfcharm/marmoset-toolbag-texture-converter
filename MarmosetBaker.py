import mset
import sys

sys.argv
print('AAAAAAAAAAAAAAAAAAAAAAAAAAAA', sys.argv)

albedoTexturePath = ''
metallicTexturePath = ''
roughnessTexturePath = ''

albedoMap = mset.MaterialSurfaceMap
albedoMap.texture = albedoTexturePath

baker = mset.BakerObject
baker.name = 'Marmoset Baker Executable'
hiMat = mset.Material
hiMat.name = 'High'
hiMat.albedo = albedoMap
