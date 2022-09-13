# !/usr/bin/env python3  Line 1
# -*- coding: utf-8 -*- Line 2
# ----------------------------------------------------------------------------
# FastAPI msaSDK, shared SDK for multiple Micro Services Platform/Systems
#
# Created By  : Stefan Welcker/U2D.ai
# Created Date: 23.08.2022
# ---------------------------------------------------------------------------

version = '0.1.2'
__author__ = "Stefan Welcker"
__copyright__ = "Copyright 2022, U2D.ai"
__license__ = "MIT"
__version__ = version
__maintainer__ = "Stefan Welcker"
__email__ = "stefan@u2d,.ai"
__status__ = "Beta"
__url__ = "https://github.com/swelcker/U2D_MSA_SDK"

from os.path import dirname, basename, isfile, join
import glob
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
