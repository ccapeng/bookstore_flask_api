from flask import request
from flask_restful import Resource
from bookstore.models import db, AuthorModel


class AuthorsView(Resource):
 
    def get(self):
        authors = AuthorModel.query.all()
        return {'authors':list(author.json() for author in authors)}
 
    def post(self):
        data = request.get_json()
        author = AuthorModel(data['last_name'], data['first_name'])
        db.session.add(author)
        db.session.commit()
        return author.json(), 201
 
 
class AuthorView(Resource):
  
    def get(self, id):
        author = AuthorModel.query.filter_by(id=id).first()
        if author:
            return author.json()
        return {'msg':'Author not found.'}, 404

    def put(self, id):
        data = request.get_json()
        author = AuthorModel.query.filter_by(id=id).first() 
        if author:
            author.last_name = data["last_name"]
            author.first_name = data["first_name"]
        else:
            author = AuthorModel(last_name=last_name, first_name=first_name, **data)
 
        db.session.add(author)
        db.session.commit()
 
        return author.json()
 
    def delete(self, id):
        author = AuthorModel.query.filter_by(id=id).first()
        if author:
            db.session.delete(author)
            db.session.commit()
            return {'msg':'Deleted'}
        else:
            return {'msg': 'Author not found.'}, 404
