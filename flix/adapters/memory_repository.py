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
import flix.utilities.services as services


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self._movies = list()
        self._users = list()

    def add_movie(self, movie: Movie):
        self._movies.append(Movie)

    def get_movie(self, movie_name: str):
        movie_list = list()
        for i in range(len(self._movies)):
            if movie_name in self._movies[i].title:
                movie_list.append(self._movies[i])
        return movie_list

    def get_movies_by_index(self, index_list):
        movies = dict()
        for index in index_list:
            movies[self._movies[index]] = services.get_movie_poster(self._movies[index])
        return movies

    def browse_movies(self, search_param_list):
        movies = list()
        for mov in self._movies:
            goes_into_list = True
            for elem in search_param_list:
                elem = elem.lower()
                elem_found_a_home = False
                if elem in mov.title.lower():
                    elem_found_a_home = True
                    continue
                elif elem in mov.director.director_full_name.lower():
                    elem_found_a_home = True
                    continue
                for genre in mov.genres:
                    if elem in genre.genre_name.lower():
                        elem_found_a_home = True
                        break
                for actor in mov.actors:
                    if elem in actor.actor_full_name.lower():
                        elem_found_a_home = True
                        break
                if elem_found_a_home == False:
                    goes_into_list = False;
                    break
            if goes_into_list:
                movies.append(mov)
        return movies

    def browse_processing(self, movies_list):
        movies_dict = services.movie_list_to_dict(movies_list)
        for key in movies_dict.keys():
            movies_dict[key] = services.get_movie_poster(key)
        return movies_dict

    def get_number_of_movies(self):
        return len(self._movies)


def populate(data_path: str, repo: MemoryRepository):
    reader = MovieFileCSVReader(data_path)
    reader.read_csv_file()
    repo._movies = reader.dataset_of_movies
    # print(repo.get_movie("Guardian"))


