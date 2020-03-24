# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow2.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Form(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(750, 630)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("C:/Users/ZakyWisnu/Pictures/arise.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(90, 450, 591, 111))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButtonStart = QtGui.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonStart.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("C:/Users/ZakyWisnu/Pictures/play-button.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonStart.setIcon(icon1)
        self.pushButtonStart.setIconSize(QtCore.QSize(50, 50))
        self.pushButtonStart.setAutoDefault(False)
        self.pushButtonStart.setObjectName(_fromUtf8("pushButtonStart"))
        self.horizontalLayout.addWidget(self.pushButtonStart)
        self.pushButtonStop = QtGui.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonStop.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("C:/Users/ZakyWisnu/Pictures/Stop-Button.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonStop.setIcon(icon2)
        self.pushButtonStop.setIconSize(QtCore.QSize(50, 50))
        self.pushButtonStop.setObjectName(_fromUtf8("pushButtonStop"))
        self.horizontalLayout.addWidget(self.pushButtonStop)
        self.logoUGM = QtGui.QLabel(self.centralwidget)
        self.logoUGM.setGeometry(QtCore.QRect(90, 0, 101, 91))
        self.logoUGM.setText(_fromUtf8(""))
        self.logoUGM.setPixmap(QtGui.QPixmap(_fromUtf8("C:/Users/ZakyWisnu/Pictures/UGM.png")))
        self.logoUGM.setScaledContents(True)
        self.logoUGM.setObjectName(_fromUtf8("logoUGM"))
        self.logoTeti = QtGui.QLabel(self.centralwidget)
        self.logoTeti.setGeometry(QtCore.QRect(600, 10, 91, 81))
        self.logoTeti.setText(_fromUtf8(""))
        self.logoTeti.setPixmap(QtGui.QPixmap(_fromUtf8("C:/Users/ZakyWisnu/Pictures/kmteti.png")))
        self.logoTeti.setScaledContents(True)
        self.logoTeti.setObjectName(_fromUtf8("logoTeti"))
        self.labelTitle = QtGui.QLabel(self.centralwidget)
        self.labelTitle.setGeometry(QtCore.QRect(260, 20, 261, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.labelTitle.setFont(font)
        self.labelTitle.setFrameShape(QtGui.QFrame.NoFrame)
        self.labelTitle.setFrameShadow(QtGui.QFrame.Raised)
        self.labelTitle.setTextFormat(QtCore.Qt.PlainText)
        self.labelTitle.setScaledContents(False)
        self.labelTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.labelTitle.setWordWrap(False)
        self.labelTitle.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.labelTitle.setObjectName(_fromUtf8("labelTitle"))
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(320, 360, 161, 24))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(260, 400, 291, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(250, 140, 311, 151))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAutoFillBackground(False)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setWordWrap(False)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 750, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.pushButtonStart, QtCore.SIGNAL(_fromUtf8("clicked()")), self.progressBar.reset)
        QtCore.QObject.connect(self.pushButtonStop, QtCore.SIGNAL(_fromUtf8("clicked()")), self.progressBar.raise_)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButtonStart.setText(_translate("MainWindow", "START", None))
        self.pushButtonStop.setText(_translate("MainWindow", "STOP", None))
        self.labelTitle.setText(_translate("MainWindow", "ARISE", None))
        self.label.setText(_translate("MainWindow", "Press Start", None))
        self.label_2.setText(_translate("MainWindow", "Number", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Form()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

