from flix.domainmodel.movie import Movie
from flix.domainmodel.review import Review
from flix.domainmodel.director import  Director
from flix.domainmodel.genre import Genre
from flix.domainmodel.user import User
from flix.domainmodel.watchlist import WatchList
from flix.domainmodel.actor import Actor
import pytest
from flix.datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from flix.activitysimulations.watchingsimulation import MovieWatchingSimulation

class TestMovieMethods:

    def test_init(self):
        movie1 = Movie("Moana", 2016)
        assert repr(movie1) == "<Movie Moana, 2016>"

    def test_get_methods(self):
        movie1 = Movie("Moana", 2016)
        movie1.description = "In Ancient Polynesia, when a terrible curse incurred by the Demigod Maui reaches " \
                             "an impetuous Chieftain's daughter's island, she answers the Ocean's call to seek out " \
                             "the Demigod to set things right."
        movie1.director = Director("Ron Clements")
        actors = ["Auli'i Cravalho", "Dwayne Johnson", "Rachel House", "Temuera Morrison"]
        for actor in actors:
            movie1.add_actor(Actor(actor))
        movie1.runtime_minutes = 107
        movie1.rating = 7.7
        movie1.rating_votes = 118171
        movie1.revenue = 248.75
        movie1.metascore = 81

        assert movie1.description == "In Ancient Polynesia, when a terrible curse incurred by the Demigod Maui reaches " \
                             "an impetuous Chieftain's daughter's island, she answers the Ocean's call to seek out " \
                             "the Demigod to set things right."
        assert repr(movie1.director) == "<Director Ron Clements>"
        assert Actor("Dwayne Johnson") in movie1.actors
        assert movie1.runtime_minutes == 107
        assert movie1.rating == 7.7
        assert movie1.rating_votes == 118171
        assert movie1.revenue == 248.75
        assert movie1.metascore == 81

    def test_eq(self):
        movie1 = Movie("Moana", 2016)
        movie2 = Movie("Chef", 2016)
        assert movie1 != movie2
        movie3 = Movie("Moana", 2016)
        assert movie1 == movie3

    def test_lt(self):
        movie1 = Movie("Moana", 2016)
        movie2 = Movie("Chef", 2016)
        assert movie1 > movie2


class TestReviewMethods:

    def test_init(self):
        movie = Movie("Moana", 2016)
        review_text = "This movie was very enjoyable"
        rating = 8
        review = Review(movie, review_text, rating)
        review.user = User("Me", "1234567890")
        assert review.review_text == "This movie was very enjoyable"
        assert review.rating == 8
        assert repr(review.user) == "<User me>"

    def test_eq(self):
        movie = Movie("Moana", 2016)
        review_text = "This movie was very enjoyable"
        rating = 8
        review = Review(movie, review_text, rating)
        review2 = Review(movie, review_text, rating)
        review3 = Review(movie, review_text + " to watch", rating)
        assert review != review2
        assert review != review3


class TestUserMethods:

    def test_init(self):
        user = User("Me", "1234567890")
        assert repr(user) == "<User me>"

    def test_get_methods(self):
        user = User("Me", "1234567890")
        movie = Movie("Moana", 2016)
        movie.runtime_minutes = 107
        movie2 = Movie("The Guardians of the Galaxy", 2014)
        movie2.runtime_minutes = 121
        review = Review(movie2, "It was really good", 9)
        user.add_review(review)
        user.watch_movie(movie2)
        user.add_to_watchlist(movie)

        assert user.time_spent_watching_movies_minutes == 121
        assert user.reviews[0].review_text == "It was really good"
        assert repr(user.watched_movies[0]) == "<Movie The Guardians of the Galaxy, 2014>"
        assert repr(user.watchlist.movies[0]) == "<Movie Moana, 2016>"



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

