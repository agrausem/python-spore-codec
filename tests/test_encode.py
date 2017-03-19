from collections import OrderedDict
from spore_codec.encode import (get_spore_method_name, build_method_from_link,
                                get_spore_methods_from_document,
                                generate_spore_object)
from . import helpers


class TestSporeMethodName:

    def test_simple_name(self):
        assert get_spore_method_name(('users', ), 'list') == 'list_users'

    def test_plural(self):
        assert get_spore_method_name(('user', ), 'list') == 'list_users'

    def test_singular(self):
        assert get_spore_method_name(('users', ), 'create') == 'create_user'

    def test_multiple_keys(self):
        assert get_spore_method_name(
            ('user', 'admin', 'inactive'), 'list'
        ) == 'list_user_admin_inactives'

    def test_one_level(self):
        assert get_spore_method_name((), 'level') == 'level'


class TestBuildingMethods:

    def test_method_building_globally(self, list_users):
        assert build_method_from_link(list_users, ()) == OrderedDict([
            ('path', '/users/'),
            ('method', 'get'),
            ('required_params', []),
            ('optional_params', []),
            ('payload_required', False),
            ('authentication', False),
            ('documentation', 'List all users')
        ])

    def test_no_payload(self, list_users):
        spore_method = build_method_from_link(list_users, ()) 
        assert spore_method['payload_required'] == False
        assert not hasattr(spore_method, 'payload_format')

    def test_payload_post(self, create_user):
        spore_method = build_method_from_link(create_user, ()) 
        assert spore_method['method'] == 'post'
        assert spore_method['payload_required']
        assert spore_method['payload_format'] == \
                'application/x-www-form-urlencoded'

    def test_payload_put(self, update_user):
        spore_method = build_method_from_link(update_user, ()) 
        assert spore_method['method'] == 'put'
        assert spore_method['payload_required'] == True
        assert spore_method['payload_format'] == 'multipart/form-data'

    def test_payload_patch(self, partial_update_user):
        spore_method = build_method_from_link(partial_update_user, ()) 
        assert spore_method['method'] == 'patch'
        assert spore_method['payload_required'] == True
        assert spore_method['payload_format'] == 'application/json'

    def test_authenticated_resource(self, authenticated_delete_user):
        spore_method = build_method_from_link(authenticated_delete_user, ())
        assert spore_method['authentication']

    def test_is_a_required_path_parameter(self, get_user_group):
        spore_method = build_method_from_link(get_user_group, ())
        assert 'user_pk' in spore_method['required_params']
        assert 'group_pk' in spore_method['required_params']

    def test_is_not_required_parameter(self, get_user_group):
        spore_method = build_method_from_link(get_user_group, ())
        assert 'not_a_param' not in spore_method['required_params']

    def test_is_not_a_path_parameter(self, get_user_group):
        spore_method = build_method_from_link(get_user_group, ())
        assert 'option' not in spore_method['required_params']

    def test_is_a_query_required_parameter(self, list_filtered_user_groups):
        spore_method = build_method_from_link(list_filtered_user_groups, ())
        assert 'primary' in spore_method['required_params']

    def test_is_an_optional_parameter(self, get_user_group):
        spore_method = build_method_from_link(get_user_group, ())
        assert 'option' in spore_method['optional_params']

    def test_is_not_an_optional_parameter(self, get_user_group):
        spore_method = build_method_from_link(get_user_group, ())
        assert 'user_pk' not in spore_method['optional_params']
        assert 'group_pk' not in spore_method['optional_params']
        assert 'not_a_param' not in spore_method['optional_params']

    def test_same_method_formats(self, get_user):
        spore_method = build_method_from_link(get_user, ('json', ))
        assert 'formats' not in spore_method

    def test_specific_method_formats(self, get_user):
        spore_method = build_method_from_link(get_user, ('xml', ))
        assert spore_method['formats'] == ('json', )


class TestMethodFromDocument:

    def test_from_flat_document(self, flat_document):
        methods = get_spore_methods_from_document(flat_document)
        assert len(methods) == 1
        assert isinstance(methods[0], tuple)
        assert isinstance(methods[0][1], OrderedDict)
        assert methods[0][0] == 'user'

    def test_one_level_document(self, simple_document):
        methods = get_spore_methods_from_document(simple_document)
        names = [name for name, _ in methods]
        assert len(methods) == 6
        assert sorted(names) == ['create_user', 'delete_user', 'get_user',
                                 'list_users', 'partial_update_user',
                                 'update_user']

    def test_multi_levels_document(self, document):
        methods = get_spore_methods_from_document(document)
        names = [name for name, _ in methods]
        assert len(methods) == 5
        assert sorted(names) == ['create_user', 'get_users_group', 'hello',
                                 'list_users', 'list_users_groups',]


class TestFullSporeDescription:

    def test_structure(self, document):
        spore_description = generate_spore_object(document, (), ())
        keys = sorted(spore_description.keys())
        assert keys == ['authority', 'base_url', 'formats', 'meta', 'methods',
                        'name', 'version']
    
    def test_name(self, document):
        spore_description = generate_spore_object(document, (), ())
        assert spore_description['name'] == 'Base API'

    def test_base_url(self, document):
        spore_description = generate_spore_object(document, (), ())
        assert spore_description['base_url'] == 'http://base_url.com'

    def test_documentation(self, document):
        spore_description = generate_spore_object(document, (), ())
        assert spore_description['meta']['documentation'] == 'doc'

    def test_has_methods(self, document):
        spore_description = generate_spore_object(document, (), ())
        assert isinstance(spore_description['methods'], OrderedDict)
        assert len(spore_description['methods']) == 5

    def test_formats(self, document):
        spore_description = generate_spore_object(document, ('json', 'xml'),
                                                  ())
        assert spore_description['formats'] == ('json', 'xml')
