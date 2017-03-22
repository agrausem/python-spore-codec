from coreapi import Document
from spore_codec import decode
from spore_codec.document import Link

class TestFieldFromMethod:

    def setup_method(self):
        self.method = {
            'path': '/users/',
            'required_params': [],
            'optional_params': []
        }

    def test_no_params(self):
        assert decode._get_fields_from_method(self.method) == []


    def test_required_in_path(self):
        self.method['path'] += '{username}/'
        self.method['required_params'].append('username')

        result = decode._get_fields_from_method(self.method)
        assert len(result) == 1
        assert result[0].required
        assert result[0].name == 'username'
        assert result[0].location == 'path'

    def test_required_in_query(self):
        self.method['required_params'].append('username')
        
        result = decode._get_fields_from_method(self.method)
        assert len(result) == 1
        assert result[0].required
        assert result[0].name == 'username'
        assert result[0].location == 'query'

    def test_optional(self):
        self.method['optional_params'].append('username')

        result = decode._get_fields_from_method(self.method)
        assert len(result) == 1
        assert not result[0].required
        assert result[0].name == 'username'
        assert result[0].location == 'query'
        
    def test_all_together(self):
        self.method['required_params'] = ['username', 'pk']
        self.method['optional_params'] = ['permissions']
        self.method['path'] = '/groups/{pk}/'

        result = decode._get_fields_from_method(self.method)
        assert len(result) == 3
        assert len([r for r in result if r.required]) == 2
        assert len([r for r in result if r.location == 'query']) == 2


class TestActionAndKeyFromMethod:

    def test_return_type_from_getting_link_method(self):
        method = ('list_users', {
            'path': '/users/',
            'method': 'GET'
        })
        result = decode._get_link_from_method(method)
        assert isinstance(result, tuple)


    def test_number_of_elements_in_tuple_simple_method(self):
        method = ('list_users', {
            'path': '/users/',
            'method': 'GET'
        })
        result = decode._get_link_from_method(method)
        assert len(result) == 3

    def test_number_of_elements_in_tuple_complex_method(self):
        method = ('list_users_groups', {
            'path': '/users/{}/groups/',
            'method': 'GET'
        })
        result = decode._get_link_from_method(method)
        assert len(result) == 3

    def test_action_element(self):
        method = ('list_users', {
            'path': '/users/',
            'method': 'GET'
        })
        result = decode._get_link_from_method(method)
        assert result[0] == 'list'

    def test_keys_element_simple_method(self):
        method = ('list_users', {
            'path': '/users/',
            'method': 'GET'
        })
        result = decode._get_link_from_method(method)
        assert result[1] == ['users']

    def test_keys_element_complex_method(self):
        method = ('list_users_groups', {
            'path': '/users/{}/groups/',
            'method': 'GET'
        })
        result = decode._get_link_from_method(method)
        assert result[1] == ['users', 'groups']

    def test_link_element(self):
        method = ('list_users', {
            'path': '/users/',
            'method': 'GET'
        })
        result = decode._get_link_from_method(method)
        assert isinstance(result[-1], Link)


