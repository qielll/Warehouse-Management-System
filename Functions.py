########################################################################
## IMPORTS
########################################################################
import os
import sys
# Import SQLite
import sqlite3
from sqlite3 import Error
#database mysql
import datetime
import mysql.connector

# Import QTableWidgetItem(For creating new table cells)
from PySide2.QtWidgets import QTableWidgetItem

# Functions class
class AppFunctions():
    """docstring for AppFunctions"""
    def __init__(self, arg):
        super(AppFunctions, self).__init__()
        self.arg = arg
        
    ########################################################################
    ## Create database connection
    ########################################################################
    def create_connection():
        try:
            conn = mysql.connector.connect(user='root', database='warehouse', password='', host='127.0.0.1')
       
        except mysql.connector.Error as err:
            print(err)
        # Return connection
        return conn


    ########################################################################
    ## Main function
    ########################################################################
    def main(dbFolder):
      
        # Create db connection
        conn = AppFunctions.create_connection()

    ########################################################################
    ## Get all items from database
    ########################################################################
    def getAllItems():
        # Create db connection
        conn = AppFunctions.create_connection()

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * from items")
            # fetch rresult
            rows = cursor.fetchall()
            return rows
        except Error as e:
            print(e)

    ########################################################################
    ## Add a item to db
    ########################################################################
    def addItem(self, inboundId):
        # Create db connection
        conn = AppFunctions.create_connection()
        cursor = conn.cursor()

        # Get form values
        # userName = self.ui.userName.text()
        # email = self.ui.email.text()
        # phoneNo = self.ui.phoneNo.text()
        weightItem = 12
        storageLoc = 1
        outBound = ""


        # Create sql statement
        query = ("INSERT INTO items "
               "(weight, storage_location, inbound_id, outbound_id) "
               "VALUES (%s, %s, %s, %s)"
               )
        
        # Execute sql statement
        if not cursor.execute(query, (weightItem, storageLoc, inboundId, outboundId)):
            print("Could not insert item data")
        else:
            cursor.execute(query, (weightItem, storageLoc, inboundId, outboundId)):
            print("Data item inserted")
            
            
            # Clear form input
            # self.ui.userName.setText("")
            # self.ui.email.setText("")
            # self.ui.phoneNo.setText("")

            # Load new user from DB to table view
            # AppFunctions.displayUsers(self, AppFunctions.getAllUsers(dbFolder))

    ########################################################################
    ## Add a inbound to db
    ########################################################################
    def addInbound(self):
        # Create db connection
        conn = AppFunctions.create_connection()
        cursor = conn.cursor()

        # Get form values
        # userName = self.ui.userName.text()
        # email = self.ui.email.text()
        # phoneNo = self.ui.phoneNo.text()
        itemName = "testProd"
        shipmentType = "reg"
        shipmentLoc = "jktTest"
        timestamp = datetime.datetime.now()
        
        # Create sql statement
        query = ("INSERT INTO inbound "
               "(item_name, shipment_type, shipment_location, timestamp) "
               "VALUES (%s, %s, %s, %s)")
        
        # Execute sql statement
        if not cursor.execute(query, (itemName, shipmentType, shipmentLoc, timestamp)):
            print("Could not insert inbound data")
        else:
            cursor.execute(query, (itemName, shipmentType, shipmentLoc, timestamp)):
            inboundId = cursor.lastrowid
            print("inbound ID: " , inboundId)
            return inboundId

            # Clear form input
            # self.ui.userName.setText("")
            # self.ui.email.setText("")
            # self.ui.phoneNo.setText("")

            # Load new user from DB to table view
            # AppFunctions.displayUsers(self, AppFunctions.getAllUsers(dbFolder))

    ########################################################################
    ## Display users
    ########################################################################
    # def displayUsers(self, rows):
    #     # Loop through all rows
    #     for row in rows:
    #         # Get number of rows
    #         rowPosition = self.ui.tableWidget.rowCount()

    #         # Skip rows that have already been loaded to table
    #         if rowPosition+1 > row[0]:
    #             continue

    #         itemCount = 0
    #         # Create new table row
    #         self.ui.tableWidget.setRowCount(rowPosition+1)
    #         qtablewidgetitem = QTableWidgetItem()
    #         self.ui.tableWidget.setVerticalHeaderItem(rowPosition, qtablewidgetitem)

    #         # Add items to row
    #         for item in row:
    #             self.qtablewidgetitem = QTableWidgetItem()
    #             self.ui.tableWidget.setItem(rowPosition, itemCount, self.qtablewidgetitem)
    #             self.qtablewidgetitem = self.ui.tableWidget.item(rowPosition, itemCount)
    #             self.qtablewidgetitem.setText(str(item))


    #             itemCount = itemCount+1

    #         rowPosition = rowPosition+1

    ########################################################################
    ## Add new storage to db
    ########################################################################
    def addOutbound(self):
        # Create db connection
        conn = AppFunctions.create_connection()
        cursor = conn.cursor()

        # Get form values
        # userName = self.ui.userName.text()
        # email = self.ui.email.text()
        # phoneNo = self.ui.phoneNo.text()
        rackId = "rackTest"
        
        # Create sql statement
        query = ("INSERT INTO storage "
               "(rack_id) "
               "VALUES (%s)")
        
        # Execute sql statement
        if not cursor.execute(query, rackId):
            print("Could not insert storage data")
        else:
            cursor.execute(query, rackId):
            print("storage data added ")

            # Clear form input
            # self.ui.userName.setText("")
            # self.ui.email.setText("")
            # self.ui.phoneNo.setText("")

            # Load new user from DB to table view
            # AppFunctions.displayUsers(self, AppFunctions.getAllUsers(dbFolder))


     ########################################################################
    ## Add a item to db
    ########################################################################
    def addItem(self, inboundId):
        # Create db connection
        conn = AppFunctions.create_connection()
        cursor = conn.cursor()

        # Get form values
        # userName = self.ui.userName.text()
        # email = self.ui.email.text()
        # phoneNo = self.ui.phoneNo.text()
        weightItem = 12
        storageLoc = 1
        outBound = ""


        # Create sql statement
        query = ("INSERT INTO items "
               "(weight, storage_location, inbound_id, outbound_id) "
               "VALUES (%s, %s, %s, %s)"
               )
        
        # Execute sql statement
        if not cursor.execute(query, (weightItem, storageLoc, inboundId, outboundId)):
            print("Could not insert item data")
        else:
            cursor.execute(query, (weightItem, storageLoc, inboundId, outboundId)):
            print("Data item inserted")
            
            
            # Clear form input
            # self.ui.userName.setText("")
            # self.ui.email.setText("")
            # self.ui.phoneNo.setText("")

            # Load new user from DB to table view
            # AppFunctions.displayUsers(self, AppFunctions.getAllUsers(dbFolder))
    
    ########################################################################
    ## Get all storage info from database
    ########################################################################
    def getAllStorage():
        # Create db connection
        conn = AppFunctions.create_connection()

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * from storage")
            # fetch rresult
            rows = cursor.fetchall()
            return rows
        except Error as e:
            print(e)

    
    ########################################################################
    ## Get all inbound from database
    ########################################################################
    def getAllInbound():
        # Create db connection
        conn = AppFunctions.create_connection()

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * from inbound")
            # fetch rresult
            rows = cursor.fetchall()
            return rows
        except Error as e:
            print(e)

    ########################################################################
    ## Get all outbound from database
    ########################################################################
    def getAllOutbound():
        # Create db connection
        conn = AppFunctions.create_connection()

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * from outbound")
            # fetch rresult
            rows = cursor.fetchall()
            return rows
        except Error as e:
            print(e)