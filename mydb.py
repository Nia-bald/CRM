import mysql.connector

database = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'Niare13$'
)

# perpare cursor object
cursorObject = database.cursor()

cursorObject.execute("CREATE DATABASE elderco")

print("DDD")    