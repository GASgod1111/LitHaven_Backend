import random
from app import app, db
from Models import Admin, Book, BookOrder, BookLendingRequest, User, Cart, CartItem, Purchase, ReturnRequest
from faker import Faker
from random import randint
from datetime import datetime
from faker.providers.phone_number import Provider

fake = Faker()

book_images = [
    'https://images.unsplash.com/photo-1544947950-fa07a98d237f?auto=format&fit=crop&q=60&w=500&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fGJvb2t8ZW58MHx8MHx8fDA%3D',
    'https://static01.nyt.com/images/2023/05/02/books/02erin-langston-cover/02erin-langston-cover-superJumbo.jpg?quality=75&auto=webp',
    'https://static01.nyt.com/images/2023/05/16/books/16samara-breger-cover/16samara-breger-cover-jumbo.jpg?quality=75&auto=webp',
    'https://static01.nyt.com/images/2023/05/02/books/02kristina-forest-cover/02kristina-forest-cover-jumbo.jpg?quality=75&auto=webp',
    'https://static01.nyt.com/images/2023/01/24/books/24EMMA-BARRY-COVER/24EMMA-BARRY-COVER-superJumbo.jpg?quality=75&auto=webp',
    'https://static01.nyt.com/images/2023/06/30/books/30rebekah-weatherspoon-cover/30rebekah-weatherspoon-cover-jumbo.jpg?quality=75&auto=webp',
    'https://hips.hearstapps.com/vader-prod.s3.amazonaws.com/1689018245-71EFaIUUbfL.jpg?crop=1xw:1xh;center,top&resize=980:*',
    'https://hips.hearstapps.com/vader-prod.s3.amazonaws.com/1689018349-81FdfnFjOUS.jpg?crop=1xw:1xh;center,top&resize=980:*',
    'https://hips.hearstapps.com/vader-prod.s3.amazonaws.com/1689018391-91BbLCJOruL.jpg?crop=1xw:1xh;center,top&resize=980:*',
    'https://hips.hearstapps.com/vader-prod.s3.amazonaws.com/1689018490-813WHPxt3eL.jpg?crop=1xw:1xh;center,top&resize=980:*',
    'https://hips.hearstapps.com/vader-prod.s3.amazonaws.com/1689018585-816JLxXG3YL.jpg?crop=1xw:1xh;center,top&resize=980:*',
    'https://hips.hearstapps.com/vader-prod.s3.amazonaws.com/1689018684-91q62eNpqGL.jpg?crop=1xw:1xh;center,top&resize=980:*',
    'https://hips.hearstapps.com/vader-prod.s3.amazonaws.com/1689018725-81N-xC3Se6L.jpg?crop=1xw:1xh;center,top&resize=980:*',
    'https://hips.hearstapps.com/vader-prod.s3.amazonaws.com/1689018773-91fqdoW5QzL.jpg?crop=1xw:1xh;center,top&resize=980:*',
    'https://hips.hearstapps.com/vader-prod.s3.amazonaws.com/1689020220-9102oXzvz1L.jpg?crop=1xw:1xh;center,top&resize=980:*',
    'https://hips.hearstapps.com/vader-prod.s3.amazonaws.com/1688059089-81UOA8fDGaL.jpg?crop=1xw:1xh;center,top&resize=980:*',
    'https://hips.hearstapps.com/vader-prod.s3.amazonaws.com/1689020333-61lwEOkIKHL.jpg?crop=1xw:1xh;center,top&resize=980:*',
    'https://hips.hearstapps.com/vader-prod.s3.amazonaws.com/1689020497-61MSV64Sl6L.jpg?crop=1xw:1xh;center,top&resize=980:*',
    'https://hips.hearstapps.com/vader-prod.s3.amazonaws.com/1689020549-61L-Bf01LAL.jpg?crop=1xw:1xh;center,top&resize=980:*',
    'https://hips.hearstapps.com/vader-prod.s3.amazonaws.com/1689020709-91gOB5yRilL.jpg?crop=1xw:1xh;center,top&resize=980:*',
    'https://m.media-amazon.com/images/I/41mjffV8MPL._SY445_SX342_.jpg'
]



