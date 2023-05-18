from django.db import models

# Create your models here.
class UserModel(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=25)
    first_name = models.TextField()
    last_name = models.TextField()
    address = models.TextField()
    phone_no = models.IntegerField()
    email_id = models.EmailField(max_length=100, null=False, unique=True)
    
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
    
class AddToCart(models.Model):
    user = models.CharField(max_length=100)
    book = models.ForeignKey(BookDetails, on_delete=models.CASCADE)
    same_book_count = models.IntegerField(default=1)
    
class LikedBooks(models.Model):
    username = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    book = models.ForeignKey(BookDetails, on_delete=models.CASCADE)
    
class Rating(models.Model):
    class Meta:
        unique_together = (('user_id', 'book_id'))
    user_id = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    book_id = models.ForeignKey(BookDetails, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)