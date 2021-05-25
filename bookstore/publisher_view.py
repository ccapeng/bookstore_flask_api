from flask import request
from flask_restful import Resource
from bookstore.models import db, PublisherModel


class PublishersView(Resource):
 
    def get(self):
        Publishers = PublisherModel.query.all()
        return list(publisher.json() for publisher in Publishers)
 
    def post(self):
        data = request.get_json()
        # publisher = PublisherModel(data['name'])
        publisher = PublisherModel.parse(data)
        db.session.add(publisher)
        db.session.commit()
        return publisher.json(), 201
 
 
class PublisherView(Resource):
  
    def get(self, id):
        publisher = PublisherModel.query.filter_by(id=id).first()
        if publisher:
            return publisher.json()
        return {'msg':'Publisher not found.'}, 404

    def put(self, id):
        data = request.get_json()
        publisher = PublisherModel.query.filter_by(id=id).first() 
        if publisher:
            publisher.name = data["name"] 
            db.session.add(publisher)
            db.session.commit()
 
        return publisher.json()
 
    def delete(self, id):
        publisher = PublisherModel.query.filter_by(id=id).first()
        if publisher:
            db.session.delete(publisher)
            db.session.commit()
            return {'msg':'Deleted'}
        else:
            return {'msg': 'Publisher not found.'}, 404
