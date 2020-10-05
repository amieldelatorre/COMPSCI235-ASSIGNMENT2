from domainmodel.movie import Movie
from domainmodel.review import Review
from domainmodel.watchlist import WatchList
from typing import List


class User:
    def __init__(self, user_name: str, password: str):
        self.__user_name: str = user_name.strip().lower()
        self.__password: str = password
        self.__watched_movies: List[Movie] = list()
        self.__reviews: List[Review] = list()
        self.__time_spent_watching_movies_minutes: int = 0
        self.__watchlist: WatchList = WatchList()

    @property
    def user_name(self) -> str:
        return self.__user_name

    @property
    def password(self) -> str:
        return self.__password

    @property
    def watched_movies(self) -> List[Movie]:
        return self.__watched_movies

    @property
    def reviews(self) -> List[Review]:
        return self.__reviews

    @property
    def time_spent_watching_movies_minutes(self) -> int:
        return self.__time_spent_watching_movies_minutes

    @property
    def watchlist(self) -> WatchList:
        return self.__watchlist

    def watch_movie(self, movie: Movie):
        self.__watched_movies.append(movie)
        self.__time_spent_watching_movies_minutes += movie.runtime_minutes

    def add_review(self, review: Review):
        self.__reviews.append(review)

    def __repr__(self):
        return f"<User {self.__user_name}>"

    def __eq__(self, other):
        if self.__user_name == other.user_name:
            return True
        else:
            return False

    def __lt__(self, other):
        if self.__user_name < other.user_name:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.__user_name)


"""
movies = [Movie("Moana", 2016), Movie("Guardians of the Galaxy", 2014)]
movies[0].runtime_minutes = 107
movies[1].runtime_minutes = 121
user = User("Martin", "pw12345")
print(user.watched_movies)
print(user.time_spent_watching_movies_minutes)
for movie in movies:
    user.watch_movie(movie)
print(user.watched_movies)
print(user.time_spent_watching_movies_minutes)"""

