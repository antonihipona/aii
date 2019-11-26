from django.shortcuts import render, redirect
from principal.models import Usuario, Director
from principal.forms import UserForm, DirectorForm

def index(request):
    return render(request, "principal/base.html")

def user_list(request):
    users = Usuario.objects.all()
    return render(request, "principal/user_list.html", {"users": users})

def director_list(request):
    directors = Director.objects.all()
    return render(request, "principal/director_list.html", {"directors": directors})


def register_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/user_list/')
    else:
        form = UserForm()

    return render(request, 'principal/register_user.html', {'form': form})

def register_director(request):
    if request.method == 'POST':
        form = DirectorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/director_list/')
    else:
        form = DirectorForm()

    return render(request, 'principal/register_director.html', {'form': form})