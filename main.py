#!/usr/bin/python3

from index import MainWindow
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtMultimedia
from PyQt5.uic import *
import pyrebase
import sys
import os

# from main_ui import Ui_MainWindow

MainUI,_ = loadUiType('main.ui')
WINDOW_SIZE = 0
counter = 0

# firebase config

firebaseConfig = { # Pute your config from firebase website firebase.com ;)
    "apiKey" : "",
    "authDomain" : "",
    "projectId" : "",
    "databaseURL":"",
    "storageBucket": "",
    "messagingSenderId": "",
    "appId": "",
    "measurementId" : ""
    }

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

class Main(QMainWindow , MainUI):
    def __init__(self , parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.ui()
        self.btns()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def ui(self):
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint)
        self.frame_top_1.mouseMoveEvent = self.mouseMoveEvent

    def btns(self): 
        # StackWidget 
        # {your QPushButton}.clicked.connect(lambda: {your QStackedWidget}.setCurrentWidget({another page}))
        self.btn_togle.clicked.connect(lambda : self.stackedWidget.setCurrentWidget(self.pg_home))
        self.btn_music.clicked.connect(lambda : self.stackedWidget.setCurrentWidget(self.pg_music))
        self.btn_goto.clicked.connect(lambda : self.stackedWidget.setCurrentWidget(self.pg_music))
        self.btn_music2.clicked.connect(lambda : self.stackedWidget.setCurrentWidget(self.pg_music))
        self.btn_go_to_setting.clicked.connect(lambda : self.stackedWidget.setCurrentWidget(self.pg_setting))
        self.btn_minimize.clicked.connect(lambda: self.showMinimized()  )
        self.btn_close.clicked.connect(self.close)
    
    # Restore or maximize your window
    def restore_or_maximize_window(self):
        # Global windows state
        global WINDOW_SIZE 
        win_status = WINDOW_SIZE

        if win_status == 0:
        	# If the window is not maximized
        	WINDOW_SIZE = 1
        	self.showMaximized()
        

        else:
        	# If the window is on its default size
            WINDOW_SIZE = 0
            self.showNormal()


# login SCREEN

Mainui,_ = loadUiType('login.ui')

class Login(QMainWindow, Mainui):
    def __init__(self , parent=None):
        super(Login, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.ui()
        self.btns()

    def btns(self):
        self.btn_exit.clicked.connect(self.close)
        self.btn_to_create.clicked.connect(lambda : self.stackedWidget.setCurrentWidget(self.pg_create))
        self.go_to_login.clicked.connect(lambda : self.stackedWidget.setCurrentWidget(self.pg_login ))
        self.btn_login.clicked.connect(self.loginfunction)
        self.btn_creat.clicked.connect(self.create_account)

    def ui(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint)
        self.invalid.setVisible(False)
        self.invalid1.setVisible(False)
    
    def loginfunction(self):
        email = self.login_user.text()
        password = self.login_passwd.text()
        try:
            auth.sign_in_with_email_and_password(email,password)
            main_win = Main()
            self.close()
            main_win.show()
        except:
            self.invalid.setVisible(True)
        
    def create_account(self):
        if self.creat_passwd1.text() == self.creat_passwd2.text() and self.creat_user.text() != "":
            password = self.creat_passwd1.text()
            mail = self.creat_user.text()
            try:
                auth.create_user_with_email_and_password(mail, password)
                lambda : self.stackedWidget.setCurrentWidget(self.pg_login)

            except:
                self.invalid.setVisible(True)


def main():
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

