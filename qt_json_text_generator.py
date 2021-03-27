from PyQt5 import QtCore, QtGui, QtWidgets
from qt_thread_updater import get_updater
import random
import time
import threading
import sys

formatting_codes = {
    "§0": "black",
    "§1": "dark_blue",
    "§2": "dark_green",
    "§3": "dark_aqua",
    "§4": "dark_red",
    "§5": "dark_purple",
    "§6": "gold",
    "§7": "gray",
    "§8": "dark_gray",
    "§9": "blue",
    "§a": "green",
    "§b": "aqua",
    "§c": "red",
    "§d": "light_purple",
    "§e": "yellow",
    "§f": "white",
    "§k": "obfuscated",
    "§l": "bold",
    "§m": "strikethrough",
    "§n": "underline",
    "§o": "italic"
}

formatting_keys = [
    "§0",
    "§1",
    "§2",
    "§3",
    "§4",
    "§5",
    "§6",
    "§7",
    "§8",
    "§9",
    "§a",
    "§b",
    "§c",
    "§d",
    "§e",
    "§f",
    "§k",
    "§l",
    "§m",
    "§n",
    "§o"
]

formatting_names = [ "black","dark_blue","dark_green","dark_aqua","dark_red","dark_purple","gold","gray","dark_gray","blue","green","aqua","red","light_purple","yellow","white","obfuscated","bold","strikethrough","underline","italic","reset", "New Line" ]

formats = {
    "red": "color: #FF5555;",
    "blue": "color: #5555FF;",
    "green": "color: #55FF55;",
    "dark_blue": "color: #0000AA;",
    "dark_aqua": "color: #00AAAA;",
    "white": "color: #ffffff;",
    "black": "color: #000000;",
    "dark_gray": "color: #555555;",
    "gray": "color: #AAAAAA;",
    "dark_purple": "color: #AA00AA;",
    "light_purple": "color: #FF55FF;",
    "dark_red": "color: #AA0000;",
    "yellow": "color: #FFFF55;",
    "gold": "color: #FFAA00;",
    "aqua": "color: #55FFFF;",
    "dark_green": "color: #00AA00;",
    "strikethrough": "text-decoration: line-through;",
    "underline": "text-decoration: underline;",
    "bold": "font-weight: 700;",
    "italic": "font-style: italic;",
    "obfuscated": ""
}

def rm_unused(tuple):
    new_tuple = tuple.copy()
    for key in new_tuple:
        if len(new_tuple[key]) >= 2:
            for format in new_tuple[key]:
                if format in formatting_names[0:16]:
                    for name in formatting_names[0:16]:
                        if str(name) != str(format) and name in new_tuple[key]:
                            new_tuple[key].remove(name)
                    break
            for format in new_tuple[key]:
                for i in range(1,new_tuple[key].count(format)):
                    new_tuple[key].remove(format)
    return new_tuple

alphabet = [
"i,;.:!|î", # 1px
"l'`Ììí·´", # 2px
"It[]ÍÎÏïªº•°", #3px
"""kf(){}*¤²”\"""", # 4px
"""ABCDEFGHJKLMNOPQRSTUVWXYZabcdeghjmnopqrsuvwxyz/?$%&+-#_¯=^¨£ÀÁÂÃÄÅÇÈÉÊËÑÒÓÔÕÖÙÚÛÜÝàáâãäåçèéêëñðòóôõöùúûüýÿ0123456789Ææß×¼½¿¬«»""", # 5px
"~@®÷±"]

