from spore_codec.helpers import get_cls
from spore_codec.core import SporeDescriptionCodec


class TestGettingsCls:
    
    def test_get_cls(self):
        klass = get_cls('spore_codec.core.SporeDescriptionCodec')
        assert klass == SporeDescriptionCodec
