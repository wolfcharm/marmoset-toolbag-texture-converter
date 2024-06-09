from configparser import ConfigParser
import Debugger
import StaticVariables

globalSectionName = 'Global'

class Settings:
    marmosetPath = ''
    marmoset_doBake = ''
    marmoset_quitAfterBake = ''

def Init():
    config = ConfigParser(allow_no_value=True)
    config.read(StaticVariables.configFile)
    SafeAddSection(config, globalSectionName)
    Save()
    Load()

def Load():
    config = ConfigParser()
    config.read(StaticVariables.configFile)

    members = vars(Settings)
    for key in members.copy():
        if (not key.startswith('__')) & (key != ''):
            memberObj = getattr(Settings, key)
            valFromFile, success = SafeGetOption(config, globalSectionName, key)
            if not success:
                Debugger.debugger_print(f'Option "[{globalSectionName}] {key}" in {StaticVariables.configFile} not found!')
            setattr(Settings, memberObj, valFromFile)

def LoadArguments(section: str, arg: str, *args: str):
    config = ConfigParser()
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

    members = vars(Settings)
    for key in members:
        if (not key.startswith('__')) & (key != ''):
            value = getattr(Settings, key)
            SafeAddOption(config, globalSectionName, key, value)

    with open(StaticVariables.configFile, 'w') as f:
        config.write(f)

def SafeAddSection(config: ConfigParser, name: str):  # return True if section exist or was created successfully
    sections = config.sections()
    if name not in sections:
        config.add_section(name)

def SafeAddOption(config: ConfigParser, section: str, optionName: str, optionValue: str):
    SafeAddSection(config, section)
    config.set(section, optionName, optionValue)

def SafeGetOption(config: ConfigParser, section: str, name: str):
    if config.has_option(section, name):
        return config.get(section, name), True
    else:
        return '', False
