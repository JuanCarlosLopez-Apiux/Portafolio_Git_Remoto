from django.db import models
from datetime import date
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    rut_usuario = models.TextField(max_length=10, default="G", null=False)
    fecha_nacimiento = models.DateField(default=date.today, null=False)
    def edad(fecha):
        hoy = datetime.now() 
        diferencia = hoy - fecha 
        return(diferencia.days / 365)
        
    def get_full_name(self):
        return '{}-{}'.format(self.first_name, self.last_name)
        
    def sample_view(request):
        current_user = request.user
        print (current_user.id)
        return current_user.id
        
    def get_contetx_data(self, **kwargs):
        context = super().get_context_data()
        context['id'] = 'aca van los datos o queryset'
        return context
        
    def get_User_profile(self):
        User = None
        if hasattr(self, 'User'):
            User = self.User
        return User


class Customer(User):
    class Meta:
        proxy = False
        
    def get_products(sef):
        return []


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    bio = models.TextField()
