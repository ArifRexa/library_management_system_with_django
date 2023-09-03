from django.contrib import admin
from . models import Books, ReviewRating
# Register your models here.
# admin.site.register(Product)

class ProductAdmin(admin.ModelAdmin): 
     list_display = [ 'id' , 'book_title', 'author', 'isbn', 'genre', 'price','stock' ,'publication_date', 'modified_date', 'is_available']
     
     prepopulated_fields = {'slug' : ('book_title',)}
     
admin.site.register(Books, ProductAdmin)
admin.site.register(ReviewRating)