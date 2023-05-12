from django.contrib import admin
from .models import UserModel, BookDetails

class UserModelAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name", "email_id", "phone_no"]
admin.site.register(UserModel, UserModelAdmin)

class BookDetailsAdmin(admin.ModelAdmin):
    list_display = ["book_code", "book_name", "book_type", "price", "quantity"]
admin.site.register(BookDetails, BookDetailsAdmin)