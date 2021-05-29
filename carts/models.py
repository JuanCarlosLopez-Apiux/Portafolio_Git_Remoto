
import uuid
import decimal
from django.db import models
from users.models import User
from products.models import Product
from django.db.models.signals import pre_save,post_save
from django.db.models.signals import m2m_changed
from django.utils import timezone
from datetime import datetime 
from django.core.validators import MaxValueValidator
# Create your models here.


class Cart(models.Model):
    cart_id = models.CharField(max_length=100, null=False, blank=False, unique=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartProducts')
    subtotal = models.IntegerField(validators=[MaxValueValidator(9999999)], default=0)
    total = models.IntegerField(validators=[MaxValueValidator(9999999)], default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(validators=[MaxValueValidator(9999)], default=1)
    fecha_inicio = models.DateField(default=timezone.now, blank=True)
    fecha_termino = models.DateField(default=timezone.now, blank=True)
    cant_ninios = models.IntegerField(validators=[MaxValueValidator(25)], default=0)
    cant_adultos = models.IntegerField(validators=[MaxValueValidator(999)], default=1)
    pagado = models.BinaryField(default=0)


    FEE = 0.05 #comision del 5% de la compra

    def __str__(self):
        return self.cart_id

    def products_related(self):
        return self.cartproducts_set.select_related('product')

    @property
    def order(self):
        return self.order_set.first()



class CartProductsManager(models.Manager):

    def create_or_update_fecha(self, cart, product, fecha_inicio, fecha_termino, quantity, cant_ninios, cant_adultos):
        object, created = self.get_or_create(cart=cart, product=product)
        object.update_cant_ninios(cant_ninios)
        object.update_cant_adultos(cant_adultos)
        object.update_quantity(quantity)
        object.update_fecha_inicio(fecha_inicio)
        object.update_fecha_termino(fecha_termino)
        
        return object
class CartProducts(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MaxValueValidator(9999)], default=1)
    fecha_inicio = models.DateField(default=timezone.now, blank=True) 
    fecha_termino = models.DateField(default=timezone.now, blank=True)
    cant_ninios = models.IntegerField(validators=[MaxValueValidator(25)], default=0)
    cant_adultos = models.IntegerField(validators=[MaxValueValidator(999)], default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def Create_CartProducts(self, cart, product, fecha_inicio, fecha_termino, quantity, cant_ninios, cant_adultos):
        self.cart = cart
        self.product = product
        self.fecha_inicio = fecha_inicio
        self.fecha_termino = fecha_termino
        self.quantity = quantity
        self.cant_ninios = cant_ninios
        self.cant_adultos = cant_adultos
        self.save()
        

    def update_fecha_inicio(self, fecha):
        self.fecha_inicio = fecha
        self.save()
    def update_fecha_termino(self, fecha):
        self.fecha_termino = fecha
        self.save()
    def update_cant_ninios(self, cant_ninios):
        self.cant_ninios = cant_ninios
        self.save()
    def update_cant_adultos(self, cant_adultos):
        self.cant_adultos = cant_adultos
        self.save()
    def update_quantity(self, quantity):
        self.quantity = quantity
        self.save()
        
def set_cart_id(sender, instance, *args, **kwargs):
    if not instance.cart_id:
        instance.cart_id = str(uuid.uuid4())


#callbacks
pre_save.connect(set_cart_id, sender=Cart)

class Check_In(models.Model):
    id_check_in = models.AutoField(primary_key=True)
    descripcion_check_in = models.TextField()
    a_id_arriendo = models.ForeignKey(Cart, models.DO_NOTHING, db_column='a_id_arriendo', default=1)
    firmado = models.BinaryField()

    class Meta:
        managed = True
        db_table = 'Check_In'

class Check_Out(models.Model):
    id_check_out = models.AutoField(primary_key=True)
    desc_danios = models.TextField()
    monto_danios = models.BigIntegerField()
    pagado = models.BinaryField()
    firmado = models.BinaryField()
    a_id_arriendo = models.ForeignKey(Cart, models.DO_NOTHING, db_column='a_id_arriendo', default=1)

    class Meta:
        managed = True
        db_table = 'Check_Out'


class Tarjeta_Credito(models.Model):
    codigo = models.IntegerField()
    numero_tarjeta = models.BigIntegerField(primary_key=True)
    compania = models.TextField()
    mes_exp = models.IntegerField(validators=[MaxValueValidator(13)], default=1)
    anio_exp = models.IntegerField(validators=[MaxValueValidator(100)], default=20)
    u_id_cliente = models.ForeignKey(User, models.DO_NOTHING, db_column='u_id_cliente')

    class Meta:
        managed = True
        db_table = 'Tarjeta_Credito'


class Tour(models.Model):
    id_tour = models.AutoField(primary_key=True)
    descripcion_tour = models.TextField()
    numero_vacantes = models.IntegerField(validators=[MaxValueValidator(501)])
    precio = models.BigIntegerField(validators=[MaxValueValidator(1000000)])
    hora_inicio = models.TimeField(default=timezone.now, blank=True)
    hora_termino = models.TimeField(default=timezone.now, blank=True)
    fecha_tour = models.DateField(default=timezone.now, blank=True)
    
    class Meta:
        managed = True
        db_table = 'Tour'


class Transporte(models.Model):
    id_transporte = models.AutoField(primary_key=True)   
    vehiculo = models.TextField() 
    destino = models.TextField()
    origen = models.TextField()
    precio = models.IntegerField(validators=[MaxValueValidator(1000000)])
    u_id_funcionario = models.ForeignKey(User, models.DO_NOTHING, db_column='u_id_funcionario')

    class Meta:
        managed = True
        db_table = 'Transporte'
        

class Servicios_Extra(models.Model):
    id_servicio_extra = models.AutoField(primary_key=True)
    monto_servicio = models.IntegerField(validators=[MaxValueValidator(1000000)])
    desc_servicio = models.TextField() 
    estado_servicio = models.TextField() 
    fecha_servicio = models.DateField(default=timezone.now, blank=True)
    a_id_cartproduct = models.ForeignKey(CartProducts, models.DO_NOTHING, db_column='a_id_cartproduct', null=True)
    horario_servicio = models.TimeField(default=timezone.now, blank=True)
    t_id_transporte = models.ForeignKey('Transporte', models.DO_NOTHING, db_column='t_id_transporte', blank=True, null=True)
    t_id_tour = models.ForeignKey('Tour', models.DO_NOTHING, db_column='t_id_tour', blank=True, null=True)
    t_id_cart = models.ForeignKey('Cart', models.DO_NOTHING, db_column='t_id_cart', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Servicios_Extra'
        
        
