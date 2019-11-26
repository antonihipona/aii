from django.db import models
from django.utils.encoding import python_2_unicode_compatible

categorias = [
    ("UN", "Unknown"),
    ("AC", "Action"),
    ("AD", "Adventure"),
    ("AN", "Animation"),
    ("CH", "Children's"),
    ("CO", "Comedy"),
    ("CR", "Crime"),
    ("DO", "Documental"),
    ("DR", "Drama"),
    ("FA", "Fantasy"),
    ("FI", "Film-Noir"),
    ("HO", "Horror"),
    ("MU", "Musical"),
]

class Usuario(models.Model):
    nombre = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=30)
    fecha_nacimiento = models.DateField()
    categoria_preferida = models.CharField(max_length=2,choices=categorias) 

    def __str__(self):
        return "{0} {1}".format(self.nombre, self.apellidos)

class Director(models.Model):
    nombre = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=30)
    biografia = models.TextField()

    def __str__(self):
        return self.nombre

class Pelicula(models.Model):
    titulo = models.CharField(max_length=30)
    anyo = models.IntegerField()
    resumen = models.TextField()
    director = models.ForeignKey(Director, on_delete=models.SET_NULL, null=True)
    categoria = models.CharField(max_length=2,choices=categorias) 

    def __str__(self):
        return self.titulo
