import os

TEMPLATE_PATH = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    'templates',
)
PORT = 5100
DEFAULT_FONT = 18
VERT_FONT = 13.5
MOBILE_HOR_FONT = 12
MOBILE_VERT_FONT = 26
MOBILE_WEIGHT_FONT = 17
TEMP_UNITS = 'celsius'
BASE_DISPLAY = 3
FONT_UNIT = 4
MIN_FONT = 8

__all__ = [
    'TEMPLATE_PATH',
    'PORT',
    'DEFAULT_FONT',
    'VERT_FONT',
    'MOBILE_HOR_FONT',
    'MOBILE_VERT_FONT',
    'MOBILE_WEIGHT_FONT',
    'TEMP_UNITS',
    'BASE_DISPLAY',
    'FONT_UNIT',
    'MIN_FONT',
]
