from django.conf import settings
from .base import *
from .production import *
try:
    from .local import *
except:
    pass
