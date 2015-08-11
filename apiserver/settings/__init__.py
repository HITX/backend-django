# application_python cookbook expects manage.py in a top level
# instead of app level dir, so the relative import can fail

# try:
#     from .backend-django.apiserver.settings.base import *
# except ImportError:
#     from apiserver.settings.base import *

from apiserver.settings.base import *

try:
    from local_settings import *
except ImportError:
    pass
