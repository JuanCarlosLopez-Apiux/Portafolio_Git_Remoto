from django.contrib import admin
from django.contrib.auth.models import User
from.models import Product, Estado_Departamento, Tipo_Departamento, Region, Comuna, Ciudad, Empresa, Mantencion, Inventario, Tipo_Inventario
from carts.models import Check_In, Check_Out, Tarjeta_Credito, Tour, Transporte, Servicios_Extra, CartProducts
# Register your models here.
 
class ProductAdmin(admin.ModelAdmin):
    #Creo esta clase porque no quiero mostrar el slug ya que se va a generar automaticamente
    fields = ('title', 'description', 'price', 'image', 'cantidad_de_baños', 'cantidad_de_dormitorios', 'cantidad_de_camas', 'cantidad_de_muebles', 'cantidad_de_televisores', 'tamaño_de_departamento', 't_id_tipo', 'e_id_estado', 'e_id_empresa')
    #mostar en el administrador aparte del title que es el str, mostrar el slug y created_at
    list_display = ('__str__', 'slug', 'created_at')

admin.site.register(Product,ProductAdmin )
admin.site.register(Tipo_Departamento)
admin.site.register(Region)
admin.site.register(User)
admin.site.register(Comuna)
admin.site.register(Ciudad)
admin.site.register(Empresa)
admin.site.register(Estado_Departamento)
admin.site.register(Mantencion)
admin.site.register(Check_In)
admin.site.register(Check_Out)
admin.site.register(Inventario)
admin.site.register(Tipo_Inventario)
admin.site.register(Tarjeta_Credito)
admin.site.register(Tour)
admin.site.register(Transporte)
admin.site.register(Servicios_Extra)
admin.site.register(CartProducts)