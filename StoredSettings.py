from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
config.get('Paths', 'marmosetPath')