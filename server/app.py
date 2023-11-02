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

class BookResource(Resource):
    @marshal_with(book_fields)
    def post(self):
        data = request.form
        new_book = Book(
            Title=data['Title'],
            Author=data['Author'],
            Genre=data['Genre'],
            Description=data['Description'],
            Price=data['Price']
        )
        db.session.add(new_book)
        db.session.commit()
        return new_book

    @marshal_with(book_fields)
    def get(self, id=None):
        if id is not None:
            # Get a single book by ID
            book = Book.query.get(id)
            if book is not None:
                return book
            else:
                return {'message': 'Book not found'}, 404
        else:
            # Get all books
            books = Book.query.all()
            return books

    @marshal_with(book_fields)
    def put(self, id):
        book = Book.query.get(id)
        if book is not None:
            try:
                data = request.form
                book.Title = data['Title']
                book.Author = data['Author']
                book.Genre = data['Genre']
                book.Description = data['Description']
                book.Price = data['Price']
                db.session.commit()
                return book
            except Exception as e:
            # Log the error for debugging
                print(f"Error updating book: {str(e)}")
            return {'message': 'Internal Server Error'}, 500
        return {'message': 'Book not found'}, 404


    def delete(self, id):
        book = Book.query.get(id)
        if book is not None:
            db.session.delete(book)
            db.session.commit()
            return {'message': 'Book deleted successfully'}, 204
        
class UserResource(Resource):
    def get(self, id=None):
        if id is None:
            # Get all users
            users = User.query.all()
            user_list = [user.to_dict() for user in users]  # Use the to_dict method
            return user_list
        else:
            # Get a user by ID
            user = User.query.get(id)
            if user is not None:
                return user.to_dict()  # Use the to_dict method
            return {'message': 'User not found'}, 404
        
  
    def post(self): 
        username = request.form.get('Username')
        Password = request.form.get('Password')
        Email = request.form.get('Email')
        Full_Name = request.form.get('Full_Name')

    # if not (username and Password and Email and Full_Name):
    #     return {'message': 'Missing form data'}, 400

        new_user = User(
            Username=username,
            Password=Password,
            Email=Email,
            Full_Name=Full_Name
        )
        db.session.add(new_user)
        db.session.commit()

        return new_user.to_dict(), 201
    def put(self, id):
        user = User.query.get(id)
        if user is not None:
           try:
            # Use request.form to access form data
               username = request.form.get('Username')
               password = request.form.get('Password')
               email = request.form.get('Email')
               full_name = request.form.get('Full_Name')

               if username:
                user.Username = username
               if password:
                user.Password = password
               if email:
                user.Email = email
               if full_name:
                user.Full_Name = full_name

               db.session.commit()
               return {'message': 'User updated successfully'}
           except Exception as e:
            # Log the error for debugging
               print(f"Error updating user: {str(e)}")
               return {'message': 'Internal Server Error'}, 500
        return {'message': 'User not found'}, 404

    def delete(self, id):
        user = User.query.get(id)
        if user is not None:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted successfully'}
        return {'message': 'User not found'}, 404


cart_fields = {
    'UserID': fields.Integer,
    'AdminID': fields.Integer,
    'Status': fields.String,
}

class CartResource(Resource):
    def get(self, id=None):
        if id is None:
            # Get all carts
            carts = Cart.query.all()
            cart_list = [cart.to_dict() for cart in carts]
            return cart_list
        else:
            # Get a cart by ID
            cart = Cart.query.get(id)
            if cart is not None:
                return cart.to_dict()
            return {'message': 'Cart not found'}, 404

    def post(self):
        UserID = request.form.get('UserID')
        AdminID = request.form.get('AdminID')
        Status = request.form.get('Status')

        if not (UserID and AdminID and Status):
            return {'message': 'Missing form data'}, 400

        new_cart = Cart(
            UserID=UserID,
            AdminID=AdminID,
            Status=Status
        )
        db.session.add(new_cart)
        db.session.commit()
        return new_cart.to_dict(), 201

    def put(self, id):
        cart = Cart.query.get(id)
        if cart is not None:
            UserID = request.form.get('UserID')
            AdminID = request.form.get('AdminID')
            Status = request.form.get('Status')

            if UserID:
                cart.UserID = UserID
            if AdminID:
                cart.AdminID = AdminID
            if Status:
                cart.Status = Status

            db.session.commit()
            return {'message': 'Cart updated successfully'}

    def delete(self, id):
        cart = Cart.query.get(id)
        if cart is not None:
            db.session.delete(cart)
            db.session.commit()
            return {'message': 'Cart deleted successfully'}
        return {'message': 'Cart not found'}, 404
    
