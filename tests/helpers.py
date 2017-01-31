from coreapi.document import Link, Field, Document


def _build_link(url, action, encoding, description, fields=None,
                authentication=False, formats=()):
    link = Link(url, action, encoding, None, None, description, fields)
    link._authentication = authentication
    link._formats = formats
    return link


def build_listing_link(url, description, authenticated=False):
    return _build_link(url, 'get', None, description, None, authenticated)


def build_getting_link(url, description, authenticated=False):
    return _build_link(url, 'get', None, description, None, authenticated,
                       ('json', ))


def build_deleting_link(url, description, authenticated=False):
    return _build_link(url, 'delete', None, description, None, authenticated)


def build_updating_link(url, encoding, description, partial=False,
                        authenticated=False):
    if partial:
        return _build_link(url, 'patch', encoding, description, None,
                           authenticated)
    return _build_link(url, 'put', encoding, description, None, authenticated)


def build_creating_link(url, encoding, description, authenticated=False):
    return _build_link(url, 'post', encoding, description, None, authenticated)


def build_field(name, location, required=False, description=''):
    return Field(name, required, location, '', description, '')


def build_document(content):
    return Document(
        url='http://base_url.com',
        title='Base API',
        description='doc',
        content=content
    )
