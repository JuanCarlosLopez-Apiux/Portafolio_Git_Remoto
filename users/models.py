from django.db import models
from datetime import date
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

#SI NO SE QUIERE EXTENDER EL MODELO USER A OTRO, SINO GENERAR UNO NOSOTROS SE PUEDE USAR EL ABSTRACT USER

class User(AbstractUser):
    rut_usuario = models.TextField(max_length=10, default="G", null=False)
    fecha_nacimiento = models.DateField(default=date.today, null=False)
    def edad(fecha):
        hoy = datetime.now()      # Tipo: datetime.datetime
        diferencia = hoy - fecha  # Tipo resultante: datetime.timedelta
        return(diferencia.days / 365)
        
    def get_full_name(self):
        return '{}-{}'.format(self.first_name, self.last_name)
        
    def sample_view(request):
        current_user = request.user
        print (current_user.id)
        return current_user.id
        
    def get_contetx_data(self, **kwargs):
        context = super().get_context_data()
        #luego agregas al contexto lo que desees que vaya a la otra pagina o se use en esta.
        context['id'] = 'aca van los datos o queryset'
        return context
        
    def get_User_profile(self):
        User = None
        if hasattr(self, 'User'):
            User = self.User
        return User


class Customer(User):
    # proxy model es que no genere una nueva tabla en la base de datos
    class Meta:
        proxy = False
        
    def get_products(sef):
        return []


    #relacion 1 a 1 con el user con la intencion de que podamos manejar nuevos campos para el User


class Profile(models.Model):
    #CASCADE ES CUANDO UN USUARIO SEA ELIMINADO TAMBIEN SE ELIMINE SU PROFILE EN CASCADA
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    bio = models.TextField()
