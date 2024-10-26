import mysql.connector, pymysql

conn = mysql.connector.connect(
    host='localhost',
    database='api',
    user='root',
    passwd='admin123',
)
cursor = conn.cursor()  #Execute SQL statement in database

sql_query = """ CREATE TABLE book (
    id INT AUTO_INCREMENT PRIMARY KEY,
    author VARCHAR(100) NOT NULL,
    title VARCHAR(100) NOT NULL
) """

# Create The Database
# cursor.execute("CREATE DATABASE api")

cursor.execute(sql_query)

for db in cursor:
    print(db)

conn.close()