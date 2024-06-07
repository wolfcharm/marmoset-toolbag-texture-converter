from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSlot, QRect

import StoredSettings
from StoredSettings import Settings
import Debugger
from CustomUIElements import ComboBoxSettings

Debugger.enabled = True

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setMinimumSize(600, 50)
        #self.setGeometry(0, 0, 400, 400)
        mainLayout = QVBoxLayout()

        marmosetSelectExeLayout = QHBoxLayout()
        labelMarmosetPath = QLabel('Marmoset path', self)
        self.fieldMarmosetPath = QLineEdit(self)
        self.fieldMarmosetPath.setEnabled(False)
        btnSelectMarmosetFile = QPushButton('Browse...', self)
        btnSelectMarmosetFile.clicked.connect(self.openFileDialog)
        marmosetSelectExeLayout.addWidget(labelMarmosetPath)
        marmosetSelectExeLayout.addWidget(self.fieldMarmosetPath)
        marmosetSelectExeLayout.addWidget(btnSelectMarmosetFile)

        self.marmosetDoBakeSetting = ComboBoxSettings('Actually Bake', ['No', 'Yes'], self, 'Yes')

        separator = QFrame(self)
        separator.setGeometry(QRect(0, 0, 100, 1))
        separator.setFrameShape(QFrame.Shape.HLine)

        saveBtnLayout = QHBoxLayout()
        btnSave = QPushButton('Save', self)
        btnSave.setMaximumWidth(100)
        btnSave.clicked.connect(self.saveSettings)
        saveBtnLayout.addWidget(btnSave)

        mainLayout.addLayout(marmosetSelectExeLayout)
        mainLayout.addWidget(separator)
        mainLayout.addLayout(saveBtnLayout)
        self.setLayout(mainLayout)

    @pyqtSlot(name='selectExe')
    def openFileDialog(self):
        Debugger.debugger_print('pressed')
        fileName = self.selectExe()
        if not fileName:
            return
        else:
            self.fieldMarmosetPath.setText(fileName)

    def selectExe(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Select toolbag.exe", self.fieldMarmosetPath.text(),
                                                  "Executable (*.exe)")
        if fileName:
            return fileName

    def saveSettings(self):
        Settings.marmosetPath = self.fieldMarmosetPath.text()
        StoredSettings.Save()
        self.close()

    def update(self):
        self.fieldMarmosetPath.setText(Settings.marmosetPath)
