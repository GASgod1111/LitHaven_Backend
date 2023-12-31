import bcrypt
from flask import Flask, jsonify, request, make_response, session
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from Models import db, Admin, Book, BookLendingRequest, BookOrder, User, Cart, CartItem, Purchase, ReturnRequest
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from serializer import book_response_serializer, book_price_serializer, book_genre_serializer, book_title_serializer, book_purchase_serializer, book_lending_serializer, book_return_request_serializer, user_serializer, cart_serializer, cart_item_serializer, book_order_serializer, admin_serializer, book_date_uploaded_serializer
from datetime import datetime
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import requests
import base64
import datetime
from requests.auth import HTTPBasicAuth
import africastalking
import bcrypt
from cryptography.fernet import  Fernet
from fpdf import FPDF
import re


class CaseInsensitiveApi(Api):
    def url_for(self, resource, **values):
        target = resource.endpoint
        for rule in self.app.url_map.iter_rules():
            if target == rule.endpoint:
                for arg in rule.arguments:
                    if arg in values:
                        values[arg] = values[arg].lower()
                if "path" in values:
                    values["path"] = values["path"].lower()
        return super(CaseInsensitiveApi, self).url_for(resource, **values)

app = Flask(__name__)
api = CaseInsensitiveApi(app) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'  # Replace with your actual database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '9f36bc095fbf40bbb94d9938bcac8847'

