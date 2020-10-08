from flask import Blueprint, render_template
from flask import request, redirect, url_for, session
import flix.utilities.utilities as utilities
import flix.utilities.services as services
import flix.adapters.repository as repo
home_blueprint = Blueprint('home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    movies = services.get_random_movies(4, repo.repo_instance)
    refresh_url = url_for('home_bp.home')
    # print(movies)
    movies_dict = services.movie_list_to_dict(movies)
    for key in movies_dict.keys():
        movies_dict[key] = url_for('browse_bp.movie', movie_name=key.title, movie_year=key.year)

    return render_template('home/home.html',
                           movies=movies_dict,
                           refresh_url=refresh_url
                           )
