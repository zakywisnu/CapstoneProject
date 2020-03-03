# import sys, time, traceback
# import numpy as np
#
# from micstream import MicrophoneStream
# # from PyQt5 import QtGui, QtWidgets, uic
#
# from PyQt5.QtGui import *
# # from PyQt5.QtCore import *
# from PyQt5.QtWidgets import *
#
# from PyQt4 import QtGui, uic
# from PyQt4.QtCore import *
# from PyQt4.QtGui import *
# qtCreatorFile = "MainWindow.ui"
#
# Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
#
# class WorkerSignals(QObject):
#     finished = pyqtSignal()
#     error = pyqtSignal(tuple)
#     result = pyqtSignal(object)
#     progress = pyqtSignal(int)
#
# class Start(QRunnable):
#     def __init__(self, fn, *args, **kwargs):
#         super(Start, self).__init__()
#
#         self.fn = fn
#         self.args = args
#         self.kwargs = kwargs
#         self.signals = WorkerSignals()
#
#     @pyqtSlot()
#     def run(self):
#         try:
#             result = self.fn(*self.args, **self.kwargs)
#         except:
#             traceback.print_exc()
#             exctype, value = sys.exc_info()[:2]
#             self.signals.error.emit((exctype, value, traceback.format_exc()))
#         else:
#             self.signals.result.emit(result)  # Return the result of the processing
#         finally:
#             self.signals.finished.emit()  # Done
#
# class Apps(QtGui.QMainWindow, Ui_MainWindow):
#     def __init__(self):
#         # QtWidgets.QMainWindow.__init__(self)
#         QtGui.QMainWindow.__init__(self)
#         Ui_MainWindow.__init__(self)
#         self.setupUi(self)
#
#         self.stream = MicrophoneStream()
#
#         self.pushButtonStart.clicked.connect(self.start)
#         self.pushButtonStop.clicked.connect(self.stop)
#         self.progressBar.setValue(0)
#
#         self.threadpool = QThreadPool()
#         print("multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
#
#         self.timer = QTimer()
#
#     def progress_fn(self,n):
#         print("%d%% done" % n)
#
#     def thread_complete(self):
#         print("thread complete!")
#         self.progressBar.setRange(0,1)
#
#     def check_button(self,button):
#         if button.isDown():
#             print("stop is clicked")
#             state_button = True
#         elif not button.isDown():
#             state_button = False
#         return state_button
#
#     def transcribe(self):
#         stateStop = self.check_button(self.pushButtonStop)
#         print("Button stop state: ", stateStop)
#
#         while not stateStop:
#             self.label.setText("Give Command!")
#             signal = self.stream.record()
#             self.progressBar.setRange(0,0)
#             self.label.setText("Processing...")
#             response, response2 = self.stream._listen()
#             resp = np.array(response2)
#             self.action(resp)
#             stateStop = self.check_button(self.pushButtonStop)
#             print("Button stop state: ", stateStop)
#
#         print("Stop Process")
#
#     def start(self):
#          start = Start(self.transcribe)
#
#          start.signals.finished.connect(self.thread_complete)
#          start.signals.progress.connect(self.progress_fn)
#
#          self.threadpool.start(start)
#
#     def stop(self):
#         self.label.setText("Stop processing..")
#         sys.exit()
#
#     # def action(self,response):
#
#
# if __name__ == "__main__":
#     app = QtGui.QApplication(sys.argv)
#     form = Apps()
#     form.show()
#     sys.exit(app.exec_())
