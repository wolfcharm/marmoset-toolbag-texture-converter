import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap, QRegion, QPainter, QBitmap, QImage
from PyQt5.QtCore import pyqtSlot, Qt, QRect

import qdarktheme
import Opener

path = "C:/Program Files/Marmoset/Toolbag 4/toolbag.exe"
pyfile = "main.py"
allowedImageFormats = ['.jpg', '.png', '.tga', '.psd', '.psb', '.exr', '.hdr', '.mpic', '.bmp', '.dds', '.tig', '.pfm']
savePath = ''
class ImageChannel(QHBoxLayout):
    def __init__(self, labelName: str, selectionItems: list, parent):
        super().__init__(parent)

        self.label = QLabel(labelName, parent)
        self.selection = QComboBox(parent)

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
        widget = QWidget(parent)
        selectionItems = ['R', 'G', 'B', 'A', '1', '0', '1-R', '1-G', '1-B', '1-A']
        if enableGrayscale:
            Gr = ImageChannel('Grayscale', selectionItems, parent)
            self.addLayout(Gr)
            self.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Policy.Expanding))

class DropArea(QLabel):
    def __init__(self, title: str, sizex: int, sizey: int, parent):
        super().__init__(parent)

        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignCenter)
        self._defaultText = title
        self.filePath = ''
        self.setText(self._defaultText)
        self.sizex = sizex
        self.sizey = sizey
        self.setFixedSize(sizex, sizey)
        self.setStyleSheet('border: 2px dashed #aaa')
        self.mask = QBitmap('mask.png')


    def setPixmap(self, image):
        super().setPixmap(image.scaled(self.sizex,self.sizey,Qt.KeepAspectRatio, 1))
        super().setStyleSheet('')
        super().setMask(self.mask)
        super().setStyleSheet('box-shadow: 3px')
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)
        shadow.setOffset(2)
        shadow.setColor(Qt.black)
        super().setGraphicsEffect(shadow)

    def clearPixmap(self):
        super().setText(self._defaultText)
        super().setStyleSheet('border: 2px dashed #aaa')
        super().clearMask()
        super().setGraphicsEffect(None)

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
        if e.button() == Qt.RightButton:
            self.clearPixmap()

class TextureCard(QHBoxLayout):
    def __init__(self, title: str, previewsizex: int, previewsizey: int, displaychannelR: bool, displaychannelG: bool, displaychannelB: bool, displaychannelA: bool, parent):
        super().__init__(parent)

        self.textureCardHLayout = QHBoxLayout(parent)
        self.dropAreaAlbedo = DropArea(title, previewsizex, previewsizey, parent)
        self.textureCardHLayout.addWidget(self.dropAreaAlbedo)
        self.textureChannelsVLayout = ImageChannels(displaychannelR, displaychannelG, displaychannelB, displaychannelA, parent)

        self.textureCardHLayout.addLayout(self.textureChannelsVLayout)
        self.addLayout(self.textureCardHLayout)
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

class MainUI(QMainWindow):

    def __init__(self):
        super(MainUI, self).__init__()

        mainWindow = QWidget(self)
        mainVLayout = QVBoxLayout(self)

        savePathHlayout = QHBoxLayout(self)
        self.pathField = QLineEdit(self)
        self.pathField.resize(350, 20)
        self.pathField.setText(savePath)
        self.pathField.textChanged.connect(self.updateSavePath)
        btn_browseSavePath = QPushButton('Browse...', self)
        btn_browseSavePath.clicked.connect(self.selectSavePath)
        savePathHlayout.addWidget(self.pathField)
        savePathHlayout.addWidget(btn_browseSavePath)


        textureCardAlb = TextureCard('Albedo', 150, 150, False, False, False, False, self)
        textureCardMet = TextureCardGrayscale('Metal', 150, 150, True, self)
        textureCardRough = TextureCardGrayscale('Roughness', 150, 150, True, self)

        mainVLayout.addLayout(textureCardAlb)
        mainVLayout.addLayout(textureCardMet)
        mainVLayout.addLayout(textureCardRough)
        mainVLayout.addLayout(savePathHlayout)
        mainVLayout.addStretch(1)
        buttonRun = QPushButton('Run', self)
        buttonRun.clicked.connect(self.runProcess)
        mainVLayout.addWidget(buttonRun)

        mainWindow.setLayout(mainVLayout)
        self.setCentralWidget(mainWindow)
        self.setGeometry(300, 300, 400, 0)
        self.setWindowTitle('Tooltips')
        self.show()

    # @pyqtSlot(name='selectExe')
    # def openFileDialog(self):
    #     pathField.setText(self.selectExe())
    #     self.updatePath()
    #
    @pyqtSlot(name='runprocess')
    def runProcess(self):
        Opener.open_(path, pyfile)
        print(path)

    # def updatePath(self):
    #     global path
    #     path = pathField.text()
    #     print(path)
    #
    # def selectExe(self):
    #     fileopen = QFileDialog.Options()
    #     fileName, _ = QFileDialog.getOpenFileName(self, "Select marmoset.exe", pathField.text(),
    #                                               "Executable (*.exe)", options=fileopen)
    #     if fileName:
    #         return fileName
    def selectSavePath(self):
        savePath_ = str(QFileDialog.getExistingDirectory(self, "Select Save Directory"))
        if savePath_:
            self.pathField.setText(savePath_)
            return savePath_
    def updateSavePath(self):
            global savePath
            path = self.pathField.text()
            print(path)

if __name__ == '__main__':
    qdarktheme.enable_hi_dpi()
    app = QApplication(sys.argv)
    qdarktheme.setup_theme("auto")
    ui = MainUI()
    sys.exit(app.exec_())
