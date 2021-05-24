from django.shortcuts import render
from products.models import Product
from django.shortcuts import redirect, get_object_or_404
from .models import Cart, Tour, Transporte, Servicios_Extra
from .utils import get_or_create_cart, days_between
from .models import CartProducts
from datetime import date, datetime
from tiendovirtual.forms import CrearCarritoForm
import decimal

# Create your views here.
def index(request, slug):
    cart = get_or_create_cart(request)
    print(cart)
    sino = None
    print(slug)
    product = Product.objects.filter(slug=slug).first()
    cart_product = CartProducts.objects.filter(cart=cart, product=product).first()
    print(product)
    form = CrearCarritoForm(request.POST or None)
    
    if cart_product:
        sino = "SI"
        print(sino)
    else:
        sino = "NO"
        print(sino)
    return render(request, 'products/product.html', {
        #contexto
        'product': product,
        'form': form,
        'sino':sino
        })

def add(request):
    if request.method == 'POST':
        cart = get_or_create_cart(request)
        product = get_object_or_404(Product, pk=request.POST.get('product_id'))
        inicio = request.POST.get('fecha_inicio')
        termino = request.POST.get('fecha_termino')
        ninios = request.POST.get('cant_ninios')
        adultos = request.POST.get('cant_adultos')
        dias = days_between(inicio, termino)
        dias = dias + 1
        subtotal = product.price * dias
        total = int(subtotal * 1.05)
        cart.subtotal = cart.subtotal + subtotal
        cart.total = cart.total +total
        print(dias)
        cart_product = CartProducts(cart=cart, product=product, fecha_inicio=inicio, fecha_termino=termino, quantity=dias, cant_ninios=ninios, cant_adultos=adultos)
        cart_product.save()
        cart.save()
        servicio = Servicios_Extra(monto_servicio= 0, desc_servicio="Transporte", estado_servicio="", fecha_servicio="2020-01-01", a_id_cartproduct=cart_product, horario_servicio="00:00", t_id_transporte=None, t_id_tour= None, t_id_cart=cart)
        servicio.save()
        servicio2 = Servicios_Extra(monto_servicio= 0, desc_servicio="Tour", estado_servicio="", fecha_servicio="2020-01-01", a_id_cartproduct=cart_product, horario_servicio="00:00", t_id_transporte=None, t_id_tour= None, t_id_cart=cart)
        servicio2.save()
        product = Product.objects.get(pk=request.POST.get('product_id'))
        # si esa llave no existe, el valor de la llave será uno por default de productos
        #esta forma de agregar no esta BIEN PORQUE CADA VEZ QUE AGREGO NUEVOS NO SE ACTUALIZA, SOLO LOS QUE ENVIE EN EL MOMENTO
        #cart.products.add(product, through_defaults={
        #    'quantity': quantity
        #    
        #})
        #'product_id' es el nombre del formulario html donde obtiene el id del producto
        
        #cart es una instacia del modelo por lo que para acceder a atributo products es la relacion ManytoMany
        
        
        return render(request, 'carts/add.html', {
            'inicio': inicio,
            'termino':termino,
            'product': product,
            'cp': cart_product
        })

    #estos nombres son los nombres del formulario los que obtiene el request
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))
    # si esa llave no existe, el valor de la llave será uno por default de productos
    #esta forma de agregar no esta BIEN PORQUE CADA VEZ QUE AGREGO NUEVOS NO SE ACTUALIZA, SOLO LOS QUE ENVIE EN EL MOMENTO
    #cart.products.add(product, through_defaults={
    #    'quantity': quantity
    #    
    #})
    #'product_id' es el nombre del formulario html donde obtiene el id del producto
    product = Product.objects.get(pk=request.POST.get('product_id'))
    #cart es una instacia del modelo por lo que para acceder a atributo products es la relacion ManytoMany
    cart.products.add(product)

    return render(request, 'carts/add.html', {
        'product': product,
        'cp': cart_product
    })
    
def cart(request):
    cart = get_or_create_cart(request)
    serv = Servicios_Extra.objects.filter(t_id_cart=cart)
    
    return render(request, 'carts/cart.html', {
        #mandando el objeto cart al template
        'cart':cart,
        'servicios':serv
    })

