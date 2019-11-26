from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("load_data/", views.cargar_datos),
    path("user_list_occupation/", views.listar_usuarios_por_ocupacion),
    path("search_film_by_year/", views.buscar_peliculas_anyo),
    path("search_user_ratings/", views.buscar_puntuacion_usuario),
    path("list_best_rated_films/", views.listar_peliculas_mejor_puntuacion),
]
