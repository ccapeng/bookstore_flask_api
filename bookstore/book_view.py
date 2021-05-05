from flask import request
from flask_restful import Resource
from bookstore.models import db, \
    BookModel, CategoryModel, PublisherModel, AuthorModel


class BooksView(Resource):
 
    def get(self):
        books = BookModel.query.join(
            CategoryModel, 
            BookModel.category_id == CategoryModel.id
        ).join (
            PublisherModel, 
            BookModel.publisher_id == PublisherModel.id
        ).join (
            AuthorModel, 
            BookModel.author_id == AuthorModel.id
        ).add_columns(
            BookModel.id,
            BookModel.title,
            BookModel.category_id,
            CategoryModel.name.label("category_name"),
            BookModel.publisher_id,
            PublisherModel.name.label("publisher_name"),
            BookModel.author_id,
            AuthorModel.last_name.label("author_last_name"),
            AuthorModel.first_name.label("author_first_name"),
        )
        book_list = []
        for book in books:
            book_list.append({
                "id": book.id,
                "title": book.title, 
                "category_id": book.category_id, 
                "category_name": book["category_name"], 
                "publisher_id": book.publisher_id,
                "publisher_name": book["publisher_name"], 
                "author_id": book.author_id,
                "author_last_name": book["author_last_name"], 
                "author_first_name": book["author_first_name"], 
            })

        return {'books': book_list}, 200

    def post(self):
        data = request.get_json()
        book = BookModel(
            data['title'], 
            data['category_id'],
            data['publisher_id'],
            data['author_id'],
        )
        db.session.add(book)
        db.session.commit()
        return book.json(), 201
 
 
class BookView(Resource):
  
    def get(self, id):
        book = BookModel.query.filter_by(id=id).first()
        if book:
            return book.json()
        return {'msg': 'Book not found.'}, 404

    def put(self, id):
        data = request.get_json()
        book = BookModel.query.filter_by(id=id).first() 
        if book:
            book.title = data["title"]
            book.category_id = data["category_id"]
            book.publisher_id = data["publisher_id"]
            book.author_id = data["author_id"]
        else:
            book = BookModel(
                title=title, 
                category_id=category_id,
                publisher_id=publisher_id,
                author_id=author_id
            )
 
        db.session.add(book)
        db.session.commit()
 
        return book.json()
 
    def delete(self, id):
        book = BookModel.query.filter_by(id=id).first()
        if book:
            db.session.delete(book)
            db.session.commit()
            return {'msg':'Deleted'}
        else:
            return {'msg': 'Book not found.'}, 404