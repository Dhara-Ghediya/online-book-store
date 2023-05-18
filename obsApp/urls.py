from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('user-register', views.userRegistration, name="user_register"),
    path('user-login', views.userLogin, name="user_login"),
    path('view-book-list', views.viewBookList, name="view_book_list"),
    path('admin-login', views.adminLogin, name="admin_login"),
    path('admin-menu', views.adminMenu, name="admin_menu"),
    path('add-book', views.addBook, name='add_book'),
    path('detail-view/<id>', views.detailsView, name="details_view"),
    path('add-to-cart/<id>', views.add_to_cart, name="add_to_cart"),
    path('remove-book/<code>', views.removeBook, name="remove_book"),
    path('logout', views.logout, name="logout"), 
    path('view-cart', views.viewCart, name="view_cart"), 
    path('remove-book-from-cart/<code>', views.removeBookFromCart, name="remove_book_from_cart"),
    path('liked-books/<id>', views.likedBook, name="liked_books"), 
    path('view-liked-books', views.viewLikedBooks, name="view_liked_books"),
    path('remove-from-like', views.removeFromLike, name="remove_from_like"), 
    path('available-books', views.availableBooks, name="available_books"),
    path('rating', views.rating, name="rating"), 
    path('admin-show', views.showBooksListForAdmin, name="admin_show")
    
    
] +static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


