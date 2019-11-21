from django.urls import path
from . import views

urlpatterns = [
    path("user_list/", views.user_list),
    path("register_user/", views.register_user)
]
