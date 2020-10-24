from flask import Blueprint, render_template
from flask import request, redirect, url_for, session
import flix.utilities.utilities as utilities
import flix.utilities.services as services
import flix.adapters.repository as repo
from flix.authentication.authentication import login_required


user_blueprint = Blueprint('user_bp', __name__)


@user_blueprint.route('/watch', methods=['GET'])
@login_required
def watch():
    username = session['username']
    try:
        title = request.args.get('movie_name')
        year = int(request.args.get('movie_year'))
    except:
        return redirect(url_for('home_bp.home'))
    mov = repo.repo_instance.find_movie_by_title_and_year(title, year)

    user = repo.repo_instance.get_user(username)
    user.watch_movie(mov)
    user.watchlist.remove_movie(mov)

    return redirect(url_for('user_bp.movies_watched'))


@user_blueprint.route('/profile', methods=['GET'])
@login_required
def profile():
    username = session['username']
    user = repo.repo_instance.get_user(username)

    return render_template('user_profile/userpage.html',
                           user=user,
                           heading=None,
                           movies=None
                           )


@user_blueprint.route('/add_to_watchlist', methods=['GET'])
@login_required
def add_to_watchlist():
    username = session['username']
    try:
        title = request.args.get('movie_name')
        year = int(request.args.get('movie_year'))
    except:
        return redirect(url_for('home_bp.home'))
    mov = repo.repo_instance.find_movie_by_title_and_year(title, year)
    user = repo.repo_instance.get_user(username)
    user.watchlist.add_movie(mov)

    return redirect(url_for('user_bp.watchlist'))


@user_blueprint.route('/remove_from_watchlist', methods=['GET'])
@login_required
def remove_from_watchlist():
    username = session['username']
    try:
        title = request.args.get('movie_name')
        year = int(request.args.get('movie_year'))
    except:
        return redirect(url_for('home_bp.home'))
    mov = repo.repo_instance.find_movie_by_title_and_year(title, year)
    user = repo.repo_instance.get_user(username)
    user.watchlist.remove_movie(mov)
    print(user.watchlist.movies)
    return redirect(url_for('user_bp.watchlist'))


@user_blueprint.route('/watchlist', methods=['GET'])
@login_required
def watchlist():
    movies_per_page = 4
    username = session['username']
    user = repo.repo_instance.get_user(username)
    movies = user.watchlist.movies

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
        prev_movie_url = url_for('user_bp.watchlist', cursor=cursor - movies_per_page)
        first_movie_url = url_for('user_bp.watchlist')

    if cursor + movies_per_page < len(movies):
        next_movie_url = url_for('user_bp.watchlist', cursor=cursor + movies_per_page)

        last_cursor = movies_per_page * int(len(movies) / movies_per_page)
        if len(movies) % movies_per_page == 0:
            last_cursor -= movies_per_page

        last_movie_url = url_for('user_bp.watchlist', cursor=last_cursor)
    for key in processed_movies.keys():
        processed_movies[key] = url_for('browse_bp.movie', movie_name=key.title, movie_year=key.year)



    return render_template('user_profile/userpage.html',
                           user=user,
                           movies=processed_movies,
                           next_movie_url=next_movie_url,
                           prev_movie_url=prev_movie_url,
                           first_movie_url=first_movie_url,
                           last_movie_url=last_movie_url,
                           heading='Watch List'
                           )


@user_blueprint.route('/movies_watched', methods=['GET'])
@login_required
def movies_watched():
    movies_per_page = 4
    username = session['username']
    user = repo.repo_instance.get_user(username)
    movies = user.watched_movies
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
        prev_movie_url = url_for('user_bp.movies_watched', cursor=cursor - movies_per_page)
        first_movie_url = url_for('user_bp.movies_watched')

    if cursor + movies_per_page < len(movies):
        next_movie_url = url_for('user_bp.movies_watched', cursor=cursor + movies_per_page)

        last_cursor = movies_per_page * int(len(movies) / movies_per_page)
        if len(movies) % movies_per_page == 0:
            last_cursor -= movies_per_page

        last_movie_url = url_for('user_bp.movies_watched', cursor=last_cursor)
    for key in processed_movies.keys():
        processed_movies[key] = url_for('browse_bp.movie', movie_name=key.title, movie_year=key.year)

    return render_template('user_profile/userpage.html',
                           user=user,
                           movies=processed_movies,
                           next_movie_url=next_movie_url,
                           prev_movie_url=prev_movie_url,
                           first_movie_url=first_movie_url,
                           last_movie_url=last_movie_url,
                           heading='Movies Watched'
                           )
