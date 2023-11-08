from datetime import datetime
from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
db = SQLAlchemy()

class Admin(db.Model, SerializerMixin):
    __tablename__ = 'Admin'
    AdminID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String, nullable=False, unique=True)
    Password = db.Column(db.String, nullable=False)
    Email = db.Column(db.String, nullable=False, unique=True)
    Full_Name = db.Column(db.String, nullable=False)
    book_orders = db.relationship("BookOrder", backref="admin")
    book_lending_requests = db.relationship("BookLendingRequest", backref="admin")
    carts = db.relationship("Cart", backref="admin")
    purchases = db.relationship("Purchase", backref="admin")
    return_requests = db.relationship("ReturnRequest", backref="admin")

class Book(db.Model, SerializerMixin):
    __tablename__ = 'Book'
    BookID = db.Column(db.Integer, primary_key=True)
    #img column can put a link
    Book_Image = db.Column(db.String)
    Title = db.Column(db.String, nullable=False)
    Author = db.Column(db.String, nullable=False)
    Genre = db.Column(db.String, nullable=False)
    Description = db.Column(db.String)
    Price = db.Column(db.Float)
    Date_Uploaded = db.Column(db.DateTime, default=datetime.utcnow)
    cart_items = db.relationship("CartItem", backref="book")
    book_orders = db.relationship("BookOrder", backref="book")
    book_lending_requests = db.relationship("BookLendingRequest", backref="book")

class BookOrder(db.Model, SerializerMixin):
    __tablename__ = 'BookOrder'
    OrderID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('User.UserID'))
    AdminID = db.Column(db.Integer, db.ForeignKey('Admin.AdminID'))
    BookID = db.Column(db.Integer, db.ForeignKey('Book.BookID'))
    Status = db.Column(db.String)

class BookLendingRequest(db.Model, SerializerMixin):
    __tablename__ = 'BookLendingRequest'
    RequestID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('User.UserID'))
    AdminID = db.Column(db.Integer, db.ForeignKey('Admin.AdminID'))
    BookID = db.Column(db.Integer, db.ForeignKey('Book.BookID'))
    Status = db.Column(db.String)

class User(db.Model, SerializerMixin):
    __tablename__ = 'User'
    UserID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String, nullable=False, unique=True)
    Password = db.Column(db.String, nullable=False)
    Email = db.Column(db.String, nullable=False, unique=True)
    Full_Name = db.Column(db.String, nullable=False)
    carts = db.relationship("Cart", backref="user")
    purchases = db.relationship("Purchase", backref="user")
    return_requests = db.relationship("ReturnRequest", backref="user")
    book_orders = db.relationship("BookOrder", backref="user")
    book_lending_requests = db.relationship("BookLendingRequest", backref="user")

class Cart(db.Model, SerializerMixin):
    __tablename__ = 'Cart'
    CartID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('User.UserID'))
    AdminID = db.Column(db.Integer, db.ForeignKey('Admin.AdminID'))
    Cart_Type = db.Column(db.Enum('Purchase', 'Lending'))   
    cart_items = db.relationship("CartItem", backref="cart")

class CartItem(db.Model, SerializerMixin):
    __tablename__ = 'CartItem'
    CartItemID = db.Column(db.Integer, primary_key=True)
    CartID = db.Column(db.Integer, db.ForeignKey('Cart.CartID'))
    BookID = db.Column(db.Integer, db.ForeignKey('Book.BookID'))
    Quantity = db.Column(db.Integer, nullable=False)

class Purchase(db.Model, SerializerMixin):
    __tablename__ = 'Purchase'
    PurchaseID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('User.UserID'))
    AdminID = db.Column(db.Integer, db.ForeignKey('Admin.AdminID'))
    OrderID = db.Column(db.Integer, db.ForeignKey('BookOrder.OrderID'))
    Total_Amount = db.Column(db.Float)
    Purchase_Date = db.Column(db.DateTime, default=datetime.utcnow)

class ReturnRequest(db.Model, SerializerMixin):
    __tablename__ = 'ReturnRequest'
    RequestID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('User.UserID'))
    AdminID = db.Column(db.Integer, db.ForeignKey('Admin.AdminID'))
    OrderID = db.Column(db.Integer, db.ForeignKey('BookOrder.OrderID'))
    Return_Reason = db.Column(db.String)
    Status = db.Column(db.String)

