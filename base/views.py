from django.shortcuts import render
from django.db.models import Count
from django.http import QueryDict
from .forms import FilmForm, ActorForm
from .models import Film, Actor

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Create your views here.
def base(request):
    return render(request, "base/base.html")


def list_films(request):
    films = []
    if request.method == "POST":
        form = FilmForm(request.POST)
        args = QueryDict(request.body, mutable=True)
        genres = args.getlist("genres")
        if len(genres) > 0:
            # source https://stackoverflow.com/questions/32963210/django-filter-where-manytomany-field-contains-all-of-list
            films = (
                Film.objects.filter(genres__name__in=genres)
                .annotate(num_genre=Count("genres"))
                .filter(num_genre=len(genres))
                .filter(title__contains=request.POST.get("title"))
            )
        else:
            films = Film.objects.filter(title__contains=request.POST.get("title"))

        if form.is_valid():
            render(request, "base/film_list.html", {"form": form, "films": films})
    else:
        films = Film.objects.all()
        form = FilmForm()

    return render(request, "base/film_list.html", {"form": form, "films": films})


def get_film(request, film_id):
    film = Film.objects.get(pk=film_id)
    return render(request, "base/film.html", {"film": film})


def get_actor_films(request, actor_id):
    films = Film.objects.filter(principal_actors__id=actor_id)
    actor = Actor.objects.get(pk=actor_id)
    return render(
        request, "base/actor_film_list.html", {"actor": actor, "films": films}
    )


def list_actors(request):
    actors = []
    if request.method == "POST":
        form = ActorForm(request.POST)
        actors = Actor.objects.filter(name__contains=request.POST.get("name"))

        if form.is_valid():
            render(request, "base/actor_list.html", {"form": form, "actors": actors})
    else:
        actors = Actor.objects.all()
        form = ActorForm()

    return render(request, "base/actor_list.html", {"form": form, "actors": actors})


def recommend_films(request, film_id):
    # source https://heartbeat.fritz.ai/recommender-systems-with-python-part-i-content-based-filtering-5df4940bd831

    # Filter by categories so that we have a smaller dataset
    film = Film.objects.get(pk=film_id)
    genres = film.genres.all()
    films = Film.objects.filter(genres__in=genres).distinct()
    ds = pd.DataFrame.from_dict(films.values())

    # TF-IDF
    tf = TfidfVectorizer(
        analyzer="word", ngram_range=(1, 3), min_df=0, stop_words="english"
    )
    tfidf_matrix = tf.fit_transform(ds["description"])

    # Cosine similarities
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
    results = {}
    for idx, row in ds.iterrows():
        similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
        similar_items = [
            (cosine_similarities[idx][i], ds["id"][i]) for i in similar_indices
        ]
        results[row["id"]] = similar_items[1:]

    num = 12
    recs = results[int(film_id)][:num]
    film_pks = [pk[1] for pk in recs]
    films = Film.objects.filter(pk__in=film_pks)
    return render(request, "base/recommended_film_list.html", {'films': films, 'film': film})

def __item(item_id, ds):
    return ds.loc[ds["id"] == int(item_id)]["description"].tolist()[0].split(" - ")[0]