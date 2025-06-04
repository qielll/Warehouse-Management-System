import mysql.connector
from mysql.connector import Error
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QTableWidgetItem

class AppFunctions:
    def __init__(self, ui):
        self.ui = ui

    def create_connection(self):
        print("[DB] Connecting using QtSql...")
        self.db = QSqlDatabase.addDatabase("QMYSQL")  
        self.db.setHostName("127.0.0.1")
        self.db.setPort(3306)
        self.db.setDatabaseName("warehouse")
        self.db.setUserName("root")
        self.db.setPassword("")

        if not self.db.open():
            print("[DB] Connection failed:", self.db.lastError().text())
            return False
        print("[DB] Connected successfully")
        return True

    # def getAllItems(self):
    #     conn = self.create_connection()
    #     if conn is None:
    #         print("[DB] Connection returned None in getAllItems")
    #         return []

    #     try:
    #         print("[DB] Creating cursor...")
    #         cursor = conn.cursor()
            
    #         query = """
    #             SELECT 
    #                 items.id,
    #                 inbound.item_name,
    #                 items.weight,
    #                 storage.rack_id,
    #                 inbound.inbound_timestamp,
    #                 outbound.outbound_timestamp
    #             FROM items
    #             LEFT JOIN storage ON items.storage_location = storage.id
    #             LEFT JOIN inbound ON items.inbound_id = inbound.id
    #             LEFT JOIN outbound ON items.outbound_id = outbound.id
    #         """
    #         print("[DB] Executing query...")
    #         cursor.execute(query)
    #         print("[DB] Query executed")

    #         rows = cursor.fetchall()
    #         print(f"[DB] Rows fetched: {len(rows)}")
    #         return rows

    #     except Error as e:
    #         print("[DB] Error fetching items:", e)
    #         return []

    #     except Exception as e:
    #         print("[App] General error in getAllItems:", e)
    #         return []

    #     finally:
    #         print("[DB] Closing connection and cursor")
    #         try:
    #             cursor.close()
    #             conn.close()
    #         except Exception as e:
    #             print("[DB] Error during cleanup:", e)

    # def displayUsers(self, rows):
    #     try:
    #         print("[UI] Displaying users...")
    #         self.ui.tableItems.setRowCount(0)

    #         for row in rows:
    #             rowPosition = self.ui.tableItems.rowCount()
    #             self.ui.tableItems.insertRow(rowPosition)

    #             for column, item in enumerate(row):
    #                 qtable_item = QTableWidgetItem(str(item))
    #                 self.ui.tableItems.setItem(rowPosition, column, qtable_item)

    #         print("[UI] Table updated with items")
    #     except Exception as e:
    #         print("[UI] Error displaying users:", e)


