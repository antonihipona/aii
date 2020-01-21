from django.urls import path
from . import views

urlpatterns = [
    path("", views.base, name='base'),
    path("films/", views.list_films, name='list_films'),
    path("film/<film_id>", views.get_film, name='get_film'),
    path("films/actor/<actor_id>", views.get_actor_films, name='get_actor_films'),
    path("actors/", views.list_actors, name='list_actors'),
]