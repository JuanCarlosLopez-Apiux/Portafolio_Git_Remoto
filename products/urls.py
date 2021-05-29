from django.urls import path

from . import views
from carts.views import index

app_name = 'products'


urlpatterns = [
    path('search',views.ProductSearchListView.as_view() , name="search"),
    path('<slug:slug>',index , name="product"),
]
