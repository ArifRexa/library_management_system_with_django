from django.db import models
from django.contrib.auth.models import User
from library.models import Books

# Create your models here.




class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    order_number = models.CharField(max_length=30)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    email = models.EmailField(max_length=50)
    address_line1 = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    order_note = models.CharField(max_length=100)
    
    status = models.CharField(max_length=10, choices = STATUS, default='New')
    ip = models.CharField(max_length=100, blank=True, null = True)
    
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.first_name


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete= models.CASCADE)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    product = models.ForeignKey(Books, on_delete= models.CASCADE)
    quantity = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.book_title


