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

def LoadArguments(*args: str):
    config = ConfigParser()
    config.read(configFile)
    for arg in args:
        arg = config.get('', arg)
    return args

def SaveArguments(section: str, **kwargs):
    config = ConfigParser()
    config.read(configFile)
    for key, value in kwargs.items():
        config.set(section, key, value)
    with open(configFile, 'w') as f:
        config.write(f)

def Save():
    config = ConfigParser()
    config.read(configFile)
    if Settings.marmosetPath != "":
        config.set('Paths', 'marmosetPath', Settings.marmosetPath)
    with open(configFile, 'w') as f:
        config.write(f)

def AddSection(config, name: str):
    sections = config.sections()
    if name in sections:
        return
    else:
        config.add_section('Paths')
