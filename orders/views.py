from django.shortcuts import render, redirect
from wishlist.models import Cart, CartItem
from .forms import OrderForm
from .models import  OrderProduct, Order
from library.models import Books
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch') 
def success_view(request):
    data = request.POST
    print('data -------', data)
    user_id = int(data['value_b'])  
    user = User.objects.get(pk=user_id)
    
    
    # working with order model
    order = Order.objects.get(user=user, is_ordered=False, order_number=data['value_a'])
    order.is_ordered = True
    order.save()
    cart_items = CartItem.objects.filter(user = user)
    
    for item in cart_items:
        orderproduct = OrderProduct()
        product = Books.objects.get(id=item.product.id)
        orderproduct.order = order
        orderproduct.user = user
        orderproduct.product = product
        orderproduct.quantity = item.quantity
        orderproduct.ordered = True
        orderproduct.save()
        product.stock -= item.quantity 
        product.save()

    # Clear cart
    CartItem.objects.filter(user=user).delete()
    return redirect('cart')
    



def order_complete(request):
    return render(request, 'orders/order_complete.html')





def place_order(request):
    print(request.POST)
    cart_items = None
    
    cart_items = CartItem.objects.filter(user = request.user.id)
    
    if cart_items.count() < 1:
        return redirect('library')
    
    print(cart_items)  
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.ip = request.META.get('REMOTE_ADDR')
            saved_instance = form.save()  
            form.instance.order_number = saved_instance.id
            form.save()
           

    return render(request, 'orders/place-order.html',{'cart_items' : cart_items})