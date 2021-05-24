from django.test import TestCase
#from applications.calculos.metric import *
from products.views import *
from django.http import HttpRequest
from django.test import SimpleTestCase
from django.template.defaultfilters import slugify
from django.urls import reverse
from products.models import *

         
class Insert_Region_TestCase(TestCase):

    def  setUp ( self ): 
        Region.objects.create(descripcion="just a region")

    def test_Region(self):
        region = Region.objects.get(descripcion="just a region")
        self.assertEqual(region.descripcion, 'just a region')

class Insert_Ciudad_TestCase(TestCase):

    def  setUp ( self ):
        Region.objects.create(descripcion="just a region")
        region = Region.objects.filter(descripcion="just a region").first()
        Ciudad.objects.create(descripcion="just a ciudad", r_id_region=region)

    def test_Ciudad(self):
        ciudad = Ciudad.objects.get(descripcion="just a ciudad")
        self.assertEqual(ciudad.descripcion, 'just a ciudad')
 
class Insert_Comuna_TestCase(TestCase):

    def  setUp ( self ):
        Region.objects.create(descripcion="just a region")
        region = Region.objects.filter(descripcion="just a region").first()
        Ciudad.objects.create(descripcion="just a ciudad", r_id_region=region)
        ciudad = Ciudad.objects.filter(descripcion="just a ciudad").first()
        Comuna.objects.create(descripcion="just a comuna", c_id_ciudad=ciudad)

    def test_Comuna(self):
        comuna = Comuna.objects.get(descripcion="just a comuna")
        self.assertEqual(comuna.descripcion, 'just a comuna')
 
class Insert_Empresa_TestCase(TestCase):

    def  setUp ( self ):
        Region.objects.create(descripcion="just a region")
        region = Region.objects.filter(descripcion="just a region").first()
        Ciudad.objects.create(descripcion="just a ciudad", r_id_region=region)
        ciudad = Ciudad.objects.filter(descripcion="just a ciudad").first()
        Comuna.objects.create(descripcion="just a comuna", c_id_ciudad=ciudad)
        comuna = Comuna.objects.filter(descripcion="just a comuna").first()
        Empresa.objects.create(id_empresa=1, direccion="910", ndepartamentos_disponibles=0, telefono=111111, nombre="empresa",c_id_comuna=comuna)

    def test_Empresa(self):
        empresa = Empresa.objects.get(id_empresa=1)
        self.assertEqual(empresa.id_empresa, 1)	
         
 
class Insert_Estado_Departamento_TestCase(TestCase):

    def  setUp ( self ): 
        Estado_Departamento.objects.create(descricion_estado="just a estado")

    def test_Estado_Departamento(self):
        estado = Estado_Departamento.objects.get(descricion_estado="just a estado")
        self.assertEqual(estado.descricion_estado, 'just a estado')
         


