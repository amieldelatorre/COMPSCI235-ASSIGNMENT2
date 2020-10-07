from flask import Blueprint, render_template
from flask import request, redirect, url_for, session
import flix.utilities.utilities as utilities
import flix.utilities.services as services
import flix.adapters.repository as repo
browse_blueprint = Blueprint('browse_bp', __name__)


@browse_blueprint.route('/browse', methods=['GET'])
def browse():
    global movie_index
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
    search_param_list = search_param.split()
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

    return render_template('movies/browse.html',
                           movies=processed_movies,
                           next_movie_url=next_movie_url,
                           prev_movie_url=prev_movie_url,
                           first_movie_url=first_movie_url,
                           last_movie_url=last_movie_url
                           )
