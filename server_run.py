from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from pydantic import BaseModel
from datetime import datetime

app = Flask(__name__)

@app.route("/create_book/", methods=['POST'])
def create_book():
    data = request.get_json()
    book = BookPydantic(**data)
    db_book = Book(**book.dict())
    db.session.add(db_book)
    db.session.commit()
    db.session.refresh(db_book)
    return jsonify({'message': "created successfully"})

@app.route("/get_books/", methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify({'data': BookPydantic.from_orm(book) for book in books})

@app.route("/get_book/<int:book_id>/", methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'message': 'not found'})
    return jsonify({'data': BookPydantic.from_orm(book)})

@app.route("/update_book/<int:book_id>/", methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    book = BookPydantic(**data)
    db_book = Book.query.get(book_id)
    if not db_book:
        return jsonify({'error': 'book not found'})
    db_book.title = book.title
    db_book.author = book.author
    db_book.genre = book.genre
    db.session.commit()
    db.session.refresh(db_book)
    return jsonify({'message': 'updated successfully'})

@app.route("/delete_book/<int:book_id>/", methods=['DELETE'])
def delete_book(book_id):
    db_book = Book.query.get(book_id)
    if not db_book:
        return jsonify({'error': 'book not found'})
    db.session.delete(db_book)
    db.session.commit()
    return jsonify({'message': 'deleted successfully'})

if __name__ == "__main__":
    db.create_all()
    app.run(host='localhost', port=8000)