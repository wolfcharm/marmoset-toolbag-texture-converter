import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap, QImage
from PyQt5.QtCore import pyqtSlot, Qt

import qdarktheme
import Opener

path = "C:/Program Files/Marmoset/Toolbag 4/toolbag.exe"
pyfile = "C:/Users/ichen/Documents/Python Projects/textureConvert/main.py"
allowedImageFormats = ['.jpg', '.png', '.tga', '.psd', '.psb', '.exr', '.hdr', '.mpic', '.bmp', '.dds', '.tig', '.pfm']

class DropArea(QLabel):
    def __init__(self, title , sizex, sizey, parent):
        super().__init__(parent)

        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignCenter)
        self.setText(title)
        self.setFixedSize(sizex, sizey)
        self.setStyleSheet('border: 2px dashed #aaa')

    def dragEnterEvent(self, e):
        mime = e.mimeData().urls()
        print(mime)
        if e.mimeData().hasUrls():
            if len(mime) > 1:
                e.ignore()
                return
            global acc
            acc = True
            for url in mime:
                text = url.toString()
                if '.png' not in text:
                    print(text)
                    acc = False
                    return
            if acc:
                e.accept()

        else:
            e.ignore()

    def dropEvent(self, e):
        self.setText(e.mimeData().text())


class MainUI(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont('Roboto', 10))

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

        drop1 = DropArea('Albedo', 100, 100,self)
        drop2 = DropArea('Metal', 100, 100,self)
        drop3 = DropArea('Gloss', 100, 100,self)

        texturesBox_layout = QHBoxLayout()
        texturesBox_layout.addWidget(drop1)
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
