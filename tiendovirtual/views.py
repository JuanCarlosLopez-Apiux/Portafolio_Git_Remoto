from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from carts.utils import get_or_create_cart, get_or_create_Tarjeta_Credito
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from .forms import RegisterForm, Editar_TarjetaForm, Editar_NombresForm, Editar_UsernameForm, Editar_PasswordForm, Editar_emailForm
from carts.models import Tarjeta_Credito
from datetime import date, datetime
#from django.contrib.auth.models import User
from products.models import Product, Tipo_Departamento, Estado_Departamento
from users.models import User

#Vistas basadas en clases. Agilizas el proceso porque usas django, mover a view del proyecto

def index(request):
    products = Product.objects.all().order_by('-id')
    tipo = Tipo_Departamento.all().order_by('id_tipo')
    estado = Estado_Departamento.all().order_by('id_estado')
    cart = get_or_create_cart(request)
    cartproduct = cart_product = CartProducts.objects.filter(cart=cart).first()
    
    return render(request, 'index.html', {
        #contexto
        'message': 'Listado de departamentos',
        'title': 'departamentos',
        'products': products,
        'tipo': tipo,
        'estado': estado,
        'cart': cart,
        'cartproduct': cartproduct
        })



def logout_view(request):
    logout(request)
    messages.success(request, 'Sesion cerrada exitosamente')
    return redirect('login')


def register(request):
    #si el usuario esta atenticado voy a redirigir a index
    error_mes = None
    if request.user.is_authenticated:
        return redirect('index')

    form = RegisterForm(request.POST or None)
            
    if request.method == 'POST' and form.is_valid():
        user = None
        #cleaned_data es un diccionario
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        rut_usuario = form.cleaned_data.get('rut_usuario')
        fecha_nacimiento = form.cleaned_data.get('fecha_nacimiento')
        #AHORA OBTENGO ESTO DEL METODO DEL FORM 
        #user = form.save()
        codigo = form.cleaned_data.get('codigo')
        numero_tarjeta = form.cleaned_data.get('numero_tarjeta')
        compania = form.cleaned_data.get('compania')
        mes_exp = form.cleaned_data.get('mes_exp')
        anio_exp = form.cleaned_data.get('anio_exp')
        

        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name, rut_usuario=rut_usuario, fecha_nacimiento=fecha_nacimiento)
        
        
        tarjeta = Tarjeta_Credito(codigo=codigo, numero_tarjeta=numero_tarjeta, compania=compania, mes_exp=mes_exp, anio_exp=anio_exp)
        tarjeta.u_id_cliente = user
        tarjeta.save()
        if user:
            login(request, user)
            messages.success(request, 'Usuario creado exitosamente')
            return redirect('index')
    else:
        error = form.errors
        print(error)
        return render(request, 'users/register.html', {
            'form': form,
            'errores': error,
            'mes': datetime.today().month,
            'ano': datetime.today().year,
            'mes': error_mes
        })
    return render(request, 'users/register.html', {
        'form': form
    })

@csrf_protect
def login_view(request):
    #si el usuario esta atenticado voy a redirigir a index
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST.get('username') #es un diccionario con dos llaves con .get obtenemos una llave si existe
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Bienvenido {}'.format(user.username))
            #si la peticion posee el parametro next hacemos un redirect
            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET['next'] )
            return redirect('index')
        else:
            messages.error(request, 'Usuario o contraseña no validos')
    return render(request, 'users/login.html', {

    })

