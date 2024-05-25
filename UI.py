import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap, QRegion, QPainter, QBitmap, QImage
from PyQt5.QtCore import pyqtSlot, Qt, QRect

import qdarktheme
import Opener

path = "C:/Program Files/Marmoset/Toolbag 4/toolbag.exe"
pyfile = "C:/Users/ichen/Documents/Python Projects/textureConvert/main.py"
allowedImageFormats = ['.jpg', '.png', '.tga', '.psd', '.psb', '.exr', '.hdr', '.mpic', '.bmp', '.dds', '.tig', '.pfm']


class ImageChannels(QWidget):
    def __init__(self, enableR, enableG, enableB, enableA, parent):
        super().__init__(parent)
        self.selectionR = QComboBox(parent)
        self.selectionR.setFixedSize(20, 10)



class DropArea(QLabel):


    def __init__(self, title, sizex, sizey, parent):
        super().__init__(parent)

        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignCenter)
        self._defaultText = title
        self.filePath = ''
        self.setText(self._defaultText)
        self.setFixedSize(sizex, sizey)
        self.setStyleSheet('border: 2px dashed #aaa')
        self.mask = QBitmap('mask.png')


    def setPixmap(self, image):
        super().setPixmap(image)
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


class MainUI(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):


        btn_browseExe = QPushButton('Browse...', self)
        btn_browseExe.resize(btn_browseExe.sizeHint())
        btn_browseExe.clicked.connect(self.openFileDialog)

        global pathField
        pathField = QLineEdit(self)
        pathField.resize(250, 20)
        pathField.setText(path)
        pathField.textChanged.connect(self.updatePath)

        btn_Run = QPushButton('Run', self)
        btn_Run.resize(btn_browseExe.sizeHint())
        btn_Run.clicked.connect(self.runProcess)

        drop1 = DropArea('Albedo', 100, 100, self)
        drop2 = DropArea('Metal', 100, 100, self)
        drop3 = DropArea('Gloss', 100, 100, self)
        channelsSelector1 = ImageChannels(1, 1, 1,1, self)
        channelsSelector2 = ImageChannels(1, 1, 1,1, self)
        channelsSelector3 = ImageChannels(1, 1, 1,1, self)

        vertTexturePanel1 = QVBoxLayout(self.parent())
        vertTexturePanel1.addWidget(drop1)
        vertTexturePanel1.addWidget(channelsSelector1)

        texturesBox_layout = QHBoxLayout(self.parent())
        texturesBox_layout.addLayout(vertTexturePanel1)
        texturesBox_layout.addWidget(drop2)
        texturesBox_layout.addWidget(drop3)

        selectExeHBox = QHBoxLayout()
        selectExeHBox.addWidget(pathField)
        selectExeHBox.addWidget(btn_browseExe)

        vbox = QVBoxLayout()
        vbox.addLayout(selectExeHBox)
        vbox.addLayout(texturesBox_layout)
        vbox.addStretch(1)
        vbox.addWidget(btn_Run)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 500, 200)
        self.setWindowTitle('Tooltips')
        self.show()

    @pyqtSlot(name='selectExe')
    def openFileDialog(self):
        pathField.setText(self.selectExe())
        self.updatePath()

    @pyqtSlot(name='runprocess')
    def runProcess(self):
        Opener.open_(path, pyfile)
        print(path)

    def updatePath(self):
        global path
        path = pathField.text()
        print(path)

    def selectExe(self):
        fileopen = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Select marmoset.exe", pathField.text(),
                                                  "Executable (*.exe)", options=fileopen)
        if fileName:
            return fileName


if __name__ == '__main__':
    qdarktheme.enable_hi_dpi()
    app = QApplication(sys.argv)
    qdarktheme.setup_theme("auto")
    ui = MainUI()
    sys.exit(app.exec_())
