import pytest

from flask import session


def test_register(client):
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    response = client.post(
        '/authentication/register',
        data={'username': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == 'http://localhost/authentication/login'


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', b'Your username is required'),
        ('cj', '', b'Your username is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must at least 8 characters, and contain an upper case letter, a lower case letter and a digit'),
        ('fmercury', 'Test#6^0', b'Your username is already taken - please supply another'),
))
def test_register_with_invalid_input(client, username, password, message):
    # Check that attempting to register with invalid combinations of username and password generate appropriate error
    # messages.
    response = client.post(
        '/authentication/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['username'] == 'thorke'


def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session


def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'CS235Flix' in response.data


def test_login_required_to_review(client):
    response = client.post('/review_movie')
    assert response.headers['Location'] == 'http://localhost/authentication/login'


def test_review(in_memory_repo, client, auth):
    # Login a user.
    auth.login()

    # Check that we can retrieve the comment page.
    response = client.get('/review_movie?movie_name=Trust&movie_year=2010')

    response = client.post(
        '/review_movie?movie_name=Trust&movie_year=2010',
        data={'review': 'Wonderful', 'movie': '254', 'rating': 7}
    )
    assert response.headers['Location'] == 'http://localhost/movie?movie_name=Trust&movie_year=2010'


@pytest.mark.parametrize(('review', 'rating', 'messages'), (
        ('Fuck this movie?', 7, (b'Your review must not contain profanity')),
        ('Hey', 8, (b'Your review is too short')),
        ('ass', 6, (b'Your review is too short', b'Your review must not contain profanity')),
        ('ass', -1, (b'Your review is too short', b'Your review must not contain profanity', b'Value must within the range of 1 - 10')),
        ('ass', 11, (b'Your review is too short', b'Your review must not contain profanity', b'Value must within the range of 1 - 10')),
))
def test_review_with_invalid_input(in_memory_repo, client, auth, review, rating, messages):
    # Login a user.
    auth.login()

    movie = in_memory_repo.find_movie_by_title_and_year('Trust', 2010)

    # Attempt to comment on an article.
    response = client.post(
        '/review_movie?movie_name=Trust&movie_year=2010',
        data={'review': review, 'movie': '254', 'rating': rating}
    )
    # Check that supplying invalid comment text generates appropriate error messages.
    for message in messages:
        assert message in response.data


def test_movie_without_parameters(client):
    # Check that we can retrieve the articles page.
    response = client.get('/movie')
    assert response.status_code == 302

    # Check that without providing a date query parameter the page includes the first article.
    response.headers['Location'] == 'http://localhost/'


def test_movie_with_parameters(client):
    # Check that we can retrieve the articles page.
    response = client.get('/movie?movie_name=The+Dark+Knight+Rises&movie_year=2012')
    assert response.status_code == 200

    # Check that all articles on the requested date are included on the page.
    assert b'The Dark Knight Rises' in response.data
    assert b'Christopher Nolan' in response.data


def test_movie_with_reviews(client):
    # Check that we can retrieve the articles page.
    response = client.get('/movie?movie_name=Guardians+of+the+Galaxy&movie_year=2014')
    assert response.status_code == 200

    # Check that all articles tagged with 'Health' are included on the page.
    assert b'Guardians of the Galaxy' in response.data
    assert b'Wonderful' in response.data
    assert b'That was amazing' in response.data


def test_browse_no_parameters(client):
    response = client.get('/browse')
    assert b'Browse' in response.data


def test_browse_with_parameters(client):
    response = client.get('/movie_search?search=action%2C+x-men%2C+hugh%2C+bryan+singer')
    assert b'X-Men: Days of Future Past' in response.data
    assert b'The X-Men send Wolverine to the past in a desperate effort to change history and prevent an event that ' \
           b'results in doom for both humans and mutants.' in response.data


def test_login_required_to_watch(client):
    response = client.get('/watch?movie_name=Guardians+of+the+Galaxy&movie_year=2014')
    assert response.headers['Location'] == 'http://localhost/authentication/login'


def test_add_to_watched_movies(client, in_memory_repo, auth):
    auth.login()

    response = client.get('/watch?movie_name=Guardians+of+the+Galaxy&movie_year=2014')
    assert response.headers['Location'] == 'http://localhost/movies_watched'


def test_login_required_for_watchlist(client):
    response = client.get('/watchlist')
    assert response.headers['Location'] == 'http://localhost/authentication/login'


def test_access_to_watch_list(client, auth):
    auth.login()
    response = client.get('/watchlist')
    assert b'Watch List' in response.data


def test_login_required_to_add_to_watch_list(client):
    response = client.get('/add_to_watchlist')
    assert response.headers['Location'] == 'http://localhost/authentication/login'


def test_add_to_watch_list(client, in_memory_repo, auth):
    auth.login()

    response = client.get('/add_to_watchlist?movie_name=Guardians+of+the+Galaxy&movie_year=2014')
    assert response.headers['Location'] == 'http://localhost/watchlist'


def test_login_required_to_access_profile(client):
    response = client.get('/profile')
    assert response.headers['Location'] == 'http://localhost/authentication/login'


def test_access_to_profile(client, auth):
    auth.login()
    response = client.get('/profile')

    assert b'thorke' in response.data
    assert b'Amount of Movies Watched (including duplicates): </strong>0 movie(s)</p>\n ' in response.data
