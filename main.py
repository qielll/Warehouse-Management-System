########################################################################
## QT GUI BY SPINN TV(YOUTUBE)
########################################################################

########################################################################
## IMPORTS
########################################################################
import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
import hashlib
from sqlite3 import Error
########################################################################
# IMPORT GUI FILE (FROM YOUR GENERATED UI FILE)
from src.ui_interface import Ui_MainWindow

from PyQt5.QtCore import QLibraryInfo
########################################################################

########################################################################
from pages.user_function import UserFunction , UserAdmin, UserStaff
from pages.item_page import ItemPage
from pages.storage_page import StoragePage
from pages.inbound_page import InboundPage
from pages.outbound_page import OutboundPage
from pages.audit_function import AuditFunction
########################################################################

########################################################################
# IMPORT Custom widgets
from Custom_Widgets import *
from Custom_Widgets.QAppSettings import QAppSettings
########################################################################

########################################################################
## MAIN WINDOW CLASS
########################################################################
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setupAuth()
        
        self.db_path = "database/warehouse.db"
 
           
        ### Custom Logic yg berhubungan dengan database

        self.items_page = ItemPage(self.ui, self.db_path)
        self.items_page.getAllItems( self.db_path)

        self.storage_page = StoragePage(self.ui, self.db_path)
        self.storage_page.getAllStorage(self.db_path)

        self.inbound_page = InboundPage(self.ui, self.db_path)
        self.inbound_page.getAllInbound(self.db_path)

        self.outbound_page = OutboundPage(self.ui, self.db_path)
        self.outbound_page.getAllOutbound(self.db_path)

        self.auditLog = AuditFunction(self.ui, self.db_path)
        self.auditLog.getAllAudit(self.db_path)

        ### Custom Logic untuk load data tabel setiap menu pada sidebar di klik
        self.ui.btnItems.clicked.connect(lambda: self.items_page.getAllItems( self.db_path))
        self.ui.btnStorage.clicked.connect(lambda: self.storage_page.getAllStorage(self.db_path))
        self.ui.btnInbound.clicked.connect(lambda: self.inbound_page.getAllInbound(self.db_path))
        self.ui.btnOutbound.clicked.connect(lambda:  self.outbound_page.getAllOutbound(self.db_path))
        self.ui.btnAudit.clicked.connect(lambda: self.auditLog.getAllAudit(self.db_path)
)
    
    
        ########################################################################
        # APPLY JSON STYLESHEET
        ########################################################################
        loadJsonStyle(self, self.ui, jsonFiles = {
            "json-styles/style.json"
        })

        #######################################################################
        # SHOW WINDOW
        #######################################################################
        self.show()        

        ########################################################################
        # UPDATE APP SETTINGS LOADED FROM JSON STYLESHEET 
        ########################################################################
        QAppSettings.updateAppSettings(self)

    def setupAuth(self):
        self.ui.roleWidget.setCurrentWidget(self.ui.loginPage)
        self.ui.submitLogin.clicked.connect(lambda: self.authQuery(self.db_path))
        self.ui.submitRegist.clicked.connect(lambda: self.registQuery(self.db_path))
        self.ui.registerLogin.clicked.connect(self.handleRegister)
        self.ui.backRegist.clicked.connect(self.handleBackRegist)
        self.ui.btnLogout.clicked.connect(self.handleLogout)
    
    def handleLogout(self):

        self.ui.usernameInput.setText("")
        self.ui.passwordInput.setText("")
        self.ui.roleWidget.setCurrentWidget(self.ui.loginPage)

    def handleRegister(self):
        self.ui.roleWidget.setCurrentWidget(self.ui.registerPage)

    def handleBackRegist(self):
        self.ui.roleWidget.setCurrentWidget(self.ui.loginPage)
    
    def authQuery(self, dbFolder):
        username = self.ui.usernameInput.text()
        password = self.ui.passwordInput.text()


        hashPass = hashlib.sha256(password.encode()).hexdigest()
        conn = UserFunction.create_connection(dbFolder)
        if not conn:
            return None, None
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, username, role FROM user 
                WHERE username = ? AND password = ?
            """, (username, hashPass))

            row = cursor.fetchone()
            self.userId = row[0]
            self.inbound_page.setUserId(self.userId)
            self.storage_page.setUserId(self.userId)
            self.outbound_page.setUserId(self.userId)


            if row is not None:
                if row[2] == "admin":
                    UserAdmin.handleAuth(self, row[2])
                elif row[2] == "staff":
                    UserStaff.handleAuth(self, row[2]) 
            else:
                UserFunction.messageAuth(self)

        except Error as e:
            print("Query Error:", e)
            return None

    def registQuery(self, dbFolder):

        username = self.ui.usernameInputRegist.text()
        password = self.ui.passwordInputRegist.text()
        passwordConfirm = self.ui.confirmInputRegist.text()

        if password == passwordConfirm:
            hashPass = hashlib.sha256(password.encode()).hexdigest()
            conn = UserFunction.create_connection(dbFolder)
        else:
            UserFunction.messageRegist(self)
            return

        if not conn:
            print("Conn error")
            return None, None
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO user (role, username, password)
                VALUES ( "staff" , ? , ?)
            """, (username, hashPass))

            conn.commit()
            UserFunction.messageSuccessReg(self)
        except Error as e:
            print("Query Error:", e)
            return None





 
        



########################################################################
## EXECUTE APP
########################################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
########################################################################
## END===>
########################################################################
