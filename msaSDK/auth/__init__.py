import gettext
import glob
import os
from os.path import basename, dirname, isfile, join

from msaSDK.admin.utils.translation import i18n

modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [
    basename(f)[:-3] for f in modules if isfile(f) and not f.endswith("__init__.py")
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

i18n.load_translations(
    {
        "zh_CN": gettext.translation(
            domain="messages",
            localedir=os.path.join(BASE_DIR, "locale"),
            languages=["zh_CN"],
        )
    }
)
