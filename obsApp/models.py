from django.db import models

# Create your models here.
class UserModel(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=25)
    first_name = models.TextField()
    last_name = models.TextField()
    address = models.TextField()
    phone_no = models.IntegerField()
    email_id = models.EmailField(max_length=100, null=False)
    
    def __str__(self):
        return self.username
    
class BookDetails(models.Model):
    book_code = models.IntegerField(unique=True)
    book_name = models.TextField()
    book_type = models.CharField(max_length=100)
    author_name = models.CharField(max_length=100)
    price = models.IntegerField()
    quantity = models.IntegerField()
    book_img = models.ImageField(upload_to='images')
    
    def __str__(self):
        return self.book_name