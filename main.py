import sys
import os
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap, QBitmap, QColor, QWindow, QIcon, QFont
from PyQt6.QtCore import pyqtSlot, Qt, QEvent, QRect, QCoreApplication, QSize

import StaticVariables
import qdarktheme
import Opener
from Opener import RunParameters
import StoredSettings
from StoredSettings import Settings
from os.path import exists
import Debugger

Debugger.enabled = True

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

class ComboBoxSettings(QHBoxLayout):
    def __init__(self, labelText: str, comboOptions: list, parent, defaultOption: str = ''):
        super().__init__(parent)

        self.label = QLabel(labelText, parent)
        self.label.setMinimumSize(120, 8)
        self.dropdown = QComboBox(parent)
        self.dropdown.addItems(comboOptions)
        self.dropdown.setCursor(Qt.CursorShape.PointingHandCursor)
        if defaultOption != '':
            self.dropdown.setCurrentText(defaultOption)
        self.addWidget(self.label)
        self.addWidget(self.dropdown)

    def get_selected_option_int(self) -> int:
        return self.dropdown.currentIndex()

    def get_selected_option_str(self) -> str:
        return self.dropdown.currentText()

class ImageChannel(QHBoxLayout):
    def __init__(self, labelName: str, selectionItems: list, parent):
        super().__init__(parent)

        self.label = QLabel(labelName, parent)
        self.selection = QComboBox(parent)
        self.selection.setCursor(Qt.CursorShape.PointingHandCursor)

        self.selection.addItems(selectionItems)

        self.addWidget(self.label)
        self.addWidget(self.selection)

class ImageChannels(QVBoxLayout):
    def __init__(self, enableR: bool, enableG: bool, enableB: bool, enableA: bool, parent):
        super().__init__(parent)

        selectionItems = ['R', 'G', 'B', 'A', '1', '0', '1-R', '1-G', '1-B', '1-A']
        if enableR:
            self.R = ImageChannel('R', selectionItems, parent)
            self.addLayout(self.R)
        if enableG:
            self.G = ImageChannel('G', selectionItems, parent)
            self.addLayout(self.G)
        if enableB:
            self.B = ImageChannel('B', selectionItems, parent)
            self.addLayout(self.B)
        if enableA:
            self.A = ImageChannel('A', selectionItems, parent)
            self.addLayout(self.A)

        self.addSpacerItem(QSpacerItem(1,1, QSizePolicy.Policy.Expanding))

class ImageChannelsGrayscale(QVBoxLayout):
    def __init__(self, enableGrayscale: bool, parent):
        super().__init__(parent)

        selectionItems = ['R', 'G', 'B', 'A', '1', '0', '1-R', '1-G', '1-B', '1-A']
        if enableGrayscale:
            self.Grayscale = ImageChannel('Grayscale', selectionItems, parent)
            self.addLayout(self.Grayscale)
            self.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Policy.Expanding))

