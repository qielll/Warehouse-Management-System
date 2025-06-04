import mysql.connector
from mysql.connector import Error
import datetime

class AppFunctions:
    def __init__(self):
        pass

    @staticmethod
    def create_connection():
        try:
            return mysql.connector.connect(
                user='root',
                password='',
                host='127.0.0.1',
                database='warehouse'
            )
        except mysql.connector.Error as err:
            print("Connection error:", err)
            return None

    @staticmethod
    def getAllItems():
        conn = AppFunctions.create_connection()
        if conn is None:
            print("Connection error in all items")
            return []

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM items")
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Error as e:
            print("Error fetching items:", e)
            return []

    def addItem(self, inboundId):
        conn = AppFunctions.create_connection()
        
        if conn is None:
            print("Connection error in all items")
            return

        try:
            cursor = conn.cursor()
            weightItem = 12
            storageLoc = 1
            outboundId = None

            query = """
                INSERT INTO items (weight, storage_location, inbound_id, outbound_id)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (weightItem, storageLoc, inboundId, outboundId))
            conn.commit()
            print("Item inserted with ID:", cursor.lastrowid)
            cursor.close()
            conn.close()
        except mysql.connector.Error as e:
            print("Item insert failed:", e)

    def addInbound(self):
        conn = AppFunctions.create_connection()
        if conn is None:
            return None

        try:
            cursor = conn.cursor()
            itemName = "testProd"
            shipmentType = "reg"
            shipmentLoc = "jktTest"
            timestamp = datetime.datetime.now()

            query = """
                INSERT INTO inbound (item_name, shipment_type, shipment_location, timestamp)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (itemName, shipmentType, shipmentLoc, timestamp))
            conn.commit()
            inboundId = cursor.lastrowid
            print("Inserted Inbound ID:", inboundId)
            cursor.close()
            conn.close()
            return inboundId
        except mysql.connector.Error as e:
            print("Insert error:", e)
            return None

    # def addOutbound(self):
    #     conn = AppFunctions.create_connection()
    #     if conn is None:
    #         return

    #     try:
    #         cursor = conn.cursor()
    #         rackId = "rackTest"

    #         query = "INSERT INTO storage (rack_id) VALUES (%s)"
    #         cursor.execute(query, (rackId,))
    #         conn.commit()
    #         print("Storage added with ID:", cursor.lastrowid)
    #         cursor.close()
    #         conn.close()
    #     except mysql.connector.Error as e:
    #         print("Storage insert error:", e)

    def addOutbound(self):
        conn = AppFunctions.create_connection()
        if conn is None:
            return

        try:
            cursor = conn.cursor()
            shipmentType = "reg"
            shipmentLoc = "jktTest"
            timestamp = datetime.datetime.now()
            idItem = 3
            
            query = """
                INSERT INTO outbound (shipment_type, shipment_location, id_item, timestamp)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (shipmentType, shipmentLoc, idItem, timestamp ))
            conn.commit()
            cursor.close()
            conn.close()
        except mysql.connector.Error as e:
            print("Storage insert error:", e)

    @staticmethod
    def getAllStorage():
        conn = AppFunctions.create_connection()
        if conn is None:
            return []

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM storage")
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Error as e:
            print("Error fetching storage:", e)
            return []

    @staticmethod
    def getAllInbound():
        conn = AppFunctions.create_connection()
        if conn is None:
            return []

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM inbound")
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Error as e:
            print("Error fetching inbound:", e)
            return []

    @staticmethod
    def getAllOutbound():
        conn = AppFunctions.create_connection()
        if conn is None:
            return []

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM outbound")
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Error as e:
            print("Error fetching outbound:", e)
            return []


app = AppFunctions()

items = app.getAllItems()

for item in items:
    print(item)

