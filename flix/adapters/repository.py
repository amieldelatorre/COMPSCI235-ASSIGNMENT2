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
    def browse_movies(self, search_param_list):
        """ Returns movies in order from the list"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_index(self, index_list):
        """ Returns a list of movies that have been found through their indexes """
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