def remove(request):
    cart = get_or_create_cart(request)
    tours = Tour.objects.all().order_by('-id_tour')
    transportes = Transporte.objects.all().order_by('-id_transporte')
    #'product_id' es el nombre del formulario html donde obtiene el id del producto
    product_id = request.POST.get('product_id')
    cartproduct_id = request.POST.get('cartproduct_id')
    product = Product.objects.get(slug=product_id)
    print(product)
    cartproduct = CartProducts.objects.get(id=cartproduct_id)
    print(cartproduct)
    subtotal = product.price * int(cartproduct.quantity)
    total = int(subtotal * 1.05)
    cart.subtotal = cart.subtotal - subtotal
    cart.total = cart.total - total
    cart.save()
    ser = Servicios_Extra.objects.filter(t_id_cart=cart)
    
    servtran = Servicios_Extra.objects.filter(a_id_cartproduct=cartproduct.id, desc_servicio="Transporte").first()
    servtour = Servicios_Extra.objects.filter(a_id_cartproduct=cartproduct.id, desc_servicio="Tour").first()
    print(servtran)
    print(servtour)
    if servtran.t_id_transporte != None:
        print(servtran.monto_servicio)
        cart.subtotal = cart.subtotal - servtran.monto_servicio
        cart.total = cart.total - servtran.monto_servicio
    
    if servtour.t_id_tour != None:
        tour = Tour.objects.filter(id_tour=servtour.t_id_tour).first()
        tour.numero_vacantes = tour.numero_vacantes + 1
        tour.save()
        cart.subtotal = cart.subtotal - servtour.monto_servicio
        cart.total = cart.total - servtour.monto_servicio
        
    servtran = Servicios_Extra.objects.filter(a_id_cartproduct=cartproduct.id, desc_servicio="Transporte").delete()
    servtour = Servicios_Extra.objects.filter(a_id_cartproduct=cartproduct.id, desc_servicio="Tour").delete()
    
    cartproduct = CartProducts.objects.get(id=cartproduct_id).delete()
    #cart.products.remove(product)
    #cart_product = CartProducts.objects.filter(cart=cart).delete()
    #cart es una instacia del modelo por lo que para acceder a atributo products es la relacion ManytoMany
    
    
    return render(request, 'carts/cart.html', {
        #mandando el objeto cart al template
        'cart':cart,
        'Tour':tours,
        'transporte':transportes,
        'servicios':ser
    })
    
def extra_tour(request, slug):
    tours = Tour.objects.all().order_by('-id_tour')
    transportes = Transporte.objects.all().order_by('-id_transporte')
    product = Product.objects.filter(slug=slug).first()
    cart = get_or_create_cart(request)
    cart_product = CartProducts.objects.filter(cart=cart, product=product).first()
    print(product)
    if request.method == 'POST':
        cart = get_or_create_cart(request)
        pro = request.POST.get('pro_id')
        print(pro)
        product = get_object_or_404(Product, pk=pro)
        fecha = request.POST.get('fecha_servicio')
        hora = request.POST.get('hora_servicio')
        id_tour = request.POST.get('id_tour')
        tour = Tour.objects.get(id_tour=id_tour)
        cart_product = CartProducts.objects.filter(cart=cart, product=product).first()
        servicio = Servicios_Extra.objects.filter(t_id_cart=cart, a_id_cartproduct=cart_product, desc_servicio = "Tour").first()
        servicio.monto_servicio = tour.precio
        servicio.estado_servicio = "En proceso"
        servicio.fecha_servicio = tour.fecha_tour
        servicio.a_id_cartproduct = cart_product
        servicio.horario_servicio = tour.hora_inicio
        servicio.t_id_transporte = None
        servicio.t_id_tour = tour
        tour.numero_vacantes = tour.numero_vacantes -1
        tour.save()
        servicio.save()
        cart.subtotal = cart.subtotal + servicio.monto_servicio
        cart.total = cart.total + servicio.monto_servicio
        cart.save()
        
        serv = Servicios_Extra.objects.all().order_by('-id_servicio_extra')
            
        
        return render(request, 'carts/cart.html', {
            #mandando el objeto cart al template
            'cart':cart,
            'servicios':serv
        })
    if tours is None:
        tours = Null
    print(tours)
    return render(request, 'carts/extra_tour.html', {
        #contexto
        'cart': cart,
        'Tour':tours,
        'transporte':transportes,
        'message': 'Listado de Tours',
        'title': 'departamentos',
        'cart_product': cart_product,
        'pro': product
        })
 
