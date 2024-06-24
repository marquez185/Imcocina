from django.db import models
from django.contrib.auth.models import AbstractUser, User

# Create your models here.

class SuperUsuario(AbstractUser):
    nombre = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=30)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'username']

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='superusuario_groups',  # Cambio de related_name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='superusuario_permissions',  # Cambio de related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=30)
    perfil = models.OneToOneField('Perfil', on_delete=models.CASCADE, related_name='usuario_perfil')

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Perfil(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil_usuario')
    preferencias = models.TextField()

    def __str__(self):
        return f"Perfil de {self.usuario.nombre}"

class Busqueda(models.Model):
    titulo = models.CharField(max_length=100)
    ingredientes = models.TextField()
    calorias = models.IntegerField()

    def __str__(self):
        return self.titulo

class Receta(models.Model):
    titulo = models.CharField(max_length=100)
    ingredientes = models.TextField()
    pasos = models.TextField()
    calorias = models.IntegerField()
    informacion_nutricional = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Cambiado a User

    def __str__(self):
        return self.titulo

class Favoritos(models.Model):
    titulo = models.CharField(max_length=255)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    url_id_receta = models.CharField(max_length=255, blank=True, null=True)
    img = models.ImageField(upload_to='favoritos/')
    id_validada = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.titulo
