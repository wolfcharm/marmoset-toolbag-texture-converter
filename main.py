import sys

import qdarktheme
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

import StaticVariables
import StoredSettings
from MainUI import MainUI

if __name__ == '__main__':
    qdarktheme.enable_hi_dpi()
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(StaticVariables.appIcon))
    qdarktheme.setup_theme("dark")
    qss = """
    QPushButton#run_btn, QPushButton#save_btn {
        background-color: #007700;
        border-color: #008800;
        border-width: 3px;
        color: #003300;
        font-size: 11pt;
        font-weight: bold;
    }
    
    QPushButton#disabled_run_btn{
        background-color: #333;
        border-color: #0022200;
        border-width: 3px;
        color: #555;
        font-size: 11pt;
        font-weight: bold;
    }
    
    QPushButton#save_btn {
        border-width: 2px;
        font-size: 10pt;
    }
    QPushButton#run_btn:hover, QPushButton#save_btn:hover {
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
    ui = MainUI()
    StoredSettings.Init(ui)
    sys.exit(app.exec())
