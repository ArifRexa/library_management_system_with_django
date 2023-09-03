from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import login, logout, authenticate
from orders.models import Order, OrderProduct
from django.core.exceptions import ObjectDoesNotExist
from wishlist.models import Cart, CartItem


def get_create_session(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key
def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('cart')
    return render(request, 'register.html', {'form':form})

def profile(request):
    return render(request, 'dashboard.html')



def user_login(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=user_name, password=password)
        print(user)
        # ekhono login hoy nai
        session_key = get_create_session(request)
        
        try:
            cart = Cart.objects.get(cart_id=session_key)
            is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
            if is_cart_item_exists:
                cart_item = CartItem.objects.filter(cart=cart)
                for item in cart_item:
                    item.user = user
                    item.save()
        except Cart.DoesNotExist:
            cart = None
        
        login(request, user)
        
        # login hoye geche
        
        return redirect('profile')
    return render(request, 'signin.html')

def user_logout(request):
    logout(request)
    return redirect('login')



def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity

    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
    }
    return render(request, 'accounts/order_detail.html', context)