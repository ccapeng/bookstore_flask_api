from flask import request
from flask_restful import Resource
from bookstore.models import db, BookModel


class BooksView(Resource):
 
    def get(self):
        books = BookModel.query.all()
        return {'books':list(x.json() for x in books)}
 
    def post(self):
        data = request.get_json()
 
        new_book = BookModel(data['name'],data['price'],data['author'])
        db.session.add(new_book)
        db.session.commit()
        return new_book.json(),201
 
 
class BookView(Resource):
  
    def get(self, id):
        book = BookModel.query.filter_by(id=id).first()
        if book:
            return book.json()
        return {'message':'book not found'},404

    def put(self, id):
        data = request.get_json()
 
        book = BookModel.query.filter_by(id=id).first() 
        if book:
            book.price = data["price"]
            book.author = data["author"]
        else:
            book = BookModel(name=name,**data)
 
        db.session.add(book)
        db.session.commit()
 
        return book.json()
 
    def delete(self, id):
        book = BookModel.query.filter_by(id=id).first()
        if book:
            db.session.delete(book)
            db.session.commit()
            return {'message':'Deleted'}
        else:
            return {'message': 'book not found'},404
