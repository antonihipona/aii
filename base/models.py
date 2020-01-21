from django.db import models

class Actor(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')
    image_url = models.CharField(max_length=100, verbose_name='Imagen')

class Genre(models.Model):
    name = models.CharField(max_length=50, verbose_name='Género')

    def __str__(self):
        return self.name

class Film(models.Model):
    title = models.CharField(max_length=100, verbose_name='Título')
    description = models.CharField(max_length=1000, verbose_name='Descripción')
    rating = models.IntegerField(verbose_name='Puntuación')
    trailer_url = models.CharField(max_length=100, verbose_name='Trailer')
    image_url = models.CharField(max_length=100, verbose_name='Imagen')
    release_date = models.DateField(verbose_name='Fecha de estreno', null=True, blank=True, default=None)
    genres = models.ManyToManyField(Genre, through='FilmGenre', related_name='genres')
    principal_actors = models.ManyToManyField(Actor, through='FilmActor', related_name='principal_actors')

    def __str__(self):
        return "{} | {}".format(self.title, self.genres.all())

class FilmGenre(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

class FilmActor(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)