from enum import Enum


class LevelEnum(str, Enum):
    """Button Level"""
    primary = 'primary'
    secondary = 'secondary'
    info = 'info'
    success = 'success'
    warning = 'warning'
    danger = 'danger'
    light = 'light'
    dark = 'dark'
    link = 'link'
    default = 'default'


class SizeEnum(str, Enum):
    """Window size"""
    xs = 'xs'
    sm = 'sm'
    md = 'md'
    lg = 'lg'
    xl = 'xl'
    full = 'full'


class DisplayModeEnum(str, Enum):
    """Form display mode"""
    normal = 'normal'
    """General mode"""
    horizontal = 'horizontal'
    """Horizontal Mode"""
    inline = 'inline'
    """Inline mode"""


class LabelEnum(str, Enum):
    """Label Style"""
    primary = 'primary'
    success = 'success'
    warning = 'warning'
    danger = 'danger'
    default = 'default'
    info = 'info'


class StatusEnum(str, Enum):
    """Default State"""
    success = 'success'
    failure = 'failure'
    pending = 'pending'
    queue = 'queue'
    schedule = 'schedule'


class TabsModeEnum(str, Enum):
    """Tab Mode"""
    line = "line"
    card = "card"
    radio = "radio"
    vertical = "vertical"
    chrome = "chrome"
    simple = "simple"
    strong = "strong"
    tiled = "tiled"
    sidebar = "sidebar"