class CartItemResource(Resource):
    def get(self, id=None):
        if id is None:
            # Get all cart items
            cart_items = CartItem.query.all()
            cart_item_list = [cart_item.to_dict() for cart_item in cart_items]
            return cart_item_list
        else:
            # Get a cart item by ID
            cart_item = CartItem.query.get(id)
            if cart_item is not None:
                return cart_item.to_dict()
            return {'message': 'Cart item not found'}, 404

    def post(self):
        CartID = request.form.get('CartID')
        BookID = request.form.get('BookID')
        Quantity = request.form.get('Quantity')

        if not (CartID and BookID and Quantity):
            return {'message': 'Missing form data'}, 400

        new_cart_item = CartItem(
            CartID=CartID,
            BookID=BookID,
            Quantity=Quantity
        )
        db.session.add(new_cart_item)
        db.session.commit()
        return new_cart_item.to_dict(), 201

    def put(self, id):
        cart_item = CartItem.query.get(id)
        if cart_item is not None:
            CartID = request.form.get('CartID')
            BookID = request.form.get('BookID')
            Quantity = request.form.get('Quantity')

            if CartID:
                cart_item.CartID = CartID
            if BookID:
                cart_item.BookID = BookID
            if Quantity:
                cart_item.Quantity = Quantity

            db.session.commit()
            return {'message': 'Cart item updated successfully'}

    def delete(self, id):
        cart_item = CartItem.query.get(id)
        if cart_item is not None:
            db.session.delete(cart_item)
            db.session.commit()
            return {'message': 'Cart item deleted successfully'}
        return {'message': 'Cart item not found'}, 404

class PurchaseResource(Resource):
    def get(self, id=None):
        if id is None:
            purchases = Purchase.query.all()
            purchase_list = [purchase.to_dict() for purchase in purchases]
            return purchase_list
        else:
            purchase = Purchase.query.get(id)
            if purchase is not None:
                return purchase.to_dict()
            return {'message': 'Purchase not found'}, 404

    def post(self):
        UserID = request.form.get('UserID')
        AdminID = request.form.get('AdminID')
        OrderID = request.form.get('OrderID')
        Total_Amount = request.form.get('Total_Amount')


        if not (UserID and AdminID and OrderID and Total_Amount ):
            return {'message': 'Missing form data'}, 400

        new_purchase = Purchase(
            UserID=UserID,
            AdminID=AdminID,
            OrderID=OrderID,
            Total_Amount=Total_Amount
        )
        db.session.add(new_purchase)
        db.session.commit()
        return new_purchase.to_dict(), 201

    def put(self, id):
        purchase = Purchase.query.get(id)
        if purchase is not None:
            UserID = request.form.get('UserID')
            AdminID = request.form.get('AdminID')
            OrderID = request.form.get('OrderID')
            Total_Amount = request.form.get('Total_Amount')
            Purchase_Date = request.form.get('Purchase_Date')

            if UserID:
                purchase.UserID = UserID
            if AdminID:
                purchase.AdminID = AdminID
            if OrderID:
                purchase.OrderID = OrderID
            if Total_Amount:
                purchase.Total_Amount = Total_Amount
            if Purchase_Date:
                purchase.Purchase_Date = Purchase_Date

            db.session.commit()
            return {'message': 'Purchase updated successfully'}

    def delete(self, id):
        purchase = Purchase.query.get(id)
        if purchase is not None:
            db.session.delete(purchase)
            db.session.commit()
            return {'message': 'Purchase deleted successfully'}
        return {'message': 'Purchase not found'}, 404
    
