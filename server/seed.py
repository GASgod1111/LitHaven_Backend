from app import app, db
from Models import Admin, Book, BookOrder, BookLendingRequest, User, Cart, CartItem, Purchase, ReturnRequest
from faker import Faker
import random
from datetime import datetime

fake = Faker()

# Create sample data using Faker to seed the database
def seed_data():
    # Create admins
    admins = []
    for _ in range(30):
        admin = Admin(
            Username=fake.user_name(),
            Password=fake.password(),
            Email=fake.email(),
            Full_Name=fake.name()
        )
        admins.append(admin)
        db.session.add(admin)

    # Create users
    users = []
    for _ in range(30):
        user = User(
            Username=fake.user_name(),
            Password=fake.password(),
            Email=fake.email(),
            Full_Name=fake.name()
        )
        users.append(user)
        db.session.add(user)

    # Create books
    books = []
    for _ in range(30):
        book = Book(
            Title=fake.sentence(nb_words=3),
            Author=fake.name(),
            Genre=fake.random_element(elements=('Fiction', 'Non-Fiction', 'Mystery', 'Romance', 'Science Fiction', 'Fantasy')),
            Description=fake.paragraph(nb_sentences=5),
            Price=fake.random_int(min=5, max=50),
            Date_Uploaded=datetime.now()
        )
        books.append(book)
        db.session.add(book)

    # Create book orders
    book_orders = []
    for _ in range(30):
        book_order = BookOrder(
            UserID=random.randint(1, 100),
            AdminID=random.randint(1, 100),
            BookID=random.randint(1, 100),
            Status=fake.word()
        )
        book_orders.append(book_order)
        db.session.add(book_order)

    # Create book lending requests
    book_lending_requests = []
    for _ in range(30):
        book_lending_request = BookLendingRequest(
            UserID=random.randint(1, 100),
            AdminID=random.randint(1, 100),
            BookID=random.randint(1, 100),
            Status=fake.word()
        )
        book_lending_requests.append(book_lending_request)
        db.session.add(book_lending_request)

    # Create carts
    carts = []
    for _ in range(30):
        cart = Cart(
            UserID=random.randint(1, 100),
            AdminID=random.randint(1, 100),
            Status=fake.word()
        )
        carts.append(cart)
        db.session.add(cart)

    # Create cart items
    cart_items = []
    for _ in range(30):
        cart_item = CartItem(
            CartID=random.randint(1, 100),
            BookID=random.randint(1, 100),
            Quantity=random.randint(1, 100)
        )
        cart_items.append(cart_item)
        db.session.add(cart_item)

    # Create purchases
    purchases = []
    for _ in range(30):
        purchase = Purchase(
            UserID=random.randint(1, 100),
            AdminID=random.randint(1, 100),
            OrderID=random.randint(1, 100),
            Total_Amount=fake.random_int(min=5, max=900),
            Purchase_Date=datetime.now()
        )
        purchases.append(purchase)
        db.session.add(purchase)

    # Create return requests
    return_requests = []
    for _ in range(30):
        return_request = ReturnRequest(
            UserID=random.randint(1, 100),
            AdminID=random.randint(1, 100),
            OrderID=random.randint(1, 100),
            Return_Reason=fake.text(),
            Status=fake.word()
        )
        return_requests.append(return_request)
        db.session.add(return_request)

    # Commit the session to the database
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        # Create all tables
        db.create_all()

        # Seed data into the database
        seed_data()
