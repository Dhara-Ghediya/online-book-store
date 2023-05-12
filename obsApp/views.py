from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .models import UserModel, BookDetails
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'index.html')

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

def userLogin(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        password = request.POST.get('password')
        login = UserModel.objects.filter(username=uname, password=password)
        if login:
            messages.success(request, "Login Successfully!")
            return redirect('view_book_list')
    return render(request, 'UserLogin.html')

def adminLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_menu')
    return render(request, 'AdminLogin.html')

def viewBookList(request):
    all_books = BookDetails.objects.all()
    if request.method == 'POST':
        pass
    return render(request, 'ViewBooks.html', {"all_books":all_books})

def adminMenu(request):
    return render(request, 'adminMenu.html')

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
    
def add_to_cart(request):
    pass

def removeBook(request):
    if request.method == 'POST':
        code = request.POST.get('barcode')
        obj = BookDetails.objects.get(book_code=code)
        print("123",obj.book_code)
        obj.delete()
        return redirect('admin_menu')
    return render(request, 'RemoveBooks.html')