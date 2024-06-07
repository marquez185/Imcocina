from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
 
class SuperUsuario(AbstractUser):
    nombre = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=30)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'username']

class Usuario(models.Model):
    id = models.AutoField(primary_key=True) 
    nombre = models.CharField(max_length=30)  
    apellido = models.CharField(max_length=30)  
    email = models.EmailField(unique=True) 
    contraseña = models.CharField(max_length=30)
    perfil = models.OneToOneField('Perfil', on_delete=models.CASCADE, related_name='usuario')

    def __str__(self):
        return f"{self.nombre} {self.apellido}" 

class Perfil(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
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
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    ingredientes = models.TextField()
    pasos = models.TextField()
    calorias = models.IntegerField()
    informacion_nutricional = models.TextField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='recetas')
    creador = models.CharField(max_length=100)

    def __str__(self):
        return self.titulo