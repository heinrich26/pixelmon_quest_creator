import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from stage import Ui_stageBox as stageBox


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(100,100,400, 200)
        self.setWindowTitle("This is PyQt Widget example")

        self.widget = QWidget(self)
        self.stage_frame = QWidget(self)

        self.label = QLabel("tada")
        self.label.setText("tada")

        self.stage = stageBox()
        self.stage.setupUi(self.stage_frame)

        self.button = QPushButton('press')
        self.button.setText("hi there")
        self.button.clicked.connect(self.clicked)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.label)

        self.widget.setGeometry(0,0,400,200)
        self.widget.setLayout(self.layout)

    def clicked(self):
        self.label2 = QLabel("hi")
        self.layout.addWidget(self.label2)

app = QApplication(sys.argv)
win = Window()
win.show()
sys.exit(app.exec_())
