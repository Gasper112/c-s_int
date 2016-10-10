#-*- coding:utf-8 -*-

from PyQt4 import QtGui, QtCore, QtNetwork
from PyQt4.phonon import Phonon
import webbrowser, time, sys, hashlib, socket, os

global logL, pasL

def regServer():
    sock = socket.socket()
    try:
        sock.connect(('127.0.0.1',9090))

        file = open('reg_file.txt','r')
        data = file.read(8000)
        data = data.encode('utf-8')
        data = data + md5hash('try.py').encode('utf-8')
        sock.send(data)

        data = sock.recv(1024)
        sock.close()
        return data
    except:
        pass

def md5hash(fPath):
    file = open(fPath, 'rb')
    m = hashlib.md5()
    while True:
        data = file.read(8000)
        if not data:
            break
        m.update(data)
    return m.hexdigest()

class MessageThread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)

    def run(self):
        while True:
            time.sleep(10.0)
            self.emit(QtCore.SIGNAL('msg()'))

class Message(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)

class OpenButton(QtGui.QPushButton):

    def __init__(self):
        QtGui.QPushButton.__init__(self, 'Choose File')

        self.mediaObject = Phonon.MediaObject(self)
        self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, self)

        Phonon.createPath(self.mediaObject, self.audioOutput)

        self.mediaObject.stateChanged.connect(self.handleStateChanged)
        self.clicked.connect(self.handleButton)

    def handleButton(self):
        if self.mediaObject.state() == Phonon.PlayingState:
            self.mediaObject.stop()
        else:
            path = QtGui.QFileDialog.getOpenFileName(self, self.text())
            if path:
                self.mediaObject.setCurrentSource(Phonon.MediaSource(path))
                self.mediaObject.play()

    def handleStateChanged(self, newstate, oldstate):
        if newstate == Phonon.PlayingState:
            self.setText('Stop')
        elif newstate == Phonon.StoppedState:
            self.setText('Choose File')
        elif newstate == Phonon.ErrorState:
            self.setText('File is incorrect choose another')

class RegButton (QtGui.QPushButton):

    def __init__(self):
        QtGui.QPushButton.__init__(self, 'Registration')
        self.clicked.connect(self.handleButton)

    def handleButton(self):
        reply = QtGui.QMessageBox.question(self,'Registration'
                                           , 'You will be directed on our website. Do you want to proceed?',
                                           QtGui.QMessageBox.Yes,
                                           QtGui.QMessageBox.No
        )
        if reply == QtGui.QMessageBox.Yes:
            webbrowser.open_new('C:\\registration.html')

class MyApp(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self, parent = None)
        self.setGeometry(300,300,280,200)
        self.setWindowTitle('Player')

        self.layout = QtGui.QVBoxLayout(self)
        hLayout = QtGui.QHBoxLayout()

        self.ob = OpenButton()
        self.rb = RegButton()

        hLayout.addWidget(self.rb)

        self.layout.addLayout(hLayout)
        self.layout.addWidget(self.ob)

@QtCore.pyqtSlot()
def msg():
    wdg = MyApp()
    QtGui.QMessageBox.warning(wdg,'Registration'
                              ,'Your program is unregistered. If you like it, buy it'
                              ,QtGui.QMessageBox.Ok
    )


if __name__ == "__main__":
    app = QtGui.QApplication (sys.argv)
    messageThread = MessageThread()
    app.connect(messageThread, QtCore.SIGNAL('msg()'), msg)
    messageThread.start()
    win = MyApp()
    win.show()
    bump = regServer()

    if os.path.exists('reg_file.txt'):
        if bump == b'True':
            QtGui.QMessageBox.information(win,'Registration',
                                  'Congratulations'+
                                  'Your program is registered now'
                                  ,QtGui.QMessageBox.Ok
            )
            messageThread.terminate()
        elif bump == b'False':
            QtGui.QMessageBox.warning(win,'Registration',
                                  'Your registration data is incorrect.'+
                                  'Please, insert correct information in reg_file.txt'
                                  ,QtGui.QMessageBox.Ok
            )
    else:
        file = open('reg_file.txt','w')

    app.exec_()

