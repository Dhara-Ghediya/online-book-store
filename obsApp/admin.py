from django.contrib import admin
from .models import UserModel, BookDetails, AddToCart, LikedBooks, Rating

class UserModelAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name", "email_id", "phone_no"]
admin.site.register(UserModel, UserModelAdmin)

class BookDetailsAdmin(admin.ModelAdmin):
    list_display = ["book_code", "book_name", "book_type", "price", "quantity"]
admin.site.register(BookDetails, BookDetailsAdmin)

class AddToCartAdmin (admin.ModelAdmin):
    list_display = ["user"]
admin.site.register(AddToCart, AddToCartAdmin)

class LikedBooksAdmin (admin.ModelAdmin):
    list_display = ["username"]
admin.site.register(LikedBooks, LikedBooksAdmin)

class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'book_id', 'rating']
admin.site.register(Rating, RatingAdmin)