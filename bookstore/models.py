from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, Column
 

db = SQLAlchemy()
 

class CategoryModel(db.Model):
    __tablename__ = 'category'
 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
 
    def __init__(self, name):
        self.name = name
     
    def json(self):
        return {
            "id": self.id,
            "name": self.name
        }


class PublisherModel(db.Model):
    __tablename__ = 'publisher'
 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
 
    def __init__(self, name):
        self.name = name
     
    def json(self):
        return {
            "id": self.id,
            "name": self.name
        }


class AuthorModel(db.Model):
    __tablename__ = 'author'
 
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(32))
    first_name = db.Column(db.String(32))
 
    def __init__(self, last_name, first_name):
        self.last_name = last_name
        self.first_name = first_name
     
    def json(self):
        return {
            "id": self.id,
            "last_name": self.last_name,
            "first_name": self.first_name
        }



class BookModel(db.Model):
    __tablename__ = 'book'
 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    category_id = Column(
        db.Integer,
        ForeignKey("category.id"),
        nullable=True,
    )
    publisher_id = db.Column(
        db.Integer,
        ForeignKey("publisher.id"),
        nullable=True,
    ) 
    author_id = db.Column(
        db.Integer,
        ForeignKey("author.id"),
        nullable=True,
    )

    category = relationship('CategoryModel')
    publisher = relationship('PublisherModel')
    author = relationship('AuthorModel')
 
    def __init__(self, title, category_id, publisher_id, author_id):
        self.title = title
        self.category_id = category_id
        self.publisher_id = publisher_id 
        self.author_id = author_id 
     
    def json(self):
        return {
            "id": self.id,
            "title": self.title, 
            "category_id": self.category_id, 
            "publisher_id": self.publisher_id,
            "author_id": self.author_id,
        }
