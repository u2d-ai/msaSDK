import os
import sys

from matplotlib.font_manager import get_fontext_synonyms, MSUserFontDirectories, win32InstalledFonts, \
    X11FontDirectories, OSXFontDirectories, win32FontDirectory, get_fontconfig_fonts, list_fonts


async def findSystemFonts(fontpaths=None, fontext='ttf'):
    """
    Search for fonts in the specified font paths.  If no paths are
    given, will use a standard set of system paths, as well as the
    list of fonts tracked by fontconfig if fontconfig is installed and
    available.  A list of TrueType fonts are returned by default with
    AFM fonts as an option.
    """
    fontfiles = set()
    fontexts = get_fontext_synonyms(fontext)

    if fontpaths is None:
        if sys.platform == 'win32':
            fontpaths = MSUserFontDirectories + [win32FontDirectory()]
            # now get all installed fonts directly...
            fontfiles.update(win32InstalledFonts(fontext=fontext))
        else:
            fontpaths = X11FontDirectories
            if sys.platform == 'darwin':
                fontpaths = [*X11FontDirectories, *OSXFontDirectories]
            fontfiles.update(get_fontconfig_fonts(fontext))

    elif isinstance(fontpaths, str):
        fontpaths = [fontpaths]

    for path in fontpaths:
        fontfiles.update(map(os.path.abspath, list_fonts(path, fontexts)))

    return [fname for fname in fontfiles if os.path.exists(fname)]