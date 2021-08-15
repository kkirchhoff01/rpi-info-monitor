#!/usr/bin/python3

import sys
import os
displaypath = os.path.join(
    os.path.dirname(__file__),
    '..',
    'display',
)
sys.path.insert(0, os.path.abspath(displaypath))
import display
from config import HOSTS
from flask import (
    Flask,
    Response,
    request,
    render_template,
)
try:
    from flask_mobility import Mobility
except ImportError:
    Mobility = None

template_path = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    'templates',
)

app = Flask(
    __name__,
    template_folder=template_path,
)

if Mobility is not None:
    Mobility(app)

PORT = 5100
DEFAULT_FONT = 18
MOBILE_FONT = 26
VERT_FONT = 13.5
TEMP_UNITS = 'celsius'
BASE_DISPLAY = 3
FONT_UNIT = 4
MIN_FONT = 8


def get_font(default=DEFAULT_FONT):
    adjust_weight = max(0, len(HOSTS) - BASE_DISPLAY)
    return max(
        default - adjust_weight * FONT_UNIT,
        MIN_FONT,
    )


@app.route('/')
def index():
    try:
        is_mobile = (
            Mobility is not None and
            request.MOBILE
        )

        orient = request.args\
            .get('orientation')
        if orient is not None:
            vertical = (orient.lower() == 'vertical')
        else:
            vertical = is_mobile

        temp_units = request.args\
            .get('temp_units', 'celcius')

        refresh_rate = request.args\
            .get('refresh', 30)
        if not isinstance(refresh_rate, int):
            if not refresh_rate.isnumeric():
                raise ValueError(
                    'Invalid refresh rate: '
                    f'{refresh_rate}. Must be '
                    'an integer'
                )
            refresh_rate = int(refresh_rate)

        content = display.get_content(
            temp_units=temp_units,
            vertical=vertical,
            colored=False,
        )
        if not vertical:
            content = display.rotate(
                content,
                as_string=True,
            )
        else:
            content = '\n'.join(content)

        if is_mobile:
            fontsize = MOBILE_FONT
        else:
            if not vertical:
                fontsize = get_font(DEFAULT_FONT)
            else:
                fontsize = VERT_FONT

        return render_template(
            'index.html',
            content=content,
            fontsize=fontsize,
            refresh=refresh_rate,
        )
    except Exception as e:
        return Response(
            f'Error: {e}',
            status=500,
        )


if __name__ == '__main__':
    app.run('0.0.0.0', PORT)
