import coreapi
import json
from spore_codec.core import SporeDescriptionCodec
from spore_codec.document import Link


class TestSporeCodec:

    document = coreapi.Document(
        title='Test document',
        url='http://test-document.doc',
        content={
            'users': {
                'list': Link(
                    url='/users/',
                    action='get',
                    authentication=True,
                    formats=[
                        'json',
                        'xml'
                    ],
                    fields=[
                        coreapi.Field(
                            name='last_name',
                            required=False,
                            location='query',
                            description='the last name of the user.'
                        ),
                        coreapi.Field(
                            name='first_name',
                            required=False,
                            location='query',
                            description='the first name of the user.'
                        )
                    ]
                ),
                'get': Link(
                    url='/users/{pk}/',
                    action='get',
                    authentication=True,
                    formats=[
                        'json'
                    ],
                    fields=[
                        coreapi.Field(
                            name='pk',
                            required=True,
                            location='path',
                            description='the id of the user.'
                        )
                    ]
                )
            }
        }
    )

    spore_description = {
        'name': 'Test document',
        'base_url': 'http://test-document.doc',
        'version': '',
        'formats': [],
        'methods': {
            'list_users': {
                'method': 'get',
                'path': '/users/',
                'required_params': [],
                'optional_params': [
                    'last_name',
                    'first_name'
                ],
                'formats': [
                    'json',
                    'xml'
                ],
                'authentication': True,
                'payload_required': False,
                'documentation': ''
            },
            'get_user': {
                'method': 'get',
                'path': '/users/{pk}/',
                'required_params': [
                    'pk'
                ],
                'optional_params': [],
                'formats': [
                    'json',
                ],
                'authentication': True,
                'payload_required': False,
                'documentation': ''
            }
        },
        'authority': '',
        'meta': {
            'authors': [],
            'documentation': ''
        }
    }

    def test_simple_spore(self):
        codec = SporeDescriptionCodec()
        spore_desc = codec.encode(self.document)
        assert json.loads(spore_desc.decode('utf-8')) == self.spore_description


