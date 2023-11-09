from Models import Book, BookLendingRequest, BookOrder, Admin, User, Cart, CartItem, Purchase, ReturnRequest

def book_response_serializer(books: Book):
    # get all books
    response = []
    for book in books:
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
        response.append(book_dict)
    return response

def book_price_serializer(books: Book):
    response = []
    for book in books:
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
        response.append(book_dict)
    return response

def book_genre_serializer(books: Book):
    response = []
    for book in books:
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
        response.append(book_dict)
    return response
    
def book_title_serializer(books: Book):
    response = []
    for book in books:
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
        response.append(book_dict)
    return response

def book_date_uploaded_serializer(books: Book):
    response = []
    for book in books:
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
        response.append(book_dict)
    return response
    
def book_purchase_serializer(book_purchases: Purchase):
    # get all book purchases
    response = []
    for book_purchase in book_purchases:
        book_purchase_dict = {
            "PurchaseID": book_purchase.PurchaseID,
            "UserID": book_purchase.UserID,
            "AdminID": book_purchase.AdminID,
            "OrderID": book_purchase.OrderID, 
            "Total_Amount": book_purchase.Total_Amount
        }
        response.append(book_purchase_dict)
    return response

def book_lending_serializer(book_lendings: BookLendingRequest):
    # get all book lendings
    response = []
    for book_lending in book_lendings:
        book_lending_dict = {
            "RequestID": book_lending.RequestID,
            "UserID": book_lending.UserID,
            "AdminID": book_lending.AdminID,
            "BookID": book_lending.BookID, 
            "Status": book_lending.Status
        }
        response.append(book_lending_dict)
    return response

def book_return_request_serializer(book_return_requests: ReturnRequest):
      # get all return requests
    response = []
    for book_return_request in book_return_requests:
        book_return_request_dict = {
            "RequestID": book_return_request.RequestID,
            "UserID": book_return_request.UserID,
            "AdminID": book_return_request.AdminID,
            "OrderID": book_return_request.OrderID,
            "Return_Reason": book_return_request.Return_Reason,
            "Status": book_return_request.Status
        }
        response.append(book_return_request_dict)
    return response

def user_serializer(users: User):
      # get all users
    response = []
    for user in users:
        user_dict = {
            "UserID": user.UserID,
            "Username": user.Username,
            "Password": user.Password,
            "Email": user.Email,
            "Full_Name": user.Full_Name,
            "Phone_Number": user.Phone_Number
        }
        response.append(user_dict)
    return response

def cart_serializer(carts: Cart):
    response = []

    for cartt in carts:
        cart_dict = {
            "CartID": cartt.CartID,
            "UserID": cartt.UserID,
            "AdminID": cartt.AdminID,
            "Cart_Type": cartt.Cart_Type
        }
        response.append(cart_dict)
    return response

def cart_item_serializer(cartitems: CartItem):
    response = []

    for cartitemm in cartitems:
        cart_item_dict = {
            "CartItemID": cartitemm.CartItemID,
            "CartID": cartitemm.CartID,
            "BookID": cartitemm.BookID,
            "Quantity": cartitemm.Quantity
        }
        response.append(cart_item_dict)
    return response

def book_order_serializer(bookorders: BookOrder):
    response = []

    for bookorderr in bookorders:
        book_order_dict = {
            "OrderID": bookorderr.OrderID,
            "UserID": bookorderr.UserID,
            "AdminID": bookorderr.AdminID,
            "BookID": bookorderr.BookID,
            "Status": bookorderr.Status
        }
        response.append(book_order_dict)
    return response

def admin_serializer(admins: Admin):
    response = []

    for admin in admins:
        admin_dict = {
            "AdminID": admin.AdminID,
            "Username": admin.Username,
            "Password": admin.Password,
            "Email": admin.Email,
            "Full_Name": admin.Full_Name,
            "Phone_Number": admin.Phone_Number
        }
        response.append(admin_dict)
    return response