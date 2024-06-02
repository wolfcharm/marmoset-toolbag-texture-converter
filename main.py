import sys
import os
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap, QBitmap, QColor, QWindow
from PyQt6.QtCore import pyqtSlot, Qt, QEvent, QRect, QCoreApplication, QSize

import qdarktheme
import Opener
import StoredSettings
from StoredSettings import Settings
from os.path import exists
import Debugger

Debugger.enabled = True

allowedImageFormats = ['.jpg', '.png', '.tga', '.psd', '.psb', '.exr', '.hdr', '.mpic', '.bmp', '.dds', '.tig', '.pfm']
savePath = ''

def CheckMissingSettings():
    path = os.getenv("SystemDrive")+"/Program Files/Marmoset/Toolbag 4/toolbag.exe"
    if not Settings.marmosetPath:
        if not exists(path):
            qdarktheme.setup_theme("auto")
            popup = QMessageBox(ui)
            popup.setWindowTitle('Warning')
            popup.setFixedSize(600, 200)
            popup.setText("toolbag.exe not found. Dou You want to specify path to Marmoset now?")
            popup.setStandardButtons(QMessageBox.StandardButton.Yes| QMessageBox.StandardButton.No)
            result = popup.exec()
            if result == QMessageBox.StandardButton.Yes:
                ui.openSettings()
        else:
            Settings.marmosetPath = path
            StoredSettings.Save()

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
            R = ImageChannel('R', selectionItems, parent)
            self.addLayout(R)
        if enableG:
            G = ImageChannel('G', selectionItems, parent)
            self.addLayout(G)
        if enableB:
            B = ImageChannel('B', selectionItems, parent)
            self.addLayout(B)
        if enableA:
            A = ImageChannel('A', selectionItems, parent)
            self.addLayout(A)

        self.addSpacerItem(QSpacerItem(1,1, QSizePolicy.Policy.Expanding))

class ImageChannelsGrayscale(QVBoxLayout):
    def __init__(self, enableGrayscale: bool, parent):
        super().__init__(parent)

        selectionItems = ['R', 'G', 'B', 'A', '1', '0', '1-R', '1-G', '1-B', '1-A']
        if enableGrayscale:
            Gr = ImageChannel('Grayscale', selectionItems, parent)
            self.addLayout(Gr)
            self.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Policy.Expanding))

class DropArea(QLabel):
    def __init__(self, title: str, sizex: int, sizey: int, parent):
        super().__init__(parent)

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.styleSheet = ("QLabel{border-style:dashed; border-color: rgba(255,255,255,50); border-width: 2px;}"
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
        self.mask = QBitmap('mask.png')
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
        filter_ = "Images (*{0})".format(' *'.join(allowedImageFormats))
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
            if any(ext in urls[0].toLocalFile() for ext in allowedImageFormats):
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
        textureChannelsVLayout = ImageChannels(displaychannelR, displaychannelG, displaychannelB, displaychannelA, parent)

        textureCardHLayout.addLayout(textureChannelsVLayout)
        self.addLayout(textureCardHLayout)
        self.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Policy.Expanding))

class TextureCardGrayscale(QHBoxLayout):

    def __init__(self, title: str, previewsizex: int, previewsizey: int, displayGrayscale: bool, parent):
        super().__init__(parent)
        self.textureCardHLayout = QHBoxLayout(parent)
        self.dropAreaAlbedo = DropArea(title, previewsizex, previewsizey, parent)
        self.textureCardHLayout.addWidget(self.dropAreaAlbedo)
        self.textureChannelsVLayout = ImageChannelsGrayscale(displayGrayscale, parent)

        self.textureCardHLayout.addLayout(self.textureChannelsVLayout)
        self.addLayout(self.textureCardHLayout)
        self.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Policy.Expanding))

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

        mainWindow = QWidget(self)
        mainVLayout = QVBoxLayout(self)

        menuBar = QMenuBar(self)
        self.fileMenu = menuBar.addMenu("File")
        self.editMenu = menuBar.addMenu("Edit")
        self.editMenu.addAction("Preferences...", self.openSettings)
        self.setMenuBar(menuBar)

        savePathHlayout = QHBoxLayout(self)
        savePathLabel = QLabel("Save Location", self)
        self.pathField = QLineEdit(self)
        self.pathField.resize(350, 20)
        self.pathField.setText(savePath)
        self.pathField.textChanged.connect(self.updateSavePath)
        btn_browseSavePath = QPushButton('Browse...', self)
        btn_browseSavePath.clicked.connect(self.selectSavePath)
        btn_browseSavePath.setCursor(Qt.CursorShape.PointingHandCursor)
        savePathHlayout.addWidget(savePathLabel)
        savePathHlayout.addWidget(self.pathField)
        savePathHlayout.addWidget(btn_browseSavePath)

        self.textureCardAlb = TextureCard('Albedo', 150, 150, False, False, False, False, self)
        self.textureCardMet = TextureCardGrayscale('Metal', 150, 150, True, self)
        self.textureCardRough = TextureCardGrayscale('Roughness', 150, 150, True, self)

        self.fileMenu.addSeparator()
        self.fileMenu.addAction("Quit", lambda: QCoreApplication.quit())

        mainVLayout.addLayout(self.textureCardAlb)
        mainVLayout.addLayout(self.textureCardMet)
        mainVLayout.addLayout(self.textureCardRough)
        mainVLayout.addStretch(1)
        mainVLayout.addLayout(savePathHlayout)
        buttonRun = QPushButton('Run', self)
        buttonRun.setCursor(Qt.CursorShape.PointingHandCursor)
        buttonRun.clicked.connect(self.runProcess)
        mainVLayout.addWidget(buttonRun)

        mainWindow.setLayout(mainVLayout)
        self.setCentralWidget(mainWindow)
        self.setGeometry(300, 300, 400, 0)
        self.setWindowTitle('Marmoset texture converter')
        self.show()

        self.settings = SettingsWindow()

    def openAlbDrop(self, dropArea: QLabel):
        Debugger.debugger_print(dropArea.text())
        pass

    def showOpenErrorDialog(self):
        popup = QMessageBox(self)
        popup.setWindowTitle('Error!')
        popup.setIcon(QMessageBox.Critical)
        popup.setFixedSize(600, 200)
        popup.setText("Selected .exe is not Toolbag application! Set proper .exe in Settings")
        popup.setStandardButtons(QMessageBox.Ok)
        popup.exec_()

    @pyqtSlot(name='runprocess')
    def runProcess(self):
        Opener.open_(Settings.marmosetPath, Settings.pyfile, self)

    def selectSavePath(self):
        savePath_ = str(QFileDialog.getExistingDirectory(self, "Select Save Directory"))
        if savePath_:
            self.pathField.setText(savePath_)
            return savePath_
    def updateSavePath(self):
            global savePath
            path = self.pathField.text()
            Debugger.debugger_print(path)

    def openSettings(self):
        self.settings.show()
        self.settings.update()


if __name__ == '__main__':
    qdarktheme.enable_hi_dpi()
    app = QApplication(sys.argv)
    qdarktheme.setup_theme("auto")
    StoredSettings.Init()
    ui = MainUI()
    CheckMissingSettings()
    sys.exit(app.exec())
