from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .models import UserModel, BookDetails, AddToCart
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
    obj = AddToCart(user = user, book=book)
    obj.save()
    messages.info(request, "your book added in Add to Cart Successfully! ")
    return redirect('view_book_list')

def viewCart(request):
    user = request.session['userlogin']
    cart_detail = AddToCart.objects.all()
    count = 0
    total_amount = 0
    for item in cart_detail:
        total_amount += item.book.price
        count += 1
    return render(request, 'viewCart.html', {"user": user, "cart_detail":cart_detail, "count": count, "total_amount": total_amount})

def removeBook(request):
    if request.method == 'POST':
        code = request.POST.get('barcode')
        obj = BookDetails.objects.get(book_code=code)
        print("123",obj.book_code)
        obj.delete()
        return redirect('admin_menu')
    return render(request, 'RemoveBooks.html')

def removeBookFromCart(request):
    if request.method == "POST":
        code = request.POST.get('code')
        
        obj = AddToCart.objects.get(book__book_code = code)
        obj.delete()
        return redirect('view_cart')

def logout(request):
    request.session.flush()
    request.session.clear_expired()
    return redirect('home')