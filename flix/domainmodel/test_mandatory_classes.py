from flix.domainmodel.movie import Movie
from flix.domainmodel.review import Review
from flix.domainmodel.director import  Director
from flix.domainmodel.genre import Genre
from flix.domainmodel.user import User
from flix.domainmodel.watchlist import WatchList
from flix.domainmodel.actor import Actor
import pytest
from flix.datafilereaders.movie_file_csv_reader import MovieFileCSVReader


class TestDirectorMethods:

    def test_init(self):
        director1 = Director("Taika Waititi")
        assert repr(director1) == "<Director Taika Waititi>"
        director2 = Director("")
        assert director2.director_full_name is None
        director3 = Director(42)
        assert director3.director_full_name is None

    def test_director_full_name(self):
        director1 = Director("Taika Waititi")
        assert director1.director_full_name == "Taika Waititi"

    def test_eq(self):
        director1 = Director("Taika Waititi")
        director2 = Director("Kevin Alejandro")
        assert director1 != director2
        director3 = Director("Taika Waititi")
        assert director1 == director3

    def test_lt(self):
        director1 = Director("Taika Waititi")
        director2 = Director("Kevin Alejandro")
        assert director2 < director1


class TestGenreMethods:
    def test_init(self):
        genre1 = Genre("Action")
        assert repr(genre1) == "<Genre Action>"
        genre2 = Genre("")
        assert genre2.genre_name is None
        genre3 = Genre(42)
        assert genre3.genre_name is None

    def test_director_full_name(self):
        genre = Genre("Comedy")
        assert genre.genre_name == "Comedy"

    def test_eq(self):
        genre1 = Genre("Action")
        genre2 = Genre("Comedy")
        assert genre1 != genre2
        genre3 = Genre("Action")
        assert genre1 == genre3

    def test_lt(self):
        genre1 = Genre("Action")
        genre2 = Genre("Comedy")
        assert genre1 < genre2


class TestActorMethods:

    def test_init(self):
        actor1 = Actor("Angelina Jolie")
        assert actor1.__repr__() == "<Actor Angelina Jolie>"
        actor2 = Actor("")
        assert actor2.__repr__() == "<Actor None>"
        actor3 = Actor(27)
        assert actor3.__repr__() == "<Actor None>"
        assert actor1


