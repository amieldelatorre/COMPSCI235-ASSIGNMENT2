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
from flix.domainmodel.review import make_review


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self._movies = list()
        self._users = list()
        self._reviews = list()

    def add_user(self, user: User):
        self._users.append(user)

    def get_user(self, username) -> User:
        return next((user for user in self._users if user.user_name == username.lower()), None)

    def add_review(self, review: Review):
        super().add_review(review)
        self._reviews.append(review)

    def get_reviews(self):
        return self._reviews

    def add_movie(self, movie: Movie):
        self._movies.append(movie)

    def get_movie(self, movie_name: str):
        movie_list = list()
        for i in range(len(self._movies)):
            if movie_name in self._movies[i].title:
                movie_list.append(self._movies[i])
        return movie_list

    def get_movies_by_index(self, index):
        movie = None
        # print(self._movies)
        try:
            movie = self._movies[index]
        except:
            pass

        return movie

    def get_movies_by_index_list(self, index_list):
        movies = list()
        for index in index_list:
            try:
                movie = self._movies[index]
            except:
                continue
            #print(movie)
            movie.poster_link = services.get_movie_poster(movie)
            movies.append(movie)
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
        for movie in movies_list:
            movie.poster_link = services.get_movie_poster(movie)

        movies_dict = services.movie_list_to_dict(movies_list)

        return movies_dict

    def get_number_of_movies(self):
        return len(self._movies)

    def find_movie_by_title_and_year(self, title: str, year: int):
        movie_obj = Movie(title, year)
        index = self._movies.index(movie_obj)
        to_return = self._movies[index]
        return to_return

    def find_movie_index(self, movie: Movie):
        return self._movies.index(movie)


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def load_movies(data_path: str, repo: MemoryRepository):
    reader = MovieFileCSVReader(os.path.join(data_path, 'Data1000Movies.csv'))
    reader.read_csv_file()
    repo._movies = reader.dataset_of_movies
    #print('here')


def load_users(data_path: str, repo: MemoryRepository):
    #print(data_path)
    for data_row in read_csv_file(os.path.join(data_path, 'users.csv')):
        user = User(data_row[1], generate_password_hash(data_row[2]))
        repo.add_user(user)


def load_review(data_path: str, repo: MemoryRepository):
    for data_row in read_csv_file(os.path.join(data_path, 'reviews.csv')):
        # print(data_row)
        review = make_review(data_row[4], int(data_row[3]), repo._users[int(data_row[1])], repo._movies[int(data_row[2])])
        # print(review)
        repo.add_review(review)


def populate(data_path: str, repo: MemoryRepository):
    load_movies(data_path, repo)
    load_users(data_path, repo)
    load_review(data_path, repo)
    # print(repo._reviews)
    # print(repo._users[0])
    # print(repo.get_movie("Guardian"))


