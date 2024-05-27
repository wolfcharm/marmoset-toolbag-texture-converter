import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap, QRegion, QPainter, QBitmap, QImage
from PyQt5.QtCore import pyqtSlot, Qt, QRect

import qdarktheme
import Opener

path = "C:/Program Files/Marmoset/Toolbag 4/toolbag.exe"
pyfile = "C:/Users/ichen/Documents/Python Projects/textureConvert/main.py"
allowedImageFormats = ['.jpg', '.png', '.tga', '.psd', '.psb', '.exr', '.hdr', '.mpic', '.bmp', '.dds', '.tig', '.pfm']


class ImageChannels(QLayout):
    def __init__(self, enableR, enableG, enableB, enableA, parent):
        super().__init__(parent)

        self.label = QLabel(parent)

        self.selectionR = QComboBox(parent)
        self.selectionR.setFixedSize(20, 10)

        self.addWidget(self.label)
        self.addWidget(self.selectionR)

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


class MainUI(QMainWindow):

    def __init__(self):
        super(MainUI, self).__init__()

        mainWindow = QWidget(self)
        mainVLayout = QVBoxLayout(self)

        self.setGeometry(300, 300, 500, 200)


        textureCardHLayout = QHBoxLayout(self)
        dropAreaAlbedo = DropArea('Albedo', 100, 100, self)
        textureCardHLayout.addWidget(dropAreaAlbedo)
        textureChannelsVLayout = QVBoxLayout(self)
        channelHLayoutR = QHBoxLayout(self)
        R = QLabel('R', self)
        channelHLayoutR.addWidget(R)
        RComboBox = QComboBox(self)
        channelHLayoutR.addWidget(RComboBox)
        textureChannelsVLayout.addLayout(channelHLayoutR)
        textureCardHLayout.addLayout(textureChannelsVLayout)

        mainVLayout.addLayout(textureCardHLayout)
        spacerItem = QSpacerItem(378, 13, QSizePolicy.Minimum, QSizePolicy.Expanding)
        buttonRun = QPushButton('Run', self)
        mainVLayout.addWidget(buttonRun)
        mainVLayout.addItem(spacerItem)

        mainWindow.setLayout(mainVLayout)
        self.setCentralWidget(mainWindow)



        #
        # btn_browseExe = QPushButton('Browse...', self)
        # btn_browseExe.resize(btn_browseExe.sizeHint())
        # btn_browseExe.clicked.connect(self.openFileDialog)
        #
        # global pathField
        # pathField = QLineEdit(self)
        # # pathField.resize(250, 20)
        # pathField.setText(path)
        # pathField.textChanged.connect(self.updatePath)
        #
        # btn_Run = QPushButton('Run', self)
        # btn_Run.resize(btn_browseExe.sizeHint())
        # btn_Run.clicked.connect(self.runProcess)
        #
        # drop1 = DropArea('Albedo', 100, 100, self)
        # drop2 = DropArea('Metal', 100, 100, self)
        # drop3 = DropArea('Gloss', 100, 100, self)
        # channelsSelector1 = ImageChannels(True, True, True,True, self)
        # channelsSelector2 = ImageChannels(True, True, True,True, self)
        # channelsSelector3 = ImageChannels(True, True, True,True, self)
        #
        # vertTexturePanel1 = QVBoxLayout(self.parent())
        # vertTexturePanel1.addWidget(drop1)
        # vertTexturePanel1.addWidget(channelsSelector1)
        #
        # vertTexturePanel2 = QVBoxLayout(self.parent())
        # vertTexturePanel2.addWidget(drop2)
        # vertTexturePanel2.addWidget(channelsSelector2)
        #
        # vertTexturePanel3 = QVBoxLayout(self.parent())
        # vertTexturePanel3.addWidget(drop3)
        # vertTexturePanel3.addWidget(channelsSelector3)
        #
        # texturesBox_layout = QHBoxLayout(self.parent())
        # texturesBox_layout.addLayout(vertTexturePanel1)
        # texturesBox_layout.addLayout(vertTexturePanel2)
        # texturesBox_layout.addLayout(vertTexturePanel3)
        # texturesBox_layout.addWidget(drop2)
        # texturesBox_layout.addWidget(drop3)
        #
        # selectExeHBox = QHBoxLayout()
        # selectExeHBox.setParent(mainLayout)
        # selectExeHBox.addWidget(pathField)
        # selectExeHBox.addWidget(btn_browseExe)
        #
        # vbox = QVBoxLayout()
        # vbox.addLayout(selectExeHBox)
        # vbox.addLayout(texturesBox_layout)
        # vbox.addStretch(1)
        # vbox.addWidget(btn_Run)
        #
        # mainLayout.addLayout(selectExeHBox)
        # mainLayout.addStretch()
        #
        # widget = QWidget()
        # widget.setLayout(selectExeHBox)
        # self.setCentralWidget(widget)

        #self.setGeometry(300, 300, 500, 200)
        self.setWindowTitle('Tooltips')
        self.show()

    # @pyqtSlot(name='selectExe')
    # def openFileDialog(self):
    #     pathField.setText(self.selectExe())
    #     self.updatePath()
    #
    # @pyqtSlot(name='runprocess')
    # def runProcess(self):
    #     Opener.open_(path, pyfile)
    #     print(path)
    #
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


if __name__ == '__main__':
    qdarktheme.enable_hi_dpi()
    app = QApplication(sys.argv)
    qdarktheme.setup_theme("auto")
    ui = MainUI()
    sys.exit(app.exec_())
