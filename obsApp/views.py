from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .models import UserModel, BookDetails, AddToCart, LikedBooks, Rating
from django.http import HttpResponse,JsonResponse

# Create your views here.
############# Home Page ##############
def home(request):
    user = request.session.get('userlogin', '') 
    return render(request, 'index.html', {"user":user})

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
        
        if len(phone) == 10:
            # obj = UserModel.objects.filter(email_id=email)
            # if obj:
            #     messages.warning(request, "You are already registered! Please, Use different Username and Email Address!")
            # else:
            register = UserModel(username=uname, password=password, first_name=fname, last_name=lname, address=address, phone_no=phone, email_id=email)
            try:
                register.save()
                messages.success(request, "Register Successfully! Now, You have to login...")
                return redirect('home')
            except Exception as e:
                messages.warning(request, e)
        else:
            messages.warning(request, "Entered Mobile number not have 10 digits!")
                
        
    return render(request, 'UserRegister.html')

############# User Login Page ##############
def userLogin(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        
        password = request.POST.get('password')
        login = UserModel.objects.filter(username=uname, password =password)
        print(login)
        if login:
        # if login.password == password:
            request.session['userlogin'] = uname
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
    if 'userlogin' in request.session.keys():
        all_books = BookDetails.objects.all()
        all_rating = Rating.objects.all()
        
        for book in all_books:
            total = 0
            count = 0
            for rate in all_rating:
                if rate.book_id.book_name == book.book_name:
                    total += rate.rating
                    count += 1
            if count != 0:
                avg = total/count
            else:
                avg = 0
            book.rating = avg
            book.count = count
        user = request.session.get('userlogin', '')
        return render(request, 'ViewBooks.html', {"all_books":all_books, "user":user})
    messages.info(request, "You can't see List of All Books without Login!")
    return redirect('home')

############# Rating of Books ##############
def rating(request):
    id = request.GET.get('id')
    rating = request.GET.get('rating')
    user = UserModel.objects.get(username = request.session.get('userlogin'))
    book = BookDetails.objects.get(id=id)
    check=Rating.objects.filter(user_id=user,book_id=book)
    if len(check) == 0:
        print("if")
        obj = Rating(user_id=user, book_id=book, rating=rating)
        obj.save()
    else:
        print("else")
        check.update(rating=rating)
    return JsonResponse({'status':True})

############# Menu for Admin ##############
def adminMenu(request):
    if 'adminlogin' in request.session.keys():
        return render(request, 'adminMenu.html')
    messages.warning(request, "You can't see this page coz You are not Admin!")
    return redirect('home')

def showBooksListForAdmin(request):
    if 'adminlogin' in request.session.keys():
        all_books = BookDetails.objects.all()
        admin = request.session.get('adminlogin', '')
        return render(request, 'adminShow.html', {"all_books":all_books, "admin":admin })
    messages.warning(request, "You can't see this page coz You are not Admin!")
    return redirect('home')

############# Add New Book ##############
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

############# Detail view for Perticular Book ##############
def detailsView(request, id):
    print(id)
    obj = BookDetails.objects.get(id=id)
    if obj:
        return render(request, 'detailView.html', {"bookdetail": obj})
    else:
        print("6666")
        return redirect('view_book_list')
    
############# Add Book in to Cart ##############
def add_to_cart(request, id):
    user = request.session['userlogin']
    book = BookDetails.objects.get(id=id)
    # obj = AddToCart(user = user, book=book)
    obj = AddToCart.objects.get_or_create(user=user, book=book)
    if obj:
        # obj.save()
        # messages.info(request, "your book added in Add to Cart Successfully! ")
        return redirect('view_book_list')
    messages.info(request, "Book is already added in Cart! ")
    return redirect('view_book_list')

############# View Cart ##############
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

############# Remove Book from Database ##############
def removeBook(request, code):
    obj = BookDetails.objects.get(book_code=code)
    obj.delete()
    return redirect('admin_show')

############# Remove Book from Cart ##############
def removeBookFromCart(request, code):
    user = request.session['userlogin']
    obj = AddToCart.objects.filter(user = user, book__book_code = code)
    obj.delete()
    return redirect('view_cart')

############# Add Book into like page ##############
def likedBook(request, id):
    user = UserModel.objects.get(username = request.session['userlogin'])
    book = BookDetails.objects.get(id=id)
    
    obj = LikedBooks.objects.get_or_create(username=user, book=book)
    if obj:
        # messages.warning(request, "book already liked!")
        # return redirect('view_book_list')
    # obj = LikedBooks(username = user, book=book)
    # obj.save()
    # else:
        # like = LikedBooks()
        return redirect('view_book_list')

############# View List of Books ##############
def viewLikedBooks(request):
    user = UserModel.objects.get(username = request.session['userlogin'])
    liked = LikedBooks.objects.filter(username=user)
    return render(request, 'viewLikedBooksList.html', {'liked_books': liked })

############# Remove Book from Like page ##############
def removeFromLike(request):
    if request.method == "POST":
        user = UserModel.objects.get(username = request.session['userlogin'])
        code = request.POST.get('code')
        
        obj = LikedBooks.objects.filter(username = user, book__book_code = code)
        obj.delete()
        return redirect('view_liked_books')

############# Available Books in store ##############
def availableBooks(request):
    books = BookDetails.objects.all()
    print(books)
    return render(request, 'availableBooks.html', {'books':books})

############# Logout User ##############
def logout(request):
    request.session.flush()
    request.session.clear_expired()
    return redirect('home')