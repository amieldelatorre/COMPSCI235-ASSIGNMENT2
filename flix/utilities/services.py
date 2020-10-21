from typing import Iterable
import random
import omdb

from flix.adapters.repository import AbstractRepository
from flix.domainmodel.movie import Movie
from flix.domainmodel.review import Review


def get_random_movies(quantity, repo: AbstractRepository):
    movies_count = repo.get_number_of_movies()

    if quantity >= movies_count:
        # Reduce the quantity of indexes to generate if the repository has an insufficient number of movies.
        quantity = movies_count - 1

    # Pick distinct and random movies.
    random_index = random.sample(range(1, movies_count), quantity)
    movies = repo.get_movies_by_index_list(random_index)
    #print(movies)

    return movies


def get_movie_poster(movie: Movie):
    omdb.set_default('apikey', "b03ac630")
    result = omdb.get(title=movie.title, year=movie.year, fullplot=True, tomatoes=True)
    to_return = None
    try:
        to_return = result['poster']
    except:
        pass
    return to_return


def add_review(movie: Movie, review_txt: str, rating: int, username: str, repo: AbstractRepository):
    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    review = Review(movie, review_txt, rating)
    review.user = user
    user.add_review(review)
    # print(movie, user)
    movie.add_review(review)

    repo.add_review(review)


class UnknownUserException(Exception):
    pass
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
