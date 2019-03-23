import mysql.connector
from mysql.connector import Error

def getcreditdata(token):
	try:
		cnx = mysql.connector.connect(user='sql9284623', password='m8QTBgHjDr',
                              	host='sql9.freesqldatabase.com',
                              	database='sql9284623')
		cursor = cnx.cursor()
		query = "SELECT * FROM `TOKEN_CREDIT` WHERE token = %s"
		cursor.execute(query, (token, ))
		fullrow = []
		for row in cursor:
			fullrow.append(row)
		cursor.close()
		cnx.close()
		return fullrow[0]['creditdata']
	except Error as e:
		print("Error while connecting to MySQL database", e)
