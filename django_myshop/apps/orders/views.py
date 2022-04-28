from django.shortcuts import render

# Create your views here.
from django_myshop.apps.cart.cart import Cart
from django_myshop.apps.orders.forms import OrderCreateForm
from django_myshop.apps.orders.models import OrderItem
from .tasks import order_created

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])

            cart.clear()
            order_created.delay()
            return render(request, 'orders/order/created.html', {'order':order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart':cart, 'form':form})

