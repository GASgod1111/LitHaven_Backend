# from flask import Flask
# from faker import Faker
# from datetime import datetime
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
# db = SQLAlchemy(app)

# class Book(db.Model):
#     __tablename__ = 'book'
#     BookID = db.Column(db.Integer, primary_key=True)
#     Title = db.Column(db.String(255))
#     Author = db.Column(db.String(255))
#     Genre = db.Column(db.String(255))
#     Description = db.Column(db.String(255))
#     Price = db.Column(db.Float)
#     Date_Uploaded = db.Column(db.DateTime, default=datetime.now)

# with app.app_context():
#     # Creating tables
#     db.create_all()

#     # fake data
#     fake = Faker()
#     with db.session.begin_nested():
#         for _ in range(10):
#             book = Book(
#                 Title=fake.sentence(nb_words=3),
#                 Author=fake.name(),
#                 Genre=fake.random_element(elements=('Fiction', 'Non-Fiction', 'Mystery', 'Romance', 'Science Fiction', 'Fantasy')),
#                 Description=fake.paragraph(nb_sentences=5),
#                 Price=fake.random_int(min=5, max=50),
#                 Date_Uploaded=datetime.now()
#             )
#             db.session.add(book)
#     db.session.commit()
