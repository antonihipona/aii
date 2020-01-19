from django.shortcuts import render
from bs4 import BeautifulSoup, SoupStrainer
import urllib.request
from django.conf import settings
from base.models import Film, Genre, Actor, FilmGenre, FilmActor
from datetime import date, datetime

# Create your views here.
def load_data(request):
    Film.objects.all().delete()
    Genre.objects.all().delete()
    Actor.objects.all().delete()
    FilmGenre.objects.all().delete()
    FilmActor.objects.all().delete()

    page_number = 2
    films = []
    film_genres = []
    film_actors = []
    genres = {}
    actors = {}
    film_id = 0
    genre_id = 0
    actor_id = 0
    for page in range(1, page_number + 1):
        with urllib.request.urlopen(
            settings.BASE_SCRAPING_URL + "/movie?page={}".format(page)
        ) as response:
            html = response.read()
        bs = BeautifulSoup(html, "html.parser", parse_only=SoupStrainer('a'))

        a_tags = bs.findAll("a", {"class": "title"})

        for a in a_tags:
            title = a["title"]
            with urllib.request.urlopen(settings.BASE_SCRAPING_URL + a["href"]) as response:
                html = response.read()
            bs = BeautifulSoup(html, "html.parser")
            section = bs.find('section', {'class': 'images'})
            description = section.find('div', {'class': 'overview'}).p.text
            rating = float(section.find('div', {'class': 'user_score_chart'})['data-percent'])
            trailer_id = section.find('a', {'class': 'play_trailer'})
            if trailer_id:
                trailer_url = 'https://www.youtube.com/watch?v=' + trailer_id['data-id']
            else:
                trailer_url = ''
            image_url = section.find('div', {'class': 'image_content'}).a.img['src'].replace('_filter(blur)', '')

            column = bs.find('div', {'class': 'grey_column'})
            release = column.find('ul', {'class': 'releases'}).li.text.strip().split('\n')[0]
            date = datetime.strptime(release, '%B %d, %Y')
            release_date = date

            # Film
            film = Film(
                id=film_id,
                title=title,
                description=description,
                rating=rating,
                trailer_url=trailer_url,
                image_url=image_url,
                release_date=release_date
            )

            # Film genres
            genre_tags = column.find('section', {'class': 'genres'}).findAll('a')
            genre_titles = map(lambda x: x.text.upper(), genre_tags)
            for g in genre_titles:
                if g not in genres:
                    genre = Genre(id=genre_id, name=g)
                    genres[g] = genre
                    film_genres.append(FilmGenre(film_id=film_id, genre_id=genre.id))
                    genre_id +=1
                else:
                    genre = genres[g]
                    film_genres.append(FilmGenre(film_id=film_id, genre_id=genre.id))


            # Film actors
            scroller = bs.find('ol', {'class': 'scroller'})
            actor_tags = scroller.findAll('li')
            for li in actor_tags:
                name = li.find('p').a.text.strip()
                try:
                    image_url = li.find('img')['data-src']
                except:
                    image_url = 'https://i.ya-webdesign.com/images/default-image-png-1.png'
                if name not in actors:
                    actor = Actor(id=actor_id, name=name, image_url=image_url)
                    actors[name] = actor
                    film_actors.append(FilmActor(film_id=film_id, actor_id=actor.id))
                    actor_id +=1
                else:
                    actor = actors[name]
                    film_actors.append(FilmActor(film_id=film_id, actor_id=actor.id))

            
            film_id += 1
            films.append(film)

    Genre.objects.bulk_create(genres.values())
    Actor.objects.bulk_create(actors.values())
    Film.objects.bulk_create(films)
    FilmGenre.objects.bulk_create(film_genres)
    FilmActor.objects.bulk_create(film_actors)
    return render(request, "dataloader/data_loaded.html", {"films": films})

