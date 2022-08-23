from lxml.html.clean import Cleaner


async def sanitize(dirty_html):
    cleaner = Cleaner(page_structure=True,
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
                      safe_attrs=frozenset(['src', 'color', 'href', 'title', 'class', 'name', 'id']),
                      remove_tags=('span', 'font', 'div')
                      )

    return cleaner.clean_html(dirty_html)