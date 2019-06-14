import os

OPS_DEBUG = os.environ.get('OPS_DEBUG', 1)
OPS_DEBUG = bool(int(OPS_DEBUG))

if OPS_DEBUG:
    from settings.dev import *  # NOQA
else:
    from settings.prod import * # NOQA