class ReturnRequestResource(Resource):
    def get(self, id=None):
        if id is None:
            # Get all return requests
            return_requests = ReturnRequest.query.all()
            request_list = [request.to_dict() for request in return_requests]
            return request_list
        else:
            # Get a return request by ID
            return_request = ReturnRequest.query.get(id)
            if return_request is not None:
                return return_request.to_dict()
            return {'message': 'Return request not found'}, 404

    def post(self):
        UserID = request.form.get('UserID')
        AdminID = request.form.get('AdminID')
        OrderID = request.form.get('OrderID')
        Return_Reason = request.form.get('Return_Reason')
        Status = request.form.get('Status')

        if not (UserID and AdminID and OrderID and Return_Reason and Status):
            return {'message': 'Missing form data'}, 400

        new_request = ReturnRequest(
            UserID=UserID,
            AdminID=AdminID,
            OrderID=OrderID,
            Return_Reason=Return_Reason,
            Status=Status
        )
        db.session.add(new_request)
        db.session.commit()
        return new_request.to_dict(), 201
    
    def put(self, id):
        return_request = ReturnRequest.query.get(id)
        if return_request is not None:
            UserID = request.form.get('UserID')
            AdminID = request.form.get('AdminID')
            OrderID = request.form.get('OrderID')
            Return_Reason = request.form.get('Return_Reason')
            Status = request.form.get('Status')

            if UserID:
                return_request.UserID = UserID
            if AdminID:
                return_request.AdminID = AdminID
            if OrderID:
                return_request.OrderID = OrderID
            if Return_Reason:
                return_request.Return_Reason = Return_Reason
            if Status:
                return_request.Status = Status

            db.session.commit()
            return {'message': 'Return request updated successfully'}

    def delete(self, id):
        return_request = ReturnRequest.query.get(id)
        if return_request is not None:
            db.session.delete(return_request)
            db.session.commit()
            return {'message': 'Return request deleted successfully'}
        return {'message': 'Return request not found'}, 404

class LoginResource(Resource):
    def post(self):
        data = request.get_json(force=True)
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return {"message": "Missing username or password"}, 400

        user = User.query.filter_by(Username=username, Password=password).first()

        if user:
            access_token = create_access_token(identity=username)
            return jsonify({"access_token": access_token}), 200
        else:
            return {"message": "Invalid username or password"}, 401

class RegistrationResource(Resource):
   def post(self):
        data = request.get_json()
        username = data.get('Username')
        password = data.get('Password')
        Email = data.get('Email')
        Full_Name = data.get('Full_Name')

        if not username or not password:
            return {"message": "Missing username or password"}, 400
        
        user = User.query.filter_by(Username=username).first()

        if user:
            return {"message": "User already exists"}, 400

        new_user = User(Username=username, Password=password, Email=Email, Full_Name=Full_Name)
        db.session.add(new_user)
        db.session.commit()

        return {"message": "User created successfully"}, 201
    
class Home(Resource):
    def get(self):
        response_dict = {
            "Hello": "Welcome to LitHaven Api. The comprehensive API for Booklovers",
        }
        response = make_response(jsonify(response_dict), 200)

        return response

api.add_resource(LoginResource, '/login')
api.add_resource(RegistrationResource, '/register')
api.add_resource(ReturnRequestResource, '/returnrequests', '/returnrequests/<int:id>')
api.add_resource(PurchaseResource, '/purchases', '/purchases/<int:id>')
api.add_resource(CartItemResource, '/cartitems', '/cartitems/<int:id>')
api.add_resource(CartResource, '/carts', '/carts/<int:id>')
api.add_resource(UserResource, '/users', '/users/<int:id>')
# api.add_resource(AdminResource, '/admins', '/admins/<int:id>')
# api.add_resource(BookResource, '/books', '/books/<int:id>')
api.add_resource(AdminResource, '/admins', '/admins/<int:id>')
api.add_resource(BookResource, '/books', '/books/<int:id>')


if __name__ == '_main_':
    app.debug = True
    app.run(debug=False)