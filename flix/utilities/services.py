from typing import Iterable
import random
import omdb

from flix.adapters.repository import AbstractRepository
from flix.domainmodel.movie import Movie


def get_random_movies(quantity, repo: AbstractRepository):
    movies_count = repo.get_number_of_movies()

    if quantity >= movies_count:
        # Reduce the quantity of indexes to generate if the repository has an insufficient number of movies.
        quantity = movies_count - 1

    # Pick distinct and random movies.
    random_index = random.sample(range(1, movies_count), quantity)
    movies = repo.get_movies_by_index(random_index)
    #print(movies)

    return movies


def get_movie_poster(movie: Movie):
    omdb.set_default('apikey', "b03ac630")
    result = omdb.search_movie(movie.title)
    to_return = None
    try:
        to_return = result[0]["poster"]
    except:
        pass
    return to_return

# ============================================
# Functions to convert dicts to model entities
# ============================================


def movie_list_to_dict(movies):
    movies_dict = {}

    for movie in movies:
        movies_dict[movie] = ""
    return movies_dict

"""
def article_to_dict(article: Article):
    article_dict = {
        'date': article.date,
        'title': article.title,
        'image_hyperlink': article.image_hyperlink
    }
    return article_dict


def articles_to_dict(articles: Iterable[Article]):
    return [article_to_dict(article) for article in articles]"""
