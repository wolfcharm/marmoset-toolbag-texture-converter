from configparser import ConfigParser
import Debugger
import StaticVariables

class Settings:
    marmosetPath = ''
    marmoset_doBake = ''
    marmoset_quitAfterBake = ''

def Init():
    Save()
    Load()

def Load():
    config = ConfigParser(allow_no_value=True)
    config.read(StaticVariables.configFile)
    Settings.marmosetPath = SafeGetOption(config, 'Paths', 'marmosetPath')
    Settings.marmoset_doBake = SafeGetOption(config, 'Marmoset', 'marmoset_doBake')
    Settings.marmoset_quitAfterBake = SafeGetOption(config, 'Marmoset', 'marmoset_quitAfterBake')

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
        SafeAddOption(config, 'Paths', 'marmosetPath', Settings.marmosetPath)
    if Settings.marmoset_doBake != "":
        SafeAddOption(config, 'Marmoset', 'marmoset_doBake', Settings.marmoset_doBake)
    if Settings.marmoset_quitAfterBake != "":
        SafeAddOption(config, 'Marmoset', 'marmoset_quitAfterBake', Settings.marmoset_quitAfterBake)
    with open(StaticVariables.configFile, 'w') as f:
        config.write(f)

def SafeAddSection(config, name: str):  # return True if section exist or was created successfully
    sections = config.sections()
    if name in sections:
        return True
    else:
        config.add_section(name)
        return True

def SafeAddOption(config: ConfigParser, section: str, optionName: str, optionValue: str):
    if SafeAddSection(config, section):
        config.set(section, optionName, optionValue)

def SafeGetOption(config: ConfigParser, section: str, name: str):
    if config.has_option(section, name):
        return config.get(section, name)
    else:
        return ''
