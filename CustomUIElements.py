from PyQt6.QtGui import QPixmap, QBitmap, QFont, QPainter, QImage, QColor, QOpenGLContext, QAction, QCursor
from PyQt6.QtCore import Qt, QObject, QPoint, pyqtSignal, QRectF
from os.path import exists

import StaticVariables
from SettingsUI import *

class SavableSettingLayout(QHBoxLayout):
    valueChanged = pyqtSignal()
    def __init__(self, parent, settingName: str = ''):
        super().__init__(parent)
        self.settingName = settingName

class ComboBoxSetting(SavableSettingLayout):
    def __init__(self, parent, labelText: str, comboOptions: list, defaultOption: str = '', settingName: str = '', labelMinWidth: int = 150):
        super().__init__(parent, settingName)

        label = QLabel(labelText, parent)
        label.setMinimumSize(labelMinWidth, 8)
        self.dropdown = QComboBox(parent)
        self.dropdown.addItems(comboOptions)
        self.dropdown.setCursor(Qt.CursorShape.PointingHandCursor)
        if defaultOption != '':
            self.dropdown.setCurrentText(defaultOption)
        self.dropdown.currentIndexChanged.connect(self.emitChanged)
        self.addWidget(label)
        self.addWidget(self.dropdown)
        self.addStretch()

    def emitChanged(self):
        self.valueChanged.emit()
        print(self.settingName, 'changed')

    def get_selected_option_int(self) -> int:
        return self.dropdown.currentIndex()

    def get_selected_option_str(self) -> str:
        return self.dropdown.currentText()

    def get_savable_option(self):
        return str(self.get_selected_option_int())

class CheckBoxSetting(SavableSettingLayout):
    def __init__(self, parent, labelText: str, defaultOption: bool = False, settingName: str = '', labelMinWidth: int = 150):
        super().__init__(parent, settingName)

        label = QLabel(labelText, parent)
        label.setMinimumSize(labelMinWidth, 8)
        self.checkbox = QCheckBox(parent)
        self.checkbox.setCursor(Qt.CursorShape.PointingHandCursor)
        self.checkbox.setChecked(defaultOption)
        self.checkbox.checkStateChanged.connect(self.emitChanged)
        self.addWidget(label)
        self.addWidget(self.checkbox)
        self.addStretch()

    def emitChanged(self):
        self.valueChanged.emit()
        print(self.settingName, 'changed')

    def get_selected_option(self) -> bool:
        return self.checkbox.isChecked()

    def set_option(self, value: str):
        if value == '1':
            self.checkbox.setCheckState(Qt.CheckState.Checked)
        if value == '0':
            self.checkbox.setCheckState(Qt.CheckState.Unchecked)

    def get_savable_option(self):
        if self.get_selected_option():
            return '1'
        else:
            return '0'

class LinePathSetting(SavableSettingLayout):
    def __init__(self, parent, labelText: str, defaultOption: str = '', settingName: str = '', labelMinWidth: int = 150):
        super().__init__(parent, settingName)

        label = QLabel(labelText, parent)
        label.setMinimumSize(labelMinWidth, 8)
        self.fieldPath = QLineEdit(parent)
        self.fieldPath.setEnabled(False)
        self.fieldPath.setText(defaultOption)
        btnSelectMarmosetFile = QPushButton('Browse...', parent)
        btnSelectMarmosetFile.setCursor(Qt.CursorShape.PointingHandCursor)
        btnSelectMarmosetFile.clicked.connect(self.openFileDialog)
        self.fieldPath.textChanged.connect(self.emitChanged)
        self.addWidget(label)
        self.addWidget(self.fieldPath)
        self.addWidget(btnSelectMarmosetFile)

    def emitChanged(self):
        self.valueChanged.emit()
        print(self.settingName, 'changed')

    def get_selected_option(self) -> str:
        return self.fieldPath.text()

    def set_option(self, value):
        self.fieldPath.setText(str(value))

    def get_savable_option(self):
        return self.get_selected_option()

    @pyqtSlot(name='selectExe')
    def openFileDialog(self):
        Debugger.debugger_print('pressed')
        fileName = self.selectExe()
        if not fileName:
            return
        else:
            self.set_option(fileName)

    def selectExe(self):
        dialog = QFileDialog()

        fileName, _ = QFileDialog.getOpenFileName(dialog, caption="Select toolbag.exe",
                                                  directory=self.get_selected_option(),
                                                  filter="Toolbag Application (toolbag.exe)")
        if fileName:
            return fileName

