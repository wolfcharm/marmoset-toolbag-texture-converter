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
        self.setMinimumWidth(550)
        #self.setGeometry(0, 0, 400, 400)
        mainVLayout = QVBoxLayout(self)

        self._hasChanges = False

        self.marmosetPathSetting = LinePathSetting(self, 'Marmoset Path', settingName='marmosetPath')
        self.marmosetPathSetting.valueChanged.connect(lambda: self.setHasChanges(True))
        self.marmosetDoBakeSetting = CheckBoxSetting(self, 'Actually Bake', True, 'marmoset_doBake')
        self.marmosetDoBakeSetting.valueChanged.connect(lambda: self.setHasChanges(True))
        self.marmosetQuitAfterBakeSetting = CheckBoxSetting(self, 'Close Toolbag After Bake', True, 'marmoset_quitAfterBake')
        self.marmosetQuitAfterBakeSetting.valueChanged.connect(lambda: self.setHasChanges(True))


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
        self.updateSettings()

    def setHasChanges(self, value: bool):
        self._hasChanges = value

    def showEvent(self, a0):
        self.updateSettings()

    def saveSettings(self):
        members = vars(self)
        for key in members.keys():
            if not key.startswith('_'):
                memberObj = getattr(self, key)
                settingName = getattr(memberObj, 'settingName')
                func = getattr(memberObj, 'get_savable_option')
                result = func()
                setattr(Settings, settingName, result)

        StoredSettings.Save()
        self._hasChanges = False
        self.close()

    def updateSettings(self):
        members = vars(self)
        for key in members.keys():
            if not key.startswith('_'):
                memberObj = getattr(self, key)
                settingName = str(getattr(memberObj, 'settingName'))
                savedValue = vars(Settings).get(settingName)
                func = getattr(memberObj, 'set_option')
                func(savedValue)
        self.setHasChanges(False)

    def closeEvent(self, event):
        if self._hasChanges:
            popup = QMessageBox(self)
            popup.setWindowTitle('Saving')
            popup.setFixedSize(600, 200)
            popup.setIcon(QMessageBox.Icon.Question)
            popup.setText("Do You want to save settings before leave?")
            popup.setStandardButtons(QMessageBox.StandardButton.Save | QMessageBox.StandardButton.No)
            result = popup.exec()
            if result == QMessageBox.StandardButton.Save:
                self.saveSettings()
            if result == QMessageBox.StandardButton.No:
                self.setHasChanges(False)
        self.setHasChanges(False)
