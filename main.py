import sys
import os
from PyQt6.QtGui import QIcon

import qdarktheme
from os.path import exists
from SettingsUI import *
from MainUI import *

def CheckMissingSettings():

    path = os.getenv("SystemDrive")+"/Program Files/Marmoset/Toolbag 4/toolbag.exe"
    if not Settings.marmosetPath:
        if not exists(path):
            qdarktheme.setup_theme("auto")
            popup = QMessageBox(ui)
            popup.setWindowTitle('Warning')
            popup.setFixedSize(600, 200)
            popup.setText("toolbag.exe not found. Dou You want to specify path to Marmoset now?")
            popup.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            result = popup.exec()
            if result == QMessageBox.StandardButton.Yes:
                ui.openSettings()
        else:
            Settings.marmosetPath = path
            StoredSettings.Save()

if __name__ == '__main__':
    qdarktheme.enable_hi_dpi()
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('data/icon.png'))
    qdarktheme.setup_theme("dark")
    qss = """
    QPushButton#run_btn {
        background-color: #007700;
        border-color: #008800;
        border-width: 3px;
        color: #003300;
        font-size: 11pt;
        font-weight: bold;
    }
    QPushButton#run_btn:hover {
        background-color: #008800;
    }
    QLineEdit:enabled {
        background-color:#17171a;
    }
    QLineEdit:disabled {
        background-color: #202124;
        border-color: #333;
    }
    """
    qdarktheme.setup_theme(additional_qss=qss, custom_colors={"primary": "#009900"})
    StoredSettings.Init()
    ui = MainUI()
    CheckMissingSettings()
    sys.exit(app.exec())
