from configparser import ConfigParser

configFile = 'settings.ini'

class Settings:
    marmosetPath = ''
    pyfile = "MarmosetBaker.py"

def Init():
    config = ConfigParser()
    config.read(configFile)
    AddSection(config, 'Paths')
    with open(configFile, 'w') as f:
        config.write(f)
    Save()
    Load()

def Load():
    config = ConfigParser()
    config.read(configFile)
    Settings.marmosetPath = config.get('Paths', 'marmosetPath')
    Settings.pyfile = config.get('Paths', 'pyfile')

def LoadArguments(*args: str):
    config = ConfigParser()
    config.read(configFile)
    for arg in args:
        arg = config.get('', arg)
    return args

def SaveArguments(section:str, *args):
    config = ConfigParser()
    config.read(configFile)
    for arg in args:
        config.set(section, arg)
    with open(configFile, 'w') as f:
        config.write(f)

def Save():
    config = ConfigParser()
    config.read(configFile)
    config.set('Paths', 'marmosetPath', Settings.marmosetPath)
    config.set('Paths','pyfile', Settings.pyfile)
    with open(configFile, 'w') as f:
        config.write(f)

def AddSection(config, name: str):
    sections = config.sections()
    if name in sections:
        return
    else:
        config.add_section('Paths')
