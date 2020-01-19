from django.shortcuts import render
from .models import Film

# Create your views here.
def base(request):
    return render(request, 'base/base.html')

def list_films(request):
    films = Film.objects.all()
    return render(request, 'base/film_list.html', {'films': films})