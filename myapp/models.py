from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import User

class UsuarioManager(BaseUserManager):
    def create_user(self, email, nombre, password=None):
        if not email:
            raise ValueError("El usuario debe tener un email válido")
        usuario = self.model(email=self.normalize_email(email), nombre=nombre)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, email, nombre, password):
        usuario = self.create_user(email, nombre, password)
        usuario.is_admin = True
        usuario.save(using=self._db)
        return usuario

class Usuario(AbstractBaseUser):
    email = models.CharField(unique=True, max_length=255)
    nombre = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre']

    def __str__(self):
        return self.email

    @property
    def is_authenticated(self):
        return True if self.is_active else False

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
from django.contrib.auth.models import User

class Documento(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Relación con el usuario
    nombre = models.CharField(max_length=255)
    archivo = models.URLField()
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

