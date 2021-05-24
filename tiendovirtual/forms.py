from django import forms
#from django.contrib.auth.models import User
from datetime import date, datetime
from django.utils import timezone
from users.models import User
from carts.models import Tarjeta_Credito, Cart
from django.forms.fields import DateField
import math
from django.contrib.admin.widgets import AdminDateWidget

class RegisterForm(forms.Form):
    rut_usuario = forms.CharField(required=True, min_length=8, max_length=10, widget=forms.TextInput(attrs={
                                    'class': 'myclass',
                                    'id': 'rut_usuario',
                                    'size':'10',
                                    'placeholder': 'xxxxxxxx-x'}))
                                    
    fecha_nacimiento = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput(attrs={
            'class': 'myclass datetimepicker-input',
            'data-target': '#datetimepicker1',
            'id': 'fecha_nacimiento',
            'placeholder': 'xx/xx/xxxx',
            'size':'10',
        })
    )
    
    username = forms.CharField(required=True, label = 'Nombre de usuario', min_length=4, max_length=50,
                                widget=forms.TextInput(attrs={
                                    'class': 'myclass',
                                    'id': 'username',
                                    'placeholder': ''
                                }))
    first_name = forms.CharField(required=True, label = 'Nombre', min_length=3, max_length=50,
                                widget=forms.TextInput(attrs={
                                    'class': 'myclass',
                                    'id': 'first_name',
                                    'placeholder': '',
                                }))
    last_name = forms.CharField(required=True, label = 'Apellido', min_length=3, max_length=50,
                                widget=forms.TextInput(attrs={
                                    'class': 'myclass',
                                    'id': 'last_name',
                                    'placeholder': '',
                                }))
    email =  forms.EmailField(required=True,  widget=forms.EmailInput(attrs={
                                    'class': 'myclass',
                                    'id': 'email',
                                    'placeholder': ''}))
    password = forms.CharField(required=True, label = 'Contraseña', widget=forms.PasswordInput(attrs={
                                    'class': 'myclass',
                                    'id': 'password',
                                    'placeholder': ''}))
    password2 = forms.CharField(required=True,  label = 'Confirmar contraseña', widget=forms.PasswordInput(attrs={
                                    'class': 'myclass',
                                    'id': 'password2',
                                    'placeholder': ''}))
    codigo = forms.IntegerField(required=True, label = 'Código', widget=forms.TextInput(attrs={
                                    'class': 'myclass',
                                    'id': 'codigo',
                                    'placeholder': '000',
                                    'size':'1'}))
    
    numero_tarjeta = forms.IntegerField(required=True, label = 'Numero de tarjeta',
                                widget=forms.TextInput(attrs={
                                    'class': 'myclass',
                                    'id': 'numero',
                                    'placeholder': '0000000000000000',
                                    'type':'number'
                                }))
    compania = forms.CharField(required=True, label = 'Compañia', min_length=3, max_length=15,
                                widget=forms.TextInput(attrs={
                                    'class': 'myclass',
                                    'id': 'compania',
                                    'placeholder': 'Visa/MasterCard'
                                }))
                                
    mes_exp = forms.IntegerField(required=True, label = 'Mes exp',
                                widget=forms.TextInput(attrs={
                                    'class': 'myclass',
                                    'id': 'mes_exp',
                                    'placeholder': '01',
                                    'size':'2',
                                    'type':'number'
                                }))
    anio_exp =  forms.IntegerField(required=True, label = 'Año exp',
                                widget=forms.TextInput(attrs={
                                    'class': 'myclass',
                                    'id': 'anio_exp',
                                    'placeholder': '01',
                                    'size':'2',
                                    'type':'number'
                                }))

    
    def clean_numero_tarjeta(self):
        numero_tarjeta = self.cleaned_data.get('numero_tarjeta')
        largo = math.floor(math.log10(numero_tarjeta))+1
        #si existe un usuario en la bd
        if Tarjeta_Credito.objects.filter(numero_tarjeta=numero_tarjeta).exists():
            raise forms.ValidationError('El Número de tarjeta {} ya se encuentra asociada'.format(numero_tarjeta))
        if largo < 15:
            raise forms.ValidationError('El Número no es valido')
        if largo > 16:
            raise forms.ValidationError('El Número no es valido')
        return numero_tarjeta 
        
    def clean_anio_exp(self):
        an = datetime.today().year
        ano = abs(an) % 100
        anio_exp = self.cleaned_data.get('anio_exp')
        #si existe un usuario en la bd
        if anio_exp < ano : 
            raise forms.ValidationError('Año no valido (Caducado)')
        return anio_exp 
    
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        #si existe un usuario en la bd
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El username ya se encuentra en uso')
        
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        #si existe un usuario en la bd
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El email {} ya se encuentra en uso'.format(email))
        
        return email 
        
    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        hoy = date.today()      # Tipo: datetime.datetime
        diferencia = hoy - fecha_nacimiento  # Tipo resultante: datetime.timedelta
        if (diferencia.days / 365) < 18:
            raise forms.ValidationError('Debes ser mayor de edad')
        
        return fecha_nacimiento
    
    def clean(self):
        cleaned_data = super().clean()
            
        if cleaned_data.get('password2') != cleaned_data.get('password'):
            self.add_error('password2', 'El password no coincide')

    def save(self):
        return User.objects.create_user(
            self.cleaned_data.get('username'),
            self.cleaned_data.get('email'),
            self.cleaned_data.get('password'),
        )

    
