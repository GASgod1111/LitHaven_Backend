from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource, fields, marshal_with
from Models import db, Admin, Book, User, Cart, CartItem, Purchase, ReturnRequest
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['JWT_SECRET_KEY'] = 'a&Tn7Rc`,6^8R/<Xqg0w"u[:S\9OIbk5' 
migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)
jwt = JWTManager(app)

# Define resource fields for marshaling
admin_fields = {
    'AdminID': fields.Integer,
    'Username': fields.String,
    'Password': fields.String,
    'Email': fields.String,
    'Full_Name': fields.String,
}

book_fields = {
    'BookID': fields.Integer,
    'Title': fields.String,
    'Author': fields.String,
    'Genre': fields.String,
    'Description': fields.String,
    'Price': fields.Float
}

# Define resource classes for each model
class AdminResource(Resource):
    @marshal_with(admin_fields)
    def post(self):
        data = request.form
        new_admin = Admin(Username=data['Username'], Password=data['Password'], Email=data['Email'], Full_Name=data['Full_Name'])
        db.session.add(new_admin)
        db.session.commit()
        return new_admin

    @marshal_with(admin_fields)
    def get(self):
        admins = Admin.query.all()
        return admins

    @marshal_with(admin_fields)
    def put(self, id):
        admin = Admin.query.get(id)
        if admin is not None:
            data = request.form
            admin.Username = data['Username']
            admin.Password = data['Password']
            admin.Email = data['Email']
            admin.Full_Name = data['Full_Name']
            db.session.commit()
            return admin

    def delete(self, id):
        admin = Admin.query.get(id)
        if admin is not None:
            db.session.delete(admin)
            db.session.commit()
            return {'message': 'Admin deleted successfully'}, 204


api.add_resource(AdminResource, '/admins', '/admins/<int:id>')
api.add_resource(BookResource, '/books', '/books/<int:id>')


if __name__ == '_main_':
    app.debug = True
    app.run(debug=False)