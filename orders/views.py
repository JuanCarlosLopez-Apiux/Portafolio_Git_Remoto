from django.shortcuts import render
from carts.utils import get_or_create_cart, get_or_create_Tarjeta_Credito
from .models import Order
from django.contrib.auth.decorators import login_required
from .utils import breadcrumb
from carts.models import Tarjeta_Credito
# Create your views here.

@login_required(login_url='login')
def order(request):
    cart = get_or_create_cart(request)
    tarjeta = get_or_create_Tarjeta_Credito(request)
    #usamos filter y no get por el probema del try exeption de la otra vez
    #order = Order.objects.filter(cart=cart).first()
    #ahora llamo a Order con el propety que defini
    print(cart.total)
    order = Order.objects.create(cart=cart, user=request.user, total=int(cart.total * 1.19))
    #me = User.get_or_create_Tarjeta_.get(u_id_cliente='ola')
    #creando una orden
    #if order is None and request.user.is_authenticated:
        #total = int(cart.total * 1.19)
        #print(total)
        #order = Order.objects.create(cart=cart, user=request.user, total=total)
    if order:
        request.session['order_id'] = order.order_id
    print('Este es cart de order', cart)
    ultimos = str(tarjeta)[24:]
    ult = str(ultimos)[:12]
    print('Este es la tarjeta de user', ult)
    current_user = request.user
    print('Este es el user', current_user.id)
    return render(request, 'orders/order.html', {
        'cart': cart,
        'order': order,
        'tarjeta': tarjeta,
        'ultimos': ult,
        'breadcrumb': breadcrumb()
    })