from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)


class Home(Resource):
    def get(self):
        return ('Welcome to LitHaven Api. The comprehensive API for Booklovers')
    

class BooksList(Resource):
    # to retrieve all books
    def get(self):
        # return books
        pass

class BooksById(Resource):
    # to retrieve books by id
    def get(self, book_id):
        # return books[book_id: books[book_id]]
        pass



    
    

api.add_resource(Home, '/')


if __name__ == '__main__':
    app.run(debug=True)

