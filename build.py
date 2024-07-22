import PyInstaller.__main__
import os

PyInstaller.__main__.run([
    'main.spec'
])

os.startfile(PyInstaller.DEFAULT_DISTPATH)