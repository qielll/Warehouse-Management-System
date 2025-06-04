import sqlite3
from sqlite3 import Error
from PyQt5.QtWidgets import QTableWidgetItem, QLineEdit, QComboBox, QMessageBox
from PyQt5 import QtCore
from .audit_function import AuditFunction

class StoragePage:
    
    def __init__(self, ui, dbFolder):
        self.ui = ui  # Simpan referensi ke UI
        self.dbFolder = dbFolder # Simpan lokasi folder database
        self.storage_id = None
        self.userId = None
        self.setup_signal() # Jalankan setup signal untuk tombol dan tabel

    # Fungsi untuk menghubungkan sinyal (klik tombol, klik tabel, dll.) ke function
    def setup_signal(self):
        self.ui.storageTable.cellClicked.connect(self.table_click)      # Saat tabel di klik
        self.ui.storageBackBtn.clicked.connect(lambda: self.table_back(self.dbFolder)) # Saat tombol back di klik
        self.ui.storageEditBtn.clicked.connect(self.messageUpdate)
        self.ui.storageDeleteBtn.clicked.connect(self.messageDelete)

        #function tombol form create
        self.ui.createStorageBackBtn.clicked.connect(lambda: self.table_back(self.dbFolder)) # Saat tombol back di klik
        self.ui.createStorageAddBtn.clicked.connect(self.messageCreate)
        self.ui.storageCreateBtn.clicked.connect(self.table_create)

    def setUserId(self, user_id):
        self.userId = user_id

    # Fungsi saat salah satu cell di tabel di klik
    def table_click(self, row, column):        # column juga dikirim dari sinyal, meskipun tidak digunakan
        self.storage_id = self.ui.storageTable.item(row, 0).text()              # Ambil ID dari kolom pertama (index 0)
        self.getOneStorage(self.dbFolder, self.storage_id)                   # Ambil detail item dari database
        self.ui.storageContent.setCurrentWidget(self.ui.storageSecondPage) # Pindah ke halaman detail

    # Fungsi untuk kembali ke halaman utama tabel
    def table_back(self, dbFolder):
        self.getAllStorage(dbFolder)
        self.ui.storageContent.setCurrentWidget(self.ui.storageTablePage)  # Kembali ke halaman tabel

    def table_create(self):
        self.ui.storageContent.setCurrentWidget(self.ui.storageCreatePage)

    def messageDelete(self):
        msg_box = QMessageBox()
        msg_box.setStyleSheet("""
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
        msg_box.setWindowTitle("Hapus Data")
        msg_box.setText("Data yg di hapus tidak bisa di kembalikan")
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
        msg_box.setDefaultButton(QMessageBox.Cancel)

        res = msg_box.exec_()

        if res == QMessageBox.Save:
            self.deleteStorage(self.dbFolder, self.storage_id, self.userId)
            self.getAllStorage(self.dbFolder)
            self.ui.storageContent.setCurrentWidget(self.ui.storageTablePage)

    def messageUpdate(self):
        msg_box = QMessageBox()
        msg_box.setStyleSheet("""
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
        msg_box.setWindowTitle("Update Data")
        msg_box.setText("Data berhasil di update")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setDefaultButton(QMessageBox.Ok)

        res = msg_box.exec_()

        if res == QMessageBox.Ok:
            self.updateStorage(self.dbFolder, self.userId)
            self.getAllStorage(self.dbFolder)
            self.ui.storageContent.setCurrentWidget(self.ui.storageTablePage)

    def messageCreate(self):
        msg_box = QMessageBox()
        msg_box.setStyleSheet("""
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
        msg_box.setWindowTitle("Create Data")
        msg_box.setText("Data berhasil di tambah")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setDefaultButton(QMessageBox.Ok)

        res = msg_box.exec_()

        if res == QMessageBox.Ok:
            self.createStorage(self.dbFolder, self.userId)
            self.getAllStorage(self.dbFolder)
            self.ui.storageContent.setCurrentWidget(self.ui.storageTablePage)


    ########## Section Untuk Function Database ##########

    # Membuat koneksi ke database
    def create_connection(db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)       # Membuka koneksi ke file database
            print("connected")                    # Tampilkan log jika sukses
        except Error as e:
            print(e)                              # Tampilkan error jika koneksi gagal
        return conn                                # Kembalikan objek koneksi

    ##### DISPLAY DATA FROM TABLE #####
    # Function menerima 'rows' dimana rows adalah sebuah list of tuple dari data hasil query
    def displayStorage(self, rows):

        self.ui.storageTable.setRowCount(0)

        for row in rows:
            # Ambil posisi row yg kosong, self.ui.storageTable.rowCount() akan return total row yg sudah ada
            rowPosition = self.ui.storageTable.rowCount()

            # Insert row ke index yg kosong (rowPosition)
            self.ui.storageTable.insertRow(rowPosition)

            # Iterasi untuk menambahkan data ke setiap kolom pada row
            for colIndex, item in enumerate(row):
                # Inisialisasi QTableWidgetItem(value) untuk mengisi setiap field pada tabel
                qtablewidgetitem = QTableWidgetItem(str(item))  # Convert item ke string
                # Set data ke table widget di baris dan kolom tertentu
                self.ui.storageTable.setItem(rowPosition, colIndex, qtablewidgetitem)

    ##### GET DATA FROM TABLE #####

    # Fungsi untuk mengambil semua data dari tabel items
    def getAllStorage(self, dbFolder):
        conn = StoragePage.create_connection(dbFolder)  # Panggil koneksi ke DB

        # Query untuk ambil data dengan JOIN ke tabel lain
        query = """
            SELECT 
                id,
                rack_id
            FROM storage
        """
        try:
            c = conn.cursor()     # Buat cursor dari koneksi
            c.execute(query)      # Eksekusi query
            rows = c.fetchall()   # Ambil semua hasil dan kembalikan sebagai list of tuple

            self.displayStorage(rows)
        except Error as e:
            print(e)              # Tampilkan error jika gagal

    # Fungsi untuk ambil 1 item berdasarkan ID
    def getOneStorage(self, dbFolder, storageId):
        conn = StoragePage.create_connection(dbFolder)  # Panggil koneksi ke DB

        # Query mirip dengan getAllItems tapi hanya ambil 1 berdasarkan ID
        query = """
            SELECT 
                id,
                rack_id
            FROM storage
            WHERE id = ?                     
        """
        try:
            c = conn.cursor()# Buat cursor
            c.execute(query, (storageId,))# Eksekusi query dengan parameter itemId
            row = c.fetchone()# Ambil satu hasil data saja berdasarkan id

            _translate = QtCore.QCoreApplication.translate

            for index, data in enumerate(row):

                field_name = f"fieldStorage_{index}"
                widget = getattr(self.ui, field_name, None)

                if widget is not None:
                    widget.setText(_translate("MainWindow", str(data)))
                    # elif isinstance(widget, QComboBox):
                    #     widget.clear()
                    #     widget.addItem(_translate("MainWindow", str(data)))
                    #     widget.setCurrentIndex(0)

        except Error as e:
            print(e)# Tampilkan error jika gagal

    def updateStorage(self, dbFolder, userId):
        conn = StoragePage.create_connection(dbFolder)  # Panggil koneksi ke DB

        field_data = []
        for index in range(2):  
            field_name = f"fieldStorage_{index}"
            widget = getattr(self.ui, field_name, None)
            field_data.append(widget.text())

        
        # Query mirip dengan getAllItems tapi hanya ambil 1 berdasarkan ID
        query = """
            UPDATE  
               storage
            SET
                rack_id = ?
            WHERE storage.id = ?                     
        """

        try:
            c = conn.cursor()# Buat cursor
            c.execute(query, (field_data[1], field_data[0]))# Eksekusi query dengan parameter itemId
            conn.commit()

            action = "update"
            table = "Storage"
        
            AuditFunction.recordAction(userId, action, table, dbFolder )

        except Error as e:
            print(e)# Tampilkan error jika gagal

        finally:
            conn.close()

    def deleteStorage(self, dbFolder, storageId, userId):
        conn = StoragePage.create_connection(dbFolder)  # Panggil koneksi ke DB
        
        # Query mirip dengan getAllItems tapi hanya ambil 1 berdasarkan ID
        query = """
            DELETE FROM  
               storage
            WHERE storage.id = ?                     
        """

        try:
            c = conn.cursor()# Buat cursor
            c.execute(query, (storageId,))# Eksekusi query dengan parameter itemId
            conn.commit()

            action = "hapus"
            table = "Storage"
        
            AuditFunction.recordAction(userId, action, table, dbFolder )

        except Error as e:
            print(e)# Tampilkan error jika gagal

        finally:
            conn.close()

    ## Need to create
    def createStorage(self, dbFolder, userId):
        conn = StoragePage.create_connection(dbFolder)  # Panggil koneksi ke DB

        inputVal = None
        field_name = f"fieldStorageCreate_{1}"
        widget = getattr(self.ui, field_name, None)

        if widget is not None:
            inputVal = widget.text()
               

        query = """
           INSERT INTO storage (rack_id) 
           VALUES ( ? )            
        """

        try:
            c = conn.cursor()# Buat cursor
            c.execute(query, (inputVal,))# Eksekusi query dengan parameter itemId
            conn.commit()

            action = "tambah"
            table = "Storage"
        
            AuditFunction.recordAction(userId, action, table, dbFolder )
        except Error as e:
            print(e)# Tampilkan error jika gagal
        finally:
            conn.close()
