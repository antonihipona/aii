from django.shortcuts import render
from django.db.models import Count
from django.http import QueryDict
from .forms import FilmForm, ActorForm
from .models import Film, Actor

# Create your views here.
def base(request):
    return render(request, 'base/base.html')

def list_films(request):
    films = []
    if request.method == 'POST':
        form = FilmForm(request.POST)
        args = QueryDict(request.body, mutable=True)
        genres = args.getlist('genres')
        if len(genres) > 0:
            # source https://stackoverflow.com/questions/32963210/django-filter-where-manytomany-field-contains-all-of-list
            films = Film.objects.filter(genres__name__in=genres).annotate(num_genre=Count('genres')).filter(num_genre=len(genres)).filter(title__contains=request.POST.get('title'))
        else:
            films = Film.objects.filter(title__contains=request.POST.get('title'))

        if form.is_valid():
            render(request, 'base/film_list.html', {'form': form, 'films': films})
    else:
        films = Film.objects.all()
        form = FilmForm()

    return render(request, 'base/film_list.html', {'form': form, 'films': films})

def get_film(request, film_id):
    film = Film.objects.get(pk=film_id)
    return render(request, 'base/film.html', {'film': film})

def get_actor_films(request, actor_id):
    films = Film.objects.filter(principal_actors__id=actor_id)
    actor = Actor.objects.get(pk=actor_id)
    return render(request, 'base/actor_film_list.html', {'actor': actor, 'films': films})

def list_actors(request):
    actors = []
    if request.method == 'POST':
        form = ActorForm(request.POST)
        actors = Actor.objects.filter(name__contains=request.POST.get('name'))

        if form.is_valid():
            render(request, 'base/actor_list.html', {'form': form, 'actors': actors})
    else:
        actors = Actor.objects.all()
        form = ActorForm()

    return render(request, 'base/actor_list.html', {'form': form, 'actors': actors})