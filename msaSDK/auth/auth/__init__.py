import glob
from os.path import basename, dirname, isfile, join

from .auth import Auth as Auth
from .auth import AuthBackend as AuthBackend
from .auth import AuthRouter as AuthRouter

modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [
    basename(f)[:-3] for f in modules if isfile(f) and not f.endswith("__init__.py")
]
