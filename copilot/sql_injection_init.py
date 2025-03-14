from flask import request, render_template
from server.webapp import flaskapp, cursor
from server.modes import book

@flaskapp.route('/books')
def books():
    name = request.args.get('name')
    author = request.args.get('author')

    # Get books from the database where the author or name matches the query
    if name:
        cursor.execute('SELECT * FROM books WHERE name = %s', name)
        books = [Book(*row) for row in cursor]

    elif author:
        cursor.execute('SELECT * FROM books WHERE author = %s', author)
        books = [Book(*row) for row in cursor]

    else:
        cursor.execute('SELECT * FROM books')
        books = [Book(*row) for row in cursor]

    return render_template('books.html', books=books)

