from domainmodel.movie import Movie
from domainmodel.user import User
from domainmodel.review import Review
from domainmodel.watchlist import WatchList
from typing import List


class MovieWatchingSimulation:
    def __init__(self, movie: Movie, users: List[User]):
        self.__movie: Movie = movie
        self.__user_list: List[User] = users
        self.remove_from_watchlist(users)
        self.add_watch_statistics(users)

    def remove_from_watchlist(self, users: List[User]):
        for user in users:
            user_watchlist = user.watchlist
            user_watchlist.remove_movie(self.__movie)

    def add_watch_statistics(self, users: List[User]):
        for user in users:
            user.watch_movie(self.__movie)

    def add_user(self, user: User):
        self.__user_list.append(user)
        self.remove_from_watchlist([user])
        self.add_watch_statistics([user])

    def add_review(self, user: User, review_text: str, rating: int):
        user_review = Review(self.__movie, review_text, rating)
        user.add_review(user_review)

    @property
    def user_list(self) -> List[User]:
        return self.__user_list

    @property
    def movie(self) -> Movie:
        return self.__movie

    def __iter__(self):
        self.__index = 0
        return self

    def __next__(self):
        if self.__index < len(self.__user_list):
            result = self.__user_list[self.__index]
            self.__index += 1
            return result
        raise StopIteration

