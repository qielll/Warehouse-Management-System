import sqlite3
from sqlite3 import Error
from PyQt5.QtWidgets import QTableWidgetItem, QLineEdit, QComboBox, QMessageBox
from PyQt5 import QtCore
from .audit_function import AuditFunction


class InboundPage:
    
    def __init__(self, ui, dbFolder):
        self.ui = ui  # Simpan referensi ke UI
        self.dbFolder = dbFolder # Simpan lokasi folder database
        self.inbound_id = None
        self.userId = None
        self.setup_signal() # Jalankan setup signal untuk tombol dan tabel

    def setUserId(self, user_id):
        self.userId = user_id
        

    # Fungsi untuk menghubungkan sinyal (klik tombol, klik tabel, dll.) ke function
    def setup_signal(self):
        self.ui.inboundTable.cellClicked.connect(self.table_click)      # Saat tabel di klik
        self.ui.inboundBackBtn.clicked.connect(lambda: self.table_back(self.dbFolder)) # Saat tombol back di klik
        self.ui.inboundEditBtn.clicked.connect(self.messageUpdate)
        self.ui.inboundDeleteBtn.clicked.connect(self.messageDelete)

        #function tombol form create
        self.ui.createInboundBackBtn.clicked.connect(lambda: self.table_back(self.dbFolder)) # Saat tombol back di klik
        self.ui.createInboundAddBtn.clicked.connect(self.messageCreate)
        self.ui.inboundCreateBtn.clicked.connect(self.table_create)

    # Fungsi saat salah satu cell di tabel di klik
    def table_click(self, row, column):        # column juga dikirim dari sinyal, meskipun tidak digunakan
        self.inbound_id = self.ui.inboundTable.item(row, 0).text()              # Ambil ID dari kolom pertama (index 0)
        print(self.inbound_id)
        self.getOneInbound(self.dbFolder, self.inbound_id)                   # Ambil detail item dari database
        self.ui.inboundContent.setCurrentWidget(self.ui.inboundSecondPage) # Pindah ke halaman detail

    # Fungsi untuk kembali ke halaman utama tabel
    def table_back(self, dbFolder):
        self.getAllInbound(dbFolder)
        self.ui.inboundContent.setCurrentWidget(self.ui.inboundTablePage)  # Kembali ke halaman tabel

    def table_create(self):
        self.ui.inboundContent.setCurrentWidget(self.ui.inboundCreatePage)
        self.fetchStorage(self.dbFolder)

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
            self.deleteInbound(self.dbFolder, self.inbound_id, self.userId)
            self.getAllInbound(self.dbFolder)
            self.ui.inboundContent.setCurrentWidget(self.ui.inboundTablePage)

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
            self.updateInbound(self.dbFolder, self.userId)
            self.getAllInbound(self.dbFolder)
            self.ui.inboundContent.setCurrentWidget(self.ui.inboundTablePage)

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
          
            self.createInbound(self.dbFolder, self.userId)
            self.getAllInbound(self.dbFolder)
            self.ui.inboundContent.setCurrentWidget(self.ui.inboundTablePage)


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
    def displayInbound(self, rows):

        self.ui.inboundTable.setRowCount(0)

        for row in rows:
            # Ambil posisi row yg kosong, self.ui.inboundTable.rowCount() akan return total row yg sudah ada
            rowPosition = self.ui.inboundTable.rowCount()

            # Insert row ke index yg kosong (rowPosition)
            self.ui.inboundTable.insertRow(rowPosition)

            # Iterasi untuk menambahkan data ke setiap kolom pada row
            for colIndex, item in enumerate(row):
                # Inisialisasi QTableWidgetItem(value) untuk mengisi setiap field pada tabel
                qtablewidgetitem = QTableWidgetItem(str(item))  # Convert item ke string
                # Set data ke table widget di baris dan kolom tertentu
                self.ui.inboundTable.setItem(rowPosition, colIndex, qtablewidgetitem)

    ##### GET DATA FROM TABLE #####

    # Fungsi untuk mengambil semua data dari tabel items
    def getAllInbound(self, dbFolder):
        conn = InboundPage.create_connection(dbFolder)  # Panggil koneksi ke DB

        # Query untuk ambil data dengan JOIN ke tabel lain
        query = """
            SELECT 
                id,
                item_name,
                shipment_type,
                shipment_location,
                inbound_timestamp
            FROM inbound
        """
        try:
            c = conn.cursor()     # Buat cursor dari koneksi
            c.execute(query)      # Eksekusi query
            rows = c.fetchall()   # Ambil semua hasil dan kembalikan sebagai list of tuple

            self.displayInbound(rows)
        except Error as e:
            print(e)              # Tampilkan error jika gagal

    # Fungsi untuk ambil 1 item berdasarkan ID
    def getOneInbound(self, dbFolder, inboundId):
        conn = InboundPage.create_connection(dbFolder)  # Panggil koneksi ke DB

        # Query mirip dengan getAllItems tapi hanya ambil 1 berdasarkan ID
        query = """
            SELECT 
                inbound.id,
                item_name,
                shipment_type,
                shipment_location
            FROM inbound
            LEFT JOIN storage ON inbound.storage_id = storage.id
            WHERE inbound.id = ?                     
        """
        try:
            c = conn.cursor()# Buat cursor
            c.execute(query, (inboundId,))# Eksekusi query dengan parameter itemId
            row = c.fetchone()# Ambil satu hasil data saja berdasarkan id

            _translate = QtCore.QCoreApplication.translate

            for index, data in enumerate(row):

                field_name = f"fieldInbound_{index}"
                widget = getattr(self.ui, field_name, None)

                if widget is not None:
                    widget.setText(_translate("MainWindow", str(data)))
                    # elif isinstance(widget, QComboBox):
                    #     widget.clear()
                    #     widget.addItem(_translate("MainWindow", str(data)))
                    #     widget.setCurrentIndex(0)

        except Error as e:
            print(e)# Tampilkan error jika gagal
        finally:
            conn.close()

    def updateInbound(self, dbFolder, userId):
        conn = InboundPage.create_connection(dbFolder)  # Panggil koneksi ke DB

        field_data = []
        for index in range(4):  
            field_name = f"fieldInbound_{index}"
            widget = getattr(self.ui, field_name, None)
            field_data.append(widget.text())

        
        # Query mirip dengan getAllItems tapi hanya ambil 1 berdasarkan ID
        query = """
            UPDATE  
               inbound
            SET
               item_name = ?,
               shipment_type = ?,
               shipment_location = ?
            WHERE inbound.id = ?                     
        """

        try:
            c = conn.cursor()# Buat cursor
            c.execute(query, (field_data[1], field_data[2], field_data[3], field_data[0],))# Eksekusi query dengan parameter itemId
            conn.commit()

            action = "update"
            table = "Inbound"
        
            AuditFunction.recordAction(userId, action, table, dbFolder )

        except Error as e:
            print(e)# Tampilkan error jika gagal

        finally:
            conn.close()

    def deleteInbound(self, dbFolder, inboundId, userId):
        conn = InboundPage.create_connection(dbFolder)  # Panggil koneksi ke DB
        
        # Query mirip dengan getAllItems tapi hanya ambil 1 berdasarkan ID
        query = """
            DELETE FROM  
               inbound
            WHERE inbound.id = ?                     
        """

        try:
            c = conn.cursor()# Buat cursor
            c.execute(query, (inboundId,))# Eksekusi query dengan parameter itemId
            conn.commit()

            action = "hapus"
            table = "Inbound"
        
            AuditFunction.recordAction(userId, action, table, dbFolder )


        except Error as e:
            print(e)# Tampilkan error jika gagal

        finally:
            conn.close()

    def fetchStorage(self, dbFolder):    
        conn = InboundPage.create_connection(dbFolder)  # Panggil koneksi ke DB

        queryChoice = """
            SELECT 
                id,
                rack_id
            FROM storage
        """

        _translate = QtCore.QCoreApplication.translate

        try:
            c = conn.cursor()# Buat cursor
            c.execute(queryChoice)# Eksekusi query dengan parameter itemId
            storages = c.fetchall()

            widgetChoice = getattr(self.ui, "fieldInboundCreate_3", None)
            widgetChoice.clear()
            for storage in storages:
                widgetChoice.addItem(_translate("MainWindow", str(storage[1])), storage[0])
        except Error as e:
            print(e)# Tampilkan error jika gagal
        finally:
            conn.close()



    ## Need to create
    def createInbound(self, dbFolder, userId):
        conn = InboundPage.create_connection(dbFolder)  # Panggil koneksi ke DB

        inputVal = []
        comboBoxVal = None

        for index in range(6):
            field_name = f"fieldInboundCreate_{index}"
            widget = getattr(self.ui, field_name, None)

            
            if widget is not None:
                if isinstance(widget, QLineEdit):
                    inputVal.append(widget.text())
                elif isinstance(widget, QComboBox):
                    comboBoxVal = widget.currentData()
                   

        query = """
           INSERT INTO inbound (item_name , storage_id , shipment_type, shipment_location, inbound_timestamp) 
           VALUES ( ?, ? , ? , ?, datetime("now", "localtime") )            
        """

        queryItem = """
           INSERT INTO items (weight , inbound_id ) 
           VALUES ( ?, ? )            
        """ 

        try:
            c = conn.cursor()# Buat cursor
            c.execute(query, (inputVal[1], comboBoxVal , inputVal[3], inputVal[4],))# Eksekusi query dengan parameter itemId
           
          
            weight = inputVal[2]
            inboundId = c.lastrowid
           
            c.execute(queryItem, (weight, inboundId,))
            conn.commit()

            action = "tambah item dan inbound"
            table = "Inbound"
        
            AuditFunction.recordAction(userId, action, table, dbFolder )
                
        except Error as e:
            print(e)# Tampilkan error jika gagal
        finally:
            conn.close()