migrate = Migrate(app, db)
api = Api(app)
CORS(app)
db.init_app(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()


class Home(Resource):
    def get(self):
        response_dict = {
            "Hello": "Welcome to LitHaven Api. The comprehensive API for Booklovers",
        }
        response = make_response(jsonify(response_dict), 200)

        return response

class BooksList(Resource):
    # to retrieve all books
    def get(self):
        books = Book.query.all()
        response = book_response_serializer(books)
        return make_response(jsonify(response), 200)

    def post(self):
        data = request.get_json()
        new_book = Book(
            Book_Image= data.get("Book_Image"),
            Title=data.get("Title"),
            Author=data.get("Author"),
            Genre=data.get("Genre"),
            Description=data.get("Title"),
            Price=data.get("Price"),
            Date_Uploaded=data.get("Date_Uploaded"),
        )

        db.session.add(new_book)
        db.session.commit()

        new_book_dict = {
            "id": new_book.BookID,
            "Book_Image": new_book.Book_Image,
            "title": new_book.Title,
            "author": new_book.Author,
            "genre": new_book.Genre,
            "description": new_book.Description,
            "price": new_book.Price,
            "date_uploaded": new_book.Date_Uploaded,
        }

        return make_response(jsonify(new_book_dict), 200)

# user to view all books
class UserBooksList(Resource):
    # to retrieve all books
    def get(self):
        books = Book.query.all()
        response = book_response_serializer(books)
        return make_response(jsonify(response), 200)

class AdminBooksList(Resource):
    # to retrieve all books
    def get(self):
        books = Book.query.all()
        response = book_response_serializer(books)
        return make_response(jsonify(response), 200)

    def post(self):
        data = request.get_json()
        new_book = Book(
            Book_Image= data.get("Book_Image"),
            Title=data.get("Title"),
            Author=data.get("Author"),
            Genre=data.get("Genre"),
            Description=data.get("Title"),
            Price=data.get("Price"),
            Date_Uploaded=data.get("Date_Uploaded"),
        )

        db.session.add(new_book)
        db.session.commit()

        new_book_dict = {
            "id": new_book.BookID,
            "Book_Image": new_book.Book_Image,
            "title": new_book.Title,
            "author": new_book.Author,
            "genre": new_book.Genre,
            "description": new_book.Description,
            "price": new_book.Price,
            "date_uploaded": new_book.Date_Uploaded,
        }

        return make_response(jsonify(new_book_dict), 200)

class BookById(Resource):
    
    # to retrieve books by id
    def get(self, BookID):

        # print(BookID, 'BookId')
        book = Book.query.filter_by(BookID=BookID).first()
        # print(book, 'book obj')
        if book:
            book_dict = {
                "BookID": book.BookID,
                "Book_Image": book.Book_Image,
                "Title": book.Title,
                "Author": book.Author,
                "Genre": book.Genre, 
                "Description": book.Description,
                "Price": book.Price,
                "Date_Uploaded": book.Date_Uploaded
            }

            return make_response(jsonify(book_dict), 200)

        else:
            return make_response(jsonify({"error": "Book not found"}), 404)

    def patch(self, BookID):
        book = Book.query.filter_by(BookID=BookID).first()
        if book:
            for attr in request.get_json():
                setattr(book, attr, request.get_json()[attr])

        db.session.add(book)
        db.session.commit()

        book_dict = {
            "BookID": book.BookID,
            "Book_Image": book.Book_Image,
            "title": book.Title,
            "author": book.Author,
            "genre": book.Genre,
            "description": book.Description,
            "price": book.Price,
            "date_uploaded": book.Date_Uploaded,
        }

        response = make_response(jsonify(book_dict), 200)

        return response
    
    def delete(self, BookID):
        book = Book.query.filter_by(BookID=BookID).first()

        db.session.delete(book)
        db.session.commit()

        response_dict = {"message": "book successfully deleted"}

        response = make_response(
            jsonify(response_dict),
            200
        )

        return response

# admin crud operations
class AdminBookById(Resource):
    
    # to retrieve books by id
    def get(self, BookID):

        # print(BookID, 'BookId')
        book = Book.query.filter_by(BookID=BookID).first()
        # print(book, 'book obj')
        if book:
            book_dict = {
                "BookID": book.BookID,
                "Book_Image": book.Book_Image,
                "Title": book.Title,
                "Author": book.Author,
                "Genre": book.Genre, 
                "Description": book.Description,
                "Price": book.Price,
                "Date_Uploaded": book.Date_Uploaded
            }

            return make_response(jsonify(book_dict), 200)

        else:
            return make_response(jsonify({"error": "Book not found"}), 404)

    def patch(self, BookID):
        book = Book.query.filter_by(BookID=BookID).first()
        if book:
            for attr in request.get_json():
                setattr(book, attr, request.get_json()[attr])

        db.session.add(book)
        db.session.commit()

        book_dict = {
            "BookID": book.BookID,
            "Book_Image": book.Book_Image,
            "title": book.Title,
            "author": book.Author,
            "genre": book.Genre,
            "description": book.Description,
            "price": book.Price,
            "date_uploaded": book.Date_Uploaded,
        }

        response = make_response(jsonify(book_dict), 200)

        return response
    
    def delete(self, BookID):
        book = Book.query.filter_by(BookID=BookID).first()

        db.session.delete(book)
        db.session.commit()

        response_dict = {"message": "book successfully deleted"}

        response = make_response(
            jsonify(response_dict),
            200
        )

        return response
    
# user to search for books by title
class UsersBookByTitle(Resource):
    # to retrieve books by Title
     def get(self, Title):
        books = Book.query.filter_by(Title=Title).all()

        if books:
            response = book_title_serializer(books)
            return make_response(jsonify(response), 200)
        else:
            return make_response(jsonify({"error": "Book not found"}), 404)
     
# user to search for books by genre
class UsersBookByGenre(Resource):
    # to retrieve books by Genre
    def get(self, Genre):
        books = Book.query.filter_by(Genre=Genre).all()

        if books:
            response = book_genre_serializer(books)
            return make_response(jsonify(response), 200)
        else:
            return make_response(jsonify({"error": "Genre not found"}), 404)
        
# user to search for books by price  
class UsersBookByPrice(Resource):
    # to retrieve books by Price
    def get(self, Price):
        books = Book.query.filter_by(Price=Price).all()

        if books:
            response = book_price_serializer(books)
            return make_response(jsonify(response), 200)
        else:
            return make_response(jsonify({"error": "Book not found"}), 404)
    
# *** Not working 
class BookByDateUploaded(Resource):
     # to retrieve books by date_uploaded
    def get(self, Date_Uploaded):
        date_obj = datetime.strptime(Date_Uploaded, '%Y-%m-%d').date()
        books = Book.query.filter_by(Date_Uploaded=date_obj).all()

        if books:
            response = book_date_uploaded_serializer(books)
            return make_response(jsonify(response), 200)
        else:
            return make_response(jsonify({"error": "Book not found"}), 404)
    
    
    # ***not working yet
    # to retrieve books by Date upladed
    # def get(self, date):
    #     date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    #     books = Book.query.filter_by(Date_Uploaded=date_obj).all()
    #     for book in books:
    #         book_dict = {
    #             "BookID": book.BookID,
    #             "Title": book.Title,
    #             "Author": book.Author,
    #             "Genre": book.Genre, 
    #             "Description": book.Description,
    #             "Price": book.Price,
    #             "Date_Uploaded": book.Date_Uploaded
    #         }

    #         return make_response(jsonify(book_dict), 200)

    #     else:
    #         return make_response(jsonify({"error": "Book not found"}), 404)

class UsersList(Resource):
     # to retrieve all users
    def get(self):
        users = User.query.all()
        response = user_serializer(users)
        return make_response(jsonify(response), 200)

    def post(self):
        data = request.get_json()
        new_user = User(
            UserID=data.get("UserID"),
            Username=data.get("Username"),
            Password=data.get("Password"),
            Email=data.get("Email"),
            Full_Name=data.get("Full_Name"),
            Phone_Number=data.get("Phone_Number")
        )

        db.session.add(new_user)
        db.session.commit()

        new_user_dict = {
            "UserID": new_user.UserID,
            "Username": new_user.Username,
            "Password": new_user.Password,
            "Email": new_user.Email,
            "Full_Name": new_user.Full_Name,
            "Phone_Number": new_user.Phone_Number
        }

        return make_response(jsonify(new_user_dict), 200)


class UserById(Resource):
    def get(self, UserID):

        user = User.query.filter_by(UserID=UserID).first()
       
        if user:
            user_dict = {
            "UserID": user.UserID,
             "Username": user.Username,
             "Password": user.Password,
             "Email": user.Email,
             "Full_Name": user.Full_Name,
             "Phone_Number": user.Phone_Number
            }

            return make_response(jsonify(user_dict), 200)

        else:
            return make_response(jsonify({"error": "User not found"}), 404)


    def patch(self, UserID):
        user = User.query.filter_by(UserID=UserID).first()
        if user:
            for attr in request.get_json():
                setattr(user, attr, request.get_json()[attr])

        db.session.add(user)
        db.session.commit()

        user_dict = {
            "UserID": user.UserID,
             "Username": user.Username,
             "Password": user.Password,
             "Email": user.Email,
             "Full_Name": user.Full_Name,
             "Phone_Number": user.Phone_Number
            }
 
        response = make_response(jsonify(user_dict), 200)

        return response
    
    def delete(self, UserID):
        user = User.query.filter_by(UserID=UserID).first()

        db.session.delete(user)
        db.session.commit()

        response_dict = {"message": "User successfully deleted"}

        response = make_response(
            jsonify(response_dict),
            200
        )

        return response

class PreviousPurchasesLendings(Resource):
    def get(self, UserID):
        user = User.query.get(UserID)
        if not user:
            return {'message': 'User not found'}, 404

        purchases = Purchase.query.filter_by(UserID=UserID).all()
        respose_purchases = book_purchase_serializer(purchases)

        lendings = BookLendingRequest.query.filter_by(UserID=UserID).all()
        response_lendings = book_lending_serializer(lendings)

        # serialized_purchases = [purchase.to_dict() for purchase in purchases]
        # serialized_lendings = [lending.to_dict() for lending in lendings]

        return {
            'purchases': respose_purchases,
            'lendings': response_lendings
        }, 200

class PurchasesList(Resource):
    # to retrieve a list of all purchases
    def get(self):
        book_purchases = Purchase.query.all()
        response = book_purchase_serializer(book_purchases)
        return make_response(jsonify(response), 200)

    def post(self):
        data = request.get_json()
        new_purchase = Purchase(
            PurchaseID=data.get("PurchaseID"),
            UserID=data.get("UserID"),
            AdminID=data.get("AdminID"),
            OrderID=data.get("OrderID"),
            Total_Amount=data.get("Total_Amount"),
            Purchase_Date=data.get("Purchase_Date")
        )
        db.session.add(new_purchase)
        db.session.commit()

        new_purchase_dict = {
            "PurchaseID": new_purchase.PurchaseID,
            "UserID": new_purchase.UserID,
            "AdminID": new_purchase.AdminID,
            "OrderID": new_purchase.OrderID,
            "Total_Amount": new_purchase.Total_Amount,
            "Purchase_Date": new_purchase.Purchase_Date
        }

        return make_response(jsonify(new_purchase_dict), 200)

class PurchaseById(Resource):
    # to retrieve book purchases by id
    def get(self, PurchaseID):

        purchase = Purchase.query.filter_by(PurchaseID=PurchaseID).first()
        
        if purchase:
            purchase_dict = {
                "PurchaseID": purchase.PurchaseID,
                "UserID": purchase.UserID,
                "AdminID": purchase.AdminID,
                "OrderID": purchase.OrderID, 
                "Total_Amount": purchase.Total_Amount,
                "Purchase_Date": purchase.Purchase_Date
                
            }

            return make_response(jsonify(purchase_dict), 200)

        else:
            return make_response(jsonify({"error": "Purchase details not found"}), 404)

    def patch(self, PurchaseID):
        purchase = Purchase.query.filter_by(PurchaseID=PurchaseID).first()
        if  purchase:
            for attr in request.get_json():
                setattr(purchase, attr, request.get_json()[attr])

        db.session.add(purchase)
        db.session.commit()

        purchase_dict = {
                "PurchaseID": purchase.PurchaseID,
                "UserID": purchase.UserID,
                "AdminID": purchase.AdminID,
                "OrderID": purchase.OrderID, 
                "Total_Amount": purchase.Total_Amount,
                "Purchase_Date": purchase.Purchase_Date
                
            }

        response = make_response(jsonify(purchase_dict), 200)

        return response
    
    def delete(self, PurchaseID):
        purchase = Purchase.query.filter_by(PurchaseID=PurchaseID).first()

        db.session.delete(purchase)
        db.session.commit()

        response_dict = {"message": "Purchase details successfully deleted"}

        response = make_response(
            jsonify(response_dict),
            200
        )

        return response


class BookLendingsList(Resource):
    # to retrieve a list of all purchases
    def get(self):
        book_lendings = BookLendingRequest.query.all()
        response = book_lending_serializer(book_lendings)
        return make_response(jsonify(response), 200)

    def post(self):
        data = request.get_json()
        new_lending = BookLendingRequest(
            RequestID=data.get("RequestID"),
            UserID=data.get("UserID"),
            AdminID=data.get("AdminID"),
            BookID=data.get("BookID"),
            Status=data.get("Status")
        )
        db.session.add(new_lending)
        db.session.commit()

        new_lending_dict = {
            "RequestID": new_lending.RequestID,
            "UserID": new_lending.UserID,
            "AdminID": new_lending.AdminID,
            "BookID": new_lending.BookID,
            "Status": new_lending.Status,
        }
        return make_response(jsonify(new_lending_dict), 200)
    
class BookLendingById(Resource):
     # to retrieve book lending by id
    def get(self, RequestID):

        lending = BookLendingRequest.query.filter_by(RequestID=RequestID).first()
        
        if lending:
            lending_dict = {
            "RequestID": lending.RequestID,
            "UserID": lending.UserID,
            "AdminID": lending.AdminID,
            "BookID": lending.BookID,
            "Status": lending.Status
                
            }

            return make_response(jsonify(lending_dict), 200)

        else:
            return make_response(jsonify({"error": "Lending details not found"}), 404)

    def patch(self, RequestID):
        lending = BookLendingRequest.query.filter_by(RequestID=RequestID).first()
        if  lending:
            for attr in request.get_json():
                setattr(lending, attr, request.get_json()[attr])

        db.session.add(lending)
        db.session.commit()

        lending_dict = {
            "RequestID": lending.RequestID,
            "UserID": lending.UserID,
            "AdminID": lending.AdminID,
            "BookID": lending.BookID,
            "Status": lending.Status
            }

        response = make_response(jsonify(lending_dict), 200)

        return response
    
    def delete(self, RequestID):
        lending = BookLendingRequest.query.filter_by(RequestID=RequestID).first()

        db.session.delete(lending)
        db.session.commit()

        response_dict = {"message": "Lending details successfully deleted"}

        response = make_response(
            jsonify(response_dict),
            200
        )

        return response
    
class ReturnRequestManagement(Resource):
    def post(self, UserID):
        data = request.get_json()
        OrderID = data.get('OrderID')
        Return_Reason = data.get('Return_Reason')

        user = User.query.get(UserID)
        if not user:
            return {'message': 'User not found'}, 404

        order = BookOrder.query.get(OrderID)
        if not order:
            return {'message': 'Order not found'}, 404

        return_request = ReturnRequest(
            UserID=UserID,
            AdminID=order.AdminID,
            OrderID=OrderID,
            Return_Reason=Return_Reason,
            Status='Pending'
        )
        db.session.add(return_request)
        db.session.commit()

        return {'message': 'Return request initiated successfully'}, 200


class ReturnRequestList(Resource):
    def get(self):
        book_return_requests = ReturnRequest.query.all()
        response = book_return_request_serializer(book_return_requests)
        return make_response(jsonify(response), 200)

    
class ReturnRequestById(Resource):
     # to retrieve book return request by id
    def get(self, RequestID):

        return_request = ReturnRequest.query.filter_by(RequestID=RequestID).first()
        
        if return_request:
            return_request_dict = {
            "RequestID": return_request.RequestID,
            "UserID": return_request.UserID,
            "AdminID": return_request.AdminID,
            "OrderID": return_request.OrderID,
            "Return_Reason": return_request.Return_Reason,
            "Status": return_request.Status
            }

            return make_response(jsonify(return_request_dict), 200)

        else:
            return make_response(jsonify({"error": "Return request details not found"}), 404)

    def patch(self, RequestID):
        new_return_request = ReturnRequest.query.filter_by(RequestID=RequestID).first()
        if  new_return_request:
            for attr in request.get_json():
                setattr(new_return_request, attr, request.get_json()[attr])

        db.session.add(new_return_request)
        db.session.commit()

        new_return_request_dict = {
            "RequestID": new_return_request.RequestID,
            "UserID": new_return_request.UserID,
            "AdminID": new_return_request.AdminID,
            "OrderID": new_return_request.OrderID,
            "Return_Reason": new_return_request.Return_Reason,
            "Status": new_return_request.Status
            }

        response = make_response(jsonify(new_return_request_dict), 200)

        return response
    
    def delete(self, RequestID):
        return_request = ReturnRequest.query.filter_by(RequestID=RequestID).first()

        db.session.delete(return_request)
        db.session.commit()

        response_dict = {"message": "Return request details successfully deleted"}

        response = make_response(
            jsonify(response_dict),
            200
        )

        return response
    
# Checkout Management (User)
class CheckoutManagement(Resource):
     def post(self, UserID):
        data = request.get_json()
        Cart_Type = data.get('Cart_Type')  # Indicates lending or purchasing cart

        user = User.query.get(UserID)
        if not user:
            return {'message': 'User not found'}, 404

        cart = Cart.query.filter_by(UserID=UserID, Cart_Type=Cart_Type).first()
        if not cart:
            return {'message': 'Cart not found'}, 404

        Cart_Items = CartItem.query.filter_by(CartID=cart.CartID).all()

        if Cart_Type == 'Lending':
            for item in Cart_Items:
                lending_request = BookLendingRequest(
                    UserID=UserID,
                    AdminID=item.book.AdminID,
                    BookID=item.BookID,
                    Status='Pending'
                )
                db.session.add(lending_request)
                db.session.delete(item)

        elif Cart_Type == 'Purchase':
            total_amount = 0
            for item in Cart_Items:
                total_amount += item.book.Price * item.Quantity
                book_order = BookOrder(
                    UserID=UserID,
                    AdminID=cart.AdminID,
                    BookID=item.BookID,
                    Status='Pending'
                )
                db.session.add(book_order)
                db.session.delete(item)

            purchase = Purchase(
                UserID=UserID,
                AdminID=cart.AdminID,
                OrderID=book_order.OrderID,
                Total_Amount=total_amount,
                Purchase_Date=datetime.utcnow()
            )
            db.session.add(purchase)

        db.session.delete(cart)
        db.session.commit()

        return {'message': 'Checkout successful'}, 200

    # def post(self, UserID):
    #     data = request.get_json()
    #     Cart_Type = data.get('Cart_Type')  # Indicates lending or purchasing cart
    #     UserID = data.get('UserID')

    #     user = User.query.get(UserID)
    #     if not user:
    #         return {'message': 'User not found'}, 404

    #     cart = Cart.query.filter_by(UserID=UserID, CartID=Cart.CartID).first()
    #     if not cart:
    #         return {'message': 'Cart not found'}, 404

    #     cart_items = CartItem.query.filter_by(CartID=cart.CartID).all()

    #     if Cart_Type == 'Lending':
    #         for item in cart_items:
    #             lending_request = BookLendingRequest(
    #                 UserID=data.get('UserID'),
    #                 BookID=data.get('BookID'),
    #                 Status=data.get('Pending')
    #             )
    #             db.session.add(lending_request)
    #             db.session.commit()
    #             db.session.delete(cart)
    #             db.session.commit()

    #     elif Cart_Type == 'Purchase':
    #         total_amount = 0
    #         for item in cart_items:
    #             total_amount += item.book.Price * item.Quantity
    #             book_order = BookOrder(
    #                 UserID=data.get('UserID'),
    #                 BookID=data.get('BookID'),
    #                 Status=data.get('Pending')
    #             )
    #             db.session.add(book_order)
    #             db.session.commit()
    #             db.session.delete(cart)
    #             db.session.commit()
                
    #         purchase = Purchase(
    #             UserID=UserID,
    #             AdminID=data.get('AdminID'),
    #             OrderID=data.get('OrderID'),
    #             Total_Amount=total_amount,
    #             Purchase_Date=datetime.utcnow()
    #         )
    #         db.session.add(purchase)

    #     db.session.delete(cart)
    #     db.session.commit()

    #     return {'message': 'Checkout successful'}, 200

    
# Cart Management (User)
class CartManagement(Resource):
    def post(self, UserID):
        data = request.get_json()
        BookID = data.get('BookID')
        Quantity = data.get('Quantity')
        Cart_Type = data.get('Cart_Type')  # Indicates lending or purchasing cart
        
        user = User.query.get(UserID)
        if not user:
            return {'message': 'User not found'}, 404

        cart = Cart.query.filter_by(UserID=UserID, Cart_Type=Cart_Type).first()
        if not cart:
            cart = Cart(UserID=UserID, Cart_Type=Cart_Type)
            db.session.add(cart)
            db.session.commit()

        cart_item = CartItem(CartID=cart.CartID, BookID=BookID, Quantity=Quantity)
        db.session.add(cart_item)
        db.session.commit()

        return {'message': 'Books added to the cart successfully'}, 200

class CartManagementDelete(Resource):
    def delete(self, UserID, CartID):
        Cart_Type = request.args.get('Cart_Type')  # Indicates lending or purchasing cart
        
        user = User.query.get(UserID)
        if not user:
            return {'message': 'User not found'}, 404

        cart = Cart.query.filter_by(UserID=UserID, CartID=CartID).first()
        if not cart:
            return {'message': 'Cart not found'}, 404

        cart_item = CartItem.query.filter_by(CartID=CartID, BookID=CartItem.BookID).first()
        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()
            db.session.delete(cart)
            db.session.commit()
            
            return {'message': 'Book removed from the cart successfully'}, 200
        else:
            return {'message': 'Book not found in the cart'}, 404
        
class CartList(Resource):
    def get(self):
        carts = Cart.query.all()
        response = cart_serializer(carts)
        return make_response(jsonify(response), 200)

    def post(self):
        data = request.get_json()
        new_cart = Cart(
            CartID=data.get("CartID"),
            UserID=data.get("UserID"),
            AdminID=data.get("AdminID"),
            Status=data.get("Status")
        )
        db.session.add(new_cart)
        db.session.commit()

        new_cart_dict = {
            "CartID": new_cart.CartID,
            "UserID": new_cart.UserID,
            "AdminID": new_cart.AdminID,
            "Status": new_cart.Status
        }
        return make_response(jsonify(new_cart_dict), 200)
    
# class CartById(Resource):
#      # to retrieve cart details by id
#     def get(self, CartID):

#         cart = Cart.query.filter_by(CartID=CartID).first()
        
#         if cart:
#             cart_dict = {
#             "CartID": cart.CartID,
#             "UserID": cart.UserID,
#             "AdminID": cart.AdminID,
#             "Status": cart.Status
#         }
#             return make_response(jsonify(cart_dict), 200)

#         else:
#             return make_response(jsonify({"error": "Cart request details not found"}), 404)

#     def patch(self, CartID):
#         cart = Cart.query.filter_by(CartID=CartID).first()
#         if  cart:
#             for attr in request.get_json():
#                 setattr(cart, attr, request.get_json()[attr])

#         db.session.add(cart)
#         db.session.commit()

#         cart_dict = {
#             "CartID": cart.CartID,
#             "UserID": cart.UserID,
#             "AdminID": cart.AdminID,
#             "Status": cart.Status
#         }

#         response = make_response(jsonify(cart_dict), 200)

#         return response
    
#     def delete(self, CartID):
#         cart = Cart.query.filter_by(CartID=CartID).first()

#         db.session.delete(cart)
#         db.session.commit()

#         response_dict = {"message": "Cart details successfully deleted"}

#         response = make_response(
#             jsonify(response_dict),
#             200
#         )

#         return response
    
# class CartItemList(Resource):
#     def get(self):
#         cartitems = CartItem.query.all()
#         response = cart_item_serializer(cartitems)
#         return make_response(jsonify(response), 200)

#     def post(self):
#         data = request.get_json()
#         new_cart_item = CartItem(
#             CartItemID=data.get("CartItemID"),
#             CartID=data.get("CartID"),
#             BookID=data.get("BookID"),
#             Quantity=data.get("Quantity")
#         )
#         db.session.add(new_cart_item)
#         db.session.commit()

#         new_cart_item_dict = {
#             "CartItemID": new_cart_item.CartItemID,
#             "CartID": new_cart_item.CartID,
#             "BookID": new_cart_item.BookID,
#             "Quantity": new_cart_item.Quantity
#         }
#         return make_response(jsonify(new_cart_item_dict), 200)
    

# class CartItemById(Resource):
#      # to retrieve cart item details by id
#     def get(self, CartItemID):

#         cart_itemm = CartItem.query.filter_by(CartItemID=CartItemID).first()
        
#         if cart_itemm:
#             cart_item_dict = {
#             "CartItemID": cart_itemm.CartItemID,
#             "CartID": cart_itemm.CartID,
#             "BookID": cart_itemm.BookID,
#             "Quantity": cart_itemm.Quantity
#         }
#             return make_response(jsonify(cart_item_dict), 200)

#         else:
#             return make_response(jsonify({"error": "Cart item details not found"}), 404)

#     def patch(self, CartItemID):
#         cart_itemm = CartItem.query.filter_by(CartItemID=CartItemID).first()
#         if  cart_itemm:
#             for attr in request.get_json():
#                 setattr(cart_itemm, attr, request.get_json()[attr])

#         db.session.add(cart_itemm)
#         db.session.commit()

#         cart_item_dict = {
#             "CartItemID": cart_itemm.CartItemID,
#             "CartID": cart_itemm.CartID,
#             "BookID": cart_itemm.BookID,
#             "Quantity": cart_itemm.Quantity
#         }

#         response = make_response(jsonify(cart_item_dict ), 200)

#         return response
    
#     def delete(self, CartItemID):
#         cart_itemm = CartItem.query.filter_by(CartItemID=CartItemID).first()

#         db.session.delete(cart_itemm)
#         db.session.commit()

#         response_dict = {"message": "Cart item details successfully deleted"}

#         response = make_response(
#             jsonify(response_dict),
#             200
#         )

#         return response

class OrderManagement(Resource):
    # for admin to change the order status to approved or rejected
    def put(self, OrderID):
        data = request.get_json()
        order = BookOrder.query.get(OrderID)
        if order:
            order.Status = data['Status']
            db.session.commit()
            return {'message': 'Order status updated successfully'}, 200
        else:
            return {'message': 'Order not found'}, 404
  
class BookOrdersList(Resource):
    def get(self):
        bookorders = BookOrder.query.all()
        response = book_order_serializer(bookorders)
        return make_response(jsonify(response), 200)

    def post(self):
        data = request.get_json()
        new_book_order = BookOrder(
            OrderID=data.get("OrderID"),
            UserID=data.get("UserID"),
            AdminID = data.get("AdminID"),
            BookID=data.get("BookID"),
            Status=data.get("Status")
        )
        db.session.add(new_book_order)
        db.session.commit()

        new_book_order_dict = {
            "OrderID": new_book_order.OrderID,
            "UserID": new_book_order.UserID,
            "AdminID": new_book_order.AdminID,
            "BookID": new_book_order.BookID,
            "Status": new_book_order.Status
        }
        return make_response(jsonify(new_book_order_dict), 200)
    
class BookOrderById(Resource):
      # to retrieve book order details by id
    def get(self, OrderID):

        bookorderr = BookOrder.query.filter_by(OrderID=OrderID).first()
        
        if bookorderr:
            book_order_dict = {
             "OrderID": bookorderr.OrderID,
            "UserID": bookorderr.UserID,
            "AdminID": bookorderr.AdminID,
            "BookID": bookorderr.BookID,
            "Status": bookorderr.Status
        }
            return make_response(jsonify(book_order_dict), 200)

        else:
            return make_response(jsonify({"error": "Book order details not found"}), 404)

    def patch(self, OrderID):
        bookorderr = BookOrder.query.filter_by(OrderID=OrderID).first()
       
        if  bookorderr:
            for attr in request.get_json():
                setattr(bookorderr, attr, request.get_json()[attr])

        db.session.add(bookorderr)
        db.session.commit()

        book_order_dict = {
            "OrderID": bookorderr.OrderID,
            "UserID": bookorderr.UserID,
            "AdminID": bookorderr.AdminID,
            "BookID": bookorderr.BookID,
            "Status": bookorderr.Status
        }

        response = make_response(jsonify(book_order_dict ), 200)

        return response
    
    def delete(self, OrderID):
        bookorderr = BookOrder.query.filter_by(OrderID=OrderID).first()

        db.session.delete(bookorderr )
        db.session.commit()

        response_dict = {"message": "Book Order details successfully deleted"}

        response = make_response(
            jsonify(response_dict),
            200
        )

        return response

class AdminsList(Resource):
    def get(self):
        admins = Admin.query.all()
        response = admin_serializer(admins)
        return make_response(jsonify(response), 200)
     
    def post(self):
        data = request.get_json()
        new_admin = Admin(
            AdminID=data.get("AdminID"),
            Username=data.get("Username"),
            Password = data.get("Password"),
            Email=data.get("Email"),
            Full_Name=data.get("Full_Name"),
            Phone_Number=data.get("Phone_Number")
        )
        db.session.add(new_admin)
        db.session.commit()

        new_admin_dict = {
            "AdminID": new_admin.AdminID,
            "Username": new_admin.Username,
            "Password": new_admin.Password,
            "Email": new_admin.Email,
            "Full_Name": new_admin.Full_Name,
            "Phone_Number":new_admin.Phone_Number
        }
        return make_response(jsonify(new_admin_dict), 200)
    

class AdminById(Resource):
      # to retrieve book order details by id
    def get(self, AdminID):

        admin = Admin.query.filter_by(AdminID=AdminID).first()
        
        if admin:
            admin_dict = {
            "AdminID": admin.AdminID,
            "Username": admin.Username,
            "Password": admin.Password,
            "Email": admin.Email,
            "Full_Name": admin.Full_Name,
            "Phone_Number":admin.Phone_Number
        }
            return make_response(jsonify(admin_dict), 200)

        else:
            return make_response(jsonify({"error": "Admin details not found"}), 404)

    def patch(self, AdminID):
        admin = Admin.query.filter_by(AdminID=AdminID).first()
       
        if admin:
            for attr in request.get_json():
                setattr(admin, attr, request.get_json()[attr])

        db.session.add(admin)
        db.session.commit()

        admin_dict = {
            "AdminID": admin.AdminID,
            "Username": admin.Username,
            "Password": admin.Password,
            "Email": admin.Email,
            "Full_Name": admin.Full_Name,
            "Phone_Number": admin.Phone_Number
        }
        response = make_response(jsonify(admin_dict ), 200)

        return response
    
    def delete(self, AdminID):
        admin = Admin.query.filter_by(AdminID=AdminID).first()
       
        db.session.delete(admin)
        db.session.commit()

        response_dict = {"message": "Admin details successfully deleted"}

        response = make_response(
            jsonify(response_dict),
            200
        )

        return response

class AdminRegistration(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('Username')
        password = data.get('Password')
        Email = data.get('Email')
        Full_Name = data.get('Full_Name')
        Phone_Number=data.get("Phone_Number")

        if not username or not password:
            return {"message": "Missing username or password"}, 400
        
        user = Admin.query.filter_by(Username=username).first()

        if user:
            return {"message": "Admin already exists"}, 400

        new_user = Admin(Username=username, Password=password, Email=Email, Full_Name=Full_Name, Phone_Number=Phone_Number)
        db.session.add(new_user)
        db.session.commit()

        return {"message": "Admin created successfully"}, 201
    

class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('Username')
        password = data.get('Password')
        Email = data.get('Email')
        Full_Name = data.get('Full_Name')
        Phone_Number=data.get("Phone_Number")

        if not username or not password:
            return {"message": "Missing username or password"}, 400
        
        user = User.query.filter_by(Username=username).first()

        if user:
            return {"message": "User already exists"}, 400

        new_user = User(Username=username, Password=password, Email=Email, Full_Name=Full_Name, Phone_Number=Phone_Number)
        db.session.add(new_user)
        db.session.commit()

        return {"message": "User created successfully"}, 201
    
class AdminLogin(Resource):
    def post(self):
        data = request.get_json()  # Use request.get_json() to get JSON data

        response = None  # Initialize the response variable

        if not data or 'Username' not in data or 'Password' not in data:
            response = make_response(jsonify(message='Invalid request'), 400)
        else:
            Username = data['Username']
            Password = data['Password']
            # Assuming User is your SQLAlchemy model representing the user table
            admin = Admin.query.filter_by(Username=Username).first()

            if admin and (admin.Password == Password):
                # Continue with the authentication process
                access_token = create_access_token(identity=admin.AdminID)
                response = make_response(jsonify(access_token=access_token), 200)
                # return jsonify({'message': 'Admin login successful'})
            else:
                response = make_response(jsonify(message='Invalid username or password'), 401)

        return response

class UserLogin(Resource):
    def post(self):
        data = request.get_json()  # Use request.get_json() to get JSON data

        response = None  # Initialize the response variable

        if not data or 'Username' not in data or 'Password' not in data:
            response = make_response(jsonify(message='Invalid request'), 400)
        else:
            Username = data['Username']
            Password = data['Password']
            # Assuming User is your SQLAlchemy model representing the user table
            user = User.query.filter_by(Username=Username).first()

            if user and (user.Password == Password):
                access_token = create_access_token(identity=user.UserID)
                response = make_response(jsonify(access_token=access_token), 200)
            else:
                response = make_response(jsonify(message='Invalid username or password'), 401)

        return response
    
# class PaymentsResource:
#     africastalking.initialize(
#         username="joe2022",
#         api_key="aab3047eb9ccfb3973f928d4ebdead9e60beb936b4d2838f7725c9cc165f0c8a"
#         #justpaste.it/1nua8
#     )
#     sms = africastalking.SMS

#     def send_sms(phone, message):
#         sms = africastalking.SMS
#         recipients = [phone]
#         sender = "AFRICASTKNG"
#         try:
#             response = sms.send(message, recipients)
#             print(response)
#         except Exception as error:
#             print("Error is ", error)

#     # Test
#     #send_sms("+254729225710", "This is test message on Fleet.")

#     def gen_random(N):
#         import string
#         import random

#         # using random.choices()
#         # generating random strings
#         res = ''.join(random.choices(string.digits, k=N))
#         # print result
#         print("The generated random string : " + str(res))
#         return str(res)

#     # Test    
#     #gen_random(N=4)

#     def hash_password(password):
#         bytes = password.encode("utf-8")
#         salt = bcrypt.gensalt()
#         hash = bcrypt.hashpw(bytes, salt)
#         print("Bytes ", bytes)
#         print("Salt ", salt)
#         print("Hashed password ", hash.decode())
#         return hash.decode()

#     # Test
#     #hash_password("kenya1234")
#     # Output
#     # $2b$12$LyTDdwhw5GHR6ILxTSrCfu69/x4xpihitQ3QZXUHOXa7YRQtg2FcO

#     def hash_verify(password,  hashed_password):
#         bytes = password.encode('utf-8')
#         result = bcrypt.checkpw(bytes, hashed_password.encode())
#         print(result)
#         return result


#     #hash_verify("kenya1234", "$2b$12$LyTDdwhw5GHR6ILxTSrCfu69/x4xpihitQ3QZXUHOXa7YRQtg2FcO")
#     # Output
#     # Returns True/False

#     # generates Encryption Key
    
#     def gen_key():
#         key = Fernet.generate_key()
#         with open("key.key", "wb") as key_file:
#             key_file.write(key)
#     # Test
#     gen_key()

#     def load_key():
#         return open("key.key", "rb").read()

#     # Test
#     #print(load_key())

#     def load_key():
#         return open("key.key", "rb").read()

#     # Test
#     #print(load_key())

#     def encrypt(data):
#         key = load_key()
#         f = Fernet(key)
#         encrypted_data = f.encrypt(data.encode())
#         print("Plain ", data)
#         print("Encrypted ", encrypted_data.decode())
#         return encrypted_data.decode()
#     # Test
#     #encrypt("+254729225710")
#     # Output
#     # gAAAAABjLX8d8JAsCS9ipJ8mO44Px4hb6GgfydOllU7P1JJqHWTQXEXchS-CMqsE2sSz2mDhrlGDjmmCYFCn4Em7X7F6nHVBTQ==

#     def decrypt(encrypted_data):
#         key = load_key()
#         f = Fernet(key)
#         decrypted_data = f.decrypt(encrypted_data.encode())
#         print("Decrypted data ", decrypted_data.decode())
#         return decrypted_data.decode()
#     # Test - Provide the Encrypted
#     #decrypt("gAAAAABjIY3vZqXEHBV9DIvizYUfsA6uPxx1pT16_OyopLYIAg4x52wUMwVWhRS2_IgVcQfKKZbWPRWmrcfJ15Nu3zj7rMdwWw==")
#     # Output
#     # +254729225710

#     # def send_email(email, message):
#     #     import smtplib
#     #     # creates SMTP session
#     #     s = smtplib.SMTP('smtp.gmail.com', 587)
#     #     # start TLS for security
#     #     s.starttls()
#     #     # Authentication
#     #     s.login("modcomlearning@gmail.com", "your password")
#     #     # sending the mail
#     #     s.sendmail("modcomlearning@gmail.com", email, message)
#     #     # terminating the session
#     #     s.quit()

#     # Test
#     #send_email("johndoe@gmail.com", "Test Email")



#     # In this fucntion we provide phone(used to pay), amount to be paid and invoice no being paid for.
#     def mpesa_payment(amount, phone, invoice_no):
#             # GENERATING THE ACCESS TOKEN
#             consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
#             consumer_secret = "amFbAoUByPV2rM5A"

#             api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
#             r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

#             data = r.json()
#             access_token = "Bearer" + ' ' + data['access_token']

#             #  GETTING THE PASSWORD
#             timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
#             passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
#             business_short_code = "174379"
#             data = business_short_code + passkey + timestamp
#             encoded = base64.b64encode(data.encode())
#             password = encoded.decode('utf-8')

#             # BODY OR PAYLOAD
#             payload = {
#                 "BusinessShortCode": "174379",
#                 "Password": "{}".format(password),
#                 "Timestamp": "{}".format(timestamp),
#                 "TransactionType": "CustomerPayBillOnline",
#                 "Amount": amount,  # use 1 when testing
#                 "PartyA": phone,  # change to your number
#                 "PartyB": "174379",
#                 "PhoneNumber": phone,
#                 "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
#                 "AccountReference": "account",
#                 "TransactionDesc": "account"
#             }

#             # POPULATING THE HTTP HEADER
#             headers = {
#                 "Authorization": access_token,
#                 "Content-Type": "application/json"
#             }

#             url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # C2B URL

#             response = requests.post(url, json=payload, headers=headers)
#             print(response.text)
#     # Test
#     # mpesa_payment("2", "254714687873", "NCV003")

#     def gen_pdf():
#         # Python program to create
#         # a pdf file
        
#         # save FPDF() class into a
#         # variable pdf
#         pdf = FPDF()
#         # Add a page
#         pdf.add_page()
#         # set style and size of font
#         # that you want in the pdf
#         pdf.set_font("Arial", size=15)
#         # create a cell
#         pdf.cell(200, 10, txt="ModcomInstitute of tech",
#                 ln=1, align='L')
#         # add another cell
#         pdf.cell(200, 10, txt="A Computer Science portal for geeks.",
#                 ln=2, align='C')
#         # save the pdf with name .pdf
#         pdf.output("cv.pdf")

#     # Test
#     # gen_pdf()

    
#     def passwordValidity (password):
#         if (len(password) <8):
#             return "Your password Must be greater than 8 characters"
#         elif not re.search("[a-z]", password):
#             return "You must have atleast a lowercase letter"
#         elif not re.search("[A-Z]", password):
#             return "You must have atleast an uppercase letter"
#         elif not re.search("[0-9]", password):
#             return "You must have atleast a number"
#         # elif not re.search("[&#&$@?*]", password):
#         #     return "You must have atleast a symbol"
#         else:
#             return True
#     #x=passwordValidity("jkheydehow")
#     # print(x)


#     def check_phone(phone):
#         regex = "^\+254\d{9}"
#         if not re.match(regex, phone)  or len(phone) !=13:
#             print("Phone Not Ok")
#             return False
#         else:
#             print("Phone Ok")
#             return True

#     check_phone("+254714687873")
# class PaymentsResource(Resource):
#     def post(self):
#         data = request.get_json()
    
#         UserID = data.get('UserID')
#         Total_Amount = data.get('Total_Amount')
#         Phone_Number = data.get('Phone_Number')

#         user = Purchase.query.get(UserID)

#         if user:
#             response = initiate_stk_push(Phone_Number, Total_Amount)
        
#             if response.get('ResponseCode') == "0":
#                 new_purchase = Purchase(UserID=UserID, Total_Amount=Total_Amount)
#                 db.session.add(new_purchase)
#                 db.session.commit()
#                 return jsonify({'message': 'Purchase initiated successfully!'})
#             else:
#                 # Handle the case where the STK push failed
#                 return jsonify({'error': 'STK push payment failed. Purchase not recorded.'})

#         return jsonify({'error': 'User not found'})
#     # UserID = request.args.get('UserID') 
    
#     # @donations_ns.expect(donation_parser)
#     # @donations_ns.marshal_with(donation_response_model, code=201)
#     # @donations_ns.doc(responses={201: 'Donation initiated successfully!', 400: 'Bad request'})
#     # def post(self):
#     #     data = request.get_json()
#     #     UserID = data.get('UserID')
#     #     # data = donation_parser.parse_args()

    #     BookID = data['BookID']
    #     amount = data['amount']
    #     Phone_Number = data['Phone_Number']
    #     is_anonymous = data['is_anonymous']
    #     OrderID = data['OrderID']
    #     is_one_time_payment = data['is_one_time_payment']  # New parameter

    #     # Logic with your charity ID determination
    #     OrderID = request.args.get('OrderID')

    #     if OrderID is None:
    #         return {'error': 'Invalid OrderID'}, 400

    #     user = User.query.get(UserID)

    #     if user:
    #         response = initiate_stk_push(Phone_Number, amount)

    #         if response.get('ResponseCode') == "0":
    #             new_payment = Purchase(
    #                 UserID=UserID,
    #                 BookID=BookID,
    #                 amount=amount,
    #                 is_anonymous=is_anonymous,
    #                 is_one_time_payment=is_one_time_payment  # Set the donation type
    #             )
    #             db.session.add(new_payment)
    #             db.session.commit()
    #             return {'message': 'Payment initiated successfully!'}, 201
    #         else:
    #             # Handle the case where the STK push failed
    #             return {'error': 'STK push payment failed. Payment not recorded.'}, 400

    #     return {'error': 'User not found'}, 400

# api.add_resource(PaymentsResource, '/payments')
api.add_resource(AdminRegistration, '/admins/register')
api.add_resource(UserRegistration, '/users/register')
api.add_resource(AdminLogin, '/admins/login')
api.add_resource(UserLogin, '/users/login')
api.add_resource(Home, "/")
api.add_resource(BooksList, "/books")
api.add_resource(AdminBooksList, "/admins/books")
api.add_resource(UserBooksList, "/users/books")
api.add_resource(AdminBookById, "/admins/books/<int:BookID>")
api.add_resource(BookById, "/books/<int:BookID>")
api.add_resource(UsersBookByTitle, "/users/books/title/<string:Title>")
api.add_resource(UsersBookByGenre, "/users/books/genre/<string:Genre>") 
api.add_resource(UsersBookByPrice, "/users/books/price/<int:Price>")
# api.add_resource(BookByDateUploaded, "/books/dateuploaded/<string:Date_Uploaded>")
api.add_resource(UsersList, "/users")
api.add_resource(UserById, "/users/<int:UserID>")
api.add_resource(PreviousPurchasesLendings, '/users/<int:UserID>/previouspurchases')
api.add_resource(PurchasesList, "/purchases")
api.add_resource(PurchaseById, "/purchases/<int:PurchaseID>")
api.add_resource(BookLendingsList, "/lendings")
api.add_resource(BookLendingById, "/lendings/<int:RequestID>")
api.add_resource(ReturnRequestManagement, '/users/<int:UserID>/returnrequests')
api.add_resource(ReturnRequestList, "/returnrequests")
api.add_resource(ReturnRequestById, "/returnrequests/<int:RequestID>")
api.add_resource(CartList, "/carts")
# api.add_resource(CartById, "/carts/<int:CartID>")
api.add_resource(CheckoutManagement, '/users/<int:UserID>/checkout')
api.add_resource(CartManagement, '/users/<int:UserID>/carts')
api.add_resource(CartManagementDelete, '/users/<int:UserID>/carts/<int:CartID>')
# api.add_resource(CartItemList, "/cartitems")
# api.add_resource(CartItemById, "/cartitems/<int:CartItemID>")
api.add_resource(OrderManagement, '/admins/order/<int:OrderID>')
api.add_resource(BookOrdersList, "/bookorders")
api.add_resource(BookOrderById, "/bookorders/<int:OrderID>")
api.add_resource(AdminsList, "/admins")
api.add_resource(AdminById, "/admins/<int:AdminID>")


if __name__ == "__main__":
    app.debug = True
    app.run(debug=False)

