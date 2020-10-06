import csv
import os
from datetime import date, datetime
from typing import List

from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash

from flix.adapters.repository import AbstractRepository, RepositoryException
from flix.domainmodel.actor import Actor
from flix.domainmodel.director import Director
from flix.domainmodel.genre import Genre
from flix.domainmodel.movie import Movie
from flix.domainmodel.review import Review
from flix.domainmodel.user import User
from flix.domainmodel.watchlist import WatchList
from flix.datafilereaders.movie_file_csv_reader import MovieFileCSVReader
import flix.utilities.services


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self._movies = list()

    def add_movie(self, movie: Movie):
        self._movies.append(Movie)

    def get_movie(self, movie_name: str):
        movie_list = list()
        for i in range(len(self._movies)):
            if movie_name in self._movies[i].title:
                movie_list.append(self._movies[i])
        return movie_list

    def get_movies_by_index(self, index_list):
        movies = list()
        for index in index_list:
            movies.append(self._movies[index])
        return movies

    def browse_movies(self):
        pass

    def get_number_of_movies(self):
        return len(self._movies)


def populate(data_path: str, repo: MemoryRepository):
    reader = MovieFileCSVReader(data_path)
    reader.read_csv_file()
    repo._movies = reader.dataset_of_movies
    # print(repo.get_movie("Guardian"))


