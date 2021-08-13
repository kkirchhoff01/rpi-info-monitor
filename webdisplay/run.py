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
MOBILE_FONT = 27
VERT_FONT = 14


@app.route('/')
def index():
    try:
        orient = request.args\
            .get('orientation', 'vertical')
        vertical = (orient.lower() == 'vertical')

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

        if Mobility is not None and \
                request.MOBILE:
            fontsize = MOBILE_FONT
        else:
            fontsize = (
                DEFAULT_FONT if not vertical
                else VERT_FONT
            )

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
