import pytest
from . import helpers


@pytest.fixture(scope='class')
def create_user():
    return helpers.build_creating_link('/users/',
                                       'application/x-www-form-urlencoded',
                                       'Creates a user')


@pytest.fixture(scope='class')
def get_user():
    return helpers.build_getting_link('/users/{pk}/', 'Get detail of a user')


@pytest.fixture(scope='class')
def list_users():
    return helpers.build_listing_link('/users/', 'List all users')


@pytest.fixture(scope='class')
def update_user():
    return helpers.build_updating_link('/users/{pk}/', 'multipart/form-data',
                                       'Update a user')


@pytest.fixture(scope='class')
def partial_update_user():
    return helpers.build_updating_link('/users/{pk}/', 'application/json',
                                       'Update a user', partial=True)


@pytest.fixture(scope='class')
def authenticated_delete_user():
    return helpers.build_deleting_link('/users/{pk}/', 'Deletes a user', True)


@pytest.fixture(scope='class')
def get_user_group():
    link =  helpers.build_getting_link('/users/{user_pk}/groups/{group_pk}/', 
                                       'Get a user group', True)
    fields = (
        helpers.build_field('user_pk', 'path', True),
        helpers.build_field('group_pk', 'path', True),
        helpers.build_field('not_a_param', 'path', False),
        helpers.build_field('option', 'query', False)
    )

    link._fields = fields
    return link


@pytest.fixture(scope='class')
def list_filtered_user_groups():
    link = helpers.build_getting_link(
        '/users/{user_pk}/groups/?primary={primary}', 'Get a user group', True
    )
    fields = (
        helpers.build_field('user_pk', 'path', True),
        helpers.build_field('primary', 'query', True)
    )

    link._fields = fields
    return link

@pytest.fixture(scope='class')
def flat_document():
    content = {
        'user': get_user()
    }
    return helpers.build_document(content)


@pytest.fixture(scope="class")
def simple_document():
    content = {
        'users': {
            'list': list_users(),
            'get': get_user(),
            'create': create_user(),
            'partial_update': partial_update_user(),
            'update': update_user(),
            'delete': authenticated_delete_user()
        }
    }
    return helpers.build_document(content)


@pytest.fixture(scope="class")
def document():
    content = {
        'hello': helpers.build_getting_link('/', 'Hello World !'),
        'users': {
            'list': list_users(),
            'groups': {
                'get': get_user_group(),
                'list': list_filtered_user_groups()
            },
            'create': create_user()
        }
    }
    return helpers.build_document(content)
