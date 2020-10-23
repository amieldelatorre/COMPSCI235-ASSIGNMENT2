import abc
from typing import List
from datetime import date

from flix.domainmodel.actor import Actor
from flix.domainmodel.director import Director
from flix.domainmodel.genre import Genre
from flix.domainmodel.movie import Movie
from flix.domainmodel.review import Review
from flix.domainmodel.user import User
from flix.domainmodel.watchlist import WatchList


repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username) -> User:
        """ Returns the User named username from the repository.

        If there is no User with the given username, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """ Adds a Comment to the repository.

        If the Comment doesn't have bidirectional links with an Article and a User, this method raises a
        RepositoryException and doesn't update the repository.
        """
        if review.user is None or review not in review.user.reviews:
            raise RepositoryException('Comment not correctly attached to a User')
        if review.movie is None or review not in review.movie.reviews:
            raise RepositoryException('Comment not correctly attached to an Article')

    @abc.abstractmethod
    def get_reviews(self):
        """ Returns the Comments stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie(self, movie: Movie):
        """" Adds a Movie to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie(self, movie_name: str):
        """ Returns the Movie named movie from the repository.

        If there is no Movie with the given name, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def browse_movies(self, search_param_list):
        """ Returns movies in order from the list"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_index_list(self, index_list):
        """ Returns a list of movies that have been found through their indexes """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_index(self, index):
        """ Returns a movies that have been found through an index """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_movies(self):
        """ Returns the amount of movies in the repo"""
        raise NotImplementedError

    @abc.abstractmethod
    def browse_processing(self, movies_list):
        """ Here the movies list will be turned into a dict and will gather the posters and return a dict """
        raise NotImplementedError

    @abc.abstractmethod
    def find_movie_by_title_and_year(self, title: str, year: int):
        """ Will find a movie by title and year """
        raise NotImplementedError

    def find_movie_index(self, movie: Movie):
        """ Will use a movie object to find it's index """
        raise NotImplementedError





