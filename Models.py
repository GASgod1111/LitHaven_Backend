
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Admin(db.Model):
    AdminID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(255))
    Password = db.Column(db.String(255))
    Email = db.Column(db.String(255))
    Full_Name = db.Column(db.String(255))

class Book(db.Model):
    BookID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(255))
    Author = db.Column(db.String(255))
    Genre = db.Column(db.String(255))
    Description = db.Column(db.String(255))
    Price = db.Column(db.Float)
    Date_Uploaded = db.Column(db.DateTime)

class BookOrder(db.Model):
    OrderID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'))
    AdminID = db.Column(db.Integer, db.ForeignKey('admin.AdminID'))
    BookID = db.Column(db.Integer, db.ForeignKey('book.BookID'))
    Status = db.Column(db.String(255))

class BookLendingRequest(db.Model):
    RequestID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'))
    AdminID = db.Column(db.Integer, db.ForeignKey('admin.AdminID'))
    BookID = db.Column(db.Integer, db.ForeignKey('book.BookID'))
    Status = db.Column(db.String(255))

class User(db.Model):
    UserID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(255))
    Password = db.Column(db.String(255))
    Email = db.Column(db.String(255))
    Full_Name = db.Column(db.String(255))

class Cart(db.Model):
    CartID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'))
    AdminID = db.Column(db.Integer, db.ForeignKey('admin.AdminID'))
    Status = db.Column(db.String(255))

class CartItem(db.Model):
    CartItemID = db.Column(db.Integer, primary_key=True)
    CartID = db.Column(db.Integer, db.ForeignKey('cart.CartID'))
    BookID = db.Column(db.Integer, db.ForeignKey('book.BookID'))
    Quantity = db.Column(db.Integer)

class Purchase(db.Model):
    PurchaseID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'))
    AdminID = db.Column(db.Integer, db.ForeignKey('admin.AdminID'))
    OrderID = db.Column(db.Integer, db.ForeignKey('book_order.OrderID'))
    Total_Amount = db.Column(db.Float)
    Purchase_Date = db.Column(db.DateTime)

class ReturnRequest(db.Model):
    RequestID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'))
    AdminID = db.Column(db.Integer, db.ForeignKey('admin.AdminID'))
    OrderID = db.Column(db.Integer, db.ForeignKey('book_order.OrderID'))
    Return_Reason = db.Column(db.String(255))
    Status = db.Column(db.String(255))

