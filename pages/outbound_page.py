import sqlite3
from sqlite3 import Error
from PyQt5.QtWidgets import QTableWidgetItem, QLineEdit, QComboBox, QMessageBox
from PyQt5 import QtCore
from .audit_function import AuditFunction


class OutboundPage:

    def __init__(self, ui, dbFolder):
        self.ui = ui
        self.dbFolder = dbFolder
        self.outbound_id = None
        self.item_id = None
        self.userId = None
        self.setup_signal()

    def setUserId(self, user_id):
        self.userId = user_id

    def setup_signal(self):
        self.ui.outboundTable.cellClicked.connect(self.table_click)
        self.ui.outboundBackBtn.clicked.connect(lambda: self.table_back(self.dbFolder))
        self.ui.outboundEditBtn.clicked.connect(self.messageUpdate)
        self.ui.outboundDeleteBtn.clicked.connect(self.messageDelete)

        self.ui.createOutboundBackBtn.clicked.connect(lambda: self.table_back(self.dbFolder))
        self.ui.createOutboundAddBtn.clicked.connect(self.messageCreate)
        self.ui.outboundCreateBtn.clicked.connect(self.table_create)

    def table_click(self, row, column):
        self.outbound_id = self.ui.outboundTable.item(row, 0).text()
        self.item_id = self.fetchIdItem(self.dbFolder, self.outbound_id)
        self.getOneOutbound(self.dbFolder, self.outbound_id)
        self.ui.outboundContent.setCurrentWidget(self.ui.outboundSecondPage)

    def table_back(self, dbFolder):
        self.getAllOutbound(dbFolder)
        self.ui.outboundContent.setCurrentWidget(self.ui.outboundTablePage)

    def table_create(self):
        self.ui.outboundContent.setCurrentWidget(self.ui.outboundCreatePage)
        self.fetchItem(self.dbFolder)
        
        for index in range(2,4):
            field_name = f"fieldOutboundCreate_{index}"
            widget = getattr(self.ui, field_name, None)
            widget.clear()  
            

    def messageDelete(self):
        msg_box = QMessageBox()
        msg_box.setStyleSheet(self.get_msgbox_style())
        msg_box.setWindowTitle("Hapus Data")
        msg_box.setText("Data yg di hapus tidak bisa di kembalikan")
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
        msg_box.setDefaultButton(QMessageBox.Cancel)

        res = msg_box.exec_()

        if res == QMessageBox.Save:
            self.deleteOutbound(self.dbFolder, self.outbound_id, self.item_id, self.userId)
            self.getAllOutbound(self.dbFolder)
            self.ui.outboundContent.setCurrentWidget(self.ui.outboundTablePage)

    def messageUpdate(self):
        msg_box = QMessageBox()
        msg_box.setStyleSheet(self.get_msgbox_style())
        msg_box.setWindowTitle("Update Data")
        msg_box.setText("Data berhasil di update")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setDefaultButton(QMessageBox.Ok)

        res = msg_box.exec_()

        if res == QMessageBox.Ok:
            self.updateOutbound(self.dbFolder, self.userId)
            self.getAllOutbound(self.dbFolder)
            self.ui.outboundContent.setCurrentWidget(self.ui.outboundTablePage)

    def messageCreate(self):
        msg_box = QMessageBox()
        msg_box.setStyleSheet(self.get_msgbox_style())
        msg_box.setWindowTitle("Create Data")
        msg_box.setText("Data berhasil di tambah")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setDefaultButton(QMessageBox.Ok)

        res = msg_box.exec_()

        if res == QMessageBox.Ok:
            self.createOutbound(self.dbFolder, self.userId)
            self.getAllOutbound(self.dbFolder)
            self.ui.outboundContent.setCurrentWidget(self.ui.outboundTablePage)

    def get_msgbox_style(self):
        return """
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
        """

    @staticmethod
    def create_connection(db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print("connected")
        except Error as e:
            print(e)
        return conn

    def displayOutbound(self, rows):
        self.ui.outboundTable.setRowCount(0)
        for row in rows:
            rowPosition = self.ui.outboundTable.rowCount()
            self.ui.outboundTable.insertRow(rowPosition)
            for colIndex, item in enumerate(row):
                self.ui.outboundTable.setItem(rowPosition, colIndex, QTableWidgetItem(str(item)))

    def getAllOutbound(self, dbFolder):
        conn = OutboundPage.create_connection(dbFolder)
        query = """
            SELECT 
                outbound.id,
                inbound.item_name,
                outbound.shipment_type,
                outbound.shipment_location,
                outbound.outbound_timestamp
            FROM outbound
            LEFT JOIN items ON outbound.id_item = items.id
            LEFT JOIN inbound on items.inbound_id = inbound.id
        """
        try:
            c = conn.cursor()
            c.execute(query)
            rows = c.fetchall()
            self.displayOutbound(rows)
        except Error as e:
            print(e)

    def getOneOutbound(self, dbFolder, outboundId):
        conn = OutboundPage.create_connection(dbFolder)
        query = """
            SELECT 
                outbound.id,
                inbound.item_name,
                outbound.shipment_type,
                outbound.shipment_location
            FROM outbound
            LEFT JOIN items ON outbound.id_item = items.id
            LEFT JOIN inbound ON items.inbound_id = inbound.id
            WHERE outbound.id = ?
        """
        try:
            c = conn.cursor()
            c.execute(query, (outboundId,))
            row = c.fetchone()
            _translate = QtCore.QCoreApplication.translate

            # filtered_row = [item for i, item in enumerate(row) if i != 1]

            for index, data in enumerate(row):
                field_name = f"fieldOutbound_{index}"
                widget = getattr(self.ui, field_name, None)
                if widget is not None:
                    widget.setText(_translate("MainWindow", str(data)))

            # last = getattr(self.ui,"fieldOutbound_3", None)
            # last.setText(_translate("MainWindow", str(filtered_row[2])))

        except Error as e:
            print(e)
        finally:
            conn.close()

    def updateOutbound(self, dbFolder, userId):
        conn = OutboundPage.create_connection(dbFolder)
        field_data = []
        for index in range(4):
            field_name = f"fieldOutbound_{index}"
            widget = getattr(self.ui, field_name, None)
            field_data.append(widget.text())

        query = """
            UPDATE  
               outbound
            SET
               shipment_type = ?,
               shipment_location = ?
            WHERE outbound.id = ?                     
        """
        try:
            c = conn.cursor()
            c.execute(query, ( field_data[2], field_data[3], field_data[0],))
            conn.commit()

            action = "update"
            table = "Outbound"
        
            AuditFunction.recordAction(userId, action, table, dbFolder )
        except Error as e:
            print(e)
        finally:
            conn.close()

    def deleteOutbound(self, dbFolder, outboundId, idItem, userId):
        conn = OutboundPage.create_connection(dbFolder)
        query = """
            DELETE FROM  
               outbound
            WHERE outbound.id = ?                     
        """

        queryUpdate = """
            UPDATE 
                items
            SET 
                outbound_id = NULL
            WHERE 
                items.id = ?
        """
        try:
            c = conn.cursor()
            c.execute(query, (outboundId,))

            c.execute(queryUpdate,(idItem,))
            conn.commit()

            action = "hapus"
            table = "Inbound"
        
            AuditFunction.recordAction(userId, action, table, dbFolder )
        except Error as e:
            print(e)
        finally:
            conn.close()

    def fetchItem(self, dbFolder):    
        conn = OutboundPage.create_connection(dbFolder)
        queryChoice = """
            SELECT 
            inbound.item_name,
            items.id
            FROM items
            LEFT JOIN inbound ON items.inbound_id = inbound.id
            WHERE items.outbound_id IS NULL
        """
        _translate = QtCore.QCoreApplication.translate
        try:
            c = conn.cursor()
            c.execute(queryChoice)
            storages = c.fetchall()

            widgetChoice = getattr(self.ui, "fieldOutboundCreate_1", None)
            widgetChoice.clear()
            for storage in storages:
                widgetChoice.addItem(_translate("MainWindow", str(storage[0])), storage[1])
        except Error as e:
            print(e)
        finally:
            conn.close()

    def fetchIdItem(self, dbFolder, outboundId):
        conn = OutboundPage.create_connection(dbFolder)
        query = """
            SELECT 
                outbound.id_item
            FROM outbound
            WHERE outbound.id = ?
        """
        try:
            c = conn.cursor()
            c.execute(query, (outboundId,))
            row = c.fetchone()
            return row[0]
        except Error as e:
            print(e)
        finally:
            conn.close()


    def createOutbound(self, dbFolder, userId):
        conn = OutboundPage.create_connection(dbFolder)
        inputVal = []
        comboBoxVal = None


        for index in range(4):
            field_name = f"fieldOutboundCreate_{index}"
            widget = getattr(self.ui, field_name, None) 
           
            if widget is not None:
                if isinstance(widget, QLineEdit):
                    inputVal.append(widget.text())
                elif isinstance(widget, QComboBox):
                    comboBoxVal = widget.currentData()
        query = """
           INSERT INTO outbound (id_item , shipment_type, shipment_location, outbound_timestamp) 
           VALUES ( ? , ? , ?, datetime("now", "localtime") )            
        """
        queryItem = """
           UPDATE 
            items 
           SET 
            outbound_id = ?      
           WHERE items.id = ?      
        """
        try:
            c = conn.cursor()
            c.execute(query, (comboBoxVal , inputVal[1], inputVal[2],))

            outboundId = c.lastrowid
            c.execute(queryItem, (outboundId, comboBoxVal))
            
            conn.commit()

            action = "tambah"
            table = "Outbound"
        
            AuditFunction.recordAction(userId, action, table, dbFolder )
        except Error as e:
            print(e)
        finally:
            conn.close()
