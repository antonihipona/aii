from django.urls import path
from . import views

urlpatterns = [
    path("", views.load_data, name='load_data')
]