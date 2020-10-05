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


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self._movies = list()

    def add_movie(self, movie: Movie):
        self._movies.append(Movie)


def populate(data_path: str, repo: MemoryRepository):
    reader = MovieFileCSVReader(os.path.join(data_path, 'news_articles.csv'))
    repo._movies = reader.dataset_of_movies
