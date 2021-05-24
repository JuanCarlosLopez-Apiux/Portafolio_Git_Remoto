from django.urls import path
from . import views

app_name = 'carts'


urlpatterns = [
    path('', views.cart, name='cart'),
    path('agregar', views.add, name='add'),
    path('Tour/<slug:slug>', views.extra_tour, name='extra_tour'),
    path('Transporte/<slug:slug>', views.extra_transporte, name='extra_transporte'),
    path('eliminar', views.remove, name='remove'),
    path('eliminar_transporte/<slug:slug>', views.eliminar_transporte, name='eliminar_transporte'),
    path('eliminar_tour/<slug:slug>', views.eliminar_tour, name='eliminar_tour'),
]
