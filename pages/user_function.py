import sqlite3
from sqlite3 import Error
from PyQt5.QtWidgets import QTableWidgetItem, QLineEdit, QComboBox, QMessageBox
from PyQt5 import QtCore
import hashlib
from abc import ABC, abstractmethod

class UserFunction(ABC):
    def __init__(self, ui, dbFolder):
        self.ui = ui
        self.dbFolder = dbFolder

    @staticmethod
    def create_connection(db_file):
        try:
            conn = sqlite3.connect(db_file)
            print("connected")
            return conn
        except Error as e:
            print("Connection Error:", e)
            return None
        

    def messageAuth(self):
        msg = QMessageBox()
        msg.setWindowTitle("Login Failed")
        msg.setText("Username atau password salah.")
        msg.setIcon(QMessageBox.Warning)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
                text-align: center;
            }

            QLabel {
                color: #000000;
                font-size: 14px;
                text-align: center;              
            }

            QPushButton {
                background-color: #1E3A8A; 
                color: white;
                padding: 5px 15px;
                border-radius: 5px;
                min-width: 80px;
            }

            QPushButton:hover {
                background-color: #3B82F6;  
            }

            QPushButton:pressed {
                background-color: #1D4ED8;
            }
        """)
        msg.exec_()

    def messageRegist(self):
        msg = QMessageBox()
        msg.setWindowTitle("Register gagal")
        msg.setText("Pastikan password dan confirm password sama!")
        msg.setIcon(QMessageBox.Warning)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
                text-align: center;
            }

            QLabel {
                color: #000000;
                font-size: 14px;
                text-align: center;              
            }

            QPushButton {
                background-color: #1E3A8A; 
                color: white;
                padding: 5px 15px;
                border-radius: 5px;
                min-width: 80px;
            }

            QPushButton:hover {
                background-color: #3B82F6;  
            }

            QPushButton:pressed {
                background-color: #1D4ED8;
            }
        """)
        msg.exec_()

    def messageSuccessReg(self):
        msg = QMessageBox()
        msg.setWindowTitle("Register berhasil")
        msg.setText("Registrasi berhasil, silahkan login dengan user dan password anda")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok )
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
                text-align: center;
            }

            QLabel {
                color: #000000;
                font-size: 14px;
                text-align: center;              
            }

            QPushButton {
                background-color: #1E3A8A; 
                color: white;
                padding: 5px 15px;
                border-radius: 5px;
                min-width: 80px;
            }

            QPushButton:hover {
                background-color: #3B82F6;  
            }

            QPushButton:pressed {
                background-color: #1D4ED8;
            }
        """)
        btn = msg.exec_()
       
        if btn == QMessageBox.Ok:
            self.ui.roleWidget.setCurrentWidget(self.ui.loginPage)

    @abstractmethod
    def handleAuth():
        pass

   
class UserAdmin(UserFunction):
    def handleAuth(self, role ):
        if role == "admin":
            self.ui.roleWidget.setCurrentWidget(self.ui.admin)
        else:
            self.messageAuth()
   

class UserStaff(UserFunction):
    def handleAuth(self, role):
        if role == "staff":
            self.ui.btnAudit.hide()
            self.ui.roleWidget.setCurrentWidget(self.ui.admin)
        else:
            self.messageAuth()
