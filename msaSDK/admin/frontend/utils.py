from functools import lru_cache
from string import Template


@lru_cache()
def msa_ui_templates(template_path: str, encoding='utf8') -> Template:
    """ Page UI Templates
    This function returns a cached instance of the Template object.
    Note:
        Caching is used to prevent re-reading the environment every time the Template is used.
    """
    with open(template_path, encoding=encoding) as f:
        return Template(f.read())
