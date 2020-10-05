from domainmodel.movie import Movie
from domainmodel.review import Review
from domainmodel.director import Director
from domainmodel.genre import Genre
from domainmodel.user import User
from domainmodel.watchlist import WatchList
from domainmodel.actor import Actor
from activitysimulations.watchingsimulation import MovieWatchingSimulation
import pytest
from datafilereaders.movie_file_csv_reader import MovieFileCSVReader


class TestWatchlistMethods:

    def test_size_and_first_movie(self):
        watchlist = WatchList()
        assert watchlist.size == 0
        watchlist.add_movie(Movie("Moana", 2016))
        watchlist.add_movie(Movie("Ice Age", 2002))
        watchlist.add_movie(Movie("Guardians of the Galaxy", 2012))
        assert repr(watchlist.first_movie_in_watchlist) == "<Movie Moana, 2016>"

    def test_first_movie_empty_list(self):
        watchlist = WatchList()
        assert watchlist.first_movie_in_watchlist == None

    def test_add_redundant_movie(self):
        watchlist = WatchList()
        watchlist.add_movie(Movie("Moana", 2016))
        watchlist.add_movie(Movie("Ice Age", 2002))
        watchlist.add_movie(Movie("Guardians of the Galaxy", 2012))
        watchlist.add_movie(Movie("Moana", 2016))
        assert watchlist.size == 3

    def test_remove_movies(self):
        watchlist = WatchList()
        watchlist.add_movie(Movie("Moana", 2016))
        watchlist.add_movie(Movie("Ice Age", 2002))
        watchlist.add_movie(Movie("Guardians of the Galaxy", 2012))
        watchlist.remove_movie(Movie("Moana", 2016))
        assert watchlist.size == 2
        watchlist.remove_movie(Movie("Transformers", 2007))
        assert watchlist.size == 2

    def test_select_movie(self):
        watchlist = WatchList()
        watchlist.add_movie(Movie("Moana", 2016))
        watchlist.add_movie(Movie("Ice Age", 2002))
        watchlist.add_movie(Movie("Guardians of the Galaxy", 2012))
        watchlist.add_movie(Movie("Transformers", 2007))
        assert repr(watchlist.select_movie_to_watch(3)) == "<Movie Transformers, 2007>"
        assert watchlist.select_movie_to_watch(10) == None

    def test_iteration(self):
        watchlist = WatchList()
        watchlist.add_movie(Movie("Moana", 2016))
        watchlist.add_movie(Movie("Ice Age", 2002))
        watchlist.add_movie(Movie("Guardians of the Galaxy", 2012))
        watchlist.add_movie(Movie("Transformers", 2007))
        movie_iter = iter(watchlist)
        assert repr(next(movie_iter)) == "<Movie Moana, 2016>"
        assert repr(next(movie_iter)) == "<Movie Ice Age, 2002>"
        assert repr(next(movie_iter)) == "<Movie Guardians of the Galaxy, 2012>"
        last = next(movie_iter)
        assert repr(last) == "<Movie Transformers, 2007>"


