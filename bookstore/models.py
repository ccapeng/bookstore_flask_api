from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, Column
import any_case


db = SQLAlchemy()

class CategoryModel(db.Model):
    __tablename__ = 'category'
 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
 
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Category('{self.name}')"

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

    def __repr__(self):
        return f"Publisher('{self.name}')"

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

    def __repr__(self):
        return f"Author('{self.last_name}', '{self.first_name}')"

    @classmethod
    def parse(cls, obj):
        obj = any_case.converts_keys(obj, case='snake')
        return cls(obj.get("last_name"), obj.get("first_name"))

    def update(self, data):
        data = any_case.converts_keys(data, case='snake')
        self.last_name = data.get("last_name")
        self.first_name = data.get("first_name")

    __id = "id"
    __last_name = "lastName"
    __first_name = "firstName"
    def json(self):
        return {
            self.__id: self.id,
            self.__last_name: self.last_name,
            self.__first_name: self.first_name
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

    def __repr__(self):
        return f"Book('{self.title}')"

    @classmethod
    def parse(cls, obj):
        obj = any_case.converts_keys(obj, case='snake')
        return cls(
            obj.get("title"),
            obj.get("category_id"),
            obj.get("publisher_id"),
            obj.get("author_id")
        )

    def update(self, obj):
        obj = any_case.converts_keys(obj, case='snake')
        self.title = obj.get("title")
        self.category_id = obj.get("category_id", None)
        self.publisher_id = obj.get("publisher_id", None)
        self.author_id = obj.get("author_id", None)

    __id = "id"
    __title = "title"
    __category_id = "categoryId"
    __publisher_id = "publisherId"
    __author_id = "authorId"
    __category = "category"
    __publisher = "publisher"
    __author = "author"
    __name = "name"
    __last_name = "lastName"
    __first_name = "firstName"

    def json(self):
        return {
            self.__id: self.id,
            self.__title: self.title, 
            self.__category_id: self.category_id, 
            self.__publisher_id: self.publisher_id,
            self.__author_id: self.author_id,
        }

    def detail_json(self):
        return {
            self.__id: self.id,
            self.__title: self.title, 
            self.__category_id: self.category_id, 
            self.__publisher_id: self.publisher_id,
            self.__author_id: self.author_id,
            self.__category: self.category.json(),
            self.__publisher: self.publisher.json(),
            self.__author: self.author.json()
        }

    @staticmethod
    def detail_join_json(obj):
        return {
            BookModel.__id: obj.id,
            BookModel.__title: obj.title, 
            BookModel.__category_id: obj.category_id, 
            BookModel.__category: {
                BookModel.__id:  obj.category_id, 
                BookModel.__name: obj.category_name
            },
            BookModel.__publisher_id: obj.publisher_id,
            BookModel.__publisher: {
                BookModel.__id: obj.publisher_id,
                BookModel.__name: obj.publisher_name
            },
            BookModel.__author_id: obj.author_id,
            BookModel.__author:{
                BookModel.__id:  obj.author_id,
                BookModel.__last_name: obj.author_last_name, 
                BookModel.__first_name: obj.author_first_name, 
            }

        }
