from flask import Blueprint, render_template
import flix.utilities.utilities as utilities
import flix.utilities.services as services
import flix.adapters.repository as repo
home_blueprint = Blueprint('home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    movies = services.get_random_movies(4, repo.repo_instance)
    # print(movies)
    return render_template('home/home.html',
                           movies=movies
                           )
