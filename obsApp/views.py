from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .models import UserModel, BookDetails, AddToCart, LikedBooks
from django.http import HttpResponse

# Create your views here.
############# Home Page ##############
def home(request):
    return render(request, 'index.html')

############# User Registration Page ##############
def userRegistration(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        password = request.POST.get('password')
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        email = request.POST.get('mailid')
        
        register = UserModel(username=uname, password=password, first_name=fname, last_name=lname, address=address, phone_no=phone, email_id=email)
        register.save()
        messages.success(request, "Register Successfully! Now, You have to login...")
        return redirect('home')
    return render(request, 'UserRegister.html')

############# User Login Page ##############
def userLogin(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        request.session['userlogin'] = uname
        password = request.POST.get('password')
        login = UserModel.objects.filter(username=uname, password=password)
        if login:
            messages.success(request, "Login Successfully!")
            return redirect('view_book_list')
        messages.info(request, "You are not registered user!")
    if 'userlogin' not in request.session.keys():
        # print(request.session['userlogin'])
        # messages.warning(request, "First you have to logout your account!")
        return render(request, 'UserLogin.html')
    messages.warning(request, "First you have to logout!")
    return redirect('home')

############# Admin Login Page ##############
def adminLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        request.session['adminlogin'] = username
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_menu')
    return render(request, 'AdminLogin.html')

############# SHow All Books List Page ##############
def viewBookList(request):
    if 'userlogin' in request.session.keys() or 'adminlogin' in request.session.keys():
        all_books = BookDetails.objects.all()
        return render(request, 'ViewBooks.html', {"all_books":all_books})
    messages.info(request, "You can't see List of All Books without Login!")
    return redirect('home')

############# Menu for Admin ##############
def adminMenu(request):
    if 'adminlogin' in request.session.keys():
        return render(request, 'adminMenu.html')
    messages.warning(request, "You can't see this page coz You are not Admin!")
    return redirect('home')

def addBook(request):
    if request.method == 'POST':
        code = request.POST.get('barcode')
        name = request.POST.get('name')
        type = request.POST.get('type')
        author = request.POST.get('author')
        price = request.POST.get('price')
        qnty = request.POST.get('quantity')
        img = request.FILES.get('img')
        
        if img is not None:
            book = BookDetails(book_code=code, book_name=name, book_type=type, author_name=author, price=price, quantity=qnty, book_img=img)
            if book:
                # Save the uploaded image to a file storage
                fs = FileSystemStorage()
                filename = fs.save(img.name, img)
                uploaded_img_url = fs.url(filename)
                book.book_img = uploaded_img_url
                book.save()
                messages.success(request, "Book added Successfully!")
                return redirect('add_book')
    return render(request, 'AddBook.html')

def detailsView(request, id):
    print(id)
    obj = BookDetails.objects.get(id=id)
    if obj:
        return render(request, 'detailView.html', {"bookdetail": obj})
    else:
        print("6666")
        return redirect('view_book_list')
    
def add_to_cart(request, id):
    user = request.session['userlogin']
    book = BookDetails.objects.get(id=id)
    # obj = AddToCart(user = user, book=book)
    obj = AddToCart.objects.get_or_create(user=user, book=book, same_book_count=1)
    if obj:
        # obj.save()
        # messages.info(request, "your book added in Add to Cart Successfully! ")
        return redirect('view_book_list')
    messages.info(request, "Book is already added in Cart! ")
    return redirect('view_book_list')

def viewCart(request):
    user = request.session['userlogin']
    cart_detail = AddToCart.objects.filter(user = user)
    print(cart_detail)
    count = 0
    total_amount = 0
    if request.method == 'POST':
        b_code = request.POST.get('code')
        same_books = request.POST.get('number')
        print("same", same_books)
        # AddToCart.objects.filter(user = user, book__book_code = b_code).update(same_book_count=same_books)
        obj = AddToCart.objects.filter(user = user, book__book_code = b_code)
        print(obj)
        if same_books == "0":
            print("*963")
            obj.delete() 
            messages.success(request, "Item removed from cart.")
        else:
            AddToCart.objects.filter(user = user, book__book_code = b_code).update(same_book_count=same_books)
            messages.success(request, "Cart updated successfully.")
    for item in cart_detail:
        total_amount += item.book.price * item.same_book_count
        count += item.same_book_count
    return render(request, 'viewCart.html', {"user": user, "cart_detail": cart_detail, "count": count, "total_amount": total_amount})

def removeBook(request):
    if request.method == 'POST':
        code = request.POST.get('barcode')
        obj = BookDetails.objects.get(book_code=code)
        obj.delete()
        return redirect('admin_menu')
    return render(request, 'RemoveBooks.html')

def removeBookFromCart(request, code):
    user = request.session['userlogin']
    obj = AddToCart.objects.filter(user = user, book__book_code = code)
    obj.delete()
    return redirect('view_cart')

def likedBook(request, id):
    user = UserModel.objects.get(username = request.session['userlogin'])
    book = BookDetails.objects.get(id=id)
    
    obj = AddToCart.objects.get_or_create(user=user, book=book)
    if obj:
    # obj = LikedBooks(username = user, book=book)
    # obj.save()
        return redirect('view_book_list')

def viewLikedBooks(request):
    user = UserModel.objects.get(username = request.session['userlogin'])
    liked = LikedBooks.objects.filter(username=user)
    return render(request, 'viewLikedBooksList.html', {'liked_books': liked })

def removeFromLike(request):
    if request.method == "POST":
        user = UserModel.objects.get(username = request.session['userlogin'])
        code = request.POST.get('code')
        
        obj = LikedBooks.objects.filter(username = user, book__book_code = code)
        obj.delete()
        return redirect('view_liked_books')

def availableBooks(request):
    books = BookDetails.objects.all()
    print(books)
    return render(request, 'availableBooks.html', {'books':books})

def logout(request):
    request.session.flush()
    request.session.clear_expired()
    return redirect('home')