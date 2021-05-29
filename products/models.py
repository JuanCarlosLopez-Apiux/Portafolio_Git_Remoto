import uuid
from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.core.validators import MaxValueValidator
from django.utils import timezone
from datetime import datetime 

class Region(models.Model):
    id_region = models.AutoField(primary_key=True)
    descripcion = models.TextField()

    class Meta:
        managed = True
        db_table = 'Region'
        
    def desc(self):
        return self.descripcion

class Ciudad(models.Model):
    id_ciudad = models.AutoField(primary_key=True)
    descripcion = models.TextField()
    r_id_region = models.ForeignKey('Region', models.DO_NOTHING, db_column='r_id_region', default=1)

    class Meta:
        managed = True
        db_table = 'ciudad'

class Comuna(models.Model):
    id_comuna = models.AutoField(primary_key=True)
    descripcion = models.TextField()
    c_id_ciudad = models.ForeignKey(Ciudad, models.DO_NOTHING, db_column='c_id_ciudad', default=1)

    class Meta:
        managed = True
        db_table = 'Comuna'

class Empresa(models.Model):
    id_empresa = models.BigIntegerField(primary_key=True, null=False, blank=False, unique=True)
    direccion = models.TextField()
    ndepartamentos_disponibles = models.IntegerField()
    telefono = models.IntegerField()
    nombre = models.TextField()
    c_id_comuna = models.ForeignKey(Comuna, models.DO_NOTHING, db_column='c_id_comuna', default=1)
    
    class Meta:
        managed = True
        db_table = 'Empresa'
  
class Estado_Departamento(models.Model):
    id_estado = models.AutoField(primary_key=True)
    descricion_estado = models.TextField()

    class Meta:
        managed = True
        db_table = 'Estado_Departamento'


class Tipo_Departamento(models.Model):
    id_tipo = models.AutoField(primary_key=True)
    descripcion = models.TextField()

    class Meta:
        managed = True
        db_table = 'Tipo_Departamento'

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=50)
    description =models.TextField()
    price = models.IntegerField(null=False, validators=[MaxValueValidator(9999999)], default=0) #12121.58
    slug = models.SlugField(null=False, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='products/', null=False, blank=False)
    cantidad_de_baños = models.IntegerField(null=False, validators=[MaxValueValidator(50)], default=1)
    cantidad_de_dormitorios = models.IntegerField(null=False, validators=[MaxValueValidator(50)], default=1)
    cantidad_de_camas = models.IntegerField(null=False, validators=[MaxValueValidator(50)], default=1)
    cantidad_de_muebles = models.IntegerField(null=False, validators=[MaxValueValidator(50)], default=1)
    cantidad_de_televisores = models.IntegerField(null=False, validators=[MaxValueValidator(50)], default=1)
    tamaño_de_departamento = models.IntegerField(null=False, validators=[MaxValueValidator(300)], default=1)
    t_id_tipo = models.ForeignKey('Tipo_Departamento', models.DO_NOTHING, db_column='t_id_tipo')
    e_id_estado = models.ForeignKey('Estado_Departamento', models.DO_NOTHING, db_column='e_id_estado')
    e_id_empresa = models.ForeignKey('Empresa', models.DO_NOTHING, db_column='e_id_empresa')

    def __str__(self):
        return self.title


    
def set_slug(sender, instance, *args, **kwargs):
    if instance.title and not instance.slug:
        slug = slugify(instance.title)
        while Product.objects.filter(slug=slug).exists():
            slug = slugify("{}-{}".format(instance.title,str(uuid.uuid4())[:8]))
            print("Este es slug", slug)

        instance.slug = slug
pre_save.connect(set_slug, sender=Product)

class Mantencion(models.Model):
    id_mantencion = models.AutoField(primary_key=True)
    fecha_inicio = models.DateField(default=timezone.now, blank=True)
    fecha_termino = models.DateField(default=timezone.now, blank=True)
    descripcion_mantencion = models.TextField()
    d_numero_de_departamento = models.ForeignKey(Product, models.DO_NOTHING, db_column='d_numero_de_departamento', default=1)

    class Meta:
        managed = True
        db_table = 'Mantencion'

class Tipo_Inventario(models.Model):
    descripcion = models.TextField()
    id_tipo = models.AutoField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'Tipo_Inventario'
        

class Inventario(models.Model):
    cantidad = models.IntegerField()
    marca = models.TextField()
    fecha_compra = models.DateField(default=timezone.now, blank=True)
    d_numero_de_departamento = models.ForeignKey(Product, models.DO_NOTHING, db_column='d_numero_de_departamento', default=1)
    t_id_tipo = models.ForeignKey('Tipo_Inventario', models.DO_NOTHING, db_column='t_id_tipo')
    costo = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'Inventario'