def editar_perfil(request):
    #si el usuario esta atenticado voy a redirigir a index
    form = RegisterForm(request.POST or None)
    form_email = Editar_emailForm(request.POST or None)
    form_tarjeta = Editar_TarjetaForm(request.POST or None)
    form_nombres= Editar_NombresForm(request.POST or None)
    form_user= Editar_UsernameForm(request.POST or None)
    form_pass= Editar_PasswordForm(request.POST or None)
    tarjeta = Tarjeta_Credito.objects.filter(u_id_cliente_id=request.user.id).first()
    ultimos = str(tarjeta)[24:]
    ult = str(ultimos)[:12]
    print('Este es la tarjeta de user', ult, tarjeta)
    current_user = request.user
    print('Este es el user', current_user.id)
    
    if request.method == 'POST' and form_tarjeta.is_valid():
        codigo = form_tarjeta.cleaned_data.get('codigo')
        numero_tarjeta = form_tarjeta.cleaned_data.get('numero_tarjeta')
        compania = form_tarjeta.cleaned_data.get('compania')
        mes_exp = form_tarjeta.cleaned_data.get('mes_exp')
        anio_exp = form_tarjeta.cleaned_data.get('anio_exp')
        print("Actualización de tarjeta:", codigo, numero_tarjeta, compania, mes_exp, anio_exp)
        num_del = tarjeta.numero_tarjeta
        tarjeta.numero_tarjeta = numero_tarjeta
        tarjeta.codigo = codigo
        tarjeta.compania = compania
        tarjeta.mes_exp = mes_exp
        tarjeta.anio_exp = anio_exp
        tarjeta.save()
        Tarjeta_Credito.objects.filter(numero_tarjeta=num_del).delete()
        print("Estado:", tarjeta.numero_tarjeta, tarjeta.codigo, tarjeta.compania, tarjeta.mes_exp, tarjeta.anio_exp)
        messages.success(request, 'Tarjeta de credito actualizada exitosamente')
        return redirect('index')
    
    if request.method == 'POST' and form_email.is_valid():
        email = form_email.cleaned_data.get('email')
        ct = User.objects.all().filter(id = request.user.id).first()
        ct.email = email
        ct.save()
        messages.success(request, 'Email actualizado exitosamente')
        return redirect('index')
    
    if request.method == 'POST' and form_nombres.is_valid():
        first_name = form_nombres.cleaned_data.get('first_name')
        last_name = form_nombres.cleaned_data.get('last_name')
        ct = User.objects.all().filter(id = request.user.id).first()
        ct.last_name = last_name
        ct.first_name = first_name
        ct.save()
        messages.success(request, 'Usuario actualizado exitosamente')
        return redirect('index')
        
    if request.method == 'POST' and form_pass.is_valid():
        password = form_pass.cleaned_data.get('password')
        un = User.objects.all().filter(id = request.user.id).first()
        un.set_password(password)
        un.save()
        messages.success(request, 'Contraseña actualizada exitosamente')
        er = authenticate(username=request.user.username, password=password)
        login(request, er)
        return redirect('index')
    else:
        error = form_pass.errors
        print(error)
        
    if request.method == 'POST' and form_user.is_valid():
        #cleaned_data es un diccionario
        #codigo = request.POST.get('codigo')
        #numero_tarjeta = request.POST.get('numero_tarjeta')
        #compania = request.POST.get('compania')
        #mes_exp = request.POST.get('mes_exp')
        #anio_exp = request.POST.get('anio_exp')
        
        #password = form.cleaned_data.get('password')
        #AHORA OBTENGO ESTO DEL METODO DEL FORM 
        #user = form.save()
        #codigo = form.cleaned_data.get('codigo')
        #numero_tarjeta = form.cleaned_data.get('numero_tarjeta')
        #compania = form.cleaned_data.get('compania')
        #mes_exp = form.cleaned_data.get('mes_exp')
        #anio_exp = form.cleaned_data.get('anio_exp')
        username = form_user.cleaned_data.get('username')
        user = request.user
        un = User.objects.all().filter(id = request.user.id).first()
        un.username = username
        un.save()

        messages.success(request, 'Nombre de usuario actualizado exitosamente')
        return redirect('index')

    print(tarjeta, "  ", ult)
    return render(request, 'editar_perfil.html', {
        'form': form,
        'form_tarjeta':form_tarjeta,
        'form_nombres': form_nombres,
        'form_pass': form_pass,
        'form_user': form_user,
        'form_email': form_email,
        'tarjeta': tarjeta,
        'ultimos': ult
    })

def eliminar_cuenta(request):
    #si el usuario esta atenticado voy a redirigir a index
    if request.user.is_authenticated:
        isd = request.user.id
        logout(request)
        Tarjeta_Credito.objects.filter(u_id_cliente=isd).delete()
        User.objects.filter(id=isd).delete()
        messages.success(request, 'Usuario eliminado exitosamente')
    form = RegisterForm(request.POST or None)
    return redirect('index')