from django.urls import path
from . import views

urlpatterns = [
    path("", views.base, name='base'),
    path("films/", views.list_films, name='list_films'),
    path("film/<film_id>", views.get_film, name='get_film'),
]