def extra_transporte(request, slug):
    tours = Tour.objects.all().order_by('-id_tour')
    transportes = Transporte.objects.all().order_by('-id_transporte')
    pro = Product.objects.filter(slug=slug).first()
    print(transportes)
    cart = get_or_create_cart(request)
    cart_product = CartProducts.objects.filter(cart=cart, product=pro).first()
        
    if request.method == 'POST':
        cart = get_or_create_cart(request)
        product = get_object_or_404(Product, pk=request.POST.get('pro_id'))
        
        fecha = request.POST.get('fecha_servicio')
        origen = request.POST.get('origen')
        hora = request.POST.get('hora_servicio')
        id_transporte = request.POST.get('id_transporte')
        transporte = Transporte.objects.get(id_transporte=id_transporte)
        cart_product = CartProducts.objects.filter(cart=cart, product=product).first()
        servicio = Servicios_Extra.objects.filter(t_id_cart=cart, a_id_cartproduct=cart_product, desc_servicio = "Transporte").first()
        servicio.monto_servicio = transporte.precio
        servicio.estado_servicio = "En proceso"
        servicio.fecha_servicio = fecha
        servicio.a_id_cartproduct = cart_product
        servicio.horario_servicio = hora
        servicio.t_id_transporte = transporte
        servicio.t_id_tour = None
        servicio.save()
        cart.subtotal = cart.subtotal + servicio.monto_servicio
        cart.total = cart.total + servicio.monto_servicio
        cart.save()
        
        serv = Servicios_Extra.objects.all().order_by('-id_servicio_extra')
            
        
        return render(request, 'carts/cart.html', {
            #mandando el objeto cart al template
            'cart':cart,
            'servicios':serv
        })
    return render(request, 'carts/extra_transporte.html', {
        #contexto
        'cart': cart,
        'pro': pro,
        'Tour':tours,
        'transporte':transportes,
        'message': 'Listado de Transportes',
        'title': 'departamentos',
        'cart_product': cart_product
        })
def eliminar_transporte(request, slug):
    servicio = Servicios_Extra.objects.filter(id_servicio_extra=slug).first()
    cart = get_or_create_cart(request)
    if servicio != None:
        servicio.estado_servicio = ""
        servicio.fecha_servicio = "2020-01-01"
        servicio.horario_servicio = "00:00"
        servicio.t_id_transporte = None
        servicio.t_id_tour = None
        cart.subtotal = cart.subtotal - servicio.monto_servicio
        cart.total = cart.total - servicio.monto_servicio
        servicio.monto_servicio = 0
        servicio.save()
        cart.save()
    serv = Servicios_Extra.objects.filter(t_id_cart=cart)
    
    return render(request, 'carts/cart.html', {
        #mandando el objeto cart al template
        'cart':cart,
        'servicios':serv
    })

def eliminar_tour(request, slug):
    servicio = Servicios_Extra.objects.filter(id_servicio_extra=slug).first()
    cart = get_or_create_cart(request)
    if servicio != None:
        servicio.estado_servicio = ""
        servicio.fecha_servicio = "2020-01-01"
        servicio.horario_servicio = "00:00"
        print(servicio.t_id_tour)
        print(servicio.t_id_tour.id_tour)
        tour = Tour.objects.filter(id_tour=servicio.t_id_tour.id_tour).first()
        print(tour)
        tour.numero_vacantes = tour.numero_vacantes + 1
        tour.save()
        servicio.t_id_transporte = None
        servicio.t_id_tour = None
        cart.subtotal = cart.subtotal - servicio.monto_servicio
        cart.total = cart.total - servicio.monto_servicio
        servicio.monto_servicio = 0
        servicio.save()
        
    serv = Servicios_Extra.objects.filter(t_id_cart=cart)
    
    return render(request, 'carts/cart.html', {
        #mandando el objeto cart al template
        'cart':cart,
        'servicios':serv
    })