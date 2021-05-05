from flask import request
from flask_restful import Resource
from bookstore.models import db, CategoryModel


class CategoriesView(Resource):
 
    def get(self):
        categories = CategoryModel.query.all()
        return {'categories':list(category.json() for category in categories)}
 
    def post(self):
        data = request.get_json()
        category = CategoryModel(data['name'])
        db.session.add(category)
        db.session.commit()
        return category.json(), 201
 
 
class CategoryView(Resource):
  
    def get(self, id):
        category = CategoryModel.query.filter_by(id=id).first()
        if category:
            return category.json()
        return {'msg':'Category not found.'}, 404

    def put(self, id):
        data = request.get_json()
        category = CategoryModel.query.filter_by(id=id).first() 
        if category:
            category.name = data["name"]
        else:
            category = CategoryModel(name=name,**data)
 
        db.session.add(category)
        db.session.commit()
 
        return category.json()
 
    def delete(self, id):
        category = CategoryModel.query.filter_by(id=id).first()
        if category:
            db.session.delete(category)
            db.session.commit()
            return {'msg':'Deleted'}
        else:
            return {'msg': 'Category not found.'}, 404
