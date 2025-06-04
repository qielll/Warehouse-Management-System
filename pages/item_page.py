import sqlite3
from sqlite3 import Error
from PyQt5.QtWidgets import QTableWidgetItem, QLineEdit, QComboBox, QMessageBox
from PyQt5 import QtCore
from .audit_function import AuditFunction

class ItemPage:
   
    
    def __init__(self, ui, dbFolder):
        self.ui = ui  # Simpan referensi ke UI
        self.dbFolder = dbFolder # Simpan lokasi folder database
        self.item_id = None
        self.storageId = None
        self.inboundId = None
        self.userId = None
        self.setup_signal() # Jalankan setup signal untuk tombol dan tabel

    # Fungsi untuk menghubungkan sinyal (klik tombol, klik tabel, dll.) ke function
    def setup_signal(self):
        self.ui.itemTable.cellClicked.connect(self.table_click)      # Saat tabel di klik
        self.ui.itemBackBtn.clicked.connect(lambda: self.table_back(self.dbFolder))          # Saat tombol back di klik
        self.ui.itemEditBtn.clicked.connect(self.messageUpdate)
        self.ui.itemDeleteBtn.clicked.connect(self.messageDelete)

    def setUserId(self, user_id):
        self.userId = user_id

    # Fungsi saat salah satu cell di tabel di klik
    def table_click(self, row, column):        # column juga dikirim dari sinyal, meskipun tidak digunakan
        self.item_id = self.ui.itemTable.item(row, 0).text()              # Ambil ID dari kolom pertama (index 0)
        self.getOneItems(self.dbFolder, self.item_id)                   # Ambil detail item dari database
        self.ui.itemsContent.setCurrentWidget(self.ui.itemSecondPage) # Pindah ke halaman detail

    # Fungsi untuk kembali ke halaman utama tabel
    def table_back(self, dbFolder):
        self.getAllItems(dbFolder)
        self.ui.itemsContent.setCurrentWidget(self.ui.itemTablePage)  # Kembali ke halaman tabel

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
            self.deleteItem(self.dbFolder, self.item_id, self.userId)
            self.getAllItems(self.dbFolder)
            self.ui.itemsContent.setCurrentWidget(self.ui.itemTablePage)

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
            self.updateItem(self.dbFolder , self.item_id, self.userId)
            self.getAllItems(self.dbFolder)
            self.ui.itemsContent.setCurrentWidget(self.ui.itemTablePage)


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
    def displayItems(self, rows):

        self.ui.itemTable.setRowCount(0)

        for row in rows:
            # Ambil posisi row yg kosong, self.ui.itemTable.rowCount() akan return total row yg sudah ada
            rowPosition = self.ui.itemTable.rowCount()

            # Insert row ke index yg kosong (rowPosition)
            self.ui.itemTable.insertRow(rowPosition)

            # Iterasi untuk menambahkan data ke setiap kolom pada row
            for colIndex, item in enumerate(row):
                # Inisialisasi QTableWidgetItem(value) untuk mengisi setiap field pada tabel
                qtablewidgetitem = QTableWidgetItem(str(item))  # Convert item ke string
                # Set data ke table widget di baris dan kolom tertentu
                self.ui.itemTable.setItem(rowPosition, colIndex, qtablewidgetitem)

    ##### GET DATA FROM TABLE #####

    # Fungsi untuk mengambil semua data dari tabel items
    def getAllItems(self, dbFolder):
        conn = ItemPage.create_connection(dbFolder)  # Panggil koneksi ke DB

        # Query untuk ambil data dengan JOIN ke tabel lain
        query = """
            SELECT 
                items.id,
                inbound.item_name,
                storage.rack_id,
                items.weight,
                inbound.inbound_timestamp,
                outbound.outbound_timestamp
            FROM items
            LEFT JOIN inbound ON items.inbound_id = inbound.id
            LEFT JOIN storage ON inbound.storage_id = storage.id
            LEFT JOIN outbound ON items.outbound_id = outbound.id;
        """
        try:
            c = conn.cursor()     # Buat cursor dari koneksi
            c.execute(query)      # Eksekusi query
            rows = c.fetchall()   # Ambil semua hasil dan kembalikan sebagai list of tuple

            self.displayItems(rows)
        except Error as e:
            print(e)              # Tampilkan error jika gagal

    # Fungsi untuk ambil 1 item berdasarkan ID
    def getOneItems(self, dbFolder, itemId):
        conn = ItemPage.create_connection(dbFolder)  # Panggil koneksi ke DB

        # Query mirip dengan getAllItems tapi hanya ambil 1 berdasarkan ID
        query = """
            SELECT 
                items.id,
                inbound.item_name,
                storage.rack_id,
                storage.id,
                inbound.id,
                items.weight,
                inbound.inbound_timestamp,
                outbound.outbound_timestamp
            FROM items
            LEFT JOIN inbound ON items.inbound_id = inbound.id
            LEFT JOIN storage ON inbound.storage_id = storage.id
            LEFT JOIN outbound ON items.outbound_id = outbound.id
            WHERE items.id = ?                     
        """

        queryChoice = """
            SELECT 
                id,
                rack_id
            FROM storage
        """
        try:
            c = conn.cursor()# Buat cursor
            c.execute(query, (itemId,))# Eksekusi query dengan parameter itemId   
            row = c.fetchone()# Ambil satu hasil data saja berdasarkan id

            c.execute(queryChoice)# Eksekusi query dengan parameter itemId
            storages = c.fetchall()
            _translate = QtCore.QCoreApplication.translate

            self.storageId = row[3]
            self.inboundId = row[4]
            filtered_row = [item for i, item in enumerate(row) if i not in (3, 4)]

            for index, data in enumerate(filtered_row):

                field_name = f"fieldItem_{index}"
                widget = getattr(self.ui, field_name, None)

                if widget is not None:
                    if isinstance(widget, QLineEdit):
                        widget.setText(_translate("MainWindow", str(data)))
                 
            
                widgetChoice = getattr(self.ui, "fieldItem_2", None)
                widgetChoice.clear()
            for storage in storages:
                widgetChoice.addItem(_translate("MainWindow", str(storage[1])), storage[0])

        except Error as e:
            print(e)# Tampilkan error jika gagal

    def updateItem(self,dbFolder,itemId, userId):
        conn = ItemPage.create_connection(dbFolder)  # Panggil koneksi ke DB

        storageField = f"fieldItem_{2}"
        widgetStorage = getattr(self.ui, storageField, None)
        
        storageVal = widgetStorage.itemData(widgetStorage.currentIndex())
        

        weightField = f"fieldItem_{3}"
        widgetWeight = getattr(self.ui, weightField, None)
        weightText = widgetWeight.text()

        
        # Query mirip dengan getAllItems tapi hanya ambil 1 berdasarkan ID
        query = """
            UPDATE  
               items
            SET
                weight = ?
            WHERE items.id = ?                     
        """
        queryInboundStore ="""
            UPDATE
                inbound
            SET 
                storage_id = ?
            WHERE inbound.id =?
        """

        try:
            c = conn.cursor()# Buat cursor
            c.execute(query, (weightText, itemId,))# Eksekusi query dengan parameter itemId
            c.execute(queryInboundStore, (storageVal, self.inboundId))
            conn.commit()

            action = "update"
            table = "Item"
        
            AuditFunction.recordAction(userId, action, table, dbFolder )

        except Error as e:
            print(e)# Tampilkan error jika gagal

        finally:
            conn.close()

    def deleteItem(self, dbFolder, itemId, userId):
        conn = ItemPage.create_connection(dbFolder)  # Panggil koneksi ke DB
        
        # Query mirip dengan getAllItems tapi hanya ambil 1 berdasarkan ID
        query = """
            DELETE FROM  
               items
            WHERE items.id = ?                     
        """

        try:
            c = conn.cursor()# Buat cursor
            c.execute(query, (itemId,))# Eksekusi query dengan parameter itemId
            conn.commit()

            action = "hapus"
            table = "Item"
        
            AuditFunction.recordAction(userId, action, table, dbFolder )

        except Error as e:
            print(e)# Tampilkan error jika gagal

        finally:
            conn.close()

    def createItem(self, dbFolder, userId):
        conn = ItemPage.create_connection(dbFolder)  # Panggil koneksi ke DB

        inputVal = []
       
        for index in range(5):
            field_name = f"fieldInboundCreate_{1}"
            widget = getattr(self.ui, field_name, None)

            if widget is not None:
                inputVal.append(widget.text())
               

        query = """
           INSERT INTO inbound (item_name, shipment_type, shipment_location, inbound_timestamp) 
           VALUES ( ? , ? , ?, datetime("now", "localtime") )            
        """

        try:
            c = conn.cursor()# Buat cursor
            c.execute(query, (inputVal[1], inputVal[3], inputVal[4],))# Eksekusi query dengan parameter itemId
            conn.commit()

            action = "tambah"
            table = "Item"
        
            AuditFunction.recordAction(userId, action, table, dbFolder )

        except Error as e:
            print(e)# Tampilkan error jika gagal
        finally:
            conn.close()
