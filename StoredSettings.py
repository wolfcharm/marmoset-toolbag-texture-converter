from configparser import ConfigParser
import Debugger
import StaticVariables
import os
from os.path import exists

globalSectionName = 'Global'

class Settings:
    marmosetPath = os.getenv("SystemDrive")+"/Program Files/Marmoset/Toolbag 4/toolbag.exe"
    marmoset_doBake = '1'
    marmoset_quitAfterBake = '1'

def Init(parent):
    config = ConfigParser()
    config.read(StaticVariables.configFile)
    SafeAddSection(config, globalSectionName)
    InitializeParameters()
    Load()
    CheckMissingSettings(parent)

def Load():
    config = ConfigParser()
    config.read(StaticVariables.configFile)

    members = vars(Settings)
    for key in members.copy():
        if (not key.startswith('_')) & (key != ''):
            valFromFile, success = SafeGetOption(config, globalSectionName, key)
            if not success:
                Debugger.debugger_print(f'Option "[{globalSectionName}] {key}" in {StaticVariables.configFile} not found!')
            setattr(Settings, key, valFromFile)

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

    members = vars(Settings).copy()
    for key in members:
        if (not key.startswith('_')) & (key != ''):
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

def InitializeParameters():
    config = ConfigParser()
    config.read(StaticVariables.configFile)

    members = vars(Settings).copy()
    for key in members:
        if (not key.startswith('_')) & (key != ''):
            if not config.has_option(globalSectionName, key):
                value = getattr(Settings, key)
                SafeAddOption(config, globalSectionName, key, value)

    with open(StaticVariables.configFile, 'w') as f:
        config.write(f)

def CheckMissingSettings(parent):
    if not exists(Settings.marmosetPath):
        parent.showMissingToolbagPath()
