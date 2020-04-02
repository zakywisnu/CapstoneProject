# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow3.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(854, 700)
        font = QtGui.QFont()
        font.setKerning(True)
        MainWindow.setFont(font)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet(_fromUtf8("background-color: rgb(216, 216, 216)"))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setStyleSheet(_fromUtf8(""))
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalWidget = QtGui.QWidget(self.centralwidget)
        self.horizontalWidget.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalWidget.sizePolicy().hasHeightForWidth())
        self.horizontalWidget.setSizePolicy(sizePolicy)
        self.horizontalWidget.setMinimumSize(QtCore.QSize(50, 0))
        self.horizontalWidget.setBaseSize(QtCore.QSize(16000, 16000))
        self.horizontalWidget.setAcceptDrops(False)
        self.horizontalWidget.setAutoFillBackground(False)
        self.horizontalWidget.setStyleSheet(_fromUtf8("background-color: silver;"))
        self.horizontalWidget.setObjectName(_fromUtf8("horizontalWidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.horizontalWidget)
        self.gridLayout_2.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.pushButtonNew = QtGui.QPushButton(self.horizontalWidget)
        self.pushButtonNew.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("C:/Users/ZakyWisnu/Pictures/SKRIPSI/new_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonNew.setIcon(icon)
        self.pushButtonNew.setObjectName(_fromUtf8("pushButtonNew"))
        self.gridLayout_2.addWidget(self.pushButtonNew, 1, 0, 1, 1)
        self.pushButtonStop = QtGui.QPushButton(self.horizontalWidget)
        self.pushButtonStop.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("C:/Users/ZakyWisnu/Pictures/Stop-Button.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonStop.setIcon(icon1)
        self.pushButtonStop.setObjectName(_fromUtf8("pushButtonStop"))
        self.gridLayout_2.addWidget(self.pushButtonStop, 1, 4, 1, 2)
        self.pushButtonSave = QtGui.QPushButton(self.horizontalWidget)
        self.pushButtonSave.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("C:/Users/ZakyWisnu/Pictures/SKRIPSI/save_icon_3.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonSave.setIcon(icon2)
        self.pushButtonSave.setObjectName(_fromUtf8("pushButtonSave"))
        self.gridLayout_2.addWidget(self.pushButtonSave, 1, 2, 1, 1)
        self.pushButtonOpen = QtGui.QPushButton(self.horizontalWidget)
        self.pushButtonOpen.setMinimumSize(QtCore.QSize(0, 0))
        self.pushButtonOpen.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8("C:/Users/ZakyWisnu/Pictures/SKRIPSI/open_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonOpen.setIcon(icon3)
        self.pushButtonOpen.setObjectName(_fromUtf8("pushButtonOpen"))
        self.gridLayout_2.addWidget(self.pushButtonOpen, 1, 1, 1, 1)
        self.pushButtonPlay = QtGui.QPushButton(self.horizontalWidget)
        self.pushButtonPlay.setText(_fromUtf8(""))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8("C:/Users/ZakyWisnu/Pictures/play-button.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonPlay.setIcon(icon4)
        self.pushButtonPlay.setObjectName(_fromUtf8("pushButtonPlay"))
        self.gridLayout_2.addWidget(self.pushButtonPlay, 1, 3, 1, 1)
        self.progressBar = QtGui.QProgressBar(self.horizontalWidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setFormat(_fromUtf8(""))
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout_2.addWidget(self.progressBar, 1, 6, 1, 1)
        self.gridLayout.addWidget(self.horizontalWidget, 0, 0, 1, 1)
        self.textEdit = QtGui.QTextEdit(self.centralwidget)
        self.textEdit.setAutoFillBackground(True)
        self.textEdit.setStyleSheet(_fromUtf8("background-color: white;"))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.gridLayout.addWidget(self.textEdit, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 854, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionNew = QtGui.QAction(MainWindow)
        self.actionNew.setShortcutContext(QtCore.Qt.WindowShortcut)
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setShortcutContext(QtCore.Qt.WindowShortcut)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.pushButtonPlay, QtCore.SIGNAL(_fromUtf8("clicked()")), self.progressBar.reset)
        QtCore.QObject.connect(self.pushButtonStop, QtCore.SIGNAL(_fromUtf8("clicked()")), self.progressBar.raise_)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "ARISE", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Help", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+X", None))
        self.actionNew.setText(_translate("MainWindow", "New", None))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N", None))
        self.actionSave.setText(_translate("MainWindow", "Save", None))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S", None))
        self.actionOpen.setText(_translate("MainWindow", "Open", None))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O", None))
        self.actionAbout.setText(_translate("MainWindow", "About", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

