from flask import Blueprint, render_template
from flask import request, redirect, url_for, session
import flix.utilities.utilities as utilities
import flix.utilities.services as services
import flix.adapters.repository as repo

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange, InputRequired
from wtforms.widgets import html5 as widgets


browse_blueprint = Blueprint('browse_bp', __name__)


@browse_blueprint.route('/browse', methods=['GET'])
def browse():
    movie_index = 0
    search_url = url_for('browse_bp.movie_search')
    return render_template('movies/browse.html',
                           search_url=search_url,
                           movies={}
                           )


@browse_blueprint.route('/movie_search', methods=['GET', 'POST'])
def movie_search():
    movies_per_page = 4
    search_param = request.args.get('search')
    search_param_list = search_param.split(',')
    for i in range(len(search_param_list)):
        search_param_list[i] = search_param_list[i].strip()

    movies = repo.repo_instance.browse_movies(search_param_list)
    # print(len(movies))
    # processed_movies = repo.repo_instance.browse_processing(movies)

    cursor = request.args.get('cursor')

    if cursor is None:
        cursor = 0
    else:
        cursor = int(cursor)

    movies_to_show = movies[cursor:cursor + movies_per_page]
    processed_movies = repo.repo_instance.browse_processing(movies_to_show)

    prev_movie_url = None
    next_movie_url = None
    first_movie_url = None
    last_movie_url = None

    if cursor > 0:
        prev_movie_url = url_for('browse_bp.movie_search',  search=search_param, cursor=cursor-movies_per_page)
        first_movie_url = url_for('browse_bp.movie_search',  search=search_param)

    if cursor + movies_per_page < len(movies):
        next_movie_url = url_for('browse_bp.movie_search', search=search_param, cursor=cursor+movies_per_page)

        last_cursor = movies_per_page * int(len(movies) / movies_per_page)
        if len(movies) % movies_per_page == 0:
            last_cursor -= movies_per_page

        last_movie_url = url_for('browse_bp.movie_search', search=search_param, cursor=last_cursor)
    for key in processed_movies.keys():
        processed_movies[key] = url_for('browse_bp.movie', movie_name=key.title, movie_year=key.year)

    return render_template('movies/browse.html',
                           movies=processed_movies,
                           next_movie_url=next_movie_url,
                           prev_movie_url=prev_movie_url,
                           first_movie_url=first_movie_url,
                           last_movie_url=last_movie_url
                           )


@browse_blueprint.route('/movie', methods=['GET', 'POST'])
def movie():
    form = ReviewForm()

    try:
        title = request.args.get('movie_name')
        year = int(request.args.get('movie_year'))
    except:
        return redirect(url_for('home_bp.home'))
    mov = repo.repo_instance.find_movie_by_title_and_year(title, year)
    # print(title,year,mov)
    poster_link = services.get_movie_poster(mov)

    search_list_of_dict = list()
    # indexes = 0 --> genres, 1 --> actors,3 --> director
    genre_dict = {}
    actor_dict = {}
    director_dict = {}
    for genre in mov.genres:
        genre_dict[genre.genre_name] = url_for('browse_bp.movie_search',  search=genre.genre_name)
    search_list_of_dict.append(genre_dict)

    for actor in mov.actors:
        actor_dict[actor.actor_full_name] = url_for('browse_bp.movie_search', search=actor.actor_full_name)
    search_list_of_dict.append(actor_dict)

    director_dict[mov.director.director_full_name] = url_for('browse_bp.movie_search', search=mov.director.director_full_name)
    search_list_of_dict.append(director_dict)

    form.movie = mov
    try:
        username = session['username']

        if repo.repo_instance.get_user(username) is not None:
            if form.validate_on_submit():
                services.add_review(form.movie, form.review.data, form.rating.data, username, repo.repo_instance)

                return redirect(url_for('browse_bp.movie', movie_name=form.movie.title, movie_year=form.movie.year))
    except KeyError:
        pass


    return render_template('movies/movie.html',
                           movie=mov,
                           poster_link=poster_link,
                           links=search_list_of_dict,
                           form=form,
                           handler_url=url_for('browse_bp.movie', movie_name=mov.title, movie_year=mov.year)
                           )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    review = TextAreaField('Review Text', [
        DataRequired(),
        Length(min=4, message='Your review is too short'),
        ProfanityFree(message='Your review must not contain profanity')])

    rating = IntegerField('Rating', widget=widgets.NumberInput(min=1, max=10), validators=[
        DataRequired(),
        NumberRange(min=1, max=10, message="Value must within the range of 1 - 10")
    ])

    submit = SubmitField('Submit')
    movie = HiddenField("movie")
