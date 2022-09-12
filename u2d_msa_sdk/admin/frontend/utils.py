from functools import lru_cache
from string import Template


@lru_cache()
def msa_ui_templates(template_path: str, encoding='utf8') -> Template:
    """Page Templates
        Returns:
         a cached MSAUITemplate
    """
    with open(template_path, encoding=encoding) as f:
        return Template(f.read())
