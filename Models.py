from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Admin(db.Model):
    AdminID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(255))
    Password = db.Column(db.String(255))
    Email = db.Column(db.String(255))
    Full_Name = db.Column(db.String(255))

    def to_dict(self):
        return {
            'AdminID': self.AdminID,
            'Username': self.Username,
            'Password': self.Password,
            'Email': self.Email,
            'Full_Name': self.Full_Name
        }

class Book(db.Model):
    BookID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(255))
    Author = db.Column(db.String(255))
    Genre = db.Column(db.String(255))
    Description = db.Column(db.String(255))
    Price = db.Column(db.Float)
    Date_Uploaded = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'BookID': self.BookID,
            'Title': self.Title,
            'Author': self.Author,
            'Genre': self.Genre,
            'Description': self.Description,
            'Price': self.Price,
            'Date_Uploaded': self.Date_Uploaded.strftime('%Y-%m-%d %H:%M:%S')
        }

class BookOrder(db.Model):
    OrderID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'))
    AdminID = db.Column(db.Integer, db.ForeignKey('admin.AdminID'))
    BookID = db.Column(db.Integer, db.ForeignKey('book.BookID'))
    Status = db.Column(db.String(255))

    def to_dict(self):
        return {
            'OrderID': self.OrderID,
            'UserID': self.UserID,
            'AdminID': self.AdminID,
            'BookID': self.BookID,
            'Status': self.Status
        }

class BookLendingRequest(db.Model):
    RequestID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'))
    AdminID = db.Column(db.Integer, db.ForeignKey('admin.AdminID'))
    BookID = db.Column(db.Integer, db.ForeignKey('book.BookID'))
    Status = db.Column(db.String(255))

    def to_dict(self):
        return {
            'RequestID': self.RequestID,
            'UserID': self.UserID,
            'AdminID': self.AdminID,
            'BookID': self.BookID,
            'Status': self.Status
        }

class User(db.Model):
    UserID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(255))
    Password = db.Column(db.String(255))
    Email = db.Column(db.String(255))
    Full_Name = db.Column(db.String(255))

    def to_dict(self):
        return {
            'UserID': self.UserID,
            'Username': self.Username,
            'Password': self.Password,
            'Email': self.Email,
            'Full_Name': self.Full_Name
        }

class Cart(db.Model):
    CartID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'))
    AdminID = db.Column(db.Integer, db.ForeignKey('admin.AdminID'))
    Status = db.Column(db.String(255))

    def to_dict(self):
        return {
            'CartID': self.CartID,
            'UserID': self.UserID,
            'AdminID': self.AdminID,
            'Status': self.Status
        }

class CartItem(db.Model):
    CartItemID = db.Column(db.Integer, primary_key=True)
    CartID = db.Column(db.Integer, db.ForeignKey('cart.CartID'))
    BookID = db.Column(db.Integer, db.ForeignKey('book.BookID'))
    Quantity = db.Column(db.Integer)

    def to_dict(self):
        return {
            'CartItemID': self.CartItemID,
            'CartID': self.CartID,
            'BookID': self.BookID,
            'Quantity': self.Quantity
        }

class Purchase(db.Model):
    PurchaseID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'))
    AdminID = db.Column(db.Integer, db.ForeignKey('admin.AdminID'))
    OrderID = db.Column(db.Integer, db.ForeignKey('book_order.OrderID'))
    Total_Amount = db.Column(db.Float)
    Purchase_Date = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'PurchaseID': self.PurchaseID,
            'UserID': self.UserID,
            'AdminID': self.AdminID,
            'OrderID': self.OrderID,
            'Total_Amount': self.Total_Amount
        }

class ReturnRequest(db.Model):
    RequestID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'))
    AdminID = db.Column(db.Integer, db.ForeignKey('admin.AdminID'))
    OrderID = db.Column(db.Integer, db.ForeignKey('book_order.OrderID'))
    Return_Reason = db.Column(db.String(255))
    Status = db.Column(db.String(255))

    def to_dict(self):
        return {
            'RequestID': self.RequestID,
            'UserID': self.UserID,
            'AdminID': self.AdminID,
            'OrderID': self.OrderID,
            'Return_Reason': self.Return_Reason,
            'Status': self.Status
        }