class animate_obfuscated_text(object):
    def __init__(self, text, starts, ends):
        self.text = text
        self.starts = starts
        self.ends = ends

    def animate_text(self):
        return self.text[0:self.starts[0]] + "".join([self.randtext(i) + self.text[self.ends[i]:self.starts[i+1]] if len(self.starts)-1 != i else self.randtext(i) + self.text[self.ends[i]:] for i in range(0, len(self.starts))])

    def next(self):
        return """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd"><html><head><meta name="qrichtext" content="1" /><style type="text/css">p, li { white-space: pre-wrap; }</style></head><body style=" font-family:'minecraft_font'; font-size:15pt; font-weight:400; font-style:normal; color:#fff; background-image:url(src/background.jpg); background-color:#AEAEAE;"><p style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">""" + self.animate_text() + "</p></body></html>"

    def randtext(self, i):
        return "".join([self.randchar(char) for char in self.text[self.starts[i]:self.ends[i]]])

    def randchar(self, i):
        global alphabet
        if i == " ":
            return " "
        elif i in alphabet[0]:
            return alphabet[0][random.randrange(0,7,1)]
        elif i in alphabet[1]:
            return alphabet[1][random.randrange(0,7,1)]
        elif i in alphabet[2]:
            return alphabet[2][random.randrange(0,11,1)]
        elif i in alphabet[3]:
            return alphabet[3][random.randrange(0,10,1)]
        elif i in alphabet[4]:
            return alphabet[4][random.randrange(0, len(alphabet[4])-1,1)]
        elif i in alphabet[5]:
            return alphabet[5][random.randrange(0,4,1)]
        else:
            return i


