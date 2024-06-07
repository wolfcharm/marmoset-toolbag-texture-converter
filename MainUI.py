from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import pyqtSlot, Qt, QRect, QCoreApplication

import StaticVariables
import Opener
from Opener import RunParameters
from SettingsUI import *
from CustomUIElements import TextureCard, TextureCardGrayscale

class MainUI(QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()

        headerFont = QFont('Segoe UI', 12)
        mainWindow = QWidget(self)
        mainVLayout = QVBoxLayout(self)
        mainHLayout = QHBoxLayout(self)
        texturesCardsVLayout = QVBoxLayout(self)

        menuBar = QMenuBar(self)
        self.fileMenu = menuBar.addMenu("File")
        self.editMenu = menuBar.addMenu("Edit")
        self.editMenu.addAction("Preferences...", self.openSettings)
        self.setMenuBar(menuBar)

        # Bake Settings
        bakeSettingsLayout = QVBoxLayout(self)
        settingsLabel = QLabel('Bake Settings', self)
        settingsLabel.setFont(headerFont)
        settingsLabel.setAlignment(Qt.AlignmentFlag.AlignTop)
        bakeSettingsLayout.addWidget(settingsLabel)
        self.bakerResolutionSetting = ComboBoxSettings('Resolution', StaticVariables.bakeResolutions, self, '2048')
        self.bakerSamplesSetting = ComboBoxSettings('Samples', StaticVariables.bakeSamples, self, '16')

        bakeSettingsLayout.addLayout(self.bakerSamplesSetting)
        bakeSettingsLayout.addLayout(self.bakerResolutionSetting)
        bakeSettingsLayout.addStretch()

        # Texture Cards
        textureCardsLabel = QLabel('TextureCards', self)
        textureCardsLabel.setFont(headerFont)
        textureCardsLabel.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.textureCardAlb = TextureCard('Albedo', 150, 150, False, False, False, False, self)
        self.textureCardMet = TextureCardGrayscale('Metal', 150, 150, True, self)
        self.textureCardRough = TextureCardGrayscale('Roughness', 150, 150, True, self)

        self.fileMenu.addSeparator()
        self.fileMenu.addAction("Quit", lambda: QCoreApplication.quit())

        texturesCardsVLayout.addWidget(textureCardsLabel)
        texturesCardsVLayout.addLayout(self.textureCardAlb)
        texturesCardsVLayout.addLayout(self.textureCardMet)
        texturesCardsVLayout.addLayout(self.textureCardRough)
        texturesCardsVLayout.addStretch(1)

        # Separators
        hSeparator = QFrame(self)
        hSeparator.setGeometry(QRect(0, 0, 100, 1))
        hSeparator.setFrameShape(QFrame.Shape.HLine)

        vSeparator = QFrame(self)
        vSeparator.setGeometry(QRect(0, 0, 1, 100))
        vSeparator.setFrameShape(QFrame.Shape.VLine)

        # Save Name
        saveNameHlayout = QHBoxLayout(self)
        saveNameLabel = QLabel("Save Name", self)
        self.saveNameField = QLineEdit(self)
        self.saveNameField.resize(350, 20)
        # self.saveNameField.textChanged.connect(self.updateSavePath)
        self.saveExtensionDropdown = QComboBox(self)
        self.saveExtensionDropdown.addItems(StaticVariables.saveFormats)
        self.saveExtensionDropdown.setCursor(Qt.CursorShape.PointingHandCursor)
        saveNameHlayout.addWidget(saveNameLabel)
        saveNameHlayout.addWidget(self.saveNameField)
        saveNameHlayout.addWidget(self.saveExtensionDropdown)

        # Save Path
        savePathHlayout = QHBoxLayout(self)
        savePathLabel = QLabel("Save Location", self)
        self.savePathField = QLineEdit(self)
        self.savePathField.setEnabled(False)
        # self.pathField.textChanged.connect(self.updateSavePath)
        btn_browseSavePath = QPushButton('Browse...', self)
        btn_browseSavePath.clicked.connect(self.selectSavePath)
        btn_browseSavePath.setCursor(Qt.CursorShape.PointingHandCursor)
        savePathHlayout.addWidget(savePathLabel)
        savePathHlayout.addWidget(self.savePathField)
        savePathHlayout.addWidget(btn_browseSavePath)

        # Run Button
        buttonRun = QPushButton('Run', self)
        buttonRun.setFixedHeight(32)
        buttonRun.setObjectName('run_btn')
        buttonRun.setCursor(Qt.CursorShape.PointingHandCursor)
        buttonRun.clicked.connect(self.runProcess)

        # Main Layout Compose
        mainHLayout.addLayout(texturesCardsVLayout)
        mainHLayout.addWidget(vSeparator)
        mainHLayout.addLayout(bakeSettingsLayout)
        mainHLayout.addStretch()
        mainVLayout.addLayout(mainHLayout)
        mainVLayout.addWidget(hSeparator)
        mainVLayout.addLayout(saveNameHlayout)
        mainVLayout.addLayout(savePathHlayout)
        mainVLayout.addWidget(buttonRun)
        mainWindow.setLayout(mainVLayout)
        self.setCentralWidget(mainWindow)
        self.setGeometry(300, 300, 400, 0)
        self.setWindowTitle('Marmoset Texture Converter')
        self.show()

        self.settings = SettingsWindow()

    @pyqtSlot()
    def showOpenErrorDialog(self):
        popup = QMessageBox(self)
        popup.setWindowTitle('Error!')
        popup.setIcon(QMessageBox.Icon.Critical)
        popup.setFixedSize(600, 200)
        popup.setText("Selected .exe is not Toolbag application! Set proper .exe in Settings")
        popup.setStandardButtons(QMessageBox.StandardButton.Ok)
        popup.exec()

    @pyqtSlot()
    def texturesSetErrorDialog(self):
        popup = QMessageBox(self)
        popup.setWindowTitle('Error!')
        popup.setIcon(QMessageBox.Icon.Critical)
        popup.setFixedSize(600, 200)
        popup.setText("Some texture slots are empty! Please fill them out.")
        popup.setStandardButtons(QMessageBox.StandardButton.Ok)
        popup.exec()

    @pyqtSlot()
    def saveParametersErrorDialog(self, paramName: str):
        popup = QMessageBox(self)
        popup.setWindowTitle('Error!')
        popup.setIcon(QMessageBox.Icon.Critical)
        popup.setFixedSize(600, 200)
        popup.setText(f"Some parameters are empty! Please fill them out:\n{self.nicify_parameter_names(paramName)}")
        popup.setStandardButtons(QMessageBox.StandardButton.Ok)
        popup.exec()

    def nicify_parameter_names(self, rawParameterName: str):
        for key, value in StaticVariables.fancyParametersNames.items():
            if key == rawParameterName:
                return value

    @pyqtSlot(name='runprocess')
    def runProcess(self):
        runParams = RunParameters()
        runParams.albedoTexturePath = self.textureCardAlb.dropArea.filePath
        runParams.metallicTexturePath = self.textureCardMet.dropArea.filePath
        runParams.roughnessTexturePath = self.textureCardRough.dropArea.filePath
        runParams.metallicChannel = self.textureCardMet.get_active_channel()
        runParams.roughnessChannel = self.textureCardRough.get_active_channel()
        runParams.saveName = self.saveNameField.text() + self.saveExtensionDropdown.currentText()
        runParams.savePath = self.savePathField.text()
        runParams.bakeSamples = self.bakerSamplesSetting.get_selected_option_str()
        runParams.bakeResolution = self.bakerResolutionSetting.get_selected_option_str()
        Opener.Open(runParams, self)

    def selectSavePath(self):
        savePath_ = str(QFileDialog.getExistingDirectory(self, "Select Save Directory"))
        if savePath_:
            self.savePathField.setText(f'{savePath_}/')

    def openSettings(self):
        self.settings.show()
        self.settings.update()
