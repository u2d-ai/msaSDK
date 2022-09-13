"""admin package, Admin Site implementation.

    The admin package implements the HTML UI Admin Site. It allows to have a Dashboard style .
"""

from os.path import dirname, basename, isfile, join
import glob
import gettext
import os

from msaSDK.admin.utils.translation import i18n
from .admin import (
    AdminApp,
    BaseAdmin,
    BaseAdminSite,
    BaseFormAdmin,
    BaseModelAction,
    BaseModelAdmin,
    FormAdmin,
    IframeAdmin,
    LinkAdmin,
    LinkModelForm,
    ModelAction,
    ModelAdmin,
    ModelFormAdmin,
    PageAdmin,
    PageSchemaAdmin,
    RouterAdmin,
    TemplateAdmin,
)
from .parser import MSAUIParser

from .site import (
    AdminSite,
    DocsAdmin,
    FileAdmin,
    HomeAdmin,
    ReDocsAdmin,
)

modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

i18n.load_translations(
    {
        "zh_CN": gettext.translation(
            domain='messages',
            localedir=os.path.join(BASE_DIR, "locale"),
            languages=['zh_CN']
        )
    }
)