class Editar_TarjetaForm(forms.Form): 

    codigo = forms.IntegerField(required=True, label = 'Código', widget=forms.TextInput(attrs={
                                    'class': 'myclass',
                                    'id': 'codigo',
                                    'placeholder': '000',
                                    'size':'1'}))
    
    numero_tarjeta = forms.IntegerField(required=True, label = 'Numero de tarjeta',
                                widget=forms.TextInput(attrs={
                                    'class': 'myclass',
                                    'id': 'numero',
                                    'placeholder': '0000000000000000',
                                    'type':'number'
                                }))
    compania = forms.CharField(required=True, label = 'Compañia', min_length=3, max_length=15,
                                widget=forms.TextInput(attrs={
                                    'class': 'myclass',
                                    'id': 'compania',
                                    'placeholder': 'Visa/MasterCard'
                                }))
                                
    mes_exp = forms.IntegerField(required=True, label = 'Mes exp',
                                widget=forms.TextInput(attrs={
                                    'class': 'myclass',
                                    'id': 'mes_exp',
                                    'placeholder': '01',
                                    'size':'2',
                                    'type':'number'
                                }))
    anio_exp =  forms.IntegerField(required=True, label = 'Año exp',
                                widget=forms.TextInput(attrs={
                                    'class': 'myclass',
                                    'id': 'anio_exp',
                                    'placeholder': '01',
                                    'size':'2',
                                    'type':'number'
                                }))
                                
    def clean(self):
        cleaned_data = super().clean()
                                
    def clean_numero_tarjeta(self):
        numero_tarjeta = self.cleaned_data.get('numero_tarjeta')
        largo = math.floor(math.log10(numero_tarjeta))+1
        #si existe un usuario en la bd
        if Tarjeta_Credito.objects.filter(numero_tarjeta=numero_tarjeta).exists():
            raise forms.ValidationError('El Número de tarjeta {} ya se encuentra asociada'.format(numero_tarjeta))
        if largo < 15:
            raise forms.ValidationError('El Número no es valido')
        if largo > 16:
            raise forms.ValidationError('El Número no es valido')
        return numero_tarjeta 
        
    def clean_anio_exp(self):
        an = datetime.today().year
        ano = abs(an) % 100
        anio_exp = self.cleaned_data.get('anio_exp')
        #si existe un usuario en la bd
        if anio_exp < ano : 
            raise forms.ValidationError('Año no valido (Caducado)')
        return anio_exp 

class Editar_NombresForm(forms.Form): 
    first_name = forms.CharField(required=True, label = 'Nombre', min_length=3, max_length=50,
                                widget=forms.TextInput(attrs={
                                    'class': 'myclass',
                                    'id': 'first_name',
                                    'placeholder': '',
                                }))
    last_name = forms.CharField(required=True, label = 'Apellido', min_length=3, max_length=50,
                                widget=forms.TextInput(attrs={
                                    'class': 'myclass',
                                    'id': 'last_name',
                                    'placeholder': '',
                                }))
    def clean(self):
        cleaned_data = super().clean()

class Editar_UsernameForm(forms.Form): 
    username = forms.CharField(required=True, label = 'Nombre de usuario', min_length=4, max_length=50,
                                widget=forms.TextInput(attrs={
                                    'class': 'myclass',
                                    'id': 'username',
                                    'placeholder': ''
                                }))
                                
    def clean_username(self):
        username = self.cleaned_data.get('username')
        #si existe un usuario en la bd
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El username ya se encuentra en uso')
        
        return username
        
    def clean(self):
        cleaned_data = super().clean()

class Editar_PasswordForm(forms.Form):
    password = forms.CharField(required=True, label = 'Contraseña', widget=forms.PasswordInput(attrs={
                                    'class': 'myclass',
                                    'id': 'password',
                                    'placeholder': ''}))
    password2 = forms.CharField(required=True,  label = 'Confirmar contraseña', widget=forms.PasswordInput(attrs={
                                    'class': 'myclass',
                                    'id': 'password2',
                                    'placeholder': ''}))
    def clean(self):
        cleaned_data = super().clean()
            
        if cleaned_data.get('password2') != cleaned_data.get('password'):
            self.add_error('password2', 'El password no coincide')

class CrearCarritoForm(forms.Form):
    cant_ninios = forms.IntegerField(required=True, label = 'Cantidad de niños:', widget=forms.TextInput(attrs={
                                    'class': 'myclass',
                                    'id': 'cant_ninios',
                                    'placeholder': '00',
                                    'size':'2'}))
    cant_adultos = forms.IntegerField(required=True, label = 'Cantidad de adultos:', widget=forms.TextInput(attrs={
                                    'class': 'myclass',
                                    'id': 'cant_ninios',
                                    'placeholder': '01',
                                    'size':'2'}))

    def clean_cant_ninios(self):
        ninios = self.cleaned_data.get('cant_ninios')
        if ninios < 0 or ninios >25 : 
            raise forms.ValidationError('La cantidad de niños debe ser menor a 25')
        return anio_exp 
        
    def clean_cant_adultos(self):
        adultos = self.cleaned_data.get('cant_adultos')
        if adultos < 1 or adultos >999 : 
            raise forms.ValidationError('La cantidad de adultos debe ser menor a 999')
        return anio_exp 

class Editar_emailForm(forms.Form):

    email =  forms.EmailField(required=True,  widget=forms.EmailInput(attrs={
                                    'class': 'myclass',
                                    'id': 'email',
                                    'placeholder': ''}))
                                    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        #si existe un usuario en la bd
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El email {} ya se encuentra en uso'.format(email))
        
        return email