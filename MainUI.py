from PyQt6.QtCore import QCoreApplication
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMainWindow, QMenuBar, QLabel, QLineEdit, QComboBox, QFileDialog, QStackedWidget

import Opener
import StaticVariables
from CustomUIElements import TextureCardRGB, TextureCardGrayscale, ComboBoxSetting
from Opener import RunParameters
from SettingsUI import *


class MainUI(QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()

        headerFont = QFont('Futura', 12)
        mainWindow = QWidget(self)
        mainVLayout = QVBoxLayout(self)
        mainHLayout = QHBoxLayout(self)

        menuBar = QMenuBar(self)
        self.fileMenu = menuBar.addMenu("File")
        self.editMenu = menuBar.addMenu("Edit")
        self.editMenu.addAction("Preferences...", self.openSettings)
        self.setMenuBar(menuBar)

        # Separators
        hSeparator = QFrame(self)
        hSeparator.setGeometry(QRect(0, 0, 100, 1))
        hSeparator.setFrameShape(QFrame.Shape.HLine)

        vSeparator = QFrame(self)
        vSeparator.setGeometry(QRect(0, 0, 1, 100))
        vSeparator.setFrameShape(QFrame.Shape.VLine)

        # Pipeline selector
        pipelineSelectionLayout = QVBoxLayout(self)
        pipelineLabel = QLabel('Pipeline selection', self)
        pipelineLabel.setFont(headerFont)
        pipelineLabel.setAlignment(Qt.AlignmentFlag.AlignTop)
        pipelineSelectionLayout.addWidget(pipelineLabel)
        self.pipelineSelection = ComboBoxSetting(self, '', StaticVariables.pipelines, StaticVariables.pipelines[0],
                                                      labelMinWidth=100)
        pipelineSelectionLayout.addLayout(self.pipelineSelection)
        # pipelineSelectionLayout.addStretch()

        # Bake Settings
        bakeSettingsLayout = QVBoxLayout(self)
        settingsLabel = QLabel('Bake Settings', self)
        settingsLabel.setFont(headerFont)
        settingsLabel.setAlignment(Qt.AlignmentFlag.AlignTop)
        bakeSettingsLayout.addWidget(settingsLabel)
        self.bakerResolutionSetting = ComboBoxSetting(self,'Resolution', StaticVariables.bakeResolutions, '2048', labelMinWidth=100)
        self.bakerSamplesSetting = ComboBoxSetting(self, 'Samples', StaticVariables.bakeSamples, '16', labelMinWidth=100)

        bakeSettingsLayout.addLayout(self.bakerSamplesSetting)
        bakeSettingsLayout.addLayout(self.bakerResolutionSetting)
        bakeSettingsLayout.addStretch()

        # Texture Cards
        texturesCardsVLayout = QVBoxLayout(self)
        self.texturesCardsStackedWidget = QStackedWidget()
        textureCardsLabel = QLabel('Texture Cards', self)
        textureCardsLabel.setFont(headerFont)
        textureCardsLabel.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.textureCardAlb = TextureCardRGB('Albedo', 150, 150, False, False, False, False, self)
        self.textureCardMetal = TextureCardGrayscale('Metal', 150, 150, True, self)
        self.textureCardRough = TextureCardGrayscale('Roughness', 150, 150, True, self)
        self.textureCardSpec = TextureCardRGB('Specular', 150, 150, False, False, False, False, self)
        self.textureCardGloss = TextureCardGrayscale('Gloss', 150, 150, True, self)

        metalToSpecCards = PipelineCards(self, self.textureCardMetal, self.textureCardRough)
        specToMetalCards = PipelineCards(self, self.textureCardSpec, self.textureCardGloss)

        self.fileMenu.addSeparator()
        self.fileMenu.addAction("Quit", self.quitApplication)

        texturesCardsVLayout.addWidget(textureCardsLabel)
        self.texturesCardsStackedWidget.addWidget(metalToSpecCards)
        self.texturesCardsStackedWidget.addWidget(specToMetalCards)

        texturesCardsVLayout.addLayout(self.textureCardAlb)
        texturesCardsVLayout.addWidget(self.texturesCardsStackedWidget)
        texturesCardsVLayout.addStretch(1)

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
        mainVLayout.addLayout(pipelineSelectionLayout)
        mainVLayout.addWidget(hSeparator)
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
        self.pipelineSelection.valueChanged.connect(lambda: self.changePipeline())
        self.changePipeline()

    def changePipeline(self):
        self.texturesCardsStackedWidget.setCurrentIndex(self.pipelineSelection.get_selected_option_int())

    def showOpenErrorDialog(self):
        popup = QMessageBox(self)
        popup.setWindowTitle('Error!')
        popup.setIcon(QMessageBox.Icon.Critical)
        popup.setFixedSize(600, 200)
        popup.setText("Selected .exe is not Toolbag application! Set proper .exe in Settings")
        popup.setStandardButtons(QMessageBox.StandardButton.Ok)
        popup.exec()

    def texturesSetErrorDialog(self):
        popup = QMessageBox(self)
        popup.setWindowTitle('Error!')
        popup.setIcon(QMessageBox.Icon.Critical)
        popup.setFixedSize(600, 200)
        popup.setText("Some texture slots are empty! Please fill them out.")
        popup.setStandardButtons(QMessageBox.StandardButton.Ok)
        popup.exec()

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
        return rawParameterName


    def runProcess(self):
        runParams = RunParameters()
        runParams.pipeline = self.pipelineSelection.get_selected_option_int()
        runParams.albedoTexturePath = self.textureCardAlb.dropArea.filePath
        runParams.metallicTexturePath = self.textureCardMetal.dropArea.filePath
        runParams.roughnessTexturePath = self.textureCardRough.dropArea.filePath
        runParams.metallicChannel = self.textureCardMetal.get_active_channel()
        runParams.roughnessChannel = self.textureCardRough.get_active_channel()
        runParams.specularTexturePath = self.textureCardSpec.dropArea.filePath
        runParams.glossTexturePath = self.textureCardGloss.dropArea.filePath
        runParams.glossChannel = self.textureCardGloss.get_active_channel()
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

    def showMissingToolbagPath(self):
        popup = QMessageBox(self)
        popup.setWindowTitle('Warning')
        popup.setFixedSize(600, 200)
        popup.setText("toolbag.exe not found. Do You want to specify path to Marmoset now?")
        popup.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        result = popup.exec()
        if result == QMessageBox.StandardButton.Yes:
            self.openSettings()

    def quitApplication(self):
        QCoreApplication.quit()

    def closeEvent(self, event):
        self.quitApplication()

class PipelineCards(QWidget):
    def __init__(self, parent, *cards: QWidget):
        super().__init__(parent)

        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        for layout in cards:
            mainLayout.addLayout(layout)

        self.setLayout(mainLayout)
