
from PyQt6.QtGui import QPixmap, QBitmap
from PyQt6.QtCore import Qt

import StaticVariables
from SettingsUI import *


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