class DropArea(QLabel):
    def __init__(self, title: str, sizex: int, sizey: int, parent):
        super().__init__(parent)

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.styleSheet = ("QLabel{color: #888; border-style:dashed; border-color: rgba(255,255,255,50); border-width: 2px;}"
                           "\nQLabel:hover {border-color: rgba(255,255,255,100)}")
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._defaultText = title
        self.filePath = ''
        self.fileAssigned = False
        self.setText(self._defaultText)
        self.sizex = sizex
        self.sizey = sizey
        self.setFixedSize(sizex, sizey)
        self.setStyleSheet(self.styleSheet)
        self.mask = QBitmap('data/mask.png')
        self.pix: QPixmap = QPixmap()
        self.pix_light: QPixmap = QPixmap()
        self.setOpenExternalLinks(True)

        parent.fileMenu.addAction("Set {0} Texture...".format(title), self.selectTexture)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.selectTexture()

    def selectTexture(self):
        file = self.openFileSelectDialog()
        if not file: return
        self.filePath = file
        self.setPixmap(QPixmap(file))

    def openFileSelectDialog(self):
        filter_ = "Images (*{0})".format(' *'.join(StaticVariables.allowedImageFormats))
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Image", '',
                                                  filter_)
        if fileName:
            return fileName

    def setPixmap(self, image: QPixmap):
        self.pix = image
        scaled = QPixmap.scaled(image, self.sizex, self.sizey, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        super().setPixmap(scaled)
        super().setMask(self.mask)
        super().setStyleSheet('')
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)
        shadow.setOffset(2)
        shadow.setColor(Qt.GlobalColor.black)
        super().setGraphicsEffect(shadow)
        self.fileAssigned = True

    def enterEvent(self, e):
        pass

    def leaveEvent(self, event):
        pass

    def clearPixmap(self):
        super().setText(self._defaultText)
        super().setStyleSheet(self.styleSheet)
        super().clearMask()
        super().setGraphicsEffect(None)
        self.fileAssigned = False

    def dragEnterEvent(self, e):
        urls = e.mimeData().urls()

        if e.mimeData().hasUrls():
            if len(urls) > 1:
                e.ignore()
                return
            if any(ext in urls[0].toLocalFile() for ext in StaticVariables.allowedImageFormats):
                e.accept()

        else:
            e.ignore()

    def dropEvent(self, e):
        filePath = e.mimeData().urls()[0].toLocalFile()
        self.filePath = filePath
        self.setPixmap(QPixmap(filePath))
        # self.setText(e.mimeData().text())

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.MouseButton.RightButton:
            self.clearPixmap()

class TextureCard(QHBoxLayout):
    def __init__(self, title: str, previewsizex: int, previewsizey: int, displaychannelR: bool, displaychannelG: bool, displaychannelB: bool, displaychannelA: bool, parent):
        super().__init__(parent)

        textureCardHLayout = QHBoxLayout(parent)
        self.dropArea = DropArea(title, previewsizex, previewsizey, parent)
        textureCardHLayout.addWidget(self.dropArea)
        self.textureChannelsVLayout = ImageChannels(displaychannelR, displaychannelG, displaychannelB, displaychannelA, parent)

        textureCardHLayout.addLayout(self.textureChannelsVLayout)
        self.addLayout(textureCardHLayout)
        self.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Policy.Expanding))

    def get_active_channels(self):
        return [self.textureChannelsVLayout.R.selection.currentIndex(),
                self.textureChannelsVLayout.G.selection.currentIndex(),
                self.textureChannelsVLayout.B.selection.currentIndex(),
                self.textureChannelsVLayout.A.selection.currentIndex()]

class TextureCardGrayscale(QHBoxLayout):

    def __init__(self, title: str, previewsizex: int, previewsizey: int, displayGrayscale: bool, parent):
        super().__init__(parent)
        self.textureCardHLayout = QHBoxLayout(parent)
        self.dropArea = DropArea(title, previewsizex, previewsizey, parent)
        self.textureCardHLayout.addWidget(self.dropArea)
        self.textureChannelsVLayout = ImageChannelsGrayscale(displayGrayscale, parent)

        self.textureCardHLayout.addLayout(self.textureChannelsVLayout)
        self.addLayout(self.textureCardHLayout)
        self.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Policy.Expanding))

    def get_active_channel(self):
        return self.textureChannelsVLayout.Grayscale.selection.currentIndex()

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
        #self.saveNameField.textChanged.connect(self.updateSavePath)
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
        #self.pathField.textChanged.connect(self.updateSavePath)
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
        runParams.saveName = self.saveNameField.text()
        runParams.savePath = self.savePathField.text()
        runParams.bakeSamples = self.bakerSamplesSetting.get_selected_option_str()
        runParams.resolution = self.bakerResolutionSetting.get_selected_option_str()
        Opener.Open(runParams, self)

    def selectSavePath(self):
        savePath_ = str(QFileDialog.getExistingDirectory(self, "Select Save Directory"))
        if savePath_:
            self.savePathField.setText(f'{savePath_}/')

    def openSettings(self):
        self.settings.show()
        self.settings.update()


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