class Qt_JSONTextGenerator(QtWidgets.QWidget):
    def __init__(self, string_name):
        self.string_name = string_name
        self.string = ""
        self.app = QtWidgets.QApplication(sys.argv)
        super().__init__()
        self.setupUi()
        self.edit_string()

    def __del__(self):
        self.alive.clear()

    def edit_string(self):
        self.show()
        self.app.exec_()
        self.alive.clear()

    def obfuscated_thread(self, is_alive):
        is_alive.set()
        self.obfuscated = True
        while is_alive.is_set():
            time.sleep(0.025)
            get_updater().call_latest(self.previewOutput.setHtml, self.animated_text.next())
        time.sleep(0.05)
        self.inputField.textChanged.emit()

    def obfuscated_finder(self, i, stack, raw_text, html, addition):
        if "obfuscated" in stack[i]:
            self.obfuscated_starts.append(html.find(raw_text[int(i):int(i)+2]) + addition)

    def setupUi(self):
        self.alive = threading.Event()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.setObjectName("self")
        self.setWindowTitle("Configure String: " + self.string_name)
        self.resize(820, 603)
        QtGui.QFontDatabase.addApplicationFont('src/fonts/minecraft_font.ttf')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.gridLayout.setObjectName("gridLayout")
        self.inputField = QtWidgets.QPlainTextEdit(self)
        self.inputField.setObjectName("inputField")
        self.gridLayout.addWidget(self.inputField, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setObjectName("label_2")
        self.setFont(font)
        self.gridLayout.addWidget(self.label_2, 2, 1, 1, 1)
        self.saveButton = QtWidgets.QPushButton(self)
        self.saveButton.setObjectName("saveButton")
        self.gridLayout.addWidget(self.saveButton, 4, 3, 1, 1)
        self.cancelButton = QtWidgets.QPushButton(self)
        self.cancelButton.setObjectName("cancelButton")
        self.gridLayout.addWidget(self.cancelButton, 4, 2, 1, 1)
        self.previewOutput = QtWidgets.QTextBrowser(self)
        self.previewOutput.setOverwriteMode(True)
        self.previewOutput.setObjectName("previewOutput")
        self.gridLayout.addWidget(self.previewOutput, 3, 1, 1, 1)
        self.label = QtWidgets.QLabel(self)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setMinimumSize(QtCore.QSize(145, 0))
        self.tableWidget.setMaximumSize(QtCore.QSize(145, 16777215))
        self.tableWidget.setSizeIncrement(QtCore.QSize(0, 0))
        self.tableWidget.setBaseSize(QtCore.QSize(50, 0))
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setTabKeyNavigation(False)
        self.tableWidget.setProperty("showDropIndicator", False)
        self.tableWidget.setDragDropOverwriteMode(False)
        self.tableWidget.setAlternatingRowColors(False)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tableWidget.setTextElideMode(QtCore.Qt.ElideRight)
        self.tableWidget.setRowCount(23)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setObjectName("tableWidget")
        item = QtWidgets.QTableWidgetItem()
        item.setBackground(QtGui.QColor(0, 0, 0))
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setBackground(QtGui.QColor(0, 0, 170))
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Code")
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Name")
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("§0")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("§1")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("§2")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(2, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("§3")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(3, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("§4")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(170, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        item.setFlags(QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(4, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(170, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(4, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("§5")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(170, 0, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(5, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(170, 0, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(5, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("§6")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(255, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(6, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(255, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(6, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("§7")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(170, 170, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(7, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(170, 170, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(7, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("§8")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(85, 85, 85))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(8, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(85, 85, 85))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(8, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("§9")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(85, 85, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(9, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(85, 85, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(9, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("§a")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(85, 255, 85))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(10, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(85, 255, 85))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(10, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("§b")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(85, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(11, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(85, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(11, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("§c")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(255, 85, 85))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(12, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(255, 85, 85))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(12, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("§d")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(255, 85, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(13, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(255, 85, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(13, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("§e")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 85))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(14, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 85))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(14, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("§f")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(15, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(15, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("§k")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(16, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(16, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("§l")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(17, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(17, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("§m")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(18, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setStrikeOut(True)
        item.setFont(font)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(18, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("§n")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(19, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setUnderline(True)
        item.setFont(font)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(19, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("§o")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(20, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setItalic(True)
        item.setFont(font)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(20, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("§r")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(21, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(21, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("\\n")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(22, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(22, 1, item)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(50)
        self.tableWidget.horizontalHeader().setHighlightSections(False)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(23)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(23)
        self.gridLayout.addWidget(self.tableWidget, 0, 2, 4, 1)
        self.save_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+S"),self)
        self.save_shortcut.activated.connect(self.actionSave)
        self.saveButton.clicked.connect(self.actionSave)
        self.cancelButton.clicked.connect(self.close)
        self.inputField.textChanged.connect(self.UpdateHtml)
        self.inputField.setFont(QtGui.QFont("minecraft_font",15))
        if self.string == "":
            self.inputField.setPlainText("This is a §6formatted§r §lstring!")
        else:
            self.inputField.setPlainText(self.string)
        self.UpdateHtml()

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.label_2.setText(_translate("self", "Preview Output (try to avoid gray):"))
        self.saveButton.setText(_translate("self", "Save"))
        self.cancelButton.setText(_translate("self", "Cancel"))
        self.previewOutput.setDocumentTitle(_translate("self", "Preview Output"))
        self.label.setText(_translate("self", "Enter formatted Text:"))
        self.tableWidget.setSortingEnabled(False)
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 1)
        item.setText(_translate("self", "black"))
        item = self.tableWidget.item(1, 1)
        item.setText(_translate("self", "dark_blue"))
        item = self.tableWidget.item(2, 1)
        item.setText(_translate("self", "dark_green"))
        item = self.tableWidget.item(3, 1)
        item.setText(_translate("self", "dark_aqua"))
        item = self.tableWidget.item(4, 1)
        item.setText(_translate("self", "dark_red"))
        item = self.tableWidget.item(5, 1)
        item.setText(_translate("self", "dark_purple"))
        item = self.tableWidget.item(6, 1)
        item.setText(_translate("self", "gold"))
        item = self.tableWidget.item(7, 1)
        item.setText(_translate("self", "gray"))
        item = self.tableWidget.item(8, 1)
        item.setText(_translate("self", "dark_gray"))
        item = self.tableWidget.item(9, 1)
        item.setText(_translate("self", "blue"))
        item = self.tableWidget.item(10, 1)
        item.setText(_translate("self", "green"))
        item = self.tableWidget.item(11, 1)
        item.setText(_translate("self", "aqua"))
        item = self.tableWidget.item(12, 1)
        item.setText(_translate("self", "red"))
        item = self.tableWidget.item(13, 1)
        item.setText(_translate("self", "light_purple"))
        item = self.tableWidget.item(14, 1)
        item.setText(_translate("self", "yellow"))
        item = self.tableWidget.item(15, 1)
        item.setText(_translate("self", "white"))
        item = self.tableWidget.item(16, 1)
        item.setText(_translate("self", "obfuscated"))
        item = self.tableWidget.item(17, 1)
        item.setText(_translate("self", "bold"))
        item = self.tableWidget.item(18, 1)
        item.setText(_translate("self", "striketrough"))
        item = self.tableWidget.item(19, 1)
        item.setText(_translate("self", "underline"))
        item = self.tableWidget.item(20, 1)
        item.setText(_translate("self", "italic"))
        item = self.tableWidget.item(21, 1)
        item.setText(_translate("self", "reset"))
        item = self.tableWidget.item(22, 1)
        item.setText(_translate("self", "New Line"))

    def actionSave(self):
        self.string = self.inputField.toPlainText().replace("\n", "\\n")
        self.close()

    def closeEvent(self, event):
        if self.sender() == None:
            warning = QtWidgets.QMessageBox.question(self, "Unsaved Changes", "Your Changes to the string haven't been saved! How to proceed?", QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Close | QtWidgets.QMessageBox.Cancel, QtWidgets.QMessageBox.Cancel)
            if warning == QtWidgets.QMessageBox.Save:
                self.string = self.inputField.toPlainText().replace("\n", "\\n")
                event.accept()
            elif warning == QtWidgets.QMessageBox.Cancel:
                event.ignore()
        else:
            event.accept()

    def UpdateHtml(self):
        global formatting_codes
        global formatting_keys
        global formatting_names
        raw_text = self.inputField.toPlainText().replace("\n", "<br>").replace("\\n", "<br>")

        # stacks
        if len(raw_text) >= 3:
            stack = {"0": []}
            for i in range(0, len(raw_text)-1):
                if raw_text[i:i+2] in formatting_keys:
                    stack[str(i)] = list(stack[str(max([int(num) for num in stack.keys()]))])
                    stack[str(i)].insert(0,formatting_names[formatting_keys.index(raw_text[i:i+2])])
                    i += 1
                if raw_text[i:i+2] == "§r":
                    stack[str(i)] = []
                    i += 1

            stack = rm_unused(stack)
            self.obfuscated_starts = []
            self.obfuscated_ends = []
            html = str(raw_text)
            no_close = True
            for i in stack.keys():
                if no_close and stack[i] != []:
                    self.obfuscated_finder(i, stack, raw_text, html, 0)
                    html = html.replace(raw_text[int(i):int(i)+2], "<span style=\"" + "".join([formats[format] for format in stack[i]]) + "\">",1)
                    no_close = False
                elif stack[i] != []:
                    self.obfuscated_finder(i, stack, raw_text, html, 7)
                    if "underline" in stack[i] and "strikethrough" in stack[i]:
                        html = html.replace(raw_text[int(i):int(i)+2], "</span><span style=\"" + "".join([formats[format] for format in stack[i] if format not in ("underline", "strikethrough")]) + "text-decoration:line-through underline;" + "\">",1)
                    else:
                        html = html.replace(raw_text[int(i):int(i)+2], "</span><span style=\"" + "".join([formats[format] for format in stack[i]]) + "\">",1)
                elif not no_close and stack[i] == [] and i != "0":
                    html = html.replace("§r", "</span>", 1)
                    no_close = True
                elif i != "0" or i == "0" and raw_text[0:2] == "§r":
                    html = html.replace("§r", "", 1)
            # remove extra §'s
            html = html.replace("§", "")

            html += "".join(["</span>" for i in range(0,max(0, html.count("<span style=") - html[html.find("<span style="):].count("</span>")))])

            if self.obfuscated_starts != []:
                for i in range(0,len(self.obfuscated_starts)):
                    self.obfuscated_starts[i] = html.find(">", self.obfuscated_starts[i]) + 1
                    self.obfuscated_ends.append(html.find("<", self.obfuscated_starts[i]))
                self.animated_text = animate_obfuscated_text(html, self.obfuscated_starts, self.obfuscated_ends)
                thread = threading.Thread(target=self.obfuscated_thread, args=(self.alive,))
                thread.start()
            elif self.alive.is_set():
                self.alive.clear()
                thread = None
        else:
            if self.alive.is_set():
                self.alive.clear()
                thread = None
            html = raw_text

        if not self.alive.is_set():
            html = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd"><html><head><meta name="qrichtext" content="1" /><title>ColorTests</title><style type="text/css">p, li { white-space: pre-wrap; }</style></head><body style="font-family:'minecraft_font'; font-size:15pt; font-weight:400; font-style:normal; background-image:url(src/background.jpg); color:#fff;"><p style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">""" + html + "</p></body></html>"

            self.previewOutput.setHtml(html)



if __name__ == "__main__":
    generator = Qt_JSONTextGenerator("hello")
