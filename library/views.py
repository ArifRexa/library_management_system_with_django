from django.shortcuts import render, get_object_or_404, redirect
from .models import Books, ReviewRating
from category.models import Category
from django.core.paginator import Paginator
from django.db.models import Q

from .forms import ReviewForm

# Create your views here.
def library(request, category_slug=None):
    if category_slug : 
        category = get_object_or_404(Category, slug = category_slug)
        products = Books.objects.filter(is_available = True, genre=category) 
        page = request.GET.get('page')
        print(page)
        paginator = Paginator(products, 2) 
        paged_product = paginator.get_page(page)
    else : 
        products = Books.objects.filter(is_available = True) # all products
        paginator = Paginator(products, 3) 
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
       
    categories = Category.objects.all()
    # print(categories)
    context = {'products' : paged_product, 'categories' : categories, }
    return render(request, 'library.html', context)

# def book_detail(request, category_slug, product_slug):
#     single_product = Books.objects.get(slug = product_slug, category__slug = category_slug)
#     reviews = ReviewRating.objects.filter(product=single_product, status=True)
#     print('single product ', single_product)
    
#     return render(request, 'book_detail.html', {'product' : single_product, 'reviews' : reviews})


def book_detail(request, category_slug, product_slug):
    single_product = get_object_or_404(Books, slug=product_slug)
    reviews = ReviewRating.objects.filter(product=single_product, status=True)
    print(reviews)
    
    return render(request, 'book_detail.html', {'product': single_product, 'reviews': reviews})









def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            data = ReviewRating()
            data.subject = form.cleaned_data['subject']
            data.rating = form.cleaned_data['rating']
            data.review = form.cleaned_data['review']
            data.product_id = product_id
            data.user = request.user
            data.save()
            return redirect(url)
        # try:
        #     product = Books.objects.get(id = product_id)
        #     reviews = ReviewRating.objects.get(user = request.user, product = product)
        #     form = ReviewForm(request.POST, instance = reviews)
        #     form.save()
        #     return redirect('cart')
        # except ReviewRating.DoesNotExist:
        #     form = ReviewForm(request.POST)
        #     if form.is_valid():
        #         data = ReviewRating()
        #         data.subject = form.cleaned_data['subject']
        #         data.rating = form.cleaned_data['rating']
        #         data.review = form.cleaned_data['review']
        #         data.product_id = product_id
        #         data.user = request.user
        #         data.save()
        #         return redirect(url)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Books.objects.order_by('-publication_date').filter(Q(description__icontains=keyword) | Q(book_title__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'p_count': product_count,
    }
    return render(request, 'library.html', context)