class KenyaPhoneNumberProvider(Provider):
    """
    A Provider for phone number.
    """

    def kenya_phone_number(self):
        return f'+254 {self.msisdn()[3:]}'


def main():
    fake = Faker()
    fake.add_provider(KenyaPhoneNumberProvider)
    return fake.kenya_phone_number()

# Create sample data using Faker to seed the database
def seed_data():
    # Create admins
    admins = []
    for _ in range(10):
        admin = Admin(
            Username=fake.user_name(),
            Password=fake.password(),
            Email=fake.email(),
            Full_Name=fake.name(),
            Phone_Number=main()
        )
        admins.append(admin)
        db.session.add(admin)

    # Create users
    users = []
    for _ in range(10):
        user = User(
            Username=fake.user_name(),
            Password=fake.password(),
            Email=fake.email(),
            Full_Name=fake.name(),
            Phone_Number=main()
        )
        users.append(user)
        db.session.add(user)

    # Create books
    books = []
    for _ in range(10):
        book = Book(
            Book_Image= random.choice(book_images),
            Title=fake.sentence(nb_words=3, variable_nb_words=True, ext_word_list=None),
            Author=fake.name(),
            Genre=fake.random_element(elements=('Fiction', 'Non-Fiction', 'Mystery', 'Romance', 'Science Fiction', 'Fantasy')),
            Description=fake.text(),
            Price=random.randint(5, 20),
            Date_Uploaded=datetime.now()
        )
        books.append(book)
        db.session.add(book)

    # Create book orders
    book_orders = []
    for _ in range(10):
        book_order = BookOrder(
            UserID=random.randint(1, 10),
            AdminID=random.randint(1, 10),
            BookID=random.randint(1, 10),
            Status=fake.random_element(elements=('Approved', 'Rejected', 'Pending')),
        )
        book_orders.append(book_order)
        db.session.add(book_order)

    # Create book lending requests
    book_lending_requests = []
    for _ in range(10):
        book_lending_request = BookLendingRequest(
            UserID=random.randint(1, 10),
            AdminID=random.randint(1, 10),
            BookID=random.randint(1, 10),
            Status=fake.random_element(elements=('Approved', 'Rejected', 'Pending')),
        )
        book_lending_requests.append(book_lending_request)
        db.session.add(book_lending_request)

    # Create carts
    carts = []

    for _ in range(10):
        cart = Cart(
            UserID=random.randint(1, 10),
            AdminID=random.randint(1, 10),
            Cart_Type=random.choice(['Purchase', 'Lending'])
                
        )

        carts.append(cart)
        db.session.add(cart)
       
    # Create cart items
    cart_items = []
    for _ in range(10):
        cart_item = CartItem(
            CartID=random.randint(1, 10),
            BookID=random.randint(1, 10),
            Quantity=random.randint(1, 10)
        )
        cart_items.append(cart_item)
        db.session.add(cart_item)

    # Create purchases
    purchases = []
    for _ in range(10):
        purchase = Purchase(
            UserID=random.randint(1, 10),
            AdminID=random.randint(1, 10),
            OrderID=random.randint(1, 10),
            Total_Amount=random.randint(5, 200),
            Purchase_Date=datetime.now()
        )
        purchases.append(purchase)
        db.session.add(purchase)

    # Create return requests
    return_requests = []
    for _ in range(10):
        return_request = ReturnRequest(
            UserID=random.randint(1, 10),
            AdminID=random.randint(1, 10),
            OrderID=random.randint(1, 10),
            Return_Reason=fake.random_element(elements=('Finished Reading', 'Lending period expired', 'Got bored of the book')),
            Status=fake.random_element(elements=('Approved', 'Pending')),
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
