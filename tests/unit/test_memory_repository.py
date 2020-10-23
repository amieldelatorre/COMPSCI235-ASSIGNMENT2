from datetime import date, datetime
from typing import List

import pytest

from flix.domainmodel.movie import Movie
from flix.domainmodel.review import Review
from flix.domainmodel.director import Director
from flix.domainmodel.genre import Genre
from flix.domainmodel.user import User
from flix.domainmodel.watchlist import WatchList
from flix.domainmodel.actor import Actor
from flix.adapters.repository import RepositoryException


def test_repository_can_add_a_user(in_memory_repo):
    user = User('Dave', '123456789')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('Dave') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_movie_count(in_memory_repo):
    number_of_movie = in_memory_repo.get_number_of_movies()

    # Check that the query returned 6 Articles.
    assert number_of_movie == 1000


def test_repository_can_add_a_movie(in_memory_repo):
    movie = Movie("Project Power", 2020)
    # print(movie)
    in_memory_repo.add_movie(movie)

    # print(in_memory_repo.get_movies_by_index(1000))
    assert in_memory_repo.get_movies_by_index(1000) is movie


def test_repository_can_retrieve_movie(in_memory_repo):
    movie = in_memory_repo.get_movies_by_index(0)
    assert movie.title == "Guardians of the Galaxy"

    review1 = [review for review in movie.reviews if review.review_text == "Wonderful"][0]
    review2 = [review for review in movie.reviews if review.review_text == "That was amazing"][0]

    assert review1.user.user_name == 'fmercury'
    assert review2.user.user_name == 'thorke'


def test_repository_can_retrieve_movie_with_title_and_year(in_memory_repo):
    movie = in_memory_repo.find_movie_by_title_and_year("Guardians of the Galaxy", 2014)
    assert len(movie.reviews) == 2


def test_repository_does_not_retrieve_a_non_existent_movie(in_memory_repo):
    movie = in_memory_repo.get_movies_by_index(1001)
    assert movie is None


def test_repository_does_not_retrieve_an_review_when_there_are_no_reviews_for_query(in_memory_repo):
    movies = in_memory_repo.browse_movies('asdfasdfas', 'asdfasdf', [], [], None)
    assert len(movies) == 0


def test_repository_retrieves_movies_on_a_search(in_memory_repo):
    movies1 = in_memory_repo.browse_movies(None, None, [], ['action'], None)
    assert len(movies1) == 303

    movies2 = in_memory_repo.browse_movies(None, None, ['angelina jolie'], [], None)
    assert len(movies2) == 7

    movies3 = in_memory_repo.browse_movies(None, 'Ron Clements', [], [], None)
    assert len(movies3) == 2

    movies4 = in_memory_repo.browse_movies(None, None, [], [], 2012)
    assert len(movies4) == 64

    movies5 = in_memory_repo.browse_movies('Guardians', None, [], [], None)
    assert len(movies5) == 1

    movies6 = in_memory_repo.browse_movies('G.I. Joe: Retaliation', 'Jon M. Chu', ['Channing Tatum', "Dwayne Johnson"],
                                            ['Action', 'Adventure', 'Sci-Fi'], 2013)
    assert len(movies6) == 1

def test_repository_gets_movies_with_index_list(in_memory_repo):
    movies = in_memory_repo.get_movies_by_index_list([0, 5, 13])
    assert len(movies) == 3
    assert movies[0].title == "Guardians of the Galaxy"
    assert movies[1].title == "The Great Wall"
    assert movies[2].title == "Moana"


def test_repository_does_not_retrieve_for_nonexistent_index(in_memory_repo):
    movies = in_memory_repo.get_movies_by_index_list([0, 1000])
    assert len(movies) == 1
    assert movies[0].title == "Guardians of the Galaxy"


def test_repository_does_not_retrieve_for_nonexistent_indices(in_memory_repo):
    movies = in_memory_repo.get_movies_by_index_list([1001, 1002])
    assert len(movies) == 0


def test_repository_can_find_index_of_movie(in_memory_repo):
    movie_index = in_memory_repo.find_movie_index(Movie("Guardians of the Galaxy", 2014))
    assert movie_index == 0


def test_repo_can_add_movie_poster_link_and_is_a_dict(in_memory_repo):
    movies = in_memory_repo.get_movies_by_index_list([0, 5, 26])
    movies_dict = in_memory_repo.browse_processing(movies)

    assert type(movies_dict) == dict
    assert movies[0].poster_link == "https://m.media-amazon.com/images/M/MV5BMTAwMjU5OTgxNjZeQTJeQWpwZ15BbWU4MDUxNDYxODEx._V1_SX300.jpg"
    assert movies[1].poster_link == "https://m.media-amazon.com/images/M/MV5BMjA3MjAzOTQxNF5BMl5BanBnXkFtZTgwOTc5OTY1OTE@._V1_SX300.jpg"
    assert movies[2].poster_link == None


def test_repository_can_add_review(in_memory_repo):
    movie = in_memory_repo.get_movies_by_index(0)
    review = Review(movie, "This is pretty lit", 9)

    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(review)


def test_repository_does_not_add_a_review_without_a_movie_properly_attached(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    movie = in_memory_repo.get_movies_by_index(0)
    review = Review(movie, "This is pretty lit", 9)

    user.add_review(review)
    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(review)


def test_repository_can_retrieve_reviews(in_memory_repo):
    assert len(in_memory_repo.get_reviews()) == 2
