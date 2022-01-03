import json

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User


def create_user(username: str, user_add_kwargs: dict=None):
    """ Create new user in db """
    user_add_kwargs = user_add_kwargs or dict()
    new_user = dict(username=username, password='123', email=username + '@.com')
    new_user.update(user_add_kwargs)
    new_user['password'] = make_password(new_user['password'])
    return User.objects.create(**new_user)


def login_user(client, user, password='123'):
    """ Login user """
    client.login(username=user.username, password=password)


def _dict_key_quotes(text):
    """ Replaces first two occurrences of double quotes " to single quotes ' in every line

        Is used to print dictionaries formatted according to the project guidelines
        (dict key are in single quotes, texts are in double quotes)
    """
    return '\n'.join([l.replace('"', "'", 2) for l in text.split('\n')])


def dump(response):
    """ Print DRF response data """
    print("\nURL:", response.request['PATH_INFO'])
    print("Method:", response.request['REQUEST_METHOD'])
    if response.request['QUERY_STRING']:
        print("Query:", response.request['QUERY_STRING'])
    print("\n")
    print("Status code:\n{}\n\nData:\n{}\n".format(
        response.status_code,
        _dict_key_quotes(json.dumps(response.data, indent=4, ensure_ascii=False))
        if hasattr(response, 'data') else None
    ))


def login_user_jwt(client, user,  url, password='123'):
    """ Get access JWT token """
    response = client.post(
        url, data={'username': user.username, 'password': password}, format='json'
    )
    token = response.data.get('access')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
