from .models import Cart, Tarjeta_Credito
from users.models import User
from datetime import date, datetime

def get_or_create_cart(request):
    user = request.user if request.user.is_authenticated else None
    cart_id = request.session.get('cart_id') #Retorna un none en caso de que la llave no exista
    cart = Cart.objects.filter(cart_id=cart_id).first()

    if cart is None:
        cart = Cart.objects.create(user=user)

    if user and cart.user is None:
        cart.user = user
        cart.save()

    request.session['cart_id'] = cart.cart_id

    return cart
    
def get_or_create_Tarjeta_Credito(request):
    current_user = request.user #Retorna un none en caso de que la llave no exista
    tarjeta = Tarjeta_Credito.objects.filter(u_id_cliente_id=current_user.id).first()

    return tarjeta
    
def days_between(d1, d2):
       d1 = datetime.strptime(d1, "%Y-%m-%d")
       d2 = datetime.strptime(d2, "%Y-%m-%d")
       return abs((d2 - d1).days)
    