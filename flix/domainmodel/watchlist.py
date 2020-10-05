from domainmodel.movie import Movie
from typing import List


class WatchList:
    def __init__(self):
        self.__movies: List[Movie] = list()

    def add_movie(self, movie: Movie):
        if movie not in self.__movies:
            self.__movies.append(movie)

    def remove_movie(self, movie: Movie):
        if movie in self.__movies:
            self.__movies.remove(movie)

    def select_movie_to_watch(self, index: int):
        if self.__movies == []:
            return None
        elif index >= 0 and index < len(self.__movies):
            return self.__movies[index]

        else:
            return None

    @property
    def movies(self) -> List[Movie]:
        return self.__movies

    @property
    def size(self) -> int:
        return len(self.__movies)

    @property
    def first_movie_in_watchlist(self) -> Movie:
        if self.__movies == []:
            return None
        else:
            return self.__movies[0]

    def __iter__(self):
        self.__index = 0
        return self

    def __next__(self):
        if self.__index < len(self.__movies):
            result = self.__movies[self.__index]
            self.__index += 1
            return result
        raise StopIteration


"""watchlist = WatchList()
watchlist.add_movie(Movie("Moana", 2016))
watchlist.add_movie(Movie("Ice Age", 2002))
watchlist.add_movie(Movie("Guardians of the Galaxy", 2012))
watchlist.add_movie(Movie("Transformers", 2007))

for movie in watchlist:
    print(movie)"""
