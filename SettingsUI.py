from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSlot, QRect, Qt

import StoredSettings
from StoredSettings import Settings
import Debugger
from CustomUIElements import ComboBoxSetting, CheckBoxSetting, LinePathSetting

Debugger.enabled = True

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setMinimumSize(600, 50)
        #self.setGeometry(0, 0, 400, 400)
        mainVLayout = QVBoxLayout(self)

        self.marmosetPathSetting = LinePathSetting(self, 'Marmoset Path', settingName='marmosetPath')
        self.marmosetDoBakeSetting = CheckBoxSetting(self, 'Actually Bake', True, 'marmoset_doBake')
        self.marmosetQuitAfterBakeSetting = CheckBoxSetting(self, 'Close Toolbag After Bake', True, 'marmoset_quitAfterBake')

        separator = QFrame(self)
        separator.setGeometry(QRect(0, 0, 100, 1))
        separator.setFrameShape(QFrame.Shape.HLine)

        saveBtnLayout = QHBoxLayout()
        btnSave = QPushButton('Save', self)
        btnSave.setMaximumWidth(100)
        btnSave.setCursor(Qt.CursorShape.PointingHandCursor)
        btnSave.clicked.connect(self.saveSettings)
        btnSave.setObjectName('save_btn')
        saveBtnLayout.addWidget(btnSave)

        mainVLayout.addLayout(self.marmosetPathSetting)
        mainVLayout.addLayout(self.marmosetDoBakeSetting)
        mainVLayout.addLayout(self.marmosetQuitAfterBakeSetting)
        mainVLayout.addWidget(separator)
        mainVLayout.addLayout(saveBtnLayout)
        self.setLayout(mainVLayout)

    def saveSettings(self):
        members = vars(self)
        for key in members.keys():
            memberObj = getattr(self, key)
            settingName = getattr(memberObj, 'settingName')
            func = getattr(memberObj, 'get_savable_option')
            result = func()
            setattr(Settings, settingName, result)

        StoredSettings.Save()
        self.close()

    def update(self):
        members = vars(self)
        for key in members.keys():
            memberObj = getattr(self, key)
            settingName = getattr(memberObj, 'settingName')
            savedValue = vars(Settings).get(settingName)
            func = getattr(memberObj, 'set_option')
            func(savedValue)
