from collections import OrderedDict
from django.conf import settings
from importlib import import_module


def get_cls(path):
    module, cls = path.rsplit('.', 1)
    return getattr(import_module(module), cls)