class TestWatchingSimulationsMethods:

    def test_init(self):
        # initialise the different movies
        movies = [Movie("Moana", 2016), Movie("Guardians of the Galaxy", 2014), Movie("Ice Age", 2002), Movie("Transformers", 2007)]
        movies[0].runtime_minutes = 107
        movies[1].runtime_minutes = 121
        movies[2].runtime_minutes = 103
        movies[3].runtime_minutes = 144
        movie = Movie("Us", 2019)
        movie.runtime_minutes = 121
        random_movie1 = Movie("Black Panther", 2018)
        random_movie1.runtime_minutes = 135
        random_movie2 = Movie("Night School", 2018)
        random_movie2.runtime_minutes = 112

        # user 1
        user1 = User("Martin", "pw12345")
        for mov in movies:
            user1.watch_movie(mov)
        user1.watchlist.add_movie(movie)
        user1.watchlist.add_movie(random_movie1)
        assert user1.time_spent_watching_movies_minutes == 475
        assert repr(user1.watched_movies) == "[<Movie Moana, 2016>, <Movie Guardians of the Galaxy, 2014>, <Movie Ice Age, 2002>, <Movie Transformers, 2007>]"
        assert user1.watchlist.size == 2

        # user 2
        user2 = User("Alfie", "pw23456")
        user2.watch_movie(movies[0])
        user2.watchlist.add_movie(random_movie1)
        user2.watchlist.add_movie(random_movie2)
        assert user2.time_spent_watching_movies_minutes == 107
        assert repr(user2.watched_movies) == "[<Movie Moana, 2016>]"
        assert user2.watchlist.size == 2

        # user 3 will be added in after the movie is watchingsimulation
        user3 = User("Yara", "pw34567")
        user3.watch_movie(movies[0])
        user3.watch_movie(movies[2])
        user3.watch_movie(movies[3])
        user3.watchlist.add_movie(movie)
        assert user3.time_spent_watching_movies_minutes == 354
        assert repr(user3.watched_movies) == "[<Movie Moana, 2016>, <Movie Ice Age, 2002>, <Movie Transformers, 2007>]"
        assert user3.watchlist.size == 1

        # user 4
        user4 = User("Danny", "pw45678")
        user4.watch_movie(movies[0])
        user4.watch_movie(movies[2])
        user4.watch_movie(movie)
        user4.watchlist.add_movie(random_movie2)
        assert user4.time_spent_watching_movies_minutes == 331
        assert repr(user4.watched_movies) == "[<Movie Moana, 2016>, <Movie Ice Age, 2002>, <Movie Us, 2019>]"
        assert user4.watchlist.size == 1

        user_list = [user1, user2, user4]
        simulation = MovieWatchingSimulation(movie, user_list)
        assert repr(simulation.movie) == "<Movie Us, 2019>"
        assert repr(simulation.user_list) == "[<User martin>, <User alfie>, <User danny>]"

    def test_remove_from_watchlist(self):
        # initialise the different movies
        movies = [Movie("Moana", 2016), Movie("Guardians of the Galaxy", 2014), Movie("Ice Age", 2002),
                  Movie("Transformers", 2007)]
        movies[0].runtime_minutes = 107
        movies[1].runtime_minutes = 121
        movies[2].runtime_minutes = 103
        movies[3].runtime_minutes = 144
        movie = Movie("Us", 2019)
        movie.runtime_minutes = 121
        random_movie1 = Movie("Black Panther", 2018)
        random_movie1.runtime_minutes = 135
        random_movie2 = Movie("Night School", 2018)
        random_movie2.runtime_minutes = 112

        # user 1
        user1 = User("Martin", "pw12345")
        for mov in movies:
            user1.watch_movie(mov)
        user1.watchlist.add_movie(movie)
        user1.watchlist.add_movie(random_movie1)

        # user 2
        user2 = User("Alfie", "pw23456")
        user2.watch_movie(movies[0])
        user2.watchlist.add_movie(random_movie1)
        user2.watchlist.add_movie(random_movie2)

        # user 3 will be added in after the movie is watchingsimulation
        user3 = User("Yara", "pw34567")
        user3.watch_movie(movies[0])
        user3.watch_movie(movies[2])
        user3.watch_movie(movies[3])
        user3.watchlist.add_movie(movie)

        # user 4
        user4 = User("Danny", "pw45678")
        user4.watch_movie(movies[0])
        user4.watch_movie(movies[2])
        user4.watch_movie(movie)
        user4.watchlist.add_movie(random_movie2)

        user_list = [user1, user2, user4]
        simulation = MovieWatchingSimulation(movie, user_list)
        assert repr(simulation.movie) == "<Movie Us, 2019>"
        assert repr(simulation.user_list) == "[<User martin>, <User alfie>, <User danny>]"

        assert user1.watchlist.size == 1
        assert user2.watchlist.size == 2
        assert user3.watchlist.size == 1
        assert user4.watchlist.size == 1

    def test_add_watch_statistics(self):
        # initialise the different movies
        movies = [Movie("Moana", 2016), Movie("Guardians of the Galaxy", 2014), Movie("Ice Age", 2002),
                  Movie("Transformers", 2007)]
        movies[0].runtime_minutes = 107
        movies[1].runtime_minutes = 121
        movies[2].runtime_minutes = 103
        movies[3].runtime_minutes = 144
        movie = Movie("Us", 2019)
        movie.runtime_minutes = 121
        random_movie1 = Movie("Black Panther", 2018)
        random_movie1.runtime_minutes = 135
        random_movie2 = Movie("Night School", 2018)
        random_movie2.runtime_minutes = 112

        # user 1
        user1 = User("Martin", "pw12345")
        for mov in movies:
            user1.watch_movie(mov)
        user1.watchlist.add_movie(movie)
        user1.watchlist.add_movie(random_movie1)

        # user 2
        user2 = User("Alfie", "pw23456")
        user2.watch_movie(movies[0])
        user2.watchlist.add_movie(random_movie1)
        user2.watchlist.add_movie(random_movie2)

        # user 3 will be added in after the movie is watchingsimulation
        user3 = User("Yara", "pw34567")
        user3.watch_movie(movies[0])
        user3.watch_movie(movies[2])
        user3.watch_movie(movies[3])
        user3.watchlist.add_movie(movie)

        # user 4
        user4 = User("Danny", "pw45678")
        user4.watch_movie(movies[0])
        user4.watch_movie(movies[2])
        user4.watch_movie(movie)
        user4.watchlist.add_movie(random_movie2)

        user_list = [user1, user2, user4]
        simulation = MovieWatchingSimulation(movie, user_list)

        assert user1.time_spent_watching_movies_minutes == 596
        assert repr(user1.watched_movies) == "[<Movie Moana, 2016>, <Movie Guardians of the Galaxy, 2014>, <Movie Ice Age, 2002>, <Movie Transformers, 2007>, <Movie Us, 2019>]"
        assert user2.time_spent_watching_movies_minutes == 228
        assert repr(user2.watched_movies) == "[<Movie Moana, 2016>, <Movie Us, 2019>]"
        assert user3.time_spent_watching_movies_minutes == 354
        assert repr(user3.watched_movies) == "[<Movie Moana, 2016>, <Movie Ice Age, 2002>, <Movie Transformers, 2007>]"
        assert user4.time_spent_watching_movies_minutes == 452
        assert repr(user4.watched_movies) == "[<Movie Moana, 2016>, <Movie Ice Age, 2002>, <Movie Us, 2019>, <Movie Us, 2019>]"

    def test_add_user(self):
        # initialise the different movies
        movies = [Movie("Moana", 2016), Movie("Guardians of the Galaxy", 2014), Movie("Ice Age", 2002),
                  Movie("Transformers", 2007)]
        movies[0].runtime_minutes = 107
        movies[1].runtime_minutes = 121
        movies[2].runtime_minutes = 103
        movies[3].runtime_minutes = 144
        movie = Movie("Us", 2019)
        movie.runtime_minutes = 121
        random_movie1 = Movie("Black Panther", 2018)
        random_movie1.runtime_minutes = 135
        random_movie2 = Movie("Night School", 2018)
        random_movie2.runtime_minutes = 112

        # user 1
        user1 = User("Martin", "pw12345")
        for mov in movies:
            user1.watch_movie(mov)
        user1.watchlist.add_movie(movie)
        user1.watchlist.add_movie(random_movie1)

        # user 2
        user2 = User("Alfie", "pw23456")
        user2.watch_movie(movies[0])
        user2.watchlist.add_movie(random_movie1)
        user2.watchlist.add_movie(random_movie2)

        # user 3 will be added in after the movie is watchingsimulation
        user3 = User("Yara", "pw34567")
        user3.watch_movie(movies[0])
        user3.watch_movie(movies[2])
        user3.watch_movie(movies[3])
        user3.watchlist.add_movie(movie)

        # user 4
        user4 = User("Danny", "pw45678")
        user4.watch_movie(movies[0])
        user4.watch_movie(movies[2])
        user4.watch_movie(movie)
        user4.watchlist.add_movie(random_movie2)

        user_list = [user1, user2, user4]
        simulation = MovieWatchingSimulation(movie, user_list)

        assert user3.time_spent_watching_movies_minutes == 354
        assert repr(user3.watched_movies) == "[<Movie Moana, 2016>, <Movie Ice Age, 2002>, <Movie Transformers, 2007>]"
        assert user3.watchlist.size == 1

        simulation.add_user(user3)

        assert user3.time_spent_watching_movies_minutes == 475
        assert repr(user3.watched_movies) == "[<Movie Moana, 2016>, <Movie Ice Age, 2002>, <Movie Transformers, 2007>, <Movie Us, 2019>]"
        assert user3.watchlist.size == 0

    def test_add_review(self):
        # initialise the different movies
        movies = [Movie("Moana", 2016), Movie("Guardians of the Galaxy", 2014), Movie("Ice Age", 2002),
                  Movie("Transformers", 2007)]
        movies[0].runtime_minutes = 107
        movies[1].runtime_minutes = 121
        movies[2].runtime_minutes = 103
        movies[3].runtime_minutes = 144
        movie = Movie("Us", 2019)
        movie.runtime_minutes = 121
        random_movie1 = Movie("Black Panther", 2018)
        random_movie1.runtime_minutes = 135
        random_movie2 = Movie("Night School", 2018)
        random_movie2.runtime_minutes = 112

        # user 1
        user1 = User("Martin", "pw12345")
        for mov in movies:
            user1.watch_movie(mov)
        user1.watchlist.add_movie(movie)
        user1.watchlist.add_movie(random_movie1)

        # user 2
        user2 = User("Alfie", "pw23456")
        user2.watch_movie(movies[0])
        user2.watchlist.add_movie(random_movie1)
        user2.watchlist.add_movie(random_movie2)

        # user 3 will be added in after the movie is watchingsimulation
        user3 = User("Yara", "pw34567")
        user3.watch_movie(movies[0])
        user3.watch_movie(movies[2])
        user3.watch_movie(movies[3])
        user3.watchlist.add_movie(movie)

        # user 4
        user4 = User("Danny", "pw45678")
        user4.watch_movie(movies[0])
        user4.watch_movie(movies[2])
        user4.watch_movie(movie)
        user4.watchlist.add_movie(random_movie2)

        user_list = [user1, user2, user4]
        simulation = MovieWatchingSimulation(movie, user_list)

        user1.add_review(Review(movies[0], "Daughter loved it", 8))
        user1.add_review(Review(movies[1], "Good laugh", 9))
        user1.add_review(Review(movies[2], "Good for the kids", 9))
        user1.add_review(Review(movies[3], "Great action sequences", 7))

        user2.add_review(Review(movies[0], "It was awesome!!", 10))

        user3.add_review(Review(movies[0], "Little siblings absolutely enjoyed it.", 9))
        user3.add_review(Review(movies[2], "Brings back all the good memories", 10))
        user3.add_review(Review(movies[3], "I'm a fan of giant robots now", 9))

        user4.add_review(Review(movies[0], "Watched it too many times now", 6))
        user4.add_review(Review(movies[2], "Take me back", 7))
        user4.add_review(Review(movie, "Greatly thrilling", 9))

        assert len(user1.reviews) == 4
        assert len(user2.reviews) == 1
        assert len(user3.reviews) == 3
        assert len(user4.reviews) == 3

        simulation.add_user(user3)

        simulation.add_review(user1, "Very entertaining and suspenseful", 9)
        simulation.add_review(user2, "Definitely not for kids my age", 4)
        simulation.add_review(user3, "Oh that was scary", 9)
        simulation.add_review(user4, "Full of wonderful twists and turns", 10)

        assert len(user1.reviews) == 5
        assert len(user2.reviews) == 2
        assert len(user3.reviews) == 4
        assert len(user4.reviews) == 4
