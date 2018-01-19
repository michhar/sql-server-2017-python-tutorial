
#####################################################################
# Program:  crud.py
# Purpose:  To demo using pyodbc to connect to SQL Server and perform
# simple CRUD operations.
# Author:  Micheleen Harris
# Date:  2018
# Based on https://www.microsoft.com/en-us/sql-server/developer-get-started/python/mac/
# with some minor corrections.
#####################################################################

import pyodbc
import os
server = '127.0.0.1'
database = 'SampleDB'
username = 'sa'
password = os.getenv('SQL_PASS')
cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

# Insert data
print ('Inserting a new row into table')
#Insert Query
tsql = "INSERT INTO Employees (Name, Location) VALUES (?,?);"
with cursor.execute(tsql, 'Humpty Dumpty', 'Sweden'):
    print('Successfully Inserted!')

# Update an entry
print('Updating Location for Humpty Dumpty')
tsql = "UPDATE Employees SET Location = ? WHERE Name = ?"
with cursor.execute(tsql, 'Thailand', 'Humpty Dumpty'):
    print('Succesfully Updated!')

# Detete entry
print('Deleting user with Name "Humpty Dumpty"')
tsql = "DELETE from Employees WHERE Name = ?"
with cursor.execute(tsql, 'Humpty Dumpty'):
    print('Successfully Deleted!')

# Read data (all rows)
print('Print all rows in table')
cursor.execute("SELECT Name, Location FROM Employees")
rows = cursor.fetchall()
for row in rows:
    print(row.Name, row.Location)