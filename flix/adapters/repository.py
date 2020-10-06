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
    def browse_movies(self):
        """ Returns movies in order from the list"""
        raise NotImplementedError

    def get_movies_by_index(self):
        """ Returns a list of movies that have been found through their indexes """
        raise NotImplementedError

    def get_number_of_movies(self):
        """ Returns the amount of movies in the repo"""
        raise NotImplementedError





