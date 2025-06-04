import sqlite3
from sqlite3 import Error
from PyQt5.QtWidgets import QTableWidgetItem, QLineEdit, QComboBox, QMessageBox
from PyQt5 import QtCore

class AuditFunction():
    def __init__(self, ui, dbFolder):
        self.ui = ui
        self.dbFolder = dbFolder
        # self.username = username
       
    @staticmethod
    def create_connection(db_file):
        try:
            conn = sqlite3.connect(db_file)
            print("connected")
            return conn
        except Error as e:
            print("Connection Error:", e)
            return None
        
    def getAllAudit(self, dbFolder):
        conn = AuditFunction.create_connection(dbFolder)  

        # Query untuk ambil data dengan JOIN ke tabel lain
        query = """
            SELECT 
                user.username,
                audit_log.action,
                audit_log.action_timestamp
            FROM audit_log
            LEFT JOIN user ON audit_log.user_id = user.id
        """
        try:
            c = conn.cursor()     # Buat cursor dari koneksi
            c.execute(query)      # Eksekusi query
            rows = c.fetchall()   # Ambil semua hasil dan kembalikan sebagai list of tuple

            self.displayAudit(rows)
        except Error as e:
            print(e)              # Tampilkan error jika gagal

    def displayAudit(self, rows):

        self.ui.auditTable.setRowCount(0)

        for row in rows:
            # Ambil posisi row yg kosong, self.ui.auditTable.rowCount() akan return total row yg sudah ada
            rowPosition = self.ui.auditTable.rowCount()

            # Insert row ke index yg kosong (rowPosition)
            self.ui.auditTable.insertRow(rowPosition)

            # Iterasi untuk menambahkan data ke setiap kolom pada row
            for colIndex, item in enumerate(row):
                # Inisialisasi QTableWidgetItem(value) untuk mengisi setiap field pada tabel
                qtablewidgetitem = QTableWidgetItem(str(item))  # Convert item ke string
                # Set data ke table widget di baris dan kolom tertentu
                self.ui.auditTable.setItem(rowPosition, colIndex, qtablewidgetitem)


    def recordAction( userId , action, tableAction , dbFolder):

        conn = AuditFunction.create_connection(dbFolder)

        getUsername = """
            SELECT username FROM user WHERE id = ?
        """

        query = """
            INSERT INTO audit_log (user_id, action, action_timestamp)
            VALUES ( ? , ? , datetime("now", "localtime") )         

        """

        try:
            c = conn.cursor()
            print(userId)
            c.execute(getUsername,(userId,))
            result = c.fetchone()
            
            if result is not None:
                username = result[0]
                templateAction = f"{username} Melakukan {action} data pada menu {tableAction}"
                c.execute(query, (userId, templateAction,))
                conn.commit()
            else:
                print(f"No user found with ID {userId}")

        except Error as e:
            print(e)
        
        finally:
            conn.close()


        
