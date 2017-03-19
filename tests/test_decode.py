from spore_codec import decode

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
