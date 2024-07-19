import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

allowedImageFormats = ['.jpg', '.png', '.tga', '.psd', '.psb', '.exr', '.hdr', '.mpic', '.bmp', '.dds', '.tig', '.pfm']
saveFormats = ['.psd', '.tga', '.png', '.jpg', '.jpeg']
bakeResolutions = ['64', '128', '256', '512', '1024', '2048', '4096', '8192']
bakeSamples = ['1', '4', '16', '64']
appIcon = resource_path('data/icon.ico')
bakerMesh = resource_path('data/Quad.obj')
configFile = 'settings.ini'
pyfile = resource_path('data/MarmosetBaker.py')
defaultRecipeFile = resource_path('data/.bakerRecipe')
fancyParametersNames = {'_savePath': 'Save Location', '_saveName': 'Save Name'}
transparencyTexture = resource_path('data/transparency.png')
textureWhite = resource_path('data/white.tif')
textureBlack = resource_path('data/black.tif')

textureWhiteOS = resource_path(textureWhite)


