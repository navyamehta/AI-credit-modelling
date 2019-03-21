import mysql.connector
from mysql.connector import Error

def gettrainingdata():
	try:
		cnx = mysql.connector.connect(user='sql9284623', password='m8QTBgHjDr',
                              	host='sql9.freesqldatabase.com',
                              	database='sql9284623')
		cursor = cnx.cursor()
		query = "SELECT * FROM `CREDIT_DATA`"
		cursor.execute(query)
		fullrow = []
		partrow = []
		for row in cursor:
			fullrow.append(row)
			partrow.append(row[1])
		cursor.close()
		cnx.close()
		finalrow = [fullrow, partrow]
		return finalrow
	except Error as e:
		print("Error while connecting to MySQL database", e)

def addnewtrainingdata():
