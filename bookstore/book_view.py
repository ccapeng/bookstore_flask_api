from flask import request
from flask_restful import Resource
from bookstore.models import db, \
    BookModel, CategoryModel, PublisherModel, AuthorModel


class BooksView(Resource):
 
    def get(self):

        books = BookModel.query.outerjoin(
            CategoryModel, 
            BookModel.category_id == CategoryModel.id
        ).outerjoin (
            PublisherModel, 
            BookModel.publisher_id == PublisherModel.id
        ).outerjoin (
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
            obj = BookModel.detail_join_json(book)
            book_list.append(obj)
        return book_list, 200

        # The following code also works, but the query is not optimized.
        # Each category, publisher, author models are sub-query.
        # books = BookModel.query.all()
        # return {'books':list(x.detail_json() for x in books)}

    def post(self):
        data = request.get_json()
        book = BookModel.parse(data)
        print("post book", book)
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
            book.update(data)
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