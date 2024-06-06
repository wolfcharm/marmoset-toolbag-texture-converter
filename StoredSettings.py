from configparser import ConfigParser
import Debugger
import StaticVariables

class Settings:
    marmosetPath = ''

def Init():
    config = ConfigParser()
    config.read(StaticVariables.configFile)
    SafeAddSection(config, 'Paths')
    with open(StaticVariables.configFile, 'w') as f:
        config.write(f)
    Save()
    Load()

def Load():
    config = ConfigParser(allow_no_value=True)
    config.read(StaticVariables.configFile)
    Settings.marmosetPath = SafeGetOption(config, 'Paths', 'marmosetPath')

def LoadArguments(section: str, arg: str, *args: str):
    config = ConfigParser(allow_no_value=True)
    config.read(StaticVariables.configFile)
    if not config.has_section(section):
        Debugger.debugger_print('There is no section {0} in {1}'.format(section, StaticVariables.configFile))
        return
    values = [SafeGetOption(config, section, arg)]
    for name in args:
        values.append(SafeGetOption(config, section, name))
    return values

def SaveArguments(section: str, namesValues: dict):
    config = ConfigParser()
    config.read(StaticVariables.configFile)
    if not config.has_section(section):
        SafeAddSection(config, section)

    for key, value in namesValues.items():
        config.set(section, key, value)
    with open(StaticVariables.configFile, 'w') as f:
        config.write(f)

def Save():
    config = ConfigParser()
    config.read(StaticVariables.configFile)
    if Settings.marmosetPath != "":
        config.set('Paths', 'marmosetPath', Settings.marmosetPath)
    with open(StaticVariables.configFile, 'w') as f:
        config.write(f)

def SafeAddSection(config, name: str):
    sections = config.sections()
    if name in sections:
        return
    else:
        config.add_section('Paths')

def SafeGetOption(config, section: str, name: str):
    if config.has_option(section, name):
        return config.get(section, name)
    else:
        return ''
