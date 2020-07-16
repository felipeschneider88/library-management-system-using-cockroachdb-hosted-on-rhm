from flask import Flask, render_template, request, redirect, jsonify
import os

import psycopg2
import psycopg2.errorcodes
import time
import logging
import random
import json

''' Initialize Flask Variables '''

app = Flask(__name__)

'''Initialize connection to Cockroach DB'''

dsn = 'postgresql://root@localhost:26257/library?sslmode=disable'

'''DB Access Methods'''

'''Method to create a table'''


def create_books_table(conn):
    with conn.cursor() as cur:
        cur.execute('CREATE TABLE IF NOT EXISTS books (id INT PRIMARY KEY, book_name VARCHAR, book_author VARCHAR, book_price FLOAT, book_availability INT)')
        logging.debug("create_books_table(): status message: {}".format(cur.statusmessage))
    conn.commit()
    

def create_borrower_table(conn):
    with conn.cursor() as cur:
        cur.execute('CREATE TABLE IF NOT EXISTS borrowers (id SERIAL PRIMARY KEY, borrower_name VARCHAR, borrower_email VARCHAR, book_id VARCHAR, total_price FLOAT, book_quantity VARCHAR)')
        logging.debug("create_borrower_table(): status message: {}".format(cur.statusmessage))
    conn.commit()


'''Method to Insert into Table'''

def insert_books(conn):
    with conn.cursor() as cur:
        cur.execute("UPSERT INTO books (id, book_name, book_author, book_price, book_availability) VALUES (1, 'Harry Potter', 'Jk Rowling', 2, 30), (2, 'Start with Why', 'Simon Sinek', 1.5, 20), (3, 'Programming with Python', 'John Smith', 1.5, 25)")
        logging.debug("create_books_table(): status message: {}".format(cur.statusmessage))
    conn.commit()
    

def insert_borrowers(borrower_name, borrower_email, book_id, total_price, book_quantity, conn):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO borrowers (borrower_name, borrower_email, book_id, total_price, book_quantity) VALUES (%s,%s,%s,%s,%s) RETURNING id", (borrower_name, borrower_email, book_id, total_price, book_quantity))
        print(cur.fetchone()[0])
        logging.debug("insert_borrowers(): status message: {}".format(cur.statusmessage))
    conn.commit()
    
    
'''Method to Query the contents from the table'''

def print_table(table, conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM {}".format(table))
        logging.debug("print_table(): status message: {}".format(cur.statusmessage))
        rows = cur.fetchall()
        conn.commit()
        return rows

def print_table_where(whereclause, conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM borrowers WHERE borrower_email like %s", (whereclause,))
        logging.debug("print_table(): status message: {}".format(cur.statusmessage))
        rows = cur.fetchall()
        conn.commit()
        return rows

def get_book_details(book_id, conn):
    with conn.cursor() as cur:
        cur.execute("SELECT book_name, book_price, book_availability FROM books WHERE id = {}".format(book_id))
        logging.debug("get_book_details(): status message: {}".format(cur.statusmessage))
        rows = cur.fetchall()
        conn.commit()
        return rows
 
'''Method to Update the contents of the table'''
    
def update_book_details(book_qty, book_id, conn):
    with conn.cursor() as cur:
        x = "UPDATE books SET book_availability = {0} WHERE id = {1}".format(
            book_qty, book_id)
        print(x)
        cur.execute("UPDATE books SET book_availability = {0} WHERE id = {1}".format(book_qty, book_id))
        print("update_book_details(): status message: {}".format(cur.statusmessage))
        conn.commit()

def get_books(conn):
    booksList = []
    Z = print_table('books', conn)
    for i in Z:
        tempDict = {
            'id': i[0],
            'book_name': i[1],
            'book_author': i[2],
            'book_price': i[3],
            'book_availability': i[4]
        }
        booksList.append(tempDict)
    return(json.dumps(booksList))


def delete_borrower(whereclause, conn):
    with conn.cursor() as cur:
        cur.execute(
            'DELETE from borrowers WHERE borrower_email like %s', (whereclause,))
        logging.debug("delete_borrower(): status message: {}".format(cur.statusmessage))
    conn.commit()

@app.route('/borrowbooks', methods=['GET','POST'])
def borrowbooks():
    
    if request.method == "POST":
        response = json.loads(request.form['borrowerDetails'])
        print(json.dumps(response, indent=2))
        bookIds = ""
        bookQtys = ""
        totalPrice = 0.0
        borrower_name = response['borrower_name']
        borrower_email = response['borrower_email']
        books = response['books']
        conn = psycopg2.connect(dsn)
        for book in books:
            bookId = book['book_id']
            bookIds += bookId + ','
            bookQty = int(book['book_qty'])
            bookQtys += str(bookQty) + ','
            bookDetails = get_book_details(bookId, conn)
            bookPrice = float(bookDetails[0][1]) * bookQty
            totalPrice += bookPrice
            updatedAvailibility = int(bookDetails[0][2]) - bookQty
            print(updatedAvailibility)
            update_book_details(updatedAvailibility, bookId, conn)
        insert_borrowers(borrower_name, borrower_email,
                         str(bookIds[:-1]), totalPrice, str(bookQtys[:-1]), conn)
            
        conn.close()
        return jsonify({"flag": 1})


@app.route('/returnbooks', methods=['GET', 'POST'])
def returnbooks():

    if request.method == "POST":
        response = json.loads(request.form['borrowerDetails'])
        borrower_email = response['borrower_email']
        
        print(json.dumps(response, indent=2))
        conn = psycopg2.connect(dsn)
        
        borrower = print_table_where(borrower_email, conn)
        try:
            books = borrower[0][3].split(',')
        except:
            temp = {
                'no': "No Books Borrowed!"
            }
            conn.close()
            return jsonify(temp)
        
        totalAmt = borrower[0][4]
        booksQts = borrower[0][5].split(',')
        bookNames = []
        
        for bookId in books:
            bookDetails = get_book_details(bookId, conn)
            bookNames.append(bookDetails[0][0])
               
        temp = {
            'borrower_name': borrower[0][1],
            'borrower_email': borrower[0][2],
            'books': bookNames,
            'book_ids': books,
            'book_qty': booksQts,
            'total_price': totalAmt
        }        
        conn.close()
        return jsonify(temp)


@app.route('/returnbookUser', methods=['GET', 'POST'])
def returnbookUser():
    if request.method == "POST":
        response = json.loads(request.form['borrowerDetails'])
        borrower_email = response['borrower_email']
        books = response['books']['book_id']
        booksQts = response['books']['book_qty']
        
        conn = psycopg2.connect(dsn)
        idx = 0
        for bookId in books:
            bookDetails = get_book_details(bookId, conn)
            updatedAvailibility = int(bookDetails[0][2]) + int(booksQts[idx])
            update_book_details(updatedAvailibility, bookId, conn)
            idx += 1
        delete_borrower(borrower_email, conn)
        
        conn.close()
        
        return jsonify({"flag": 1})

@app.route('/')
def index():
    conn = psycopg2.connect(dsn)
    create_books_table(conn)
    books = print_table('books', conn)
    
    if books == []:
        insert_books(conn)
    else:
        pass
    
    create_borrower_table(conn)
    books = json.loads(get_books(conn))
    conn.close()
    return render_template('index.html', books=books)

port = os.getenv('VCAP_APP_PORT', '8090')
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=port)