class ImageChannel(QHBoxLayout):
    currentIndexChanged = pyqtSignal(int)
    def __init__(self, labelName: str, selectionItems: list, parent):
        super().__init__(parent)

        self.label = QLabel(labelName, parent)
        self.label.setMinimumSize(65,8)
        self.selection = QComboBox(parent)
        self.selection.setCursor(Qt.CursorShape.PointingHandCursor)
        self.selection.currentIndexChanged.connect(self.indexChanged)

        self.selection.addItems(selectionItems)

        self.addWidget(self.label)
        self.addWidget(self.selection)

    def indexChanged(self):
        self.currentIndexChanged.emit(self.selection.currentIndex())

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

        self.addStretch()

class ImageChannelsGrayscale(QVBoxLayout):
    def __init__(self, enableGrayscale: bool, parent):
        super().__init__(parent)

        selectionItems = ['R', 'G', 'B', 'A', '1', '0', '1-R', '1-G', '1-B', '1-A']
        if enableGrayscale:
            self.channel = ImageChannel('Grayscale', selectionItems, parent)
            self.addLayout(self.channel)
            self.addStretch()
            self.currentIndexChanged = self.channel.currentIndexChanged

class DropArea(QLabel):
    def __init__(self, parent: QWidget, title: str, sizex: int, sizey: int, displayChannel: int = -1):
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
        self.displayChannel = displayChannel

        parent.fileMenu.addAction("Set {0} Texture...".format(title), self.selectTexture)

    # def channelChanged(self, index):
    #     self.displayChannel = index
    #     self.paintChannelPix()
    #     self.update()
    #
    # def paintEvent(self, a0):
    #     p = QPainter(self)
    #     p.drawText(60, 80, self._defaultText)
    #     if self.fileAssigned:
    #         rect = self.pix.rect()
    #         if self.displayChannel == 0:  # R
    #             p.fillRect(rect, Qt.GlobalColor.red)
    #             p.setCompositionMode(QPainter.CompositionMode.CompositionMode_Multiply)
    #             p.drawPixmap(QPoint(0, 0), self.pix)
    #         if self.displayChannel == 1:  # G
    #             p.fillRect(rect, Qt.GlobalColor.green)
    #             p.setCompositionMode(QPainter.CompositionMode.CompositionMode_Multiply)
    #             p.drawPixmap(QPoint(0, 0), self.pix)
    #         if self.displayChannel == 2:  # B
    #             p.fillRect(rect, Qt.GlobalColor.blue)
    #             p.setCompositionMode(QPainter.CompositionMode.CompositionMode_Multiply)
    #             p.drawPixmap(QPoint(0, 0), self.pix)
    #         if self.displayChannel == 3:  # A
    #             p.fillRect(rect, QColor(0,0,0,255))
    #             p.setCompositionMode(QPainter.CompositionMode.CompositionMode_Multiply)
    #             p.drawPixmap(QPoint(0, 0), self.pix)
    #         if self.displayChannel == 4:  # White
    #             pix = QPixmap(1, 1)
    #             pix.fill(Qt.GlobalColor.white)
    #             p.setCompositionMode(QPainter.CompositionMode.CompositionMode_Overlay)
    #             p.drawPixmap(rect, pix)
    #         if self.displayChannel == 5:  # Black
    #             pix = QPixmap(1, 1)
    #             pix.fill(Qt.GlobalColor.black)
    #             p.setCompositionMode(QPainter.CompositionMode.CompositionMode_Multiply)
    #             p.drawPixmap(rect, pix)
    #         if self.displayChannel == 6:
    #             p.fillRect(rect, Qt.GlobalColor.red)
    #             p.setCompositionMode(QPainter.CompositionMode.CompositionMode_Multiply)
    #             p.drawPixmap(QPoint(0, 0), self.pix)
    #             p.fillRect(rect, Qt.GlobalColor.red)
    #             p.setCompositionMode(QPainter.CompositionMode.RasterOp_NotDestination)
    #             p.drawPixmap(QPoint(0, 0), self.pix)
    #         else:
    #             p.drawPixmap(QPoint(0, 0), self.pix)

    def paintEvent(self, a0):
        p = QPainter(self)
        if self.fileAssigned:
            rect = self.pix.rect()
            p.drawPixmap(QPoint(0, 0), QPixmap(StaticVariables.transparencyTexture))
            p.drawPixmap(rect, self.pix)
        else:
            p.drawText(QRectF(self.rect()), Qt.AlignmentFlag.AlignCenter, self._defaultText)

    def paintChannelPix(self):
        pass

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.selectTexture()

    def assignTexture(self, path: str):
        if (not path) | (not exists(path)):
            return
        self.filePath = path
        self.setPixmap(QPixmap(path))

    def selectTexture(self):
        file = self.openFileSelectDialog()
        if not file:
            return
        self.filePath = file
        self.setPixmap(QPixmap(file))

    def openFileSelectDialog(self):
        filter_ = "Images (*{0})".format(' *'.join(StaticVariables.allowedImageFormats))
        dialog = QFileDialog()
        fileName, _ = QFileDialog.getOpenFileName(dialog, "Select Image", '',
                                                  filter_)
        if fileName:
            return fileName

    def setPixmap(self, image: QPixmap):
        scaled = QPixmap.scaled(image, self.sizex, self.sizey, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.pix = scaled
        super().setPixmap(scaled)
        super().setMask(self.mask)
        super().setStyleSheet('')
        # shadow = QGraphicsDropShadowEffect(self)
        # shadow.setBlurRadius(10)
        # shadow.setOffset(2)
        # shadow.setColor(Qt.GlobalColor.black)
        # super().setGraphicsEffect(shadow)

        if self.displayChannel != -1:
            col = QGraphicsColorizeEffect(self)
            col.setColor(Qt.GlobalColor.black)
            super().setGraphicsEffect(col)

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

    def contextMenuEvent(self, e):
        self.menu = QMenu(self)
        clearAction = QAction('Clear', self)
        clearAction.triggered.connect(lambda: self.clearPixmap())
        assignAction = QAction('Assign texture...', self)
        assignAction.triggered.connect(lambda: self.selectTexture())
        assignWhite = QAction('Assign "white"', self)
        assignWhite.triggered.connect(lambda: self.assignTexture(StaticVariables.textureWhite))
        assignBlack = QAction('Assign "black"', self)
        assignBlack.triggered.connect(lambda: self.assignTexture(StaticVariables.textureBlack))


        self.menu.addAction(assignAction)
        self.menu.addAction(assignWhite)
        self.menu.addAction(assignBlack)
        if self.fileAssigned:
            self.menu.addAction(clearAction)
        # add other required actions
        self.menu.popup(QCursor.pos())
        #self.clearPixmap()

    # def mouseReleaseEvent(self, e):
    #     if e.button() == Qt.MouseButton.RightButton:
    #         self.clearPixmap()

class TextureCard(QHBoxLayout):
    def __init__(self, title: str, previewsizex: int, previewsizey: int, displaychannelR: bool, displaychannelG: bool, displaychannelB: bool, displaychannelA: bool, parent):
        super().__init__(parent)

        self.dropArea = DropArea(parent, title, previewsizex, previewsizey)
        self.addWidget(self.dropArea)

        infoArea = QVBoxLayout(parent)
        self.textureChannelsVLayout = ImageChannels(displaychannelR, displaychannelG, displaychannelB, displaychannelA, parent)

        headerFont = QFont('Futura', 11)
        label = QLabel(title, parent)
        label.setFont(headerFont)
        label.setAlignment(Qt.AlignmentFlag.AlignTop)

        infoArea.addWidget(label)
        infoArea.addLayout(self.textureChannelsVLayout)

        self.addLayout(infoArea)
        self.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Policy.Expanding))

class TextureCardGrayscale(QHBoxLayout):

    def __init__(self, title: str, previewsizex: int, previewsizey: int, displayGrayscale: bool, parent):
        super().__init__(parent)

        headerFont = QFont('Futura', 11)

        label = QLabel(title, parent)
        label.setFont(headerFont)
        label.setAlignment(Qt.AlignmentFlag.AlignTop)

        infoArea = QVBoxLayout(parent)
        self.textureChannelsVLayout = ImageChannelsGrayscale(displayGrayscale, parent)
        infoArea.addWidget(label)
        infoArea.addLayout(self.textureChannelsVLayout)

        self.dropArea = DropArea(parent, title, previewsizex, previewsizey, self.get_active_channel())
        self.addWidget(self.dropArea)

        self.addLayout(infoArea)
        self.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Policy.Expanding))

        self.textureChannelsVLayout.currentIndexChanged.connect(self.updateChannelSelection)

    def get_active_channel(self):
        return self.textureChannelsVLayout.channel.selection.currentIndex()

    def updateChannelSelection(self, index: int):
        pass
        # self.dropArea.channelChanged(index)
