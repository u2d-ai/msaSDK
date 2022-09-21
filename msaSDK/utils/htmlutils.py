# -*- coding: utf-8 -*-
from typing import Any, Optional

from lxml.html.clean import Cleaner


async def sanitize(dirty_html: Any) -> Optional[str]:
    """Clean/Sanitize HTML using lxml.html.clean.Cleaner

    Cleans the following:

    * Removes any ``<meta>`` tags
    * Removes any embedded objects (flash, iframes)
    * Removes any ``<link>`` tags
    * Removes any style tags.
    * Removes any processing instructions.
    * Removes any style attributes.  Defaults to the value of the ``style`` option.
    * Removes any ``<script>`` tags.
    * Removes any Javascript, like an ``onclick`` attribute. Also removes stylesheets as they could contain Javascript.
    * Removes any comments.
    * Removes any frame-related tags
    * Removes any form tags
    * Removes Tags that aren't *wrong*, but are annoying.  ``<blink>`` and ``<marquee>``
    * Remove any tags that aren't standard parts of HTML.
    * Remove any attributes which are not frozenset(['src', 'color', 'href', 'title', 'class', 'name', 'id']),
    * Remove Tags ('span', 'font', 'div'), their content will get pulled up into the parent tag.

    Args:
        dirty_html: Any, usually a html str

    Returns:
         clean_html: Optional[str] cleaned html
    """
    cleaner = Cleaner(
        page_structure=True,
        meta=True,
        embedded=True,
        links=True,
        style=True,
        processing_instructions=True,
        inline_style=True,
        scripts=True,
        javascript=True,
        comments=True,
        frames=True,
        forms=True,
        annoying_tags=True,
        remove_unknown_tags=True,
        safe_attrs_only=True,
        safe_attrs=frozenset(["src", "color", "href", "title", "class", "name", "id"]),
        remove_tags=("span", "font", "div"),
    )

    return cleaner.clean_html(dirty_html)
