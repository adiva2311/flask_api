from flask import Flask, request, jsonify
import json
import mysql.connector, pymysql

app = Flask(__name__)

# Connection To Database
def db_connection():
    conn = None
    try:
        conn = pymysql.connect(
            host='localhost',
            database='api',
            user='root',
            passwd='admin123',
        )
    except pymysql.error as e:
        print(e)
    return conn

@app.route('/books/', methods=['GET', 'POST'])
def books():
    # Make Connection with Database
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        # Execute The Query to Get All The Books
        sql_query = """ SELECT * FROM book """
        cursor.execute(sql_query)
        books = [
            dict(id=row[0], author=row[1], title=row[2])
            for row in cursor.fetchall()
        ]
        if books is not None:
            return jsonify(books)

    if request.method == 'POST':
        new_author = request.form['author']
        new_title = request.form['title']

        # Execute The Query to CREATE The Books
        sql_query = """ INSERT INTO book(author, title) VALUES (%s, %s) """
        cursor.execute(sql_query, (new_author, new_title))
        conn.commit()
        return f"Book with ID : {cursor.lastrowid} has been CREATED successfully", 201


@app.route('/book/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_book(id):
    # Make Connection with Database
    conn = db_connection()
    cursor = conn.cursor()
    book = None

    if request.method == 'GET':
        sql_query = """ SELECT * FROM book WHERE id=%s """
        cursor.execute(sql_query, (id,)) # ID is returning an INTEGER, so it must included with a comma (id,)
        rows = cursor.fetchall() 
        # Grab All The Books with ID
        for row in rows:
            book = row
        if book is not None:
            return jsonify(book), 200
        else:
            return "Something's Wrong", 404

    if request.method == 'PUT':
        sql_query = """ UPDATE book SET
                        author=%s,
                        title=%s
                        WHERE id=%s
                    """
        author = request.form['author']
        title = request.form['title']
        updated_book = {
            'id':id,
            'author':author,
            'title':title,
        }
        cursor.execute(sql_query, (author, title, id))
        conn.commit()
        return jsonify(updated_book)
            
    if request.method == 'DELETE':
        sql_query = """ DELETE FROM book WHERE id = %s """
        cursor.execute(sql_query, (id,))
        conn.commit()
        return f"Book with ID : {id} has been DELETED", 200
    

if __name__ == "__main__":
    app.run(debug=True)