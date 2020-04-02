import sys, time
import traceback

from mainwindow_edit import _fromUtf8
from micstream import Streaming
from PyQt4 import QtGui, uic, QtCore

from PyQt4.QtCore import *
from PyQt4.QtGui import *

qtCreatorFile = "MainWindow3.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Start(QRunnable):
    '''
    Worker thread
    '''

    def __init__(self, fn, *args, **kwargs):
        super(Start, self).__init__()

        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):

        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.stream = Streaming()
        self.actionNew.triggered.connect(self.newFile)
        self.actionOpen.triggered.connect(self.openFile)
        self.actionSave.triggered.connect(self.saveFile)
        self.actionAbout.triggered.connect(self.aboutMenu)

        self.pushButtonPlay.clicked.connect(self.mulai)  # start the process
        self.pushButtonStop.clicked.connect(self.stop)  # stop the process
        self.pushButtonOpen.clicked.connect(self.openFile)
        self.pushButtonNew.clicked.connect(self.newFile)
        self.pushButtonSave.clicked.connect(self.saveFile)
        self.progressBar.setValue(0)  # set progress bar value

        # Set the threads
        self.threadpool = QThreadPool()  # initialize thread
        print("Multi threading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.timer = QTimer()

    def progress_fn(self, n):
        print("%d%% done" % n)

    def thread_complete(self):
        print("THREAD COMPLETE!")
        self.progressBar.setRange(0, 1)  # finish thread

    def check_button(self, button):  # checking the state of the button
        if button.isDown():
            print("STOP IS CLICKED")
            state_buttons = True
        elif not button.isDown():
            state_buttons = False
        return state_buttons

    def transcribe(self):
        state_stop = self.check_button(self.pushButtonStop)
        print("State button stop:", state_stop)

        while (state_stop == False):
            # self.label.setText("Say a number")
            signal = self.stream.record()
            self.progressBar.setRange(0, 0)
            # self.label.setText("Processing...")
            response = self.stream.listening(signal)
            print("Your response: ")
            new_resp = self.convertToText(response)
            self.textEdit.setFontPointSize(18)
            self.textEdit.insertPlainText(new_resp)
            state_stop = self.check_button(self.pushButtonStop)
            print("State button stop:", state_stop)

        print("STOP THE PROCESS")

    def mulai(self):
        start = Start(self.transcribe)

        start.signals.finished.connect(self.thread_complete)  # ACTION SAAT FINISH
        start.signals.progress.connect(self.progress_fn)  # PROGRESS %

        # Execute
        self.threadpool.start(start)

    def stop(self):
        self.label.setText("Stop Processing..")
        self.progressBar.setRange(0, 1)
        self.check_button(self.pushButtonStop)

    def convertToText(self, response):
        if response == "nol":
            new_resp = response[0] + " "
        elif response == "satu":
            new_resp = response[0] + " "
        elif response == "dua":
            new_resp = response[0] + " "
        elif response == "tiga":
            new_resp = response[0] + " "
        elif response == "empat":
            new_resp = response[0] + " "
        elif response == "lima":
            new_resp = response[0] + " "
        elif response == "enam":
            new_resp = response[0] + " "
        elif response == "tujuh":
            new_resp = response[0] + " "
        elif response == "delapan":
            new_resp = response[0] + " "
        elif response == "sembilan":
            new_resp = response[0] + " "
        else:
            new_resp = "unknown "
            time.sleep(1)
        print("new resp: ", new_resp)
        return new_resp

    def newFile(self):
        self.textEdit.clear()

    def saveFile(self):
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
        f = open(filename, 'w')
        filedata = self.textEdit.toPlainText()
        f.write(filedata)
        f.close()

    def openFile(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File')
        f = open(filename, 'r')
        filedata = f.read()
        self.textEdit.setText(filedata)
        f.close()

    def aboutMenu(self):
        msg = QMessageBox()
        font = QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(12)
        msg.setFont(font)
        msg.setStyle(QStyleFactory.create('Cleanlooks'))
        msg.setIcon(QMessageBox.Information)
        msg.setTextFormat(Qt.RichText)
        msg.setText("A Simple Text Editor with Speech Recognition Feature")
        msg.setWindowTitle("About ARISE")
        msg.setDetailedText("Electrical and Information Engineering Universitas Gadjah Mada\n"
                            "Capstone Project\n"
                            "Made by : Ahmad Zaky W & Raka Andinan P\n"
                            "With help of Dr. Ir. Risanuri Hidayat, M.Sc. and Dr. Indah Soesanti, S.T., M.T. ")
        msg.exec_()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = MyApp()
    form.show()
    sys.exit(app.exec_())
