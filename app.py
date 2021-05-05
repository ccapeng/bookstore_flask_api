from flask import Flask, request
from flask_restful import Api
#from flask_cors import CORS

from bookstore.models import db
from bookstore.category_view import CategoriesView, CategoryView
from bookstore.publisher_view import PublishersView, PublisherView
from bookstore.author_view import AuthorsView, AuthorView
from bookstore.book_view import BooksView, BookView


app = Flask(__name__)
#CORS(app)
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
api = Api(app)
db.init_app(app)
 
@app.before_first_request
def create_table():
    db.create_all()
 
@app.after_request
def after_request(response):
    print("after_request")
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header["Access-Control-Allow-Headers"] = '*'
    header["Access-Control-Allow-Methods"] = '*'
    return response


api.add_resource(CategoriesView, '/api/categories')
api.add_resource(CategoryView, '/api/categories/<int:id>')
api.add_resource(PublishersView, '/api/publishers')
api.add_resource(PublisherView, '/api/publishers/<int:id>')
api.add_resource(AuthorsView, '/api/authors')
api.add_resource(AuthorView, '/api/authors/<int:id>')
api.add_resource(BooksView, '/api/books')
api.add_resource(BookView, '/api/books/<int:id>')


app.debug = True
if __name__ == '__main__':
    app.run(host='localhost', port=8081)