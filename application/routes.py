from flask import render_template, request, jsonify
from application import app


books_list = [{'ID': 1, 'Title': 'Title 1', 'Author': 'Author 1'}, {'ID': 2, 'Title': 'Title 2', 'Author': 'Author 2'}]


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html', title='Home')


@app.route('/allbooks', methods=['GET'])
def all_books():
    return jsonify(books_list)


@app.route('/books', methods=['GET', 'POST'])
def books():
    return render_template('books.html', books_list=books_list, title='Books')


@app.route('/book/<int:book_id>', methods=['GET'])
def book(book_id):
    book_title = None
    book_author = None
    for book_info in books_list:
        if book_info['ID'] == int(book_id):
            book_title = book_info['Title']
            book_author = book_info['Author']
    return render_template('book.html', book_title=book_title, book_id=book_id, book_author=book_author, title='Book')


@app.route('/book_edit/<book_id>', methods=['GET', 'POST'])
def book_edit(book_id):
    if request.method == 'GET':
        book_title = None
        book_author = None
        for book_info in books_list:
            if book_info['ID'] == int(book_id):
                book_title = book_info['Title']
                book_author = book_info['Author']
        return render_template('book_edit.html', book_title=book_title, book_id=book_id, title='Edit Book', book_author=book_author)
    else:
        title = request.form['title']
        author = request.form['author']
        book_id = request.form['book_id']
        print(book_id, title, author)
        if title == ''or author == '' or book_id == '':
            return render_template('book_edit.html', message="Please enter required fields", book_title=title, book_id=book_id, book_author=author)
        book_info = books_list[int(book_id) - 1]
        book_info['Title'] = title
        book_info['Author'] = author
        # if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
        #     data = Feedback(customer, engineer, rating, comments)
        #     db.session.add(data)
        #     db.session.commit()
        return render_template('books.html', books_list=books_list, title='Books')


@app.route('/book_add', methods=['GET', 'POST'])
def book_add():
    if request.method == 'GET':

        return render_template('book_add.html', title='Add Book')
    else:
        title = request.form['title']
        author = request.form['author']
        book_id = request.form['book_id']
        print(book_id, title, author)
        if title == '' or author == '' or book_id == '':
            return render_template('book_add.html', message="Please enter required fields")
        new_book = {'ID': int(book_id), 'Title': title, 'Author': author}
        books_list.append(new_book)

        return render_template('books.html', books_list=books_list, title='Books')


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', title='Error')




