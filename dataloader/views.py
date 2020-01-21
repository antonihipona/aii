from django.shortcuts import render
import django
django.setup()
from multiprocessing import Pool
from bs4 import BeautifulSoup, SoupStrainer
import urllib.request
from django.conf import settings
from base.models import Film, Genre, Actor, FilmGenre, FilmActor
from datetime import date, datetime

proc_number = 8

film_id = 0
genre_id = 0
actor_id = 0
film_genres = []
film_actors = []
genres = {}
actors = {}
films = []

def load_data(request):
    return render(request, "dataloader/data_loaded.html", {"films": films})
    Film.objects.all().delete()
    Genre.objects.all().delete()
    Actor.objects.all().delete()
    FilmGenre.objects.all().delete()
    FilmActor.objects.all().delete()

    page_number = 100
    urls = []
    for page in range(1, page_number + 1):
        urls.append(settings.BASE_SCRAPING_URL + "/movie?page={}".format(page))
    p = Pool(proc_number)
    top_html = p.map(get_html, urls)
    p.terminate()
    p.join()

    all_tags = []
    for html in top_html:
        bs = BeautifulSoup(html, "html.parser", parse_only=SoupStrainer('a'))

        all_tags.extend(bs.findAll("a", {"class": "title"}))

    p = Pool(proc_number)
    all_html = p.map(get_html, get_urls(all_tags))
    p.terminate()
    p.join()
    for html in all_html:
        try:
            get_films(html)
        except:
            continue

    Genre.objects.bulk_create(genres.values())
    Actor.objects.bulk_create(actors.values())
    Film.objects.bulk_create(films)
    FilmGenre.objects.bulk_create(film_genres)
    FilmActor.objects.bulk_create(film_actors)
    return render(request, "dataloader/data_loaded.html", {"films": films})

def get_films(html):
    global film_id
    global genre_id
    global actor_id
    bs = BeautifulSoup(html, "html.parser")
    section = bs.find('section', {'class': 'images'})
    description = section.find('div', {'class': 'overview'}).p.text
    rating = float(section.find('div', {'class': 'user_score_chart'})['data-percent'])
    trailer_id = section.find('a', {'class': 'play_trailer'})
    if trailer_id:
        trailer_url = 'https://www.youtube.com/watch?v=' + trailer_id['data-id']
    else:
        trailer_url = ''
    section_img = section.find('div', {'class': 'image_content'}).a.img
    image_url = section_img['src'].replace('_filter(blur)', '')
    title = section_img['alt']

    column = bs.find('div', {'class': 'grey_column'})
    release = column.find('ul', {'class': 'releases'})
    if release:
        release = release.li.text.strip().split('\n')[0]
        date = datetime.strptime(release, '%B %d, %Y')
        release_date = date
    else:
        release_date = None

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

def get_html(url):
    with urllib.request.urlopen(url) as response:
        return response.read()

def get_urls(a_tags):
    urls = []
    for a in a_tags:
        urls.append(settings.BASE_SCRAPING_URL + a["href"])
    return urls
