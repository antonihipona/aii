from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("user_list/", views.user_list),
    path("register_user/", views.register_user),
    path("director_list/", views.director_list),
    path("register_director/", views.register_director),
]