class TestLinkFromMethod:

    def test_link_url(self):
        method = ('list_users', {
            'path': '/users/',
            'method': 'GET'
        })
        link = decode._get_link_from_method(method)[-1]
        assert link.url == '/users/'

    def test_link_action(self):
        method = ('list_users', {
            'path': '/users/',
            'method': 'GET'
        })
        link = decode._get_link_from_method(method)[-1]
        assert link.action == 'get'

    def test_link_title(self):
        method = ('list_users', {
            'path': '/users/',
            'method': 'GET',
            'description': 'List users from app'
        })
        link = decode._get_link_from_method(method)[-1]
        assert link.title == 'List users from app'

    def test_link_default_title(self):
        method = ('list_users', {
            'path': '/users/',
            'method': 'GET',
        })
        link = decode._get_link_from_method(method)[-1]
        assert link.title == 'List users'

    def test_link_authentication(self):
        method = ('list_users', {
            'path': '/users/',
            'method': 'GET',
            'authentication': True
        })
        link = decode._get_link_from_method(method)[-1]
        assert link.authentication

    def test_link_default_authentication(self):
        method = ('list_users', {
            'path': '/users/',
            'method': 'GET',
        })
        link = decode._get_link_from_method(method)[-1]
        assert not link.authentication

    def test_link_formats(self):
        method = ('list_users', {
            'path': '/users/',
            'method': 'GET',
            'formats': ['xml', 'json']
        })
        link = decode._get_link_from_method(method)[-1]
        assert link.formats == ['xml', 'json']

    def test_link_default_formats(self):
        method = ('list_users', {
            'path': '/users/',
            'method': 'GET',
        })
        link = decode._get_link_from_method(method)[-1]
        assert link.formats == []

    def test_link_fields(self):
        method = ('list_users', {
            'path': '/users/',
            'method': 'GET',
        })
        link = decode._get_link_from_method(method)[-1]
        assert len(link.fields) == 0

    def test_link_description(self):
        method = ('list_users', {
            'path': '/users/',
            'method': 'GET',
            'documentation': 'Blabla'
        })
        link = decode._get_link_from_method(method)[-1]
        assert link.description == 'Blabla'

    def test_link_default_description(self):
        method = ('list_users', {
            'path': '/users/',
            'method': 'GET',
        })
        link = decode._get_link_from_method(method)[-1]
        assert link.description == ''


class TestDocumentFromSpore:

    def test_returning_document(self):
        spore_data = {
            'name': 'API',
            'methods': {}
        }
        result = decode.parse_spore_description(spore_data, 'http://test/')
        assert isinstance(result, Document)

    def test_document_title(self):
        spore_data = {
            'name': 'API',
            'methods': {}
        }
        result = decode.parse_spore_description(spore_data, 'http://test/')
        assert result.title == 'API'

    def test_document_url_from_signature(self):
        spore_data = {
            'name': 'API',
            'methods': {}
        }
        result = decode.parse_spore_description(spore_data, 'http://test/')
        assert result.url == 'http://test/'

    def test_document_url_from_data(self):
        spore_data = {
            'name': 'API',
            'base_url': 'http://other-test/',
            'methods': {}
        }
        result = decode.parse_spore_description(spore_data)
        assert result.url == 'http://other-test/'

    def test_document_url_precedence(self):
        spore_data = {
            'name': 'API',
            'base_url': 'http://other-test/',
            'methods': {}
        }
        result = decode.parse_spore_description(spore_data, 'http://test/')
        assert result.url == 'http://test/'

    def test_document_description(self):
        spore_data = {
            'name': 'API',
            'methods': {},
            'meta': {
                'documentation': 'doc'
            }
        }
        result = decode.parse_spore_description(spore_data, 'http://test/')
        assert result.description == 'doc'

    def test_document_default_description(self):
        spore_data = {
            'name': 'API',
            'methods': {},
            'meta': {
            }
        }
        result = decode.parse_spore_description(spore_data, 'http://test/')
        assert result.description == ''

    def test_document_media_type(self):
        spore_data = {
            'name': 'API',
            'methods': {},
        }
        result = decode.parse_spore_description(spore_data, 'http://test/')
        assert result.media_type == 'application/sporeapi+json'

    def test_document_simple_content(self):
        spore_data = {
            'name': 'API',
            'methods': {
                'list_users': {
                    'path': '/users/',
                    'method': 'GET'
                },
                'create_users': {
                    'path': '/users/',
                    'method': 'POST'
                }
            },
        }
        result = decode.parse_spore_description(spore_data, 'http://test/')
        assert 'users' in result.data
        assert 'list' in result.data['users']
        assert 'create' in result.data['users']

    def test_document_complex_content(self):
        spore_data = {
            'name': 'API',
            'methods': {
                'list_users': {
                    'path': '/users/',
                    'method': 'GET'
                },
                'list_users_groups': {
                    'path': '/users/{pk}/groups/',
                    'method': 'GET',
                    'required_params': ['pk']
                }
            },
        }
        result = decode.parse_spore_description(spore_data, 'http://test/')
        assert 'list' in result.data['users']
        assert 'groups' in result.data['users']
        assert 'list' in result.data['users']